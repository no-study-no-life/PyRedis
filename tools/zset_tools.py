""" Redis 有序Set 相关操作 """

from .core import _redis_register, _command, _unpack_kwargs


### 获取

@_redis_register
def _zscore(key: str, member: str):
	return _command('ZSCORE', key, member)


@_redis_register
def _zrank(key: str, member: str):
	return _command('ZRANK', key, member)


@_redis_register
def _zrevrank(key: str, member: str):
	return _command('ZREVRANK', key, member)


@_redis_register
def _zrange(key: str, start: int, stop: int, withscores=False):
	if withscores:
		return _command('ZRANGE', key, start, stop, 'WITHSCORES')
	return _command('ZRANGE', key, start, stop)


@_redis_register
def _zrangebyscore(key: str, start: int, stop: int, withscores=False, offset=None, count=None):
	extra = []
	if withscores:
		extra.append('WITHSCORES')
	if offset is not None and count is not None:
		extra.extend(['LIMIT', offset, count])
	return _command('ZRANGEBYSCORE', key, start, stop, *extra)


@_redis_register
def _zrevrange(key: str, start: int, stop: int, withscores=False):
	if withscores:
		return _command('ZREVRANGE', key, start, stop, 'WITHSCORES')
	return _command('ZREVRANGE', key, start, stop)


@_redis_register
def _zrevrangebyscore(key: str, start: int, stop: int, withscores=False, offset=None, count=None):
	extra = []
	if withscores:
		extra.append('WITHSCORES')
	if offset is not None and count is not None:
		extra.extend(['LIMIT', offset, count])
	return _command('ZREVRANGEBYSCORE', key, start, stop, *extra)


### 修改

@_redis_register
def _zadd(key: str, *args):
	if not args:
		raise ValueError("ZADD Member Number Error")
	return _command('ZADD', key, *args)


@_redis_register
def _zincrby(key: str, incr: int | float, member: str):
	return _command('ZINCRBY', key, incr, member)


@_redis_register
def _zrem(key: str, *args):
	if not args:
		raise ValueError("ZREM Member Number Error")
	return _command('ZREM', key, *args)


@_redis_register
def _zremrangebyrank(key: str, start: int, stop: int):
	return _command('ZREMRANGEBYRANK', key, start, stop)


@_redis_register
def _zremrangebyscore(key: str, start: int | float, stop: int | float):
	return _command('ZREMRANGEBYSCORE', key, start, stop)



### 信息

@_redis_register
def _zcard(key: str):
	return _command('ZCARD', key)


@_redis_register
def _zcount(key: str, start: int, stop: int):
	return _command('ZCOUNT', key, start, stop)


### 多个集合操作



