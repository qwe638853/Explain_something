from fastapi import FastAPI
from pydantic import BaseModel
from transaction import get_wallet_transactions
from LLM import analyze_transactions
from fastapi.middleware.cors import CORSMiddleware  

app = FastAPI()

# 設定 CORS，允許 Vue 前端請求
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

DAY_TIME = 24 * 60 * 60
WEEK_TIME = 7 * DAY_TIME
MONTH_TIME = 31 * WEEK_TIME

class WalletRequest(BaseModel):
    address: str
    period: str  

@app.post("/app/analyze_wallet")
def analyze_wallet(request: WalletRequest):
    timeSize = WEEK_TIME
    if request.period == "day":
        timeSize = DAY_TIME
    elif request.period == "month":
        timeSize = MONTH_TIME

    transactions = get_wallet_transactions(request.address, timeSize)
    analysis = analyze_transactions(request.address, transactions)

    return {"wallet": request.address, "analysis": analysis}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
