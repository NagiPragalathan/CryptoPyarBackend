from web3 import Web3
from web3.middleware import geth_poa_middleware
import json

# Load the ABI
with open("G:/Nillion-Compute/Backup/abi1.json", 'r') as f:
    abi = json.load(f)

def StoreMusic(current_address, music_ipfs, music_name, duration, language, artist_name, genre, ipfs_song_image):
    provider_url = "https://rpc-amoy.polygon.technology/"
    w3 = Web3(Web3.HTTPProvider(provider_url))

    # Inject the POA middleware (for Polygon or other chains that require it)
    w3.middleware_onion.inject(geth_poa_middleware, layer=0)

    contract_address = "0x59009D0a30CF0ccCC2780a618fc862d0A13EaB70"  
    user_address = "0xB022BDdd12168BaaB3022E87500d2C71E8109264" 
    private_key = "09a670370d9096c270d3a049e79696859e0ca6eb07866a7d77c3c6ccca9435ca" 

    balance = w3.eth.get_balance(user_address)
    print(f"Account balance: {w3.from_wei(balance, 'ether')} ETH")

    # Load the contract
    contract = w3.eth.contract(address=contract_address, abi=abi)

    # Build the transaction to add a song
    transaction = contract.functions.addSong(
        current_address,
        music_ipfs,
        music_name,
        duration,
        language,
        artist_name,
        genre,
        ipfs_song_image
    ).build_transaction({
        'chainId': 80002,  # Polygon Mumbai Testnet chain ID
        'from': user_address,
        'gas': 30000,  # Adjusted gas limit to ensure the transaction can be processed
        'gasPrice': w3.to_wei('30', 'gwei'),  # Lowered gas price (could reduce cost, but may delay confirmation)
        'nonce': w3.eth.get_transaction_count(user_address)
    })

    # Sign the transaction
    signed_tx = w3.eth.account.sign_transaction(transaction, private_key)

    # Send the transaction
    tx_hash = w3.eth.send_raw_transaction(signed_tx.rawTransaction)

    # Wait for the transaction receipt
    tx_receipt = w3.eth.wait_for_transaction_receipt(tx_hash)

    # Return the transaction details
    return f"Transaction hash: {tx_hash.hex()} --- Transaction receipt: {tx_receipt}"

# Sample data to store a music record
current_address = "0xB022BDdd12168BaaB3022E87500d2C71E8109264"  # Replace with a valid Ethereum address
music_ipfs = "ipfs://examplehash"
music_name = "Test Song"
duration = 180  # duration in seconds
language = "English"
artist_name = "Test Artist"
genre = "Pop"
ipfs_song_image = "ipfs://imagehash"

# Store the music record using the function
result = StoreMusic(current_address, music_ipfs, music_name, duration, language, artist_name, genre, ipfs_song_image)
print(result)
