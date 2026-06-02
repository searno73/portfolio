import pandas as pd
import json

# METS TON LIEN COPIÉ ENTRE LES GUILLEMETS CI-DESSOUS :
SHEET_CSV_URL = "https://docs.google.com/spreadsheets/d/e/2PACX-1vT47ujfdBRIw6zeueBvuFWKagcl47oy8AcORsLKgiCpP7U-Eh01bcC2MZ77VC5pfAWN4xRDCfA-0hHI/pub?gid=14&single=true&output=csv"

def clean_percentage(val):
    if pd.isna(val): return 0.0
    if isinstance(val, str):
        val = val.replace('%', '').replace(',', '.').strip()
    try:
        return float(val) / 100.0
    except:
        return 0.0

def clean_float(val):
    if pd.isna(val): return 0.0
    if isinstance(val, str):
        val = val.replace(',', '').replace(' ', '').strip()
    try:
        return float(val)
    except:
        return 0.0

def main():
    df = pd.read_csv(SHEET_CSV_URL)
    portfolio_items = []
    
    for _, row in df.iterrows():
        # Détection de la colonne Ticker (s'adapte si le nom varie légèrement)
        ticker_col = 'Stock Ticker' if 'Stock Ticker' in df.columns else df.columns[1]
        if pd.isna(row.get(ticker_col)) or str(row.get(ticker_col)).strip() == '' or 'total' in str(row.get(ticker_col)).lower():
            continue
            
        item = {
            "style": str(row.get('Name', 'QUALITY')).upper().strip(),
            "name": str(row.get('Name', '')).capitalize().strip(),
            "ticker": str(row.get(ticker_col, '')).strip(),
            "px_achat": clean_float(row.get("prix\n d'achat\n") or row.get("prix d'achat")),
            "px_actuel": clean_float(row.get('Google\n Price\n') or row.get('Google Price')),
            "dcf_cible": clean_float(row.get('DCF 5y\n') or row.get('DCF 5y')),
            "valeur_chf": clean_float(row.get('valeur\n') or row.get('valeur')),
            "perf_tot": clean_percentage(row.get('perf\n') or row.get('perf')),
            "ytd": clean_percentage(row.get('YTD\n') or row.get('YTD'))
        }
        
        if item["dcf_cible"] > 0 and item["px_actuel"] > 0:
            item["upside"] = (item["dcf_cible"] - item["px_actuel"]) / item["px_actuel"]
        else:
            item["upside"] = 0.0
            
        portfolio_items.append(item)
        
    with open('data.json', 'w', encoding='utf-8') as f:
        json.dump(portfolio_items, f, indent=4, ensure_ascii=False)

if __name__ == "__main__":
    main()
