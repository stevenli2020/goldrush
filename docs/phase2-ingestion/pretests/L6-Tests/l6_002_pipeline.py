import os
import subprocess
import pandas as pd

def fetch_ofac_sdn_list():
    """Downloads official US Treasury OFAC Specially Designated Nationals (SDN) List

  using curl and saves it locally to ./data/sanctions/sdn.csv.
  """
    output_dir = './data/sanctions'
    save_path = os.path.join(output_dir, 'sdn.csv')
    ofac_url = 'https://www.treasury.gov/ofac/downloads/sdn.csv'
    os.makedirs(output_dir, exist_ok=True)
    print(f'[1/3] Downloading official OFAC SDN List from: {ofac_url}')
    cmd = ['curl', '-s', '-L', '-A', 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko)', '-o', save_path, ofac_url]
    subprocess.run(cmd, check=True)
    print(f'      Successfully saved raw list to: {save_path}')
    return save_path

def parse_and_engineer_l6_002(file_path):
    """Parses OFAC SDN CSV file and engineers quantitative features for variable L6-002."""
    print('[2/3] Parsing SDN database and engineering features...')
    columns = ['ent_num', 'sdn_name', 'sdn_type', 'program', 'title', 'call_sign', 'vess_type', 'tonnage', 'grt', 'vess_flag', 'vess_owner', 'remarks']
    df = pd.read_csv(file_path, names=columns, header=None, on_bad_lines='skip', encoding='latin1')
    df['sdn_type'] = df['sdn_type'].astype(str).str.strip().str.title()
    type_mapping = {'0': 'Entity', '-': 'Entity', '': 'Entity', 'Nan': 'Entity', 'None': 'Entity'}
    df['sdn_type'] = df['sdn_type'].replace(type_mapping)
    total_sdn_count = len(df)
    type_counts = df['sdn_type'].value_counts().to_dict()
    df['program_str'] = df['program'].fillna('').astype(str)
    df['remarks_str'] = df['remarks'].fillna('').astype(str)
    russia_ukr_mask = df['program_str'].str.contains('UKRAINE|RUSSIA|RUSHAR|EO14024|EO13661|PEESA|CAATSA', case=False)
    iran_mask = df['program_str'].str.contains('IRAN|IRGC|IFSR|IFCA|HRIT-IR', case=False)
    china_hk_mask = df['program_str'].str.contains('HKAA|HK-EO13936|CMIC|UFLPA|CHINA', case=False) | df['remarks_str'].str.contains('China|Hong Kong|\\bPRC\\b', case=False, regex=True)
    cyber_mask = df['program_str'].str.contains('CYBER', case=False)
    sdgt_mask = df['program_str'].str.contains('SDGT|TERR', case=False)
    program_exposure = {'Russia / Ukraine Exposure': russia_ukr_mask.sum(), 'Iran Exposure': iran_mask.sum(), 'China / Hong Kong Exposure': china_hk_mask.sum(), 'Counter-Terrorism (SDGT)': sdgt_mask.sum(), 'Cyber-Related Sanctions': cyber_mask.sum()}
    print('[3/3] Feature extraction complete.')
    return {'total_sdn_count': total_sdn_count, 'type_counts': type_counts, 'program_exposure': program_exposure, 'raw_df': df}
if __name__ == '__main__':
    try:
        raw_csv = fetch_ofac_sdn_list()
        features = parse_and_engineer_l6_002(raw_csv)
        pd.set_option('display.max_columns', None)
        pd.set_option('display.width', 1000)
        print('\n=========================================================================')
        print('           L6-002: OFAC SANCTIONS & FINANCIAL WARFARE SUMMARY           ')
        print('=========================================================================')
        print(f"Total Active Sanctioned Targets : {features['total_sdn_count']:,}")
        print('\n[Target Type Breakdown]')
        print('-------------------------------------------------------------------------')
        for ent_type, count in features['type_counts'].items():
            pct = count / features['total_sdn_count'] * 100
            print(f'  • {ent_type:<25} : {count:>7,}  ({pct:>5.1f}%)')
        print('\n[Key Geopolitical Program & Country Exposure]')
        print('-------------------------------------------------------------------------')
        for prog_name, count in features['program_exposure'].items():
            pct = count / features['total_sdn_count'] * 100
            print(f'  • {prog_name:<25} : {count:>7,}  ({pct:>5.1f}%)')
        print('\n[Sample Sanctioned Entries (First 5 Rows)]')
        print('-------------------------------------------------------------------------')
        sample_cols = ['ent_num', 'sdn_name', 'sdn_type', 'program']
        print(features['raw_df'][sample_cols].head(5).to_string(index=False))
        print('=========================================================================\n')
    except Exception as e:
        print(f'\nError occurred: {e}')
