# from cachetools import LRUCache
#
#
# class CustomLRUCache(LRUCache):
#     def __init__(self, maxsize, *args, **kwargs):
#         super().__init__(maxsize, *args, **kwargs)
#         self.hits = 0
#         self.misses = 0
#
#     def __getitem__(self, key):
#         if key in self:
#             self.hits += 1
#         else:
#             self.misses += 1
#         return super().__getitem__(key)
#
# # from CacheTools import CustomLRUCache
#
# cache = CustomLRUCache(maxsize=100 * 1024 * 1024, getsizeof=lambda x: len(str(x)))
#
# cache['key1'] = 'value1'
# cache['key2'] = 'value2'
# cache['key3'] = 'value3'
# cache['key4'] = 'value4'
# cache['key5'] = 'value5'
# cache['key6'] = 'value6'
# cache['key7'] = 'value7'
#
# print(cache.get('key19'))
# cache.popitem()
#
# # Print hit rate and miss rate
# total_gets = cache.hits + cache.misses
# hit_rate = cache.hits / total_gets if total_gets > 0 else 0
# miss_rate = cache.misses / total_gets if total_gets > 0 else 0
# print(f"Hit rate: {hit_rate:.2%}")
# print(f"Miss rate: {miss_rate:.2%}")
#

import psycopg2

from datetime import datetime, timezone
import time


database = "Photos"
user = "postgres"
pwd = "root"
host = "localhost"
port = '5432'
cur = None
conn = None


def CreateMemCacheStatusTable ():
    global cur
    global conn
    try:
        conn = psycopg2.connect(database=database,
                                user=user,
                                password=pwd,
                                host=host,
                                port=port)

        print("Connection successfully")
        cur = conn.cursor()
        create_script = ''' create table if  not exists memcache_status3(             
                        id SERIAL,
                        key_id varchar(200),
                        value   varchar(200),
                        arrive  time,
                        hit_or_miss boolean)'''
        cur.execute(create_script)
        conn.commit()

        cur.close()
        conn.close()
    except Exception as error:
        print(error)
    finally:
        if cur is not None:
            cur.close()
        if conn is not None:
            conn.close()

CreateMemCacheStatusTable()


def insertMemHit (k, val, hitBool):
    global conn
    global cur
    try:
        conn = psycopg2.connect(database=database,
                                user=user,
                                password=pwd,
                                host=host,
                                port=port)


        cur = conn.cursor()
        sql = """INSERT INTO memcache_status2 (key_id,value,arrive, hit_or_miss)
                 VALUES(%s, %s, %s,%s );"""
        dt = datetime.now(timezone.utc)
        cur.execute(sql, (k,val,time.time(),hitBool))
        print("Mem Cache Inserted")
        conn.commit()
        cur.close()
        conn.close()
    except Exception as error:
        print(error)
    finally:
        if cur is not None:
            cur.close()
        if conn is not None:
            conn.close()

insertMemHit ('k', 'val', True)