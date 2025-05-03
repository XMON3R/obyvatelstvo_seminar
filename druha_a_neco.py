'''import pandas as pd
import matplotlib.pyplot as plt
import os
import requests

# Cesta k výstupnímu adresáři s CSV soubory
output_directory = './edited/umrtnost'

# Roky, pro které chceme zobrazit data
zajimave_roky = ['2019', '2020', '2021', '2022', '2023']

# Názvy měsíců tak, jak jsou v CSV souborech
nazvy_mesicu_male = ['leden', 'únor', 'březen', 'duben', 'květen', 'červen', 'červenec', 'srpen', 'září', 'říjen', 'listopad', 'prosinec']
nazvy_mesicu_velke = ['Leden', 'Únor', 'Březen', 'Duben', 'Květen', 'Červen', 'Červenec', 'Srpen', 'Září', 'Říjen', 'Listopad', 'Prosinec']

# Funkce pro načtení dat z CSV souboru
def nacti_data(soubor):
    try:
        df = pd.read_csv(os.path.join(output_directory, soubor), encoding='utf-8')
        kraj_nazev = os.path.splitext(soubor)[0]
        kraj_nazev = kraj_nazev.replace('umrtnost_', '').replace(' (DEMD007M-ABS)', '').replace('_', ' ').strip()
        kraj_nazev = kraj_nazev.replace('jihocesky', 'Jihočeský kraj').replace('jihomoravsky', 'Jihomoravský kraj').replace('karlovarsky', 'Karlovarský kraj').replace('kralovohradecky', 'Královéhradecký kraj').replace('liberecky', 'Liberecký kraj').replace('moravskoslezsky', 'Moravskoslezský kraj').replace('olomoucky', 'Olomoucký kraj').replace('pardubicky', 'Pardubický kraj').replace('plzensky', 'Plzeňský kraj').replace('praha', 'Hlavní město Praha').replace('stredocesky', 'Středočeský kraj').replace('ustecky', 'Ústecký kraj').replace('vysocina', 'Kraj Vysočina').replace('zlinsky', 'Zlínský kraj').replace('cr', 'Česká republika')
        df['Kraj'] = kraj_nazev
        return df
    except Exception as e:
        print(f"Chyba při načítání souboru '{soubor}': {e}")
        return None

# Načteme data ze všech CSV souborů
all_data = []
for soubor in os.listdir(output_directory):
    if soubor.endswith('.csv'):
        df_kraj = nacti_data(soubor)
        if df_kraj is not None and df_kraj['Kraj'].iloc[0] != 'Česká republika':
            all_data.append(df_kraj)

# Sloučíme všechna data do jednoho DataFrame
df_all = pd.concat(all_data)

# Nastavíme index na sloupec 'Měsíc'
df_all = df_all.set_index('Měsíc')

# Připravíme data pro scatterplot
plt.figure(figsize=(14, 8))
for kraj in df_all['Kraj'].unique():
    df_kraj = df_all[df_all['Kraj'] == kraj][zajimave_roky].sum(axis=1)
    max_mesic = df_kraj.idxmax()
    min_mesic = df_kraj.idxmin()

    mesice_df = pd.DataFrame({'Měsíc': df_kraj.index, 'Celková úmrtnost': df_kraj.values})
    mesice_df['Měsíc_velky'] = mesice_df['Měsíc'].map(dict(zip(nazvy_mesicu_male, nazvy_mesicu_velke)))

    # Zvýrazníme měsíc s nejvyšší úmrtností
    max_row = mesice_df[mesice_df['Měsíc'] == max_mesic]
    plt.scatter(max_row['Měsíc_velky'], max_row['Celková úmrtnost'], color='red', label=f'{kraj} (nejvyšší)', s=80)

    # Zvýrazníme měsíc s nejnižší úmrtností
    min_row = mesice_df[mesice_df['Měsíc'] == min_mesic]
    plt.scatter(min_row['Měsíc_velky'], min_row['Celková úmrtnost'], color='green', label=f'{kraj} (nejnižší)', s=80)

plt.xlabel('Měsíc')
plt.ylabel(f'Celková úmrtnost ({", ".join(zajimave_roky)})')
plt.title('Nejvyšší a nejnižší měsíční úmrtnost podle krajů (2019-2023)')
plt.xticks(rotation=45, ha='right')
plt.legend(title='Kraj', bbox_to_anchor=(1.05, 1), loc='upper left')
plt.grid(True)
plt.tight_layout()
plt.show()

'''


import pandas as pd
import geopandas
import matplotlib.pyplot as plt
import os
import requests

# Cesta k výstupnímu adresáři s CSV soubory
output_directory = './edited/umrtnost'

# URL k GeoJSON souboru s hranicemi krajů ČR
geojson_url = 'https://raw.githubusercontent.com/Plavit/Simple-Dash-Plotly-Map-Czech-Regions/main/maps/czech-regions-low-res.json'

# Roky, pro které chceme zobrazit data
zajimave_roky = ['2019', '2020', '2021', '2022', '2023']

