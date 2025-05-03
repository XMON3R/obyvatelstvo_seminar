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

# Funkce pro načtení dat z CSV souboru a extrakci roční úmrtnosti
def nacti_a_extrahuj_data(soubor):
    try:
        df = pd.read_csv(os.path.join(output_directory, soubor))
        # Předpokládáme, že data jsou měsíční, takže roční úmrtnost je součet za 12 měsíců
        rocni_data = df[['Měsíc'] + zajimave_roky].iloc[:12].sum(numeric_only=True)
        kraj_nazev = os.path.splitext(soubor)[0]
        kraj_nazev = kraj_nazev.replace('umrtnost_', '')
        kraj_nazev = kraj_nazev.replace(' (DEMD007M-ABS)', '')
        kraj_nazev = kraj_nazev.replace('_', ' ')  # Replace underscores with spaces
        kraj_nazev = kraj_nazev.strip()        # Remove leading/trailing whitespace
        # Add more specific replacements if needed based on the GeoJSON names
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
        kraj_nazev = kraj_nazev.replace('cr', 'Česká republika') # Handle the national total if present
        return pd.Series(rocni_data, name=kraj_nazev)
    except Exception as e:
        print(f"Chyba při načítání souboru '{soubor}': {e}")
        return None

# Načteme data ze všech CSV souborů
data_kraje = {}
cleaned_kraj_names = []
for soubor in os.listdir(output_directory):
    if soubor.endswith('.csv'):
        rocni_umrtnost = nacti_a_extrahuj_data(soubor)
        if rocni_umrtnost is not None:
            data_kraje[rocni_umrtnost.name] = rocni_umrtnost[zajimave_roky]
            cleaned_kraj_names.append(rocni_umrtnost.name)

# Vytvoříme DataFrame s roční úmrtností pro jednotlivé kraje
df_umrtnost = pd.DataFrame.from_dict(data_kraje, orient='index')
df_umrtnost.index.name = 'Kraj'
print("\nCleaned Kraj Names from CSVs:")
print(cleaned_kraj_names)

# Načteme GeoJSON z URL pomocí geopandas
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

# Propojíme data o úmrtnosti s geografickými daty
mapa_umrtnost = mapa_cr.merge(df_umrtnost, left_on='name', right_index=True, how='left')

# Nastavíme počet sloupců pro grafy (pro každý rok jeden)
num_columns = len(zajimave_roky)
fig, axes = plt.subplots(1, num_columns, figsize=(15, 7))

# Vykreslíme mapu pro každý rok
for i, rok in enumerate(zajimave_roky):
    ax = axes[i]
    mapa_umrtnost.plot(column=rok, cmap='RdBu_r', linewidth=0.8, ax=ax, edgecolor='0.8', legend=True, missing_kwds={'color': 'lightgrey', 'label': 'Chybějící data'})
    ax.set_title(f'Úmrtnost v ČR - {rok}')
    ax.set_axis_off()

plt.tight_layout()
plt.show()