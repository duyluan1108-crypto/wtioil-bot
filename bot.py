import requests
import json
from datetime import datetime

def get_wtioil_data():
    url = "https://api.hyperliquid.xyz/info"
    payload = {
        "type": "metaAndAssetCtxs",
        "dex": "xyz"
    }
    
    try:
        response = requests.post(url, json=payload, timeout=10)
        data = response.json()
        
        universe = data[0]["universe"]
        ctxs = data[1]
        
        # Tìm cặp xyz:CL (WTIOIL)
        for i, coin in enumerate(universe):
            if coin["name"] == "xyz:CL":
                ctx = ctxs[i]
                
                mark_price = float(ctx["markPx"])
                funding = float(ctx["funding"])  # funding hourly
                funding_8h = funding * 8         # quy đổi ra 8 tiếng
                oi = float(ctx["openInterest"])
                
                return {
                    "time": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                    "pair": "WTIOIL (xyz:CL)",
                    "mark_price": mark_price,
                    "funding_hourly": funding,
                    "funding_8h": funding_8h,
                    "open_interest": oi
                }
        
        return None
        
    except Exception as e:
        return {"error": str(e)}

def main():
    result = get_wtioil_data()
    
    if result is None:
        print("Không tìm thấy cặp WTIOIL")
        return
    
    if "error" in result:
        print("Lỗi:", result["error"])
        return
    
    # In ra màn hình
    print("=" * 50)
    print(f"Thời gian      : {result['time']}")
    print(f"Cặp           : {result['pair']}")
    print(f"Giá Mark      : {result['mark_price']:.3f}")
    print(f"Funding (1h)  : {result['funding_hourly']*100:.6f}%")
    print(f"Funding (8h)  : {result['funding_8h']*100:.6f}%")
    print(f"Open Interest : {result['open_interest']:,.0f}")
    print("=" * 50)
    
    # Ghi vào file log
    with open("log.txt", "a", encoding="utf-8") as f:
        f.write(f"{result['time']} | Giá: {result['mark_price']:.3f} | Funding 8h: {result['funding_8h']*100:.6f}% | OI: {result['open_interest']:,.0f}\n")

if __name__ == "__main__":
    main()
