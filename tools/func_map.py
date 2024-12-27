""" 转换请求操作为resp信息 """

import functools

from .core import RedisFuncDict, _redis_register, _command, _unpack_kwargs
from .hash_tools import *
from .set_tools import *
from .zset_tools import *


__all__ = ['RedisFuncDict']


@_redis_register
def _set(key: str, value):
	return _command("SET", key, value)

@_redis_register
def _get(key: str):
	return _command("GET", key)

@_redis_register
def _delete(key: str):
	return _command("DEL", key)

@_redis_register
def _exists(key: str):
	return _command("EXISTS", key)

@_redis_register
def _expire(key: str, seconds: int | str):
	return _command("EXPIRE", key, seconds)

@_redis_register
def _expireat(key: str, timestamp: int | str):
	return _command("EXPIREAT", key, timestamp)

@_redis_register
def _ttl(key: str):
	return _command("TTL", key)

@_redis_register
def _hello(ver: int | str):
	return _command("HELLO", ver)

@_redis_register
def _select(db: int | str):
	return _command("SELECT", db)


