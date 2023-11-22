from async_timeout import asyncio
from diskcache import Cache
from threading import Lock
from urllib.parse import urlparse

from hamunafs.utils.singleton_wrapper import Singleton
from hamunafs.utils.redisutil import XRedis
from hamunafs.utils.nsqmanager import MQManager
from hamunafs.utils.minio_async import MinioAgentAsync
from hamunafs.backends import BackendBase, backend_factory
from hamunafs.conf import REDIS, NSQ

import random
import os
import shutil
import time
import uuid
import json
import httpx
try:
    import nest_asyncio
    nest_asyncio.apply()
except:
    pass

class Client(Singleton):
    @staticmethod
    def get_client(host, redis_client, mq_manager: MQManager, async_mq_mode=True, cache_path='../cache', custom_async_loop=None, init_redis=True):
        client = Client(host, redis_client, mq_manager, async_mq_mode, init_redis=init_redis)
        return client
    
    def __init__(self, host, redis_client, mq_manager: MQManager, async_mq_mode=True, cache_path='../cache', custom_async_loop=None, init_redis=True) -> None:
        if not self.need_init():
            return
        
        self.host = host
        if redis_client is None and init_redis:
            redis_client = XRedis(REDIS['host'], REDIS['pass'], REDIS['port'], REDIS['db'])
        self.redis = redis_client
        
        self.mq = mq_manager
        self.async_mq = async_mq_mode
        self.lock = Lock()
        
        #self.cache_path = cache_path
        os.makedirs(cache_path, exist_ok=True)
        self.index_cache = Cache(cache_path)
        
        self.put_topic = 'fs_put'
        self.get_topic = 'fs_get'

        # mqtt_client = MQTTClient('fs_server', 'opush', 'innovation').connect('kafka.ai.hamuna.club', 1883)
        # mqtt_client.subscribe('fs_backend_update', 2)
        # mqtt_client.register_on_message_handler(self.__on_mqtt_message)
        
        self.update()
        self._inited = True

        self.direct_minio_client = MinioAgentAsync([
            {
                'endpoint': "10.26.0.4:9002", 
                'access_key': 'hmcz', 
                'secret_key': '1987yang', 
                'secure': False,
                'region': 'brick1'
            },
            {
                'endpoint': "ml.ai.hamuna.club:8333", 
                'access_key': 'hmcz', 
                'secret_key': '1987yang', 
                'secure': False,
                'region': 'brick1'
            }
        ], [
            5, 1
        ], check_awailable_ts=10, timeout=5)

    
    def __on_mqtt_message(self, client, userdata, msg):
        if msg.topic == 'fs_backend_update':
            self.update()

    def get_qiniu_token(self, fname):
        qiniu_backend_keys = [k for k in list(self.backend_pools.keys()) if k.startswith('qiniu')]
        if len(qiniu_backend_keys) > 0:
            backend_key = random.sample(qiniu_backend_keys, 1)[0]
            backend = self.backend_pools[backend_key]
            return backend.get_token(fname)
        return None

    def decode_download_url(self, encode_url):
        backend, bucket, bucket_name = self._get_appropriate_backend(encode_url)
        return backend.geturl('{}/{}'.format(bucket, bucket_name))
    
    def update(self, force=False):
        with self.lock:
            if self._inited and not force:
                return

            print('updating backends...')
            resp = httpx.get('https://{}/api/system/fs/backends'.format(self.host), headers={
                'from': 'edge'
            }, timeout=httpx.Timeout(20), verify=False)
            if resp.status_code == 200:
                resp = json.loads(resp.text)
                if resp['success'] == 'ok':
                    print('backend cfg loaded')
                    backend_pools = {}
                    pool_data = resp['data']
                    for info in pool_data:
                        backend_pools[info['key']] = backend_factory[info['backend']](info['conf'])
                    self.backend_pools = backend_pools
                else:
                    raise Exception('error on acquiring fs backends...')
            else:
                raise Exception('error on acquiring fs backends...')
        
    def _random_pick_backend(self, ignore_prefix=[]) -> BackendBase:
        with self.lock:
            keys = [k for k in list(self.backend_pools.keys()) if k not in ignore_prefix]
            if len(keys) > 0:

                selected_ind = int(random.uniform(0, len(keys)))
                
                selected_key = keys[selected_ind]
                print('choosing {} backend'.format(selected_key))
                return selected_key, self.backend_pools[selected_key]
            else:
                return None, None
    
    def _get_appropriate_backend(self, url):
        with self.lock:
            prefix, _url = url.split('://')
            
            if prefix in self.backend_pools:
                if '/' in _url:
                    bucket, bucket_name = _url.split('/')
                elif '_' in url:
                    bucket, bucket_name = _url.split('_')
                else:
                    return None, None, None
                return self.backend_pools[prefix], bucket, bucket_name
            return None, None, None

    def _get_backend(self, key):
        return key, self.backend_pools[key]

    def cache(self, key, val, ttl=7200):
        if not isinstance(val, str):
            _val = json.dumps(val)
        else:
            _val = val
        try:
            with self.redis._get_connection(pipeline=True) as pipe:
                pipe.set(key, _val)
                pipe.set_expire_time(key, ttl)
                pipe.execute()
        except:
            pass
        self.index_cache.set(key, _val, expire=ttl)

    def get_cache(self, key, toObj=True):
        data = self.index_cache.get(key)
        if data is None:
            if self.redis is not None:
                data = self.redis.get(key)

        if data is not None and toObj:
            data = json.loads(data)
        
        return data

    async def get_cache_async(self, key, toObj=True):
        data = self.index_cache.get(key)
        if data is None:
            if self.redis is not None:
                data = await self.redis.get(key)

        if data is not None and toObj:
            data = json.loads(data)
        
        return data

    async def cache_async(self, key, val, ttl=7200):
        if not isinstance(val, str):
            _val = json.dumps(val)
        else:
            _val = val
        try:
            await self.redis.set(key, _val, expired=ttl)
        except:
            pass
        self.index_cache.set(key, _val, expire=ttl)

    def __put_to_cloud(self, path, bucket, bucket_name, tmp=True, tries=0, ignore_prefix=[]):
        prefix, backend = self._random_pick_backend(ignore_prefix)
        if prefix is None:
            return False, '尝试过所有Backend都失败'
        
        ret, e = backend.put(path, bucket, bucket_name, tmp)
        if ret:
            url = '{}://{}'.format(prefix, e)
            return True, url
        else:
            ignore_prefix.append(prefix)
            return self.__put_to_cloud(path, bucket, bucket_name, tmp, tries+1, ignore_prefix=ignore_prefix)
            
    def put_to_cloud(self, path, bucket, bucket_name, tmp=True, refresh=False):
        if os.path.isfile(path):
            cache_key = 'cloud_{}_{}'.format(bucket, bucket_name)
            cache_data = self.get_cache(cache_key, toObj=False) if not refresh else None
            if cache_data is None:
                ret, e = self.__put_to_cloud(path, bucket, bucket_name, tmp)
                if ret:
                    self.cache(cache_key, e)

                return ret, e
            else:
                return True, cache_data
        else:
            return False, '文件不存在'

    async def __put_to_cloud_async(self, path, bucket, bucket_name, tmp=True, tries=0, ignore_prefix=[]):
        prefix, backend = self._random_pick_backend(ignore_prefix)
        if prefix is None:
            return False, '尝试过所有Backend都失败'
        
        ret, e = await backend.put_async(path, bucket, bucket_name, tmp)
        if ret:
            url = '{}://{}'.format(prefix, e)
            return True, url
        else:
            ignore_prefix.append(prefix)
            return await self.__put_to_cloud_async(path, bucket, bucket_name, tmp, tries+1, ignore_prefix=ignore_prefix)

        
    async def put_to_cloud_async(self, path, bucket, bucket_name, tmp=True, refresh=False):
        if os.path.isfile(path):
            cache_key = 'cloud_{}_{}'.format(bucket, bucket_name)
            cache_data = await self.get_cache_async(cache_key, toObj=False) if not refresh else None
            if cache_data is None:
                ret, e = await self.__put_to_cloud_async(path, bucket, bucket_name, tmp)
                if ret:
                    await self.cache_async(cache_key, e)
                return ret, e
            else:
                return True, cache_data
        else:
            return False, '文件不存在'
    
    def get_from_cloud(self, path, url, force_copy=False, min_size=0):
        file_path = self.index_cache.get(url)
        if file_path is not None and os.path.isfile(file_path) and os.path.getsize(file_path) // 1024 >= min_size:
            print('loading from disk...')
            if force_copy:
                if file_path == path:
                    return True, path
                else:
                    os.makedirs(os.path.split(path)[0], exist_ok=True)
                    
                    shutil.copy(file_path, path)
                    
                    return True, path
            return True, file_path             
        
        print('loading from cloud...')
        backend, bucket, bucket_name = self._get_appropriate_backend(url)
        
        if backend is not None:
            ret, e = backend.get(path, bucket, bucket_name)
            if ret:
                self.index_cache.set(url, e)
                return True, path
            else:
                return ret, e
        else:
            return False, '未受支持的Backend'

    async def get_from_cloud_async(self, path, url, force_copy=False, min_size=0, refresh=False):
        file_path = self.index_cache.get(url)
        if file_path is not None and os.path.isfile(file_path) and os.path.getsize(file_path) // 1024 >= min_size and not refresh:
            print('loading from disk...')
            if force_copy:
                if file_path == path:
                    return True, path
                else:
                    os.makedirs(os.path.split(path)[0], exist_ok=True)
                    
                    shutil.copy(file_path, path)
                    
                    return True, path
            return True, file_path             
        
        print('loading from cloud...')
        backend, bucket, bucket_name = self._get_appropriate_backend(url)
        
        if backend is not None:
            ret, e = await backend.get_async(path, bucket, bucket_name)
            if ret:
                self.index_cache.set(url, e)
                return True, path
            else:
                return ret, e
        else:
            return False, '未受支持的Backend'

    def put_from_cloud(self, url, bucket, bucket_name, timeout=120, file_ttl=-1):
        # save to cache
        task_id = 'tmp_file_{}_{}'.format(bucket, bucket_name)
        try:
            ret = self.mq.publish(self.put_topic, {
                'url': url,
                'bucket': bucket,
                'bucket_name': bucket_name,
                'ttl': file_ttl
            })
            
            if ret:
                t = time.time()
                while True:
                    if time.time() - t >= timeout:
                        break
                    
                    resp = self.redis.get(task_id)
                    
                    if resp is not None and len(resp) > 0:
                        resp = json.loads(resp)
                        if resp['ret']:
                            return True, '{}/{}'.format(bucket, bucket_name)
                        else:
                            return False, resp['err']
                    
                    time.sleep(1/30)
            
            return False, '上传出错'
        except Exception as e:
            return False, str(e)
    
    def put(self, path, bucket, bucket_name, timeout=60, file_ttl=-1):
        ret, e = self.put_to_cloud(path, bucket, bucket_name)
        if ret:
            ret, e = self.put_from_cloud(e, bucket, bucket_name, timeout, file_ttl)
                
        return ret, e
    
    def get(self, path, url, force_copy=False, min_size=0, timeout=60, refresh=False):
        if '://' in url:
            bucket, bucket_name = url.split('://')[1].split('/')
        else:
            bucket, bucket_name = url.split('/')

        task_id = 'tmp_file_{}_{}'.format(bucket, bucket_name)
        if not refresh:
            if '://' in url:
                ret, e = self.get_from_cloud(path, url, force_copy, min_size)
                return ret, e
            
            print('downloading {}...'.format(url))

            cached_resp = self.redis.get(task_id)

            if cached_resp is not None and len(cached_resp) > 0:
                resp = json.loads(cached_resp)
                if resp['ret']:
                    tmp_url = resp['url']
                    return self.get_from_cloud(path, tmp_url, force_copy, min_size)
        else:
            self.redis.delkey(task_id)
        ret = self.mq.publish(self.get_topic, {
            'bucket': bucket,
            'bucket_name': bucket_name,
            'refresh': 'yes' if refresh else 'no'
        })
        if ret:
            t = time.time()
            resp = None
            while True:
                if time.time() - t >= timeout:
                    break
                
                resp = self.redis.get(task_id)
                if resp is not None and len(resp) > 0:
                    resp = json.loads(resp)
                    if resp['ret']:
                        tmp_url = resp['url']
                        return self.get_from_cloud(path, tmp_url, force_copy, min_size)
                
                time.sleep(1/30)
                
        return False, '获取失败'

    def get_cloud_url(self, path, url, force_copy=False, min_size=0, timeout=60, refresh=False):
        if '://' in url:
            bucket, bucket_name = url.split('://')[1].split('/')
        else:
            bucket, bucket_name = url.split('/')

        task_id = 'tmp_file_{}_{}'.format(bucket, bucket_name)
        if not refresh:
            if '://' in url:
                return True, url
            cached_resp = self.redis.get(task_id)

            if cached_resp is not None and len(cached_resp) > 0:
                resp = json.loads(cached_resp)
                if resp['ret']:
                    tmp_url = resp['url']
                    return True, tmp_url
        else:
            self.redis.delkey(task_id)
        ret = self.mq.publish(self.get_topic, {
            'bucket': bucket,
            'bucket_name': bucket_name,
            'refresh': 'yes' if refresh else 'no'
        })
        if ret:
            t = time.time()
            resp = None
            while True:
                if time.time() - t >= timeout:
                    break
                
                resp = self.redis.get(task_id)
                if resp is not None and len(resp) > 0:
                    resp = json.loads(resp)
                    if resp['ret']:
                        tmp_url = resp['url']
                        return True, tmp_url
                
                time.sleep(1/30)
                
        return False, '获取失败'
    
    async def try_direct_get_async(self, path, bucket, bucket_name):
        return await self.direct_minio_client.download_file(path, bucket, bucket_name, max_tries=1)

    async def get_async(self, path, url, force_copy=False, min_size=0, timeout=60, refresh=False):
        file_path = self.index_cache.get(url)
        if file_path is not None and os.path.isfile(file_path) and os.path.getsize(file_path) // 1024 >= min_size and not refresh:
            print('loading from disk...')
            if force_copy:
                if file_path == path:
                    return True, path
                else:
                    os.makedirs(os.path.split(path)[0], exist_ok=True)
                    
                    shutil.copy(file_path, path)
                    
                    return True, path
            return True, file_path             


        if '://' in url:
            bucket, bucket_name = url.split('://')[1].split('/')
        else:
            bucket, bucket_name = url.split('/')

        ret, e = await self.try_direct_get_async(path, bucket, bucket_name)

        if ret:
            self.index_cache.set(url, e)
            return ret, e
            
        task_id = 'tmp_file_{}_{}'.format(bucket, bucket_name)
        if not refresh:
            if '://' in url:
                ret, e = await self.get_from_cloud_async(path, url, force_copy, min_size)
                return ret, e
            
            print('downloading {}...'.format(url))

            cached_resp = await self.redis.get(task_id)

            if cached_resp is not None and len(cached_resp) > 0:
                resp = json.loads(cached_resp)
                if resp['ret']:
                    tmp_url = resp['url']
                    return await self.get_from_cloud_async(path, tmp_url, force_copy, min_size)
        else:
            await self.redis.delkey(task_id)
        
        try:
            ret = await self.mq.async_publish(self.get_topic, {
                'bucket': bucket,
                'bucket_name': bucket_name,
                'refresh': 'yes' if refresh else 'no'
            })
            if ret:
                t = time.time()
                resp = None
                while True:
                    if time.time() - t >= timeout:
                        break
                    
                    resp = await self.redis.get(task_id)
                    if resp is not None and len(resp) > 0:
                        resp = json.loads(resp)
                        if resp['ret']:
                            tmp_url = resp['url']
                            return await self.get_from_cloud_async(path, tmp_url, force_copy, min_size, refresh=True)
                        else:
                            return False, resp['err']
                    
                    await asyncio.sleep(1/30)
                return False, '超时'
            else:
                return False, 'MQ发送失败'
        except Exception as e:
            return False, '获取失败'
    
    async def get_cloud_url_async(self, path, url, force_copy=False, min_size=0, timeout=60, refresh=False):
        if '://' in url:
            bucket, bucket_name = url.split('://')[1].split('/')
        else:
            bucket, bucket_name = url.split('/')
            
        task_id = 'tmp_file_{}_{}'.format(bucket, bucket_name)
        if not refresh:
            if '://' in url:
                return True, url

            cached_resp = await self.redis.get(task_id)

            if cached_resp is not None and len(cached_resp) > 0:
                resp = json.loads(cached_resp)
                if resp['ret']:
                    tmp_url = resp['url']
                    return True, tmp_url
        else:
            await self.redis.delkey(task_id)
        
        try:
            ret = await self.mq.async_publish(self.get_topic, {
                'bucket': bucket,
                'bucket_name': bucket_name,
                'refresh': 'yes' if refresh else 'no'
            })
            if ret:
                t = time.time()
                resp = None
                while True:
                    if time.time() - t >= timeout:
                        break
                    
                    resp = await self.redis.get(task_id)
                    if resp is not None and len(resp) > 0:
                        resp = json.loads(resp)
                        if resp['ret']:
                            tmp_url = resp['url']
                            return True, tmp_url
                    
                    await asyncio.sleep(1/30)
        except Exception as e:
            return False, '获取失败'

    async def get_mq_conn(self):
        return await self.mq.get_mq_conn()

    async def put_from_cloud_async(self, url, bucket, bucket_name, timeout=120, tries=0, file_ttl=-1):
        # save to cache
        task_id = 'tmp_file_{}_{}'.format(bucket, bucket_name)
        try:
            ret = await self.mq.async_publish(self.put_topic, {
                'url': url,
                'bucket': bucket,
                'bucket_name': bucket_name,
                'ttl': file_ttl
            })
            if ret:
                t = time.time()
                while True:
                    if time.time() - t >= timeout:
                        break
                    
                    resp = await self.redis.get(task_id)
                    
                    if resp is not None and len(resp) > 0:
                        resp = json.loads(resp)
                        if resp['ret']:
                            return True, '{}/{}'.format(bucket, bucket_name)
                        else:
                            return False, resp['err']
                    
                    await asyncio.sleep(1/30)
                if tries < 3:
                    return await self.put_from_cloud_async(url, bucket, bucket_name, timeout, tries+1, file_ttl)
                else:
                    return False, '等待文件服务回执超时， 可能是文件服务器发生错误'
            else:
                if tries < 3:
                    return await self.put_from_cloud_async(url, bucket, bucket_name, timeout, tries+1, file_ttl)
                else:
                    return False, '推送到MQ失败'
        except Exception as e:
            return False, str(e)
        
    def try_direct_put(self, path, bucket, bucket_name):
        return self.direct_minio_client.upload_file(path, bucket, bucket_name, max_tries=1)
    
    async def put_async(self, path, bucket, bucket_name, timeout=60, file_ttl=-1):
        ret, e = await self.put_to_cloud_async(path, bucket, bucket_name)
        if ret:
            ret, e = await self.put_from_cloud_async(e, bucket, bucket_name, timeout, file_ttl)
        return ret, e
    
    def geturl(self, entrypoint):
        prefix, bucket_info = entrypoint.split('://')
        if prefix in self.backend_pools:
            backend = self.backend_pools[prefix]
            return backend.geturl(bucket_info)
        else:
            return entrypoint

    async def cleanup_cloud(self):
        for k, backend in self.backend_pools.items():
            print('cleanup {} files'.format(k))
            await backend.cleanup_old_files()
                    
                    