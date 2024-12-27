import functools

from .id_register import id_register
from .conn_encoder import ConnEncoder


__all__ = ['RedisFuncDict', "_redis_register", "_command", "_unpack_kwargs"]


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
