import pandas as pd
import geopandas
import matplotlib.pyplot as plt
import os
import requests

# Cesta k výstupnímu adresáři s CSV soubory
output_directory = './edited/umrtnost'

# URL k GeoJSON souboru s hranicemi krajů ČR
geojson_url = 'https://raw.githubusercontent.com/Plavit/Simple-Dash-Plotly-Map-Czech-Regions/main/maps/czech-regions-low-res.json'

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

# data ze všech CSV souborů
all_data = []
for soubor in os.listdir(output_directory):
    if soubor.endswith('.csv'):
        df_kraj = nacti_data(soubor)
        if df_kraj is not None and df_kraj['Kraj'].iloc[0] != 'Česká republika':
            all_data.append(df_kraj)

# sloučení všech dat do jednoho DataFrame
df_all = pd.concat(all_data)

# všechny dostupné roky (sloupce, které nejsou index 'Měsíc' a 'Kraj')
vsechny_roky = [col for col in df_all.columns if col not in ['Kraj']]

# příprava: prázdné DataFrames pro extrémy
df_max_umrtnost = pd.DataFrame(columns=['Kraj', 'Měsíc'])
df_min_umrtnost = pd.DataFrame(columns=['Kraj', 'Měsíc'])

# každý kraj a extrémní měsíce za všechny roky
for kraj in df_all['Kraj'].unique():
    df_kraj = df_all[df_all['Kraj'] == kraj]
    if vsechny_roky:
        mesicni_umrtnost = df_kraj[vsechny_roky].sum(axis=1)
        if not mesicni_umrtnost.empty:
            max_mesic = mesicni_umrtnost.idxmax()
            min_mesic = mesicni_umrtnost.idxmin()
            df_max_umrtnost = pd.concat([df_max_umrtnost, pd.DataFrame({'Kraj': [kraj], 'Měsíc': [max_mesic]})], ignore_index=True)
            df_min_umrtnost = pd.concat([df_min_umrtnost, pd.DataFrame({'Kraj': [kraj], 'Měsíc': [min_mesic]})], ignore_index=True)

# GeoJSON z URL pomocí geopandas
try:
    response = requests.get(geojson_url)
    response.raise_for_status()
    mapa_cr = geopandas.read_file(response.text)
    mapa_cr = mapa_cr.rename(columns={'name': 'Kraj'}) 
except requests.exceptions.RequestException as e:
    print(f"Error fetching GeoJSON from URL: {e}")
    exit()
except fiona.errors.DriverError as e:
    print(f"Error reading GeoJSON: {e}")
    exit()
except Exception as e:
    print(f"An unexpected error occurred while reading GeoJSON: {e}")
    exit()

# data o maximální úmrtnosti s geografickými daty
mapa_max = mapa_cr.merge(df_max_umrtnost, on='Kraj', how='left')

# graf pro maximální úmrtnost
fig_max, ax_max = plt.subplots(1, 1, figsize=(10, 10))
mapa_max.plot(linewidth=0.8, ax=ax_max, edgecolor='0.8', color='lightgray')
ax_max.set_title('Měsíce s nejvyšší úmrtností dle krajů (2011-2024)', fontsize=26)
ax_max.set_axis_off()

# textové anotace s názvy měsíců a názvem kraje na centroidy krajů (pro maximální úmrtnost)
for idx, row in mapa_max.iterrows():
    centroid = row.geometry.centroid
    kraj_nazev = row['Kraj']
    mesic = row['Měsíc']
    if pd.notna(mesic):
        ax_max.annotate(f'{mesic} ({kraj_nazev})', xy=(centroid.x, centroid.y), xytext=(-25, 10), textcoords="offset points", fontsize=13, ha='left', color='red')

# data o minimální úmrtnosti s geografickými daty
mapa_min = mapa_cr.merge(df_min_umrtnost, on='Kraj', how='left')

# graf pro minimální úmrtnost
fig_min, ax_min = plt.subplots(1, 1, figsize=(10, 10))
mapa_min.plot(linewidth=0.8, ax=ax_min, edgecolor='0.8', color='lightgray')
ax_min.set_title('Měsíce s nejnižší úmrtností dle krajů (2011-2024)', fontsize=26)
ax_min.set_axis_off()

# textové anotace s názvy měsíců a názvem kraje na centroidy krajů (pro minimální úmrtnost)
for idx, row in mapa_min.iterrows():
    centroid = row.geometry.centroid
    kraj_nazev = row['Kraj']
    mesic = row['Měsíc']
    if pd.notna(mesic):
        ax_min.annotate(f'{mesic} ({kraj_nazev})', xy=(centroid.x, centroid.y), xytext=(-15, -15), textcoords="offset points", fontsize=13, ha='left', color='green')

plt.tight_layout()
plt.show()