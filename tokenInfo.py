import requests
import json
from web3 import Web3
from datetime import datetime
from config import INFURA_URL, ETHERSCAN_TOKEN
from contract_addresses import *



#   // Call the Tokensets API
#   var response = UrlFetchApp.fetch("https://api.tokensets.com/v2/funds/ethfli");

#   // var BTC_response = UrlFetchApp.fetch("https://api.tokensets.com/v2/funds/btcfli");
  
#   // Logger.log(response.getContentText());
#   // getGraphData()
#   return populateCells()
def divideBy(x):
    def numerator(y):
        return int(y / x);
    return numerator
  
def getPercent(y): 
  return divideBy(1000000000000000000)(y);

def multiplyBy(x):
  def input(y):
    return int(x + y)
  return input

def handleFloat(x):
  return multiplyBy(1e-18)(x);
  
def roundFloat(x):
  return round(float(handleFloat(x)), 2)

w3 = Web3(Web3.HTTPProvider(INFURA_URL))

def getAbi(contractAddress):
  response = requests.get(f"https://api.etherscan.io/api?module=contract&action=getabi&address={contractAddress}&apikey={ETHERSCAN_TOKEN}")
  json_data = json.loads(response.text)
  return((json_data['result']))

def getContract(address):
  contract = w3.eth.contract(address=address, abi=getAbi(address))
  return contract

def getTotalSupply(address):
  check = w3.toChecksumAddress(address)
  contract = getContract(check, getAbi(address))
  execut = contract.functions.totalSupply().call()
  execut_rounded = int(execut/1000000000000000000)
#   print(f'The current total supply is {execut_rounded}')
  return(getPercent(execut))
  
def getCurrentLeverageRatio(address):
  contract = getContract(address, getAbi(address))
  leverageRatio = contract.functions.getCurrentLeverageRatio().call()
  leverageRatioRounded = round(leverageRatio/1000000000000000000,2)
#   print(f'the current leverage ratio is {leverageRatioRounded}')
  return(leverageRatioRounded)


# struct ExecutionSettings { 
#     uint256 unutilizedLeveragePercentage;            // Percent of max borrow left unutilized in precise units (1% = 10e16)
#     uint256 twapMaxTradeSize;                        // Max trade size in collateral base units
#     uint256 twapCooldownPeriod;                      // Cooldown period required since last trade timestamp in seconds
#     uint256 slippageTolerance;                       // % in precise units to price min token receive amount from trade quantities
#     string exchangeName;                             // Name of exchange that is being used for leverage
#     bytes leverExchangeData;                         // Arbitrary exchange data passed into rebalance function for levering up
#     bytes deleverExchangeData;                       // Arbitrary exchange data passed into rebalance function for delevering
# }

def getExecution(address):
  execut = getContract(address, getAbi(address)).functions.getExecution().call()
#   print(f'This is unutilized leverage percentage {unutilizedLeveragePercent} and this is twapmaxtradesize {twapMaxTradeSize}, and here is cooldown {coolDownPeriod}, and here is slippage tolerence {slippageAllowance} and here is exchangeName {exchangeName}')
  return(f'This is unutilized leverage percentage {getPercent(execut[0]} and this is twapmaxtradesize {getPercent(execut[1]}, and here is cooldown {getPercent(execut[2]}, and here is slippage tolerence {getPercent(execut[3]} and here is exchangeName {execut[4]}')

# struct IncentiveSettings {
#     uint256 etherReward;                             // ETH reward for incentivized rebalances
#     uint256 incentivizedLeverageRatio;               // Leverage ratio for incentivized rebalances
#     uint256 incentivizedSlippageTolerance;           // Slippage tolerance percentage for incentivized rebalances
#     uint256 incentivizedTwapCooldownPeriod;          // TWAP cooldown in seconds for incentivized rebalances
#     uint256 incentivizedTwapMaxTradeSize;            // Max trade size for incentivized rebalances in collateral base units
# }

def getIncentive(address):
    #currently just returning the incentivizedLeverageRatio
    #
  contract = w3.eth.contract(address=address, abi=getAbi(address))
  execut = contract.functions.getIncentive().call()
  etherReward = float(execut[0]*1e-18)
  incentivizedLeverageRatio = float(execut[1]*1e-18)
  incentivizedSlippageTolerance = float(execut[2]*1e-18)
  incentivizedTwapCooldownPeriod = float(execut[3]*1e-18)
  # incentivizedTwapMaxTradeSize = float(execut[4]*1e-18)
  #return(f'either reward {etherReward},{incentivizedLeverageRatio},{incentivizedSlippageTolerance},{incentivizedTwapMaxTradeSize}')
  return(incentivizedLeverageRatio)
  
  
#   struct MethodologySettings { 
#     uint256 targetLeverageRatio;                     // Long term target ratio in precise units (10e18)
#     uint256 minLeverageRatio;                        // In precise units (10e18). If current leverage is below, rebalance target is this ratio
#     uint256 maxLeverageRatio;                        // In precise units (10e18). If current leverage is above, rebalance target is this ratio
#     uint256 recenteringSpeed;                        // % at which to rebalance back to target leverage in precise units (10e18)
#     uint256 rebalanceInterval;                       // Period of time required since last rebalance timestamp in seconds
# }

def getMethodology(address):
  contract = w3.eth.contract(address=address, abi=getAbi(address))
  execut = contract.functions.getMethodology().call()
  return(f' targetleverage -> {roundFloat(exect[0])} minLevRatio -> {roundFloat(execut[1])}, maxLevRatio -> {roundFloat(execut[2])}, recentingspeed -> {oundFloat(execut[3])} rebalance interbal -> {execut[4]/60}')
    
def getCurrentAndTotalSupply(address,address1):
  check = w3.toChecksumAddress(address)
  contract = w3.eth.contract(address=check, abi=getAbi(address))
  execut = contract.functions.totalSupply().call()
  contract2 = w3.eth.contract(address=address1, abi=getAbi(address1))
  execut = contract.functions.totalSupply().call()
  execut2 = contract2.functions.supplyCap().call()
  current_supply = format(int(execut/1000000000000000000),',d')
  supply_cap = format(int(execut2/1000000000000000000),',d')
#   print(f'The current supply is {current_supply} out of a max of {supply_cap}')
  return(f'{current_supply} / {supply_cap}')


def getSupplyCap(address):
  check = w3.toChecksumAddress(address)
  contract2 = w3.eth.contract(address=address, abi=getAbi(address))
  execut2 = contract2.functions.supplyCap().call()
  supply_cap = int(execut2/1000000000000000000)
#   print(f'The current supply is {current_supply} out of a max of {supply_cap}')
  return(supply_cap)
