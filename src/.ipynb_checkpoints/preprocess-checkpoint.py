from pathlib import Path
import pandas as pd

# 1. Determine project root
try:
    # when run as a script
    ROOT = Path(__file__).parent.parent
except NameError:
    # when run in a notebook via %run
    ROOT = Path().resolve().parent

# 2. Define input & output paths
RAW_CSV     = ROOT / "data" / "survey.csv"
CLEANED_CSV = ROOT / "data" / "cleaned_survey.csv"

# 3. Load raw data
print(f"📥 Loading raw data from {RAW_CSV}")
df = pd.read_csv(RAW_CSV)

# 4. Drop rows missing the target
df = df.dropna(subset=['work_interfere'])

# 5. Map to RiskLevel
risk_map = {
    'Never':     'Low',
    'Rarely':    'Moderate',
    'Sometimes': 'Moderate',
    'Often':     'High'
}
df['RiskLevel'] = df['work_interfere'].map(risk_map)

# 6. Drop unused columns
for col in ['work_interfere','Timestamp','state','comments','treatment']:
    if col in df.columns:
        df = df.drop(columns=[col])

# 7. Save cleaned data
print(f"💾 Saving cleaned data to {CLEANED_CSV}")
df.to_csv(CLEANED_CSV, index=False)
print("✅ Preprocessing complete.")