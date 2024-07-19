import logging
import json
from web3 import Web3
from solidity_python_sdk.error_handling import InsufficientFundsError
    
def check_funds(web3, account_address, required_amount):
    balance = web3.eth.get_balance(account_address)
    if balance < required_amount:
        raise ValueError(f"Insufficient funds: balance {balance}, required {required_amount}")


