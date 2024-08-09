from web3 import Web3
from web3.middleware import geth_poa_middleware
import json

with open("G:/Nillion-Compute/Backup/abi1.json", 'r') as f:
    abi = json.load(f)

def StoreChat(chat_id, sender_address, content, endpoint):
	provider_url = "https://rpc-amoy.polygon.technology/"
	w3 = Web3(Web3.HTTPProvider(provider_url))

	w3.middleware_onion.inject(geth_poa_middleware, layer=0)


	contract_address = "0x59009D0a30CF0ccCC2780a618fc862d0A13EaB70"  
	user_address = "0xB022BDdd12168BaaB3022E87500d2C71E8109264" 
	private_key = "09a670370d9096c270d3a049e79696859e0ca6eb07866a7d77c3c6ccca9435ca" 

	balance = w3.eth.get_balance(user_address)
	print(f"Account balance: {w3.from_wei(balance, 'ether')} ETH")


	contract = w3.eth.contract(address=contract_address, abi=abi)

	timestamp = int(w3.eth.get_block('latest')['timestamp'])

	transaction = contract.functions.addChat(
		chat_id,
		sender_address,
		content,
		endpoint,
		timestamp
	).build_transaction({
		'chainId': 80002,  
		'from': user_address,
		'gas': 210000,  
		'gasPrice': w3.to_wei('50', 'gwei'),
		'nonce': w3.eth.get_transaction_count(user_address)
	})

	signed_tx = w3.eth.account.sign_transaction(transaction, private_key)

	tx_hash = w3.eth.send_raw_transaction(signed_tx.rawTransaction)

	tx_receipt = w3.eth.wait_for_transaction_receipt(tx_hash)

	a = f"Transaction hash: {tx_hash.hex()} --- "
	b = f"Transaction receipt: {tx_receipt}"
	return a+b


chat_id = "chat123"
sender_address = "0x123...abc"
content = "Hello, this is a test chat."
endpoint = "http://example.com"

StoreChat(chat_id, sender_address, content, endpoint)