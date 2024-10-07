""" 
My Redis Client v0.0.1 
似乎Client发送方只能以 大容量字符串 数组 的形式向服务端发送请求;

"""

import asyncio
from client import RedisClient


async def main():
	cli = RedisClient(db=6)
	await cli.connectWithTimeout()
	p = cli.pipeline()
	p.hello(3)
	mem = {"t1": "1", "t2": "2"}
	p.hset("hello", **mem)
	res = await p.execute()
	print(res)
	res = await cli.expire("hello", 60)
	# res = await cli.hello(3)
	# print(type(res), res)
	# res = await cli.select(1)
	print(res)
	await cli.close()


if __name__ == '__main__':
	asyncio.run(main())
	pass
