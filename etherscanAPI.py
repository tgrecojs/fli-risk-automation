import requests
import json
from web3 import Web3
from datetime import datetime
from config import INFURA_URL, ETHERSCAN_TOKEN
from token_addresses import *

# uses etherscan API to pull total token supply
def etherscanTokenSupply():
  response = requests.get(f"https://api.etherscan.io/api?module=stats&action=tokensupply&contractaddress=0xaa6e8127831c9de45ae56bb1b0d4d4da6e5665bd&apikey={ETHERSCAN_TOKEN}")
  data3 = json.loads(response.text)
  supply = int(data3['result'])/1000000000000000000
  return(f'the current total supply for ETH2x-FLI is {supply}')

def getAbi(contractAddress):
  response = requests.get(f"https://api.etherscan.io/api?module=contract&action=getabi&address={contractAddress}&apikey={ETHERSCAN_TOKEN}")
  json_data = json.loads(response.text)
  return((json_data['result']))