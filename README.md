# PORTFX — Portfolio Tracker

Dashboard de portfolio publié sur GitHub Pages, connecté à Google Sheets.

## 🚀 Mise en place (10 minutes)

### 1. Créer le dépôt GitHub

```bash
git init
git add .
git commit -m "Initial commit"
git remote add origin https://github.com/VOTRE_USERNAME/portfolio-tracker.git
git push -u origin main
```

### 2. Activer GitHub Pages

1. Aller dans **Settings > Pages**
2. Source : **GitHub Actions**
3. Le site sera disponible à `https://VOTRE_USERNAME.github.io/portfolio-tracker/`

### 3. Publier votre Google Sheet en CSV

1. Ouvrir votre Google Sheet
2. **Fichier > Partager > Publier sur le web**
3. Choisir **Feuille 1** et format **Valeurs séparées par des virgules (.csv)**
4. Cliquer **Publier** et copier l'URL

> ⚠️ L'URL ressemble à :  
> `https://docs.google.com/spreadsheets/d/VOTRE_ID/pub?output=csv`

### 4. Configurer le site

Ouvrir `index.html` et modifier la section CONFIG :

```javascript
const CONFIG = {
  SHEET_CSV_URL: 'https://docs.google.com/spreadsheets/d/VOTRE_ID/pub?output=csv',
  REFRESH_INTERVAL: 15 * 60 * 1000, // 15 minutes
  CASH: 37400, // Votre cash disponible en CHF
  COST_BASIS_CHF: 710632, // Coût total d'acquisition en CHF
};
```

### 5. Colonnes Google Sheet requises

Le site lit ces colonnes (noms exacts) :

| Colonne | Description |
|---------|-------------|
| `Stock Ticker` | Symbole boursier (ex: GOOGL) |
| `Name` | Nom de la position |
| `style` | quality / garp / growth+ / value / defensive / cyclic / etf |
| `prix d'achat` | Prix d'achat en devise locale |
| `Google price` | Prix actuel (peut être une formule GOOGLEFINANCE) |
| `DCF 5y` | Prix cible DCF |
| `valeur` | Valeur en CHF |
| `perf` | Performance totale en % |
| `YTD` | Performance YTD en % |

### 6. Formules Google Sheets utiles

Utilisez `GOOGLEFINANCE` pour des prix en temps réel :

```
=GOOGLEFINANCE("GOOGL","price")
=GOOGLEFINANCE("CURRENCY:USDCHF")
```

Pour la valeur en CHF :
```
=nb_actions * prix_actuel * taux_usdchf
```

## 🔄 Mise à jour automatique

Le site se rafraîchit **toutes les 15 minutes** directement depuis Google Sheets via JavaScript.

Pas besoin de redéployer — tant que votre Google Sheet est publié, les données se mettent à jour automatiquement dans le navigateur.

## 📱 Fonctionnalités

- **Vue d'ensemble** : KPIs, graphiques secteur/géographie, tableau des positions
- **Positions** : Détail complet avec DCF et upside
- **ETF** : Vue séparée des fonds
- **Performance** : Graphiques total et YTD
- **Allocation** : Répartition par secteur, géographie, style
- **Watchlist** : Positions triées par upside DCF

## ⚙️ Personnalisation

### Modifier la répartition géographique

Dans `index.html`, chercher `renderGeoChart` et ajuster les pourcentages selon votre portefeuille réel.

### Modifier le cash disponible

Modifier `CASH: 37400` dans la section CONFIG.

### Changer l'intervalle de rafraîchissement

`REFRESH_INTERVAL: 15 * 60 * 1000` (en millisecondes). 15 min = 15 * 60 * 1000.
