from cachetools import LRUCache, RRCache

# Create a cache with a capacity of 100 MB and LRU replacement policy
cache_size = 10
cache = LRUCache(maxsize=100 * 1024 * 1024, getsizeof=lambda x: len(str(x)))
# Or, create a cache with a capacity of 100 MB and random replacement policy
# cache = RRCache(maxsize=100 * 1024 * 1024, getsizeof=lambda x: len(str(x)))

# Add some key-value pairs to the cache
cache['key1'] = 'value1'
cache['key2'] = 'value2'
cache['key3'] = 'value3'
cache['key4'] = 'value4'
cache['key5'] = 'value5'
cache['key6'] = 'value6'
cache['key7'] = 'value7'


cache.popitem()
#
# for k, v in cache.items():
#     print(k,"\t",v)
# # Get a value from the cache
# value = cache.get('key1')
# print(value)
# # Clear the cache
# now = time.time()
# cache
#
# cache_info =  ctu.StatsCache(cache)
# for zz in cache_info.values():
#     print(zz)
# hit_rate= cache_info.hits()
# miss_rate = cache_info.values()
# # Print cache statistics
# print('Cache statistics for the past 10 minutes:')
# print(f'  Hit rate: {hit_rate:.2%}')
# print(f'  Miss rate: {miss_rate:.2%}')
# print(f'  Max size: {cache_info.maxsize / (1024 * 1024):.2f} MB')
# print(f'  Current size: {cache_info.currsize / (1024 * 1024):.2f} MB')
# print(f'  Evictions: {cache_info.evictions}')
# cache.clear()
#
#
#
#
#
# # Get cache statistics for the past 10 minutes
# cache_info = CacheInfo(*cache.cache_info())
# last_10_min_hits = cache_info.hits - cache_info.misses
#
# # Print cache statistics
# print('Cache statistics for the past 10 minutes:')
# print(f'  Hit rate: {last_10_min_hits / (last_10_min_hits + cache_info.misses):.2%}')
# print(f'  Miss rate: {cache_info.misses / (last_10_min_hits + cache_info.misses):.2%}')
# print(f'  Max size: {cache_info.maxsize / (1024 * 1024):.2f} MB')
# print(f'  Current size: {cache_info.currsize / (1024 * 1024):.2f} MB')
# print(f'  Evictions: {cache_info.hits - cache_info.currsize}')


import random
import time

# Define a dictionary as the local key-value store
kv_store = {'key1': 'value1', 'key2': 'value2', 'key3': 'value3'}

# Define variables to keep track of hits and misses
hits = 0
misses = 0

# Define a function to simulate get requests
def simulate_get_request(key):
    global hits, misses
    if key in kv_store:
        hits += 1
        return kv_store[key]
    else:
        misses += 1
        return None

# Simulate some get requests
for i in range(1000):
    key = 'key' + str(random.randint(1, 5))  # Choose a random key
    value = simulate_get_request(key)  # Simulate a get request for the key
    time.sleep(0.01)  # Wait for a short period of time to simulate network latency

# Calculate hit rate and miss rate
total_gets = hits + misses
hit_rate = hits / total_gets if total_gets > 0 else 0
miss_rate = misses / total_gets if total_gets > 0 else 0

# Print the results
print(f"Hit rate: {hit_rate:.2%}")
print(f"Miss rate: {miss_rate:.2%}")
