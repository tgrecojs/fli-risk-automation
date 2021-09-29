import streamlit as st
import pandas as pd
import numpy as np
import altair as alt
import streamlit as st
import random
import time
from coinGeckoPrices import *
from contract_addresses import *
from tokenInfo import *

from urllib.error import URLError

st.title('FLI Risk Automation')

productSelection = st.selectbox('Select', ["ETH2x-FLI","BTC2x-FLI"])

if productSelection == "ETH2x-FLI":
    # ## Left Column is ETH info ##
    # # left_column.write(f"Coingecko ETH FLI Price is: "+str(coinGeckoPriceData(ETHFLI_COINGECKO_ID)))
    # left_column.write("Coingecko ETH FLI Price is:")
    # left_column.write(coinGeckoPriceData(ETHFLI_COINGECKO_ID))

    # # left_column.write(f"Coingecko ETH Price is: "+str(coinGeckoPriceData(ETH)))
    # left_column.write("Coingecko ETH Price is:")
    # left_column.write(coinGeckoPriceData(ETH))

    # # left_column.write(f"ETH FLI current supply is: "+str(getTotalSupply(ETHFLI_TOKEN_ADDRESS)))
    # left_column.write("ETH FLI Current Supply is:")
    # left_column.write(getTotalSupply(ETHFLI_TOKEN_ADDRESS))

    # left_column.write("ETH FLI Current Leverage Ratio is:")
    # left_column.write(getCurrentLeverageRatio(ETHFLI_STRATEGY_ADAPTER_ADDRESS))

    # left_column.write("ETH FLI Supply Cap is:")
    # left_column.write(getSupplyCap(ETHFLI_SUPPLY_CAP_ISSUANCE_ADDRESS))
    
    
    
    # def writeAbstracted(value,string,value):
    #     st.sidebar.write(string)
    #     st.sidebar.write(value)
        
    # def Writecoingetckoprice(value,string,value):
    #     st.sidebar.write(string)
    #     st.sidebar.write(value)
    
    
    #original
    st.sidebar.write("Coingecko ETH FLI Price is:")
    ethFliPrice = coinGeckoPriceData(ETHFLI_COINGECKO_ID)
    st.sidebar.write(ethFliPrice)
    
    
    # #second
    # ethFliPrice = coinGeckoPriceData(ETHFLI_COINGECKO_ID)
    # writeAbstracted("Coingecko ETH FLI Price is:",ethFliPrice)
    
    # #thrid
    # writeAbstracted("Coingecko ETH FLI Price is:",coinGeckoPriceData(ETHFLI_COINGECKO_ID))
    
    
    st.sidebar.write("Coingecko ETH Price is:")
    ethPrice = coinGeckoPriceData(ETH)
    st.sidebar.write(ethPrice)

    st.sidebar.write("ETH FLI Current Supply is:")
    ethFliCurrentSupply = getTotalSupply(ETHFLI_TOKEN_ADDRESS)
    st.sidebar.write(ethFliCurrentSupply)

    st.sidebar.write("ETH FLI Current Leverage Ratio is:")
    ethFliCurrentLeverageRatio = getCurrentLeverageRatio(ETHFLI_STRATEGY_ADAPTER_ADDRESS)
    st.sidebar.write(ethFliCurrentLeverageRatio)

    st.sidebar.write("ETH FLI Supply Cap is:")
    sc = getSupplyCap(ETHFLI_SUPPLY_CAP_ISSUANCE_ADDRESS)
    st.sidebar.write(sc)

    priceChange = st.number_input('Enter Price Change in %',min_value=-50,max_value=150,value=0,step=10)
    userInputEthPrice = (1+(priceChange/100))*ethPrice
    st.write("post eth price percent change")
    st.write(userInputEthPrice)
    userInput_eth_max_trade_size_slider = st.slider('ETH Max Trade Size', min_value=400, max_value=2000, value=800, step=100)
    userInput_supply = st.slider('ETH FLI Supply', min_value=(sc-10000), max_value=(sc+100000), value=sc, step=100)
    
    st.write("current Collateral Notaional units:")
    collateralNotaionalUnits = ethFliPrice*ethFliCurrentLeverageRatio/userInputEthPrice*ethFliCurrentSupply
    
    st.write(collateralNotaionalUnits)
    
    st.write("current Collateral Notaional Price:")
    st.caption('collateralNotaionalUnits*ethPrice')
    collateralNotionalPrice = collateralNotaionalUnits*ethPrice
    st.write(collateralNotionalPrice)
    
    st.write("current borrowed asset Notional Price:")
    st.caption('collateralNotionalPrice-ethFliPrice*ethFliCurrentSupply')
    borrowNotionalPrice = collateralNotionalPrice-ethFliPrice*ethFliCurrentSupply
    st.write(borrowNotionalPrice)
    
    st.write("AUM")
    st.caption('collateralNotionalPrice-borrowNotionalPrice')
    aum = collateralNotionalPrice-borrowNotionalPrice
    st.write(aum)
    
    st.write("Price Drop to Liquidation from current LR")
    
    endLR = 2.9
    diff = endLR - ethFliCurrentLeverageRatio
    drop = diff/2
    st.caption('(Max LR of 2.9 - current LR) / 2')
    st.write(drop*100)
    
    newCollateralAssetPrice = ethPrice * (1-drop)
    st.write("new Collateral Asset Price")
    st.caption('ethPrice * (1-drop)')
    st.write(newCollateralAssetPrice)


    newCollateralNotionalValue = newCollateralAssetPrice *collateralNotaionalUnits
    st.caption('newCollateralAssetPrice *collateralNotaionalUnits')
    st.write(newCollateralNotionalValue)
    
    newBorrowNotionalValue = borrowNotionalPrice
    st.caption('newBorrowNotionalValue = borrowNotionalPrice')
    st.write(newBorrowNotionalValue)
    
    newAUM = newCollateralNotionalValue - newBorrowNotionalValue
    st.caption('newCollateralNotionalValue - newBorrowNotionalValue')
    st.write(newAUM)
    
    newLR = newCollateralNotionalValue/newAUM
    st.write("New Leverage Ratio")
    st.caption('newCollateralNotionalValue/newAUM')
    st.write(newLR)
    
    


