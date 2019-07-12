import asyncio
import aiohttp
import json

class CoinApi:
	""" API implementation for retrieving the current pricing. """
	url = 'https://min-api.cryptocompare.com/data/generateAvg?fsym={}&tsym={}&e={}'
	loop = None

	def __init__(self, loop, coin, market, currency):
		self.loop = loop
		self.coin = coin
		self.market = market
		self.currency = currency

	async def percent_change(self):
		""" called to retrieve data from the API """
		async with aiohttp.ClientSession(loop=self.loop) as session:
			return await self.get(session)

	async def get(self, session):
		async with session.get(self.url.format(self.coin, self.currency, self.market)) as resp:
			await asyncio.sleep(3)
			percent_change = json.loads(await resp.text())['DISPLAY']['CHANGEPCT24HOUR']
			return float(percent_change)

	def get_coin(self):
		return self.coin

	def get_market(self):
		return self.market

	def get_endpoint(self):
		return self.url.format(self.coin, self.currency, self.market)

	def throttle(self):
		""" returns the minimum number of seconds to wait before calling data. """
		return 30
