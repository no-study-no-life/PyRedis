""" 

基础异常类

"""


class BaseError(Exception):
	pass


class RecvDataError(BaseError):
	pass


class ServerProcessError(BaseError):
	pass


class BaseHostError(BaseError):
	def __init__(self, msg="", ip=None, port=None):
		msg = f"connect to {ip}:{port} {msg}"
		super().__init__(msg)


class ConnLost(BaseHostError):
	pass


class ConnTimeout(BaseHostError):
	pass
