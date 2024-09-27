import requests
import pandas as pd

# 定義要抓取的 URL 列表
urls = [
    "https://www.twse.com.tw/rwd/zh/afterTrading/STOCK_DAY?date=20240801&stockNo=2330",
    "https://www.twse.com.tw/rwd/zh/afterTrading/STOCK_DAY?date=20240701&stockNo=2330",
    "https://www.twse.com.tw/rwd/zh/afterTrading/STOCK_DAY?date=20240601&stockNo=2330"
]

# 儲存所有資料的列表
all_data = []

# 抓取每個 URL 的資料
for url in urls:
    response = requests.get(url)
    
    if response.status_code == 200:
        json_data = response.json()
        # 這假設 JSON 包含我們需要的資料在 'data' 這個 key 下
        if 'data' in json_data:
            # 解析 JSON 並將其轉換為資料框
            df = pd.DataFrame(json_data['data'], columns=json_data['fields'])
            all_data.append(df)
    else:
        print(f"Failed to retrieve data from {url}")

# 將所有資料框合併在一起
merged_df = pd.concat(all_data, ignore_index=True)

# 去除重複的標題
merged_df = merged_df.loc[:, ~merged_df.columns.duplicated()]

# 將結果存入 Excel 檔案
excel_file = 'stock_data.xlsx'
merged_df.to_excel(excel_file, index=False)

print(f"Data has been successfully saved to {excel_file}")
