import requests
import os
from datetime import datetime
from dotenv import load_dotenv

load_dotenv()
ETHERSCAN_API_KEY = os.getenv("ETHERSCAN_API_KEY")

def get_wallet_transactions(wallet_address: str,timeSize: int):
    
    #篩選時間範圍
    now = int(datetime.utcnow().timestamp())
    startTime = now - timeSize
    
     # 取得 ETH 交易
    eth_url = f"https://api.etherscan.io/api?module=account&action=txlist&address={wallet_address}&startblock=0&endblock=99999999&sort=desc&apikey={ETHERSCAN_API_KEY}"
    eth_transactions = requests.get(eth_url).json().get("result", [])

    # 取得 ERC-20 交易
    erc20_url = f"https://api.etherscan.io/api?module=account&action=tokentx&address={wallet_address}&startblock=0&endblock=99999999&sort=desc&apikey={ETHERSCAN_API_KEY}"
    erc20_transactions = requests.get(erc20_url).json().get("result", [])

    # 取得 ERC-721 (NFT) 交易
    nft_url = f"https://api.etherscan.io/api?module=account&action=tokennfttx&address={wallet_address}&startblock=0&endblock=99999999&sort=desc&apikey={ETHERSCAN_API_KEY}"
    nft_transactions = requests.get(nft_url).json().get("result", [])

    # 取得 ERC-1155 交易
    erc1155_url = f"https://api.etherscan.io/api?module=account&action=token1155tx&address={wallet_address}&startblock=0&endblock=99999999&sort=desc&apikey={ETHERSCAN_API_KEY}"
    erc1155_transactions = requests.get(erc1155_url).json().get("result", [])
    
     # 過濾 ETH 交易
    filtered_eth = [
        {
            "type": "ETH",
            "time": datetime.utcfromtimestamp(int(tx["timeStamp"])).strftime('%Y-%m-%d %H:%M:%S'),
            "from": tx["from"],
            "to": tx["to"],
            "value": (int(tx["value"])/1e18), #轉換代幣單位
            "hash": tx["hash"],
            "input": tx["input"],
            "functionName": (tx["functionName"] if tx["functionName"] else "未顯示")
        }
        for tx in eth_transactions if int(tx["timeStamp"]) >= startTime
    ]
    
    # 過濾 ERC-20 交易
    filtered_erc20 = [
        {
            "type": "ERC-20",
            "token": tx["tokenSymbol"],
            "time": datetime.utcfromtimestamp(int(tx["timeStamp"])).strftime('%Y-%m-%d %H:%M:%S'),
            "from": tx["from"],
            "to": tx["to"],
            "value": (int(tx["value"]) / (10 ** int(tx["tokenDecimal"]))),  # 轉換代幣單位
            "hash": tx["hash"],
            "input": tx["input"]
        }
        for tx in erc20_transactions if int(tx["timeStamp"]) >= startTime
    ]

    # 過濾 ERC-721 (NFT) 交易
    filtered_nft = [
        {
            "type": "ERC-721",
            "token": tx["tokenName"],
            "tokenId": tx["tokenID"],
            "time": datetime.utcfromtimestamp(int(tx["timeStamp"])).strftime('%Y-%m-%d %H:%M:%S'),
            "from": tx["from"],
            "to": tx["to"],
            "hash": tx["hash"],
            "input": tx["input"]
        }
        for tx in nft_transactions if int(tx["timeStamp"]) >= startTime
    ]

    # 過濾 ERC-1155 交易
    filtered_erc1155 = [
        {
            "type": "ERC-1155",
            "token": tx["tokenName"],
            "tokenId": tx["tokenID"],
            "value": tx["value"],
            "time": datetime.utcfromtimestamp(int(tx["timeStamp"])).strftime('%Y-%m-%d %H:%M:%S'),
            "from": tx["from"],
            "to": tx["to"],
            "hash": tx["hash"],
            "input": tx["input"],
        }
        for tx in erc1155_transactions if int(tx["timeStamp"]) >= startTime
    ]

    # 合併所有交易
    all_transactions = filtered_eth + filtered_erc20 + filtered_nft + filtered_erc1155
    return all_transactions