# Názvy měsíců tak, jak jsou v CSV souborech
nazvy_mesicu_male = ['leden', 'únor', 'březen', 'duben', 'květen', 'červen', 'červenec', 'srpen', 'září', 'říjen', 'listopad', 'prosinec']
nazvy_mesicu_velke = ['Leden', 'Únor', 'Březen', 'Duben', 'Květen', 'Červen', 'Červenec', 'Srpen', 'Září', 'Říjen', 'Listopad', 'Prosinec']
mesic_mapovani = dict(zip(nazvy_mesicu_male, nazvy_mesicu_velke))

# Funkce pro načtení dat z CSV souboru
def nacti_data(soubor):
    try:
        df = pd.read_csv(os.path.join(output_directory, soubor), encoding='utf-8')
        kraj_nazev = os.path.splitext(soubor)[0]
        kraj_nazev = kraj_nazev.replace('umrtnost_', '').replace(' (DEMD007M-ABS)', '').replace('_', ' ').strip()
        kraj_nazev = kraj_nazev.replace('jihocesky', 'Jihočeský kraj').replace('jihomoravsky', 'Jihomoravský kraj').replace('karlovarsky', 'Karlovarský kraj').replace('kralovohradecky', 'Královéhradecký kraj').replace('liberecky', 'Liberecký kraj').replace('moravskoslezsky', 'Moravskoslezský kraj').replace('olomoucky', 'Olomoucký kraj').replace('pardubicky', 'Pardubický kraj').replace('plzensky', 'Plzeňský kraj').replace('praha', 'Hlavní město Praha').replace('stredocesky', 'Středočeský kraj').replace('ustecky', 'Ústecký kraj').replace('vysocina', 'Kraj Vysočina').replace('zlinsky', 'Zlínský kraj').replace('cr', 'Česká republika')
        df['Kraj'] = kraj_nazev
        df = df.set_index('Měsíc')
        return df
    except Exception as e:
        print(f"Chyba při načítání souboru '{soubor}': {e}")
        return None

# Načteme data ze všech CSV souborů
all_data = []
for soubor in os.listdir(output_directory):
    if soubor.endswith('.csv'):
        df_kraj = nacti_data(soubor)
        if df_kraj is not None and df_kraj['Kraj'].iloc[0] != 'Česká republika':
            all_data.append(df_kraj)

# Sloučíme všechna data do jednoho DataFrame
df_all = pd.concat(all_data)

# Připravíme prázdný DataFrame pro extrémy
df_extremy_mesicu = pd.DataFrame(columns=['Kraj', 'Nejvyšší úmrtnost', 'Nejnižší úmrtnost'])

# Projdeme každý kraj a najdeme extrémní měsíce
for kraj in df_all['Kraj'].unique():
    df_kraj = df_all[df_all['Kraj'] == kraj]
    mesicni_umrtnost = df_kraj[zajimave_roky].sum(axis=1)
    if not mesicni_umrtnost.empty:
        max_mesic = mesicni_umrtnost.idxmax()
        min_mesic = mesicni_umrtnost.idxmin()
        df_extremy_mesicu = pd.concat([df_extremy_mesicu, pd.DataFrame({'Kraj': [kraj], 'Nejvyšší úmrtnost': [max_mesic], 'Nejnižší úmrtnost': [min_mesic]})], ignore_index=True)

# Načteme GeoJSON z URL pomocí geopandas
try:
    response = requests.get(geojson_url)
    response.raise_for_status()
    mapa_cr = geopandas.read_file(response.text)
    mapa_cr = mapa_cr.rename(columns={'name': 'Kraj'}) # Rename for consistent merging
except requests.exceptions.RequestException as e:
    print(f"Error fetching GeoJSON from URL: {e}")
    exit()
except fiona.errors.DriverError as e:
    print(f"Error reading GeoJSON: {e}")
    exit()
except Exception as e:
    print(f"An unexpected error occurred while reading GeoJSON: {e}")
    exit()

# Propojíme data o extrémech s geografickými daty
mapa_extremy = mapa_cr.merge(df_extremy_mesicu, on='Kraj', how='left')

# Vytvoříme graf
fig, ax = plt.subplots(1, 1, figsize=(10, 10))
mapa_extremy.plot(linewidth=0.8, ax=ax, edgecolor='0.8', color='lightgray')
ax.set_title('Měsíce s nejvyšší a nejnižší úmrtností (2019-2023)')
ax.set_axis_off()

# Přidáme textové anotace s názvy měsíců a názvem kraje na centroidy krajů
for idx, row in mapa_extremy.iterrows():
    centroid = row.geometry.centroid
    kraj_nazev = row['Kraj']
    nejvyssi = row['Nejvyšší úmrtnost']
    nejnizsi = row['Nejnižší úmrtnost']

    if pd.notna(nejvyssi):
        ax.annotate(f'Max: {nejvyssi} ({kraj_nazev})', xy=(centroid.x, centroid.y), xytext=(5, 5), textcoords="offset points", fontsize=7, ha='left', color='red')
    if pd.notna(nejnizsi):
        ax.annotate(f'Min: {nejnizsi} ({kraj_nazev})', xy=(centroid.x, centroid.y), xytext=(5, -15), textcoords="offset points", fontsize=7, ha='left', color='green')

plt.tight_layout()
plt.show()