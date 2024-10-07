""" 编码/解码RESP协议 """
import json
import math

from exception import RecvDataError, ServerProcessError


class ConnEncoder:
	INT_MAX = (1 << 63)


	@classmethod
	def encode(cls, data):
		""" 客户端只支持编码bulkstr以及数组 """
		match data:
			case list() | tuple() | set():
				return cls.encodeArray(data)
			case str():
				return cls.encodeBulkStr(data)
			case bool():
				return cls.encodeBulkStr("1" if data else "0")
			case int() | float():
				return cls.encodeBulkStr(str(data))
			case dict():
				return cls.encodeBulkStr(json.dumps(data))
		return None

	@classmethod
	def encodeNone(cls) -> str:
		return '_\r\n'

	@classmethod
	def encodeBool(cls, data) -> str:
		return '#t\r\n' if data else '#f\r\n'

	@classmethod
	def encodeInt(cls, data: int) -> str:
		if data >= cls.INT_MAX or data < -cls.INT_MAX:
			return f'({data}\r\n'
		return f":{data}\r\n"

	@classmethod
	def encodeFloat(cls, data: float) -> str:
		if math.isinf(data):
			return ',inf\r\n' if data > 0 else ',-inf\r\n'
		msg = f'{data:.6e}'
		a, b = msg.split('e')
		return f",{a}e{b}\r\n"

	@classmethod
	def encodeBulkStr(cls, msg: str) -> str:
		# if not msg:
		# 	return "$-1\r\n"  # 通常用于返回表示不存在
		return f"${len(msg)}\r\n{msg}\r\n"

	@classmethod
	def encodeArray(cls, data: list | tuple) -> str:
		""" 编码数组 """
		n = len(data)
		res = [f"*{n}\r\n"]
		res.extend([cls.encode(each) for each in data])
		return "".join(res)

	@classmethod
	def encodeDict(cls, data: dict) -> str:
		""" 编码字典 """
		n = len(data)
		res = [f"%{n}\r\n"]
		for k, v in data.items():
			res.append(cls.encode(k))
			res.append(cls.encode(v))
		return "".join(res)

	@classmethod
	def encodeSet(cls, data: set) -> str:
		n = len(data)
		res = [f"~{n}\r\n"]
		res.extend([cls.encode(each) for each in data])
		return ''.join(res)

	@classmethod
	async def decode(cls, reader, ip=None, port=None):
		""" 读取数据并解码 """
		typ = await reader.read(1)
		if not typ:
			raise RecvDataError(f'read error type: {typ}.')
		ori = await reader.readuntil(b'\r\n')
		ori = ori.strip()
		msg = None
		match typ:
			case b'+'| b'-':
				msg = ori.decode()
				if typ == b'-':
					raise ServerProcessError(msg)
			case b'(' | b':':
				msg = int(ori)
			case b'#':
				msg = ori == b't'
			case b',':
				msg = float(ori)
			case b'_':
				msg = None
			case b'$':
				length = int(ori)
				if length < 0:
					return ""
				ori = await reader.readuntil(b'\r\n')
				ori = ori.strip()
				assert length == len(ori)
				msg = ori.decode()
			case b'*' | b'>':
				length = int(ori)
				if length <= 0:
					return []
				msg = []
				for _ in range(length):
					msg.append(await cls.decode(reader))
			case b'~':
				length = int(ori)
				if length <= 0:
					return set()
				msg = set()
				for _ in range(length):
					msg.add(await cls.decode(reader))
			case b'%':
				length = int(ori)
				if length <= 0:
					return {}
				msg = {}
				for _ in range(length):
					k = await cls.decode(reader)
					v = await cls.decode(reader)
					msg[k] = v

			case _:
				raise RecvDataError(f'read error msg {_}')
		return msg
