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
zajimave_roky = ['2011', '2019', '2020', '2021', '2022', '2023', '2024']
rok_prvni_okno = ['2011']
roky_druhe_okno = [rok for rok in zajimave_roky if rok not in ['2011', '2023', '2024']]
rok_treti_okno = ['2023']
rok_ctvrte_okno = ['2024']

# načtení dat z CSV souboru a extrakci roční úmrtnosti
def nacti_a_extrahuj_data(soubor):
    try:
        df = pd.read_csv(os.path.join(output_directory, soubor))
        rocni_data = df[['Měsíc'] + zajimave_roky].iloc[:12].sum(numeric_only=True)
        kraj_nazev = os.path.splitext(soubor)[0]
        kraj_nazev = kraj_nazev.replace('umrtnost_', '')
        kraj_nazev = kraj_nazev.replace(' (DEMD007M-ABS)', '')
        kraj_nazev = kraj_nazev.replace('_', ' ') 
        kraj_nazev = kraj_nazev.strip()     
        kraj_nazev = kraj_nazev.replace('jihocesky', 'Jihočeský kraj')
        kraj_nazev = kraj_nazev.replace('jihomoravsky', 'Jihomoravský kraj')
        kraj_nazev = kraj_nazev.replace('karlovarsky', 'Karlovarský kraj')
        kraj_nazev = kraj_nazev.replace('kralovohradecky', 'Královéhradecký kraj')
        kraj_nazev = kraj_nazev.replace('liberecky', 'Liberecký kraj')
        kraj_nazev = kraj_nazev.replace('moravskoslezsky', 'Moravskoslezský kraj')
        kraj_nazev = kraj_nazev.replace('olomoucky', 'Olomoucký kraj')
        kraj_nazev = kraj_nazev.replace('pardubicky', 'Pardubický kraj')
        kraj_nazev = kraj_nazev.replace('plzensky', 'Plzeňský kraj')
        kraj_nazev = kraj_nazev.replace('praha', 'Hlavní město Praha')
        kraj_nazev = kraj_nazev.replace('stredocesky', 'Středočeský kraj')
        kraj_nazev = kraj_nazev.replace('ustecky', 'Ústecký kraj')
        kraj_nazev = kraj_nazev.replace('vysocina', 'Kraj Vysočina')
        kraj_nazev = kraj_nazev.replace('zlinsky', 'Zlínský kraj')
        kraj_nazev = kraj_nazev.replace('cr', 'Česká republika') 
        return pd.Series(rocni_data, name=kraj_nazev)
    except Exception as e:
        print(f"Chyba při načítání souboru '{soubor}': {e}")
        return None

# data ze všech CSV souborů
data_kraje = {}
cleaned_kraj_names = []
for soubor in os.listdir(output_directory):
    if soubor.endswith('.csv'):
        rocni_umrtnost = nacti_a_extrahuj_data(soubor)
        if rocni_umrtnost is not None:
            data_kraje[rocni_umrtnost.name] = rocni_umrtnost[zajimave_roky]
            cleaned_kraj_names.append(rocni_umrtnost.name)

#  DataFrame s roční úmrtností pro jednotlivé kraje
df_umrtnost = pd.DataFrame.from_dict(data_kraje, orient='index')
df_umrtnost.index.name = 'Kraj'
print("\nCleaned Kraj Names from CSVs:")
print(cleaned_kraj_names)

# GeoJSON z URL pomocí geopandas
try:
    response = requests.get(geojson_url)
    response.raise_for_status()
    mapa_cr = geopandas.read_file(response.text)
    print("\nUnique Kraj Names from GeoJSON:")
    print(mapa_cr['name'].unique())
except requests.exceptions.RequestException as e:
    print(f"Error fetching GeoJSON from URL: {e}")
    exit()
except fiona.errors.DriverError as e:
    print(f"Error reading GeoJSON: {e}")
    exit()
except Exception as e:
    print(f"An unexpected error occurred while reading GeoJSON: {e}")
    exit()

# propojení dat o úmrtnosti s geografickými daty
mapa_umrtnost = mapa_cr.merge(df_umrtnost, left_on='name', right_index=True, how='left')

# Společná normalizace pro všechny grafy
vmin = mapa_umrtnost[zajimave_roky].min().min()
vmax = mapa_umrtnost[zajimave_roky].max().max()
norm = plt.Normalize(vmin=vmin, vmax=vmax)
cmap = 'RdBu_r'
sm = plt.cm.ScalarMappable(cmap=cmap, norm=norm)
sm._A = []

# První okno (rok 2011 + legenda)
fig1, axes1 = plt.subplots(1, 1, figsize=(8, 7)) # Jeden graf pro rok 2011
mapa_umrtnost.plot(column=rok_prvni_okno[0], cmap=cmap, norm=norm, linewidth=0.8, ax=axes1, edgecolor='0.8', legend=True, missing_kwds={'color': 'lightgrey', 'label': 'Chybějící data'})
axes1.set_title(f'Úmrtnost v ČR - {rok_prvni_okno[0]}')
axes1.set_axis_off()
plt.tight_layout()
plt.show()

# Druhé okno (roky 2019, 2020, 2021, 2022)
num_columns2 = len(roky_druhe_okno)
fig2, axes2 = plt.subplots(1, num_columns2, figsize=(15, 7))

for i, rok in enumerate(roky_druhe_okno):
    ax2 = axes2[i]
    mapa_umrtnost.plot(column=rok, cmap=cmap, norm=norm, linewidth=0.8, ax=ax2, edgecolor='0.8', missing_kwds={'color': 'lightgrey', 'label': 'Chybějící data'})
    ax2.set_title(f'Úmrtnost v ČR - {rok}')
    ax2.set_axis_off()

plt.tight_layout()
plt.show()

# Třetí okno (rok 2023)
fig3, axes3 = plt.subplots(1, 1, figsize=(8, 7))
mapa_umrtnost.plot(column=rok_treti_okno[0], cmap=cmap, norm=norm, linewidth=0.8, ax=axes3, edgecolor='0.8', missing_kwds={'color': 'lightgrey', 'label': 'Chybějící data'})
axes3.set_title(f'Úmrtnost v ČR - {rok_treti_okno[0]}')
axes3.set_axis_off()
plt.tight_layout()
plt.show()

# Čtvrté okno (rok 2024)
fig4, axes4 = plt.subplots(1, 1, figsize=(8, 7))
mapa_umrtnost.plot(column=rok_ctvrte_okno[0], cmap=cmap, norm=norm, linewidth=0.8, ax=axes4, edgecolor='0.8', missing_kwds={'color': 'lightgrey', 'label': 'Chybějící data'})
axes4.set_title(f'Úmrtnost v ČR - {rok_ctvrte_okno[0]}')
axes4.set_axis_off()
plt.tight_layout()
plt.show()