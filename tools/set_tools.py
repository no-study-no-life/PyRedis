""" Redis Set 相关操作 """

from .core import _redis_register, _command, _unpack_kwargs


### 存在

@_redis_register
def _sismember(key: str, member: str):
	return _command('SISMEMBER', key, member)

### 获取

@_redis_register
def _smembers(key: str):
	return _command('SMEMBERS', key)


@_redis_register
def _srandmember(key: str, count: int = 1):
	if count <= 0:
		raise ValueError(f'SRANDMEMBER Count Error: {count}')
	if count == 1:
		return _command('SRANDMEMBER', key)
	return _command('SRANDMEMBER', key, count)

### 修改

@_redis_register
def _sadd(key: str, *args):
	if not args:
		raise ValueError("SADD Member Number Error")
	return _command('SADD', key, *args)


@_redis_register
def _spop(key: str):
	return _command('SPOP', key)


@_redis_register
def _srem(key: str, *args):
	if not args:
		raise ValueError("SREM Member Number Error")
	return _command('SREM', key, *args)


### 信息

@_redis_register
def _scard(key: str):
	return _command('SCARD', key)


### 多个集合操作

@_redis_register
def _sdiff(*keys):
	if not keys:
		raise ValueError('SDIFF Keys Number Error')
	return _command('SDIFF', *keys)


@_redis_register
def _sdiffstore(destination: str, *args):
	if not args:
		raise ValueError("SDIFFSTORE Keys Number Error")
	return _command('SDIFFSTORE', destination, *args)


@_redis_register
def _sinter(*keys):
	if not keys:
		raise ValueError('SINTER Keys Number Error')
	return _command('SINTER', key1, key2)


@_redis_register
def _sinterstore(destination: str, *args):
	if not args:
		raise ValueError("SINTERSTORE Keys Number Error")
	return _command('SINTERSTORE', destination, *args)


@_redis_register
def _sunion(*keys):
	if not args:
		raise ValueError("SUNION Keys Number Error")
	return _command('SUNION', *keys)


@_redis_register
def _sunionstore(destination: str, *args):
	if not args:
		raise ValueError("SUNIONSTORE Keys Number Error")
	return _command('SUNIONSTORE', destination, *args)


@_redis_register
def _smove(source: str, destination: str, member: str):
	return _command('SMOVE', source, destination, member)
