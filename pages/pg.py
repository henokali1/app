from binance.client import Client
import pickle
import platform


def read_pickle_file(fn):
    with open(fn, 'rb') as handle:
        val = pickle.load(handle)
    return val

pt = platform.system()
fn = 'C:/Users/HENOK/Documents/Bkey/bkey.pickle' if pt == 'Windows' else '/home/ubuntu/Bkey/bkey.pickle'
val = read_pickle_file(fn)
api_key=val['binance_api_key']
api_secret=val['binance_api_secret']


client = Client(api_key, api_secret)


def get_usdt_pair_coins():
	r=[]
	exchange_info = client.get_exchange_info()
	for s in exchange_info['symbols']:
		pair = s['symbol']
		if pair[-4:] == 'USDT':
			r.append(pair[:-4])
	return r

print(get_usdt_pair_coins())
