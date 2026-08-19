import json
from curl_cffi import requests

DIRECT_FILE_URL = (
    "https://www.gold.org/download/file/21037/ETF_Flows_2026-08-04_1202.xlsx"
)


def download_file_directly():
  # 1. Load cookies
  try:
    with open("cookies.json", "r") as f:
      cookie_list = json.load(f)
    cookies = {c["name"]: c["value"] for c in cookie_list}
  except FileNotFoundError:
    print("❌ 'cookies.json' not found.")
    return

  # 2. Request the file directly with browser TLS impersonation
  session = requests.Session()
  print("[*] Downloading file directly from endpoint...")
  response = session.get(DIRECT_FILE_URL, cookies=cookies, impersonate="chrome")

  if response.status_code == 200:
    filename = "gold_etfs_holdings_flows.xlsx"
    with open(filename, "wb") as f:
      f.write(response.content)
    print(f"🎉 Success! File downloaded and saved as '{filename}'.")
  else:
    print(
        f"❌ Failed to download. Status code: {response.status_code} (Your"
        " cookies might have expired; try re-exporting fresh ones)."
    )


if __name__ == "__main__":
  download_file_directly()