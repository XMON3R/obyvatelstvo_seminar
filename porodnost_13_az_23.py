import pandas as pd
import matplotlib.pyplot as plt
import os
import matplotlib.cm as cm
import seaborn as sns

# Cesta k adresáři s daty
data_directory = './edited/stav_obyvatel'

# Roky, pro které chceme zobrazit data
zajimave_roky = ['2013','2014','2015','2016','2017','2018','2019','2020', '2021', '2022', '2023']

# Funkce pro načtení dat z CSV souboru a extrakci porodnosti
def nacti_a_extrahuj_porodnost(soubor, rok):
    try:
        df = pd.read_csv(os.path.join(data_directory, soubor))
        # Předpokládáme, že první sloupec je 'Kraj'
        df.set_index('Kraj', inplace=True)
        porodnost_data = df[['Živě narození']]
        porodnost_data['Rok'] = rok
        porodnost_data.reset_index(inplace=True)
        return porodnost_data
    except Exception as e:
        print(f"Chyba při načítání souboru '{soubor}': {e}")
        return None

# data o porodnosti pro zvolené roky
vsechna_porodnost_data = []
for soubor in os.listdir(data_directory):
    if soubor.endswith('.csv') and 'stav_cr_' in soubor:
        casti_nazvu = soubor.split('_')
        if len(casti_nazvu) > 1:
            rok_cast = casti_nazvu[-1].split('.')[0]
            if len(rok_cast) == 2 and rok_cast.isdigit():
                rok_ctyr_ciferny = '20' + rok_cast
                if rok_ctyr_ciferny in zajimave_roky:
                    porodnost_rok = nacti_a_extrahuj_porodnost(soubor, rok_ctyr_ciferny)
                    if porodnost_rok is not None:
                        vsechna_porodnost_data.append(porodnost_rok)

# data do jednoho DataFrame
if vsechna_porodnost_data:
    df_porodnost = pd.concat(vsechna_porodnost_data)

    # Přetransformujeme data pro graf
    df_porodnost_pivot = df_porodnost.pivot_table(index='Rok', columns='Kraj', values='Živě narození')

    # Vytvoříme graf
    plt.figure(figsize=(14, 8))
    ax = plt.gca()

    # Definujeme větší paletu "Paired"
    num_kraje = len(df_porodnost_pivot.columns)
    palette = sns.color_palette("Paired", n_colors=num_kraje)
    ax.set_prop_cycle(color=palette)

    # Proiterujeme přes všechny kraje a vykreslíme čáry
    for kraj in df_porodnost_pivot.columns:
        ax.plot(df_porodnost_pivot.index, df_porodnost_pivot[kraj], marker='o', label=kraj)

    plt.xlabel('Rok')
    plt.ylabel('Počet živě narozených')
    plt.title('Vývoj porodnosti v ČR v letech 2013–2023')
    plt.xticks(zajimave_roky)
    plt.legend(title='Kraj', bbox_to_anchor=(1.05, 1), loc='upper left')
    plt.grid(True)
    plt.tight_layout()
    plt.show()
else:
    print("Žádná data pro zvolené roky nebyla nalezena.")