from web3 import Web3
from web3.middleware import geth_poa_middleware
from dotenv import load_dotenv
import os
load_dotenv()

private_key = os.environ.get('account_private_key')
adress = os.environ.get('account_address')
rpc_url = "https://avalanche.drpc.org"
web3 = Web3(Web3.HTTPProvider(rpc_url))
web3.middleware_onion.inject(geth_poa_middleware, layer=0)
print(web3.isConnected())
print(Web3.fromWei(web3.eth.get_balance(adress),'ether')) 
c=0
while True:
    nonce = web3.eth.get_transaction_count(adress)

    # Get and determine gas parameters
    latest_block = web3.eth.get_block('latest')
    base_fee_per_gas = latest_block.baseFeePerGas   # Base fee in the latest block (in wei)
    max_priority_fee_per_gas = web3.toWei(0, 'gwei') # Priority fee to include the transaction in the block
    max_fee_per_gas = (2 * base_fee_per_gas) + max_priority_fee_per_gas # Maximum amount you’re willing to pay 

    tx = {
        'nonce': nonce,
        'chainId': 43114,
        'to': adress, 
        'from':adress,
        'data':'0x646174613a2c7b2270223a226173632d3230222c226f70223a226d696e74222c227469636b223a226176616c222c22616d74223a22313030303030303030227d',
        # 'gasPrice': web3.eth.gas_price,
        'maxFeePerGas': max_fee_per_gas, # Maximum amount you’re willing to pay
        'maxPriorityFeePerGas': max_priority_fee_per_gas, # Priority fee to include the transaction in the block
        'value': Web3.toWei(0, 'ether') 
    }
    try:
        gas = web3.eth.estimate_gas(tx) 
        tx['gas'] = gas 
        print(tx)
        signed_tx = web3.eth.account.sign_transaction(tx,private_key)
        tx_hash = web3.eth.send_raw_transaction(signed_tx.rawTransaction)
        print(web3.toHex(tx_hash))
        receipt = web3.eth.wait_for_transaction_receipt(tx_hash)
        if receipt.status == 1:
            c = c+1
            print("%s Mint Success!" %c)
            continue
        else:
            continue
    except Exception as e:
        print(e)
