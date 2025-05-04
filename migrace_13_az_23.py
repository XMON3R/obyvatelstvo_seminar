import pandas as pd
import matplotlib.pyplot as plt
import os

# Cesta k adresáři s daty
data_directory = './edited/stav_obyvatel'

# Cesta k adresáři s daty
data_directory = './edited/stav_obyvatel'
print(f"Obsah adresáře '{data_directory}' před načítáním:")
for filename in os.listdir(data_directory):
    print(filename)

# Roky, pro které chceme zobrazit data
zajimave_roky = ['2014','2015','2016','2017','2018','2019','2020', '2021', '2022', '2023']

# Funkce pro načtení dat z CSV souboru a extrakci migrace
def nacti_a_extrahuj_migraci(soubor, rok):
    try:
        df = pd.read_csv(os.path.join(data_directory, soubor))
        # Předpokládáme, že první sloupec je 'Kraj'
        df.set_index('Kraj', inplace=True)
        migrace_data = df[['Přistěhovalí', 'Vystěhovalí']]
        migrace_data['Rok'] = rok
        migrace_data.reset_index(inplace=True)
        return migrace_data
    except Exception as e:
        print(f"Chyba při načítání souboru '{soubor}': {e}")
        return None

# Načteme data o migraci pro zvolené roky
vsechna_migrace_data = []
for soubor in os.listdir(data_directory):
    if soubor.endswith('.csv') and 'stav_cr_' in soubor:
        casti_nazvu = soubor.split('_')
        if len(casti_nazvu) > 1:
            rok_cast = casti_nazvu[-1].split('.')[0]
            if len(rok_cast) == 2 and rok_cast.isdigit():
                rok_ctyr_ciferny = '20' + rok_cast
                if rok_ctyr_ciferny in zajimave_roky:
                    migrace_rok = nacti_a_extrahuj_migraci(soubor, rok_ctyr_ciferny)
                    if migrace_rok is not None:
                        vsechna_migrace_data.append(migrace_rok)
# Sloučíme data do jednoho DataFrame
if vsechna_migrace_data:
    df_migrace = pd.concat(vsechna_migrace_data)

    # Přetransformujeme data pro graf
    df_migrace_pivot = df_migrace.pivot_table(index='Rok', columns='Kraj', values=['Přistěhovalí', 'Vystěhovalí'])

    # Vytvoříme graf
    plt.figure(figsize=(15, 10))

    # Proiterujeme přes všechny kraje a vykreslíme čáry
    for kraj in df_migrace_pivot.columns.levels[1]:
        plt.plot(df_migrace_pivot.index, df_migrace_pivot[('Přistěhovalí', kraj)], label=f'{kraj} - Přistěhovalí', linestyle='-')
        plt.plot(df_migrace_pivot.index, df_migrace_pivot[('Vystěhovalí', kraj)], label=f'{kraj} - Vystěhovalí', linestyle='--')

    plt.xlabel('Rok')
    plt.ylabel('Počet migrujících')
    plt.title('Migrace v ČR v letech 2013–2023')
    plt.xticks(zajimave_roky)
    plt.legend(title='Kraj - Směr', bbox_to_anchor=(1.05, 1), loc='upper left')
    plt.grid(True)
    plt.tight_layout()
    plt.show()
else:
    print("Žádná data pro zvolené roky nebyla nalezena.")