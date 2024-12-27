""" Redis Hash 相关操作 """

from .core import _redis_register, _command, _unpack_kwargs


### 存在

@_redis_register
def _hexists(key: str, field: str):
	return _command("HEXISTS", key, field)

### 获取

@_redis_register
def _hget(key: str, field: str):
	return _command("HGET", key, field)


@_redis_register
def _hmget(key: str, *fields):
	return _command("HMGET", key, *fields)


@_redis_register
def _hgetall(key: str):
	return _command("HGETALL", key)

# 修改

@_redis_register
def _hset(key: str, *args, **kwargs):
	if len(args) % 2 != 0:
		raise ValueError('hset argument num error.')
	return _command("HSET", key, *args, *_unpack_kwargs(kwargs))


@_redis_register
def _hsetnx(key: str, filed: str, value: str):
	return _command("HSETNX", key, field, value)


@_redis_register
def _hmset(key: str, *args, **kwargs):
	if len(args) % 2 != 0:
		raise ValueError('hmset argument num error.')
	return _command('HSET', key, *args, *_unpack_kwargs(kwargs))


@_redis_register
def _hincrby(key: str, field: str, incr: int | str):
	return _command('HINCRBY', key, field, incr)


@_redis_register
def hincrbyfloat(key: str, field: str, incr: int | float | str):
	return _command('HINCRBYFLOAT', key, field, incr)


@_redis_register
def _hdel(key: str, field: str):
	return _command("HDEL", key, field)

# 表的信息

@_redis_register
def _hlen(key: str):
	return _command('HLEN', key)


@_redis_register
def _hkeys(key: str):
	return _command("HKEYS", key)


@_redis_register
def _hvals(key: str):
	return _command('HVALS', key)

