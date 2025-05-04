import pandas as pd
import os

# --- Nastavení ---
vstupni_adresar = 'datasets/stav_obyvatel'
vystupni_adresar = 'edited/stav_obyvatel'
nazev_listu = 'DATA'
hlavicka_radek = 2  # Index řádku (od 0) s popisky sloupců
pocet_datovych_radku = 14  # Počet řádků s daty krajů

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

# Vytvoříme výstupní adresář, pokud neexistuje
os.makedirs(vystupni_adresar, exist_ok=True)

# Projdeme všechny soubory v zadaném adresáři
for soubor in os.listdir(vstupni_adresar):
    if soubor.endswith('.xlsx'):
        cesta_excel = os.path.join(vstupni_adresar, soubor)
        nazev_souboru_bez_pripony = os.path.splitext(soubor)[0]
        cesta_csv_vystup = os.path.join(vystupni_adresar, f'{nazev_souboru_bez_pripony}.csv')

        try:
            # Načteme data z Excel souboru BEZ HLAVIČKY, přeskočíme úvodní řádky
            df = pd.read_excel(cesta_excel, sheet_name=nazev_listu, header=hlavicka_radek, skiprows=range(hlavicka_radek))

            # Odstraníme sloupec 'Unnamed: 0' (pokud existuje)
            if 'Unnamed: 0' in df.columns:
                df = df.drop(columns=['Unnamed: 0'])

            # Nastavíme vlastní hlavičku
            df.columns = vlastni_hlavicka

            # Odstraníme první dva řádky, které obsahují starou hlavičku
            df = df.iloc[2:]

            # Vezmeme stanovený počet datových řádků
            df = df.iloc[:pocet_datovych_radku]

            # Uložíme DataFrame do CSV souboru
            df.to_csv(cesta_csv_vystup, index=False, encoding='utf-8')

            print(f"Soubor '{soubor}' byl úspěšně zpracován a uložen jako '{os.path.basename(cesta_csv_vystup)}'.")

        except FileNotFoundError:
            print(f"Chyba: Soubor '{soubor}' nebyl nalezen.")
        except KeyError:
            print(f"Chyba: List s názvem '{nazev_listu}' nebyl nalezen v souboru '{soubor}'.")
        except Exception as e:
            print(f"Došlo k chybě při zpracování souboru '{soubor}': {e}")

print("Zpracování všech souborů dokončeno.")