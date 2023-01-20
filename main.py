from web3 import Web3
import time

#eth node
web3 = Web3(Web3.HTTPProvider(''))

#your address
sender_address = ""

#private key
private_key = ""

#dex contract
contract_address = "" 

#weth contract
spend = web3.toChecksumAddress("")

#token contract
contract_id = web3.toChecksumAddress("")

#contract abi
contarct_abi = ''

#token abi
sellAbi = ''


contract = web3.eth.contract(address=contract_address, abi=contarct_abi)
SellTokenContract = web3.eth.contract(contract_id, abi=sellAbi)
balance = SellTokenContract.functions.balanceOf(sender_address).call()
symbol = SellTokenContract.functions.symbol().call()

#token ammount to sold
tokenValue = web3.toWei(1.018, 'ether')

nonce = web3.eth.get_transaction_count(sender_address)

#approve tx
tokenValue2 = web3.fromWei(tokenValue, 'ether')
start = time.time()
approve = SellTokenContract.functions.approve(contract_address, balance).buildTransaction({
            'from': sender_address,
            'gasPrice': web3.toWei('5','gwei'),
            'nonce': nonce,
            })

signed_txn = web3.eth.account.sign_transaction(approve, private_key)
tx_token = web3.eth.send_raw_transaction(signed_txn.rawTransaction)

print(tx_token.hex())
time.sleep(10)

#swap tx
swap_transaction = contract.functions.swapExactTokensForETH(
            tokenValue ,0, 
            [contract_id, spend],
            sender_address,
            (int(time.time()) + 1000000)

            ).buildTransaction({
            'from': sender_address,
            'gasPrice': web3.toWei('5','gwei'),
            'nonce': web3.eth.get_transaction_count(sender_address),
            })
    
signed_txn = web3.eth.account.sign_transaction(swap_transaction, private_key)
tx_token = web3.eth.send_raw_transaction(signed_txn.rawTransaction)
print(f"Sold {symbol}: " + web3.toHex(tx_token))
