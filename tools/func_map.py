""" 转换请求操作为resp信息 """

import functools

from .id_register import id_register
from .conn_encoder import ConnEncoder


__all__ = ['RedisFuncDict']


class DictViewer:
	__slots__ = ("_data", )

	def __init__(self, data: dict):
		self._data = data

	def __getitem__(self, index):
		return self._data[index]

	def __len__(self):
		return len(self._data)

	def __contains__(self, index):
		return index in self._data


def _unpack_kwargs(kwargs):
	res = []
	for each in kwargs.items():
		res.extend(each)
	return res

def _command(*args):
	if not args:
		return
	return ConnEncoder.encode(args)


_redis_func_dict = {}
_redis_register = functools.partial(id_register, func_dict=_redis_func_dict)

RedisFuncDict = DictViewer(_redis_func_dict)


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
def _hset(key: str, *args, **kwargs):
	if len(args) % 2 != 0:
		raise ValueError('hset argument num error.')
	return _command("HSET", key, *args, *_unpack_kwargs(kwargs))

@_redis_register
def _hmset(key: str, *args, **kwargs):
	if len(args) % 2 != 0:
		raise ValueError('hmset argument num error.')
	return _command('HSET', key, *args, *_unpack_kwargs(kwargs))

@_redis_register
def _hget(key: str, field: str):
	return _command("HGET", key, field)

@_redis_register
def _hmget(key: str, *fields):
	return _command("HMGET", key, *fields)

@_redis_register
def _hlen(key: str):
	return _command('HLEN', key)

@_redis_register
def _hkeys(key: str):
	return _command("HKEYS", key)

@_redis_register
def _hgetall(key: str):
	return _command("HGETALL", key)

@_redis_register
def _hdel(key: str, field: str):
	return _command("HDEL", key, field)

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


