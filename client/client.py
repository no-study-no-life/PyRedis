import asyncio

from tools import RedisFuncDict, ConnEncoder
from exception import BaseError, ConnLost, ConnTimeout


class ClientBase:

	_default_limit = 1 << 16

	def __init__(self, ip, port, *, limit=None):
		self.ip = ip
		self.port = port
		self.reader = None
		self.writer = None
		self.limit = limit if limit else ClientBase._default_limit

	async def close(self):
		if self.writer is not None:
			self.writer.close()
			await self.writer.wait_closed()
			self.writer = None
			self.reader = None

	def checkConnection(self):
		if not self.writer or not self.writer or self.writer.is_closing():
			raise ConnError("connection lost", ip=self.ip, port=self.port)

	async def connectWithTimeout(self, timeout=5):
		""" 带有连接超时的连接尝试 """
		await self.close()
		try:
			r, w = await asyncio.wait_for(
				asyncio.open_connection(self.ip, self.port, limit=self.limit), 
				timeout=timeout
				)
		except asyncio.TimeoutError:
			raise ConnTimeout(f"{timeout=}", ip=self.ip, port=self.port)
		except Exception as e:
			raise BaseError(e)
		else:
			self.writer = w
			self.reader = r

	async def connectWithoutTimeout(self):
		await self.close()
		self.reader, self.writer = await asyncio.open_connection(self.ip, self.port, limit=self.limit)

	async def send(self, msg: str):
		self.checkConnection()
		self.writer.write(msg.encode())
		await self.writer.drain()

	async def read(self, n: int = -1):
		""" 获取接收的信息 """
		if self.reader is None:
			raise ConnLost(f'read conn lost', ip=self.ip, port=self.port)
		return await self.reader.read(n)

	async def readLine(self, f='\r\n'):
		""" 读取直到f出现 """
		if self.reader is None:
			raise ConnLost(f'read conn lost', ip=self.ip, port=self.port)
		resp = None
		try:
			resp = await self.reader.readuntil(f)
		except LimitOverrunError:
			# 超过限制, ?
			resp = await self.reader.read(self.limit)
			flag = False
			while not flag:
				tmp, flag = await self._readOverflow(f)
				if tmp is not None:
					resp += tmp
		return resp

	async def _readOverflow(self, f):
		resp = None
		flag = True
		try:
			resp = await self.reader.readuntil(f)
		except LimitOverrunError:
			resp = await self.reader.read(self.limit)
			flag = False
		return resp, flag



class RedisPipeClient(ClientBase):
	def __init__(self, ip, port, reader=None, writer=None):
		super().__init__(ip, port)
		self.writer = writer
		self.reader = reader
		self._cached_command = []

	def __getattr__(self, key):
		if key in RedisFuncDict:
			func = RedisFuncDict[key]
			def f(*args, **kwargs):
				msg = func(*args, **kwargs)
				self._cached_command.append(msg)
			return f
		raise AttributeError(f'{self.__class__.__name__} has no attribute {key}')

	async def execute(self):
		self.checkConnection()
		command = self._cached_command
		self._cached_command = []
		msg = "".join(command)
		res = []
		try:
			await self.send(msg)
			for _ in range(len(command)):
				res.append(await ConnEncoder.decode(self.reader))
		except Exception as e:
			await self.close()
			raise BaseError(e)
		else:
			return res


class RedisClient(ClientBase):

	def __init__(self, ip="localhost", port=6379, db=0):
		super().__init__(ip, port)
		self.db = db

	def pipeline(self):
		return RedisPipeClient(self.ip, self.port, writer=self.writer, reader=self.reader)

	def __getattr__(self, key):
		if key in RedisFuncDict:
			func = RedisFuncDict[key]
			async def f(*args, **kwargs):
				msg = func(*args, **kwargs)
				return await self._command(msg)
			return f

		raise AttributeError(f'{self.__class__.__name__} has no attribute {key}')

	async def _command(self, msg):
		if not msg:
			return
		self.checkConnection()
		try:
			await self.send(msg)
			return await ConnEncoder.decode(self.reader)
		except Exception as e:
			await self.close()
			raise BaseError(e)

	async def connectWithTimeout(self, timeout=60):
		await super().connectWithTimeout(timeout)
		if self.db:
			await self.select(self.db)

	async def connectWithoutTimeout():
		await super().connectWithoutTimeout()
		if self.db:
			await self.select(self.db)