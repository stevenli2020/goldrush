import os
import tempfile
import time
import pandas as pd
import cot_reports as cot

print("Downloading CFTC Disaggregated Futures COT reports (2010–2026)...")

all_years_data = []

# Fetch annual files from CFTC archive
with tempfile.TemporaryDirectory() as tmpdir:
    original_cwd = os.getcwd()
    os.chdir(tmpdir)
    try:
        for year in range(2010, 2027):
            print(f"Fetching {year}...")
            try:
                df_year = pd.DataFrame(cot.cot_year(year, cot_report_type="disaggregated_fut"))
                all_years_data.append(df_year)
                time.sleep(1.2)
            except Exception as e:
                print(f" -> Skipped {year}: {e}")
    finally:
        os.chdir(original_cwd)

# Combine datasets and standardize headers
df_disagg = pd.concat(all_years_data, ignore_index=True)
df_disagg.columns = df_disagg.columns.str.strip()

# 1. Exact Filter for Primary COMEX Gold (Code 088691)
if "CFTC_Contract_Market_Code" in df_disagg.columns:
    gold_df = df_disagg[
        df_disagg["CFTC_Contract_Market_Code"].astype(str).str.strip().str.zfill(6) == "088691"
    ].copy()
else:
    gold_df = df_disagg[
        df_disagg["Market_and_Exchange_Names"].str.strip() == "GOLD - COMMODITY EXCHANGE INC."
    ].copy()

# 2. Date Parsing
date_parsed = False
for date_col in [
    "Report_Date_as_YYYY-MM-DD",
    "Report_Date_as_MM_DD_YYYY",
    "As_of_Date_In_Form_YYMMDD",
    "As_of_Date_In_Form_YYYYMMDD",
]:
    if date_col in gold_df.columns:
        gold_df["Parsed_Date"] = pd.to_datetime(gold_df[date_col], errors="coerce")
        if gold_df["Parsed_Date"].notna().sum() > 0:
            date_parsed = True
            break

if not date_parsed:
    gold_df["Parsed_Date"] = pd.to_datetime(gold_df.index, errors="coerce")

gold_df = gold_df.dropna(subset=["Parsed_Date"]).sort_values("Parsed_Date").reset_index(drop=True)

# 3. Dynamic Column Mapping & Conversions
money_cols = [c for c in gold_df.columns if "Money" in c or "M_Money" in c]
long_col = [c for c in money_cols if "Long" in c and "All" in c][0]
short_col = [c for c in money_cols if "Short" in c and "All" in c][0]

gold_df[long_col] = pd.to_numeric(gold_df[long_col], errors="coerce")
gold_df[short_col] = pd.to_numeric(gold_df[short_col], errors="coerce")
gold_df["Open_Interest_All"] = pd.to_numeric(gold_df["Open_Interest_All"], errors="coerce")

gold_df["L10_001_Managed_Money_Net_Pos"] = gold_df[long_col] - gold_df[short_col]
gold_df["L10_002_Gold_Open_Interest"] = gold_df["Open_Interest_All"]

result_df = gold_df[[
    "Parsed_Date",
    "L10_002_Gold_Open_Interest",
    long_col,
    short_col,
    "L10_001_Managed_Money_Net_Pos"
]].copy()

# 4. Ingestion Validation Suite
print("\n" + "=" * 50)
print("RUNNING DATA VALIDATION CHECKS")
print("=" * 50)

duplicates = result_df[result_df["Parsed_Date"].duplicated(keep=False)]
if not duplicates.empty:
    print(f"❌ FAIL: Found {len(duplicates)} duplicate date rows!")
else:
    print("✅ PASS: Zero duplicate dates detected.")

result_df["Date_Diff"] = result_df["Parsed_Date"].diff().dt.days
gaps = result_df[result_df["Date_Diff"] > 10]
if not gaps.empty:
    print(f"⚠️  WARNING: Found {len(gaps)} potential missing report weeks (>10 day gap):")
    for idx, row in gaps.iterrows():
        prev_date = result_df.loc[idx - 1, "Parsed_Date"].strftime("%Y-%m-%d")
        curr_date = row["Parsed_Date"].strftime("%Y-%m-%d")
        print(f"   - {int(row['Date_Diff'])} day gap between {prev_date} and {curr_date}")
else:
    print("✅ PASS: Continuous weekly series verified.")

null_counts = result_df.drop(columns=["Date_Diff"]).isnull().sum()
if null_counts.sum() > 0:
    print("⚠️  WARNING: Null values found in target metrics:")
    print(null_counts[null_counts > 0])
else:
    print("✅ PASS: No null metric values.")

result_df = result_df.drop(columns=["Date_Diff"])

# 5. Export to File
output_csv = "comex_gold_cot_2010_2026.csv"
result_df.to_csv(output_csv, index=False)

print(f"\n=== Processed {len(result_df)} Unique Weekly COMEX Gold Records ===")
print(f"💾 File created: {os.path.abspath(output_csv)}")

print("\n--- Latest 10 Weekly Records ---")
print(result_df.tail(10).to_string(index=False))