if productSelection == "BTC2x-FLI":
# ## Right Column is BTC info
# # right_column.write(f"Coingecko BTC FLI Price is: "+str(coinGeckoPriceData(BTCFLI_COINGECKO_ID)))
#     right_column.write("Coingecko BTC FLI Price is")
#     right_column.write(coinGeckoPriceData(BTCFLI_COINGECKO_ID))

#     # right_column.write(f"Coingecko BTC Price is: "+str(coinGeckoPriceData(BTC)))
#     right_column.write("Coingecko BTC Price is")
#     right_column.write(coinGeckoPriceData(BTC))

#     # right_column.write(f"BTC FLI current supply is: "+str(getTotalSupply(BTCFLI_TOKEN_ADDRESS)))
#     right_column.write("BTC FLI Current Supply is:")
#     right_column.write(getTotalSupply(BTCFLI_TOKEN_ADDRESS))

#     right_column.write("BTC FLI Current Leverage Ratio is:")
#     right_column.write(getCurrentLeverageRatio(BTCFLI_STRATEGY_ADAPTER_ADDRESS))

#     right_column.write("BTC FLI Supply Cap is:")
#     right_column.write(getSupplyCap(BTCFLI_SUPPLY_CAP_ISSUANCE_ADDRESS))
    
    st.write("Coingecko BTC FLI Price is")
    st.write(coinGeckoPriceData(BTCFLI_COINGECKO_ID))

    st.write("Coingecko BTC Price is")
    st.write(coinGeckoPriceData(BTC))

    st.write("BTC FLI Current Supply is:")
    st.write(getTotalSupply(BTCFLI_TOKEN_ADDRESS))

    st.write("BTC FLI Current Leverage Ratio is:")
    st.write(getCurrentLeverageRatio(BTCFLI_STRATEGY_ADAPTER_ADDRESS))

    st.write("BTC FLI Supply Cap is:")
    st.write(getSupplyCap(BTCFLI_SUPPLY_CAP_ISSUANCE_ADDRESS))
    
    
    btc_max_trade_size_slider = st.slider('BTC Max Trade Size', min_value=0, max_value=10, step=100)





st.button('Optimize')
# st.checkbox('Check me out')
# st.radio('Radio', [1,2,3])
