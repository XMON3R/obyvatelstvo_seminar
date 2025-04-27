import pandas as pd

# --- Nastavení ---
soubor_excel = 'DEMD007M-ABS.xlsx'  # Nahraď názvem tvého Excel souboru
nazev_listu = 'DATA'            # Nahraď názvem listu
soubor_csv = 'umrtnost_mesice_cr.csv' # Název výstupního CSV souboru
hlavicka_radek = 3               # Index řádku (od 0), který obsahuje hlavičku (roky)

try:
    # Načteme data z Excel souboru s určenou hlavičkou, přeskočíme úvodní řádky
    df = pd.read_excel(soubor_excel, sheet_name=nazev_listu, header=hlavicka_radek, skiprows=range(hlavicka_radek))

    # Přejmenujeme druhý sloupec na 'Měsíc'
    df = df.rename(columns={df.columns[1]: 'Měsíc'})

    # Přesuneme sloupec 'Měsíc' na první pozici
    mesic_sloupec = df.pop('Měsíc')
    df.insert(0, 'Měsíc', mesic_sloupec)

    # Odstraníme sloupec 'Unnamed: 0' (pokud existuje)
    if 'Unnamed: 0' in df.columns:
        df = df.drop(columns=['Unnamed: 0'])

    # Ořízneme DataFrame na prvních 12 řádků (leden až prosinec)
    df = df.iloc[:12]

    df = df.rename(columns={'2024 [1]': '2024'})

    df.drop(columns=['2025 [1]'], inplace=True, errors='ignore')  # Odstraníme sloupec '2024 [2]' pokud existuje

    # Uložíme DataFrame do CSV souboru
    df.to_csv(soubor_csv, index=False, encoding='utf-8')

    print(f"Data pro leden až prosinec z Excel souboru '{soubor_excel}', list '{nazev_listu}' byla úspěšně načtena, sloupec '2024 [1]' přejmenován na '2024' a uložena do '{soubor_csv}'.")

except FileNotFoundError:
    print(f"Soubor '{soubor_excel}' nebyl nalezen.")
except KeyError:
    print(f"List s názvem '{nazev_listu}' nebyl nalezen.")
except Exception as e:
    print(f"Došlo k chybě při načítání Excel souboru: {e}")