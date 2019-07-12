from coin_display import CoinDisplay
from coin_api import CoinApi
import asyncio
import sys
import traceback
import time

async def main(loop):
	""" main class that starts the event loop controlling the API and the display """
	usage()
	display = CoinDisplay(loop)
	api = CoinApi(loop, get_coin(), get_market(), get_currency())
	log('using api ' + api.get_endpoint())
	while 1:
		display.on_load()
		try:
			log('updating value of ' + api.get_coin() + ' at ' + api.get_market())
			percent_change = await api.percent_change()
			log('market change in last 24hrs is ' + str(percent_change) + '%')
			display.on_data(percent_change)
		except KeyError:
			log('no api data available for coin:market:currency combination.')
			display.on_error()
		except Exception:
			print(traceback.format_exc())
			display.on_error()
		await asyncio.sleep(api.throttle())

def usage():
	print('================================================')
	print('|              <!> ETHERMETER 1.0 <!>           |')
	print('-------------------------------------------------')
	print('usage: python main.py <coin> <market> <currency>')
	print('example: python main.py ETH Coinbase USD')
	print('-------------------------------------------------\n')

def get_coin():
	return get_arg(1, 'ETH')

def get_market():
	return get_arg(2, 'Coinbase')

def get_currency():
	return get_arg(3, 'EUR')	


def get_arg(index, default):
	params = ['coin', 'market', 'currency']
	if (len(sys.argv) > index):
		log('using ' + sys.argv[index] + ' as ' + params[index - 1])
		return sys.argv[index]
	else:
		log('no ' + params[index - 1] + ' specified, using ' + default)
		return default

def log(line):
	print(time.strftime('%H:%M:%S') + ' > ' + line + ' ..')

try:
	loop = asyncio.get_event_loop()
	loop.run_until_complete(main(loop))
	loop.run_forever()
except KeyboardInterrupt:
	log('blockchain is the future, goodnight')
	pass
