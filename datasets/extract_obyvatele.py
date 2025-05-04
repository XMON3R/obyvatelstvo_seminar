import pandas as pd

# --- Nastavení ---
soubor_excel = 'datasets\stav_obyvatel\stav_cr_23 (DEMZU02-a).xlsx'
nazev_listu = 'DATA'            # Nahraď názvem listu
soubor_csv = 'edited\stav_2023.csv' # Název výstupního CSV souboru
hlavicka_radek = 2               # Index řádku (od 0), který obsahuje hlavičku (roky)

vlastni_hlavicka = [
    'Kraj',
    'Počet obyvatel - koncový stav',
    'Počet obyvatel - střední stav',
    'Sňatky',
    'Rozvody',
    'Živě narození',
    'z toho mimo manželství',
    'Zemřelí',
    'z toho do 1 roku',
    'Přirozený přírůstek/úbytek',
    'Přistěhovalí',
    'z toho z ciziny',
    'Vystěhovalí',
    'z toho do ciziny',
    'Přírůstek/úbytek stěhováním',
    'z toho s cizinou',
    'Celkový přírůstek/úbytek'
]

try:
    # Načteme data z Excel souboru s určenou hlavičkou, přeskočíme úvodní řádky
    df = pd.read_excel(soubor_excel, sheet_name=nazev_listu, header=hlavicka_radek, skiprows=range(hlavicka_radek))

    # Přejmenujeme druhý sloupec na 'Měsíc'
    #df = df.rename(columns={df.columns[1]: 'Měsíc'})

    # Přesuneme sloupec 'Měsíc' na první pozici
    #mesic_sloupec = df.pop('Měsíc')
    #df.insert(0, 'Měsíc', mesic_sloupec)

    # Odstraníme sloupec 'Unnamed: 0' (pokud existuje)
    if 'Unnamed: 0' in df.columns:
        df = df.drop(columns=['Unnamed: 0'])

    df.columns = vlastni_hlavicka

    # Odstraníme první dva řádky, které obsahují starou hlavičku
    df = df.iloc[2:]

    # Vezmeme prvních 14 řádků (data krajů)
    df = df.iloc[:14]

    #df = df.rename(columns={'2024 [1]': '2024'})

    #df.drop(columns=['2025 [1]'], inplace=True, errors='ignore')  # Odstraníme sloupec '2024 [2]' pokud existuje

    # Uložíme DataFrame do CSV souboru
    df.to_csv(soubor_csv, index=False, encoding='utf-8')

    #print(f"Data pro leden až prosinec z Excel souboru '{soubor_excel}', list '{nazev_listu}' byla úspěšně načtena, sloupec '2024 [1]' přejmenován na '2024' a uložena do '{soubor_csv}'.")

except FileNotFoundError:
    print(f"Soubor '{soubor_excel}' nebyl nalezen.")
except KeyError:
    print(f"List s názvem '{nazev_listu}' nebyl nalezen.")
except Exception as e:
    print(f"Došlo k chybě při načítání Excel souboru: {e}")