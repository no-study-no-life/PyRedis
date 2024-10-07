import functools


def id_register(func=None, *, func_dict=None):
	if func is None:
		return functools.partial(id_register, func_dict=func_dict)

	if not callable(func):
		raise TypeError(f"func not callable: type={type(func)}")

	if not isinstance(func_dict, dict):
		raise TypeError(f"func_dict err typr: {type(func_dict)}")

	id1 = func.__name__
	id2 = id1.lstrip('_')   # 去除前缀下划线
	if id2 in func_dict:
		raise KeyError(f'id:{id1} has been registered: {id2}')

	func_dict[id2] = func
	return func

