# pi-zero-ethermeter
Small python script for monitoring various crypto currencies using a raspberry pi zero with a blinkt!. [[video]](https://www.youtube.com/watch?v=rkcM4-2oynY)

# background
First project on the raspberry pi zero w! Trying out python 3.6 and its async module with event loops.
The aiohttp module is used for REST requests and it uses the api from [cryptowat.ch](https://cryptowat.ch/). Supports retrieving price for more than 20+ supported markets and a load of crypto-currencies. 

The following endpoint is used to retrieve the 24 hour percent change:
https://min-api.cryptocompare.com/data/generateAvg?fsym={}&tsym={}&markets={}

- fsym: from symbol, example ETH for Ethereum
- markets: Coinbase, Poloniex, Kraken, BitRex and more .. !
- tsym: to symbol, example EUR, USD or BTC.. 

These values are provided when running the script, or defaults to fsym = ETH, market = Coinbase and tsym = EUR.
Note that some combinations are unavailable, and the leds will flash in PINK.

The values used for the BLINKT that is attached to the pi is 'CHANGEPCT24HOUR', one percent matches 1 led. Negative change gives red leds, positive gives green. Rainbows when reloading data and pink stuff on error. The script will continously poll the API for updates.

# build & install
This is easy! Just build python 3.6 from source, install the aiohttp module with pip3.6 and optionally the aiodns for faster DNS lookups.

- python 3.6
  there is even a guide here: https://gist.github.com/dschep/24aa61672a2092246eaca2824400d37f
  it took around 45 minutes to compile and install python3.6 on the raspberry pi zero w!
  
- aiohttp and aiodns
  sudo pip3.6 install aiohttp && sudo pip3.6 install aiodns

# final notes
:cold_sweat: :X: CRYPTO CURRENCY FEVER :X: :cold_sweat:
