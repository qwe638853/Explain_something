import openai
import os
from dotenv import load_dotenv

# 加載 .env 環境變數
load_dotenv()
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

def analyze_transactions(wallet_address: str, transactions):

    if not transactions:
        return "該錢包在此期間沒有交易紀錄。"

    # 格式化交易數據
    #print("🚀 DEBUG: transactions =", transactions)

    formatted_data = "\n".join([
    # ETH 交易（value 以 Wei 顯示）
    f"{tx.get('time', '未知時間')} [ETH] {tx.get('from', '無顯示')} 轉 {tx.get('value', '0')} wei 給 {tx.get('to', '無顯示')}\n"
    f"🔹 方法: {tx.get('functionName', '無顯示')}\n"
    if tx.get('type') == "ETH" else

    # ERC-20 交易（顯示 Token 符號）
    f"{tx.get('time', '未知時間')} [ERC-20] {tx.get('from', '無顯示')} 轉 {tx.get('value', '0')} {tx.get('token', '未知 Token')} 給 {tx.get('to', '未知地址')}\n"
    if tx.get('type') == "ERC-20" else

    # ERC-721（NFT 交易，顯示 tokenId）
    f"{tx.get('time', '未知時間')} [ERC-721] {tx.get('from', '無顯示')} 轉 NFT ID {tx.get('tokenId', '未知 ID')} {tx.get('token', '未知 NFT')} 給 {tx.get('to', '未知地址')}\n"
    f"🔹 方法: {tx.get('functionName', '無顯示')}\n"
    if tx.get('type') == "ERC-721" else

    # ERC-1155（NFT 多資產交易）
    f"{tx.get('time', '未知時間')} [ERC-1155] {tx.get('from', '無顯示')} 轉 {tx.get('value', '未知數量')} 個 NFT ID {tx.get('tokenId', '未知 ID')} {tx.get('token', '未知 NFT')} 給 {tx.get('to', '無顯示')}\n"
    if tx.get('type') == "ERC-1155" else "其他交易類型"
    for tx in transactions if isinstance(tx, dict)
    ])
    
    print(formatted_data)

    # 設定 OpenAI Prompt
    prompt = f"""
    以下是錢包 {wallet_address} 的近期交易紀錄：
    {formatted_data}

    請基於這些交易紀錄進行分析，回答以下問題：
    1. 該錢包的交易模式是否存在明顯的特徵？請詳細描述。
    2. 是否可以根據交易數據推測該錢包的用途？例如，它是否偏向 DeFi 互動、NFT 交易、CEX 出入金，或其他用途？請詳細解釋你的推論過程。
    3. 是否存在異常交易行為，例如短時間內的大量交易、與已知風險地址的交互、或其他異常模式？
    4. 該錢包的交易行為是否有潛在的風險，例如洗錢、機器人操作，或者其他需要特別注意的模式？如果有，請說明你的判斷依據。

    請詳細解釋你的分析方法與推論過程，並確保基於交易數據進行客觀判斷，而非預設任何結論，並在最後給我關於這個地址的結論
    """

    # 發送 OpenAI API 請求
    try:
        client = openai.OpenAI(api_key=OPENAI_API_KEY)

        response = client.chat.completions.create(
            model="gpt-4",
            messages=[{"role": "user", "content": prompt}],
            temperature=0.7
        )

        return response.choices[0].message.content.strip()
    
    except Exception as e:
        print(f"❌ OpenAI API 錯誤: {e}")
        return "無法分析該錢包，請稍後再試。"

