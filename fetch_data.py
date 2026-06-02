import pandas as pd
import json
import sys

# TON LIEN GOOGLE SHEET PUBLIÉ EN CSV
SHEET_CSV_URL = "https://docs.google.com/spreadsheets/d/e/2PACX-1vT47ujfdBRIw6zeueBvuFWKagcl47oy8AcORsLKgiCpP7U-Eh01bcC2MZ77VC5pfAWN4xRDCfA-0hHI/pub?gid=14&single=true&output=csv"

def clean_percentage(val):
    if pd.isna(val) or val == '': return 0.0
    try:
        val = str(val).replace('%', '').replace(',', '.').replace(' ', '').strip()
        return float(val) / 100.0
    except:
        return 0.0

def clean_float(val):
    if pd.isna(val) or val == '': return 0.0
    try:
        val = str(val).replace('CHF', '').replace(',', '').replace(' ', '').strip()
        return float(val)
    except:
        return 0.0

def main():
    try:
        # Lecture du fichier CSV
        df = pd.read_csv(SHEET_CSV_URL)
        
        # Nettoyage forcé des espaces et sauts de ligne dans les noms des colonnes
        df.columns = [str(c).replace('\n', ' ').replace('  ', ' ').strip() for c in df.columns]
        print("Colonnes détectées dans ton fichier :", list(df.columns))
        
        portfolio_items = []
        
        # Parcourir les lignes du tableau
        for _, row in df.iterrows():
            # Trouver la colonne Ticker (souvent la 2ème colonne, ou appelée 'Stock Ticker' / 'Ticker')
            ticker_val = row.iloc[1] if len(row) > 1 else None
            for col in df.columns:
                if 'ticker' in col.lower():
                    ticker_val = row[col]
                    break
            
            # Si pas de ticker ou si c'est une ligne de total, on passe
            if pd.isna(ticker_val) or str(ticker_val).strip() == '' or 'total' in str(ticker_val).lower():
                continue
            
            # Extraction intelligente des colonnes par mots-clés
            item = {
                "style": "QUALITY",
                "name": "Inconnu",
                "ticker": str(ticker_val).strip(),
                "px_achat": 0.0,
                "px_actuel": 0.0,
                "dcf_cible": None,
                "valeur_chf": 0.0,
                "perf_tot": 0.0,
                "ytd": 0.0
            }
            
            for col in df.columns:
                c_low = col.lower()
                if 'style' in c_low or 'type' in c_low:
                    item["style"] = str(row[col]).upper().strip()
                elif 'name' in c_low or 'nom' in c_low:
                    item["name"] = str(row[col]).capitalize().strip()
                elif "achat" in c_low:
                    item["px_achat"] = clean_float(row[col])
                elif "google price" in c_low or "prix actuel" in c_low or "price" in c_low:
                    item["px_actuel"] = clean_float(row[col])
                elif "dcf" in c_low:
                    item["dcf_cible"] = clean_float(row[col])
                elif "valeur" in c_low or "value" in c_low:
                    item["valeur_chf"] = clean_float(row[col])
                elif "perf" in c_low:
                    item["perf_tot"] = clean_percentage(row[col])
                elif "ytd" in c_low:
                    item["ytd"] = clean_percentage(row[col])
            
            # Correction si le nom est vide
            if item["name"] == "Inconnu" and len(row) > 0:
                item["name"] = str(row.iloc[0]).capitalize().strip()
                
            # Calcul de l'upside
            if item["dcf_cible"] and item["px_actuel"] > 0:
                item["upside"] = (item["dcf_cible"] - item["px_actuel"]) / item["px_actuel"]
            else:
                item["upside"] = 0.0
                
            portfolio_items.append(item)
            
        # Si le tableau est vide, erreur volontaire pour le log
        if not portfolio_items:
            print("Erreur : Aucune donnée valide extraite du Google Sheet.")
            sys.exit(1)
            
        with open('data.json', 'w', encoding='utf-8') as f:
            json.dump(portfolio_items, f, indent=4, ensure_ascii=False)
        print(f"Succès ! {len(portfolio_items)} lignes traitées avec succès.")

    except Exception as e:
        print(f"Erreur critique pendant l'exécution : {str(e)}")
        sys.exit(1)

if __name__ == "__main__":
    main()
