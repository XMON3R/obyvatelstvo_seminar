import pandas as pd
import os

input_directory = './datasets/umrtnost_kraje'  # Cesta k adresáři s Excel soubory
output_directory = './edited/umrtnost'        # Cesta k výstupnímu adresáři

# Vytvoříme výstupní adresář, pokud neexistuje
if not os.path.exists(output_directory):
    os.makedirs(output_directory)

# --- Nastavení pro čtení dat z každého listu ---
nazev_listu = 'DATA'         # Předpokládaný název listu s daty
hlavicka_radek = 3            # Index řádku (od 0), který obsahuje hlavičku (roky)

# Projdeme všechny soubory v daném vstupním adresáři
for filename in os.listdir(input_directory):
    if filename.endswith('.xlsx'):  # Zpracujeme pouze soubory s příponou .xlsx
        filepath = os.path.join(input_directory, filename)
        base_filename, _ = os.path.splitext(filename)  # Získáme název souboru bez přípony
        output_csv_filepath = os.path.join(output_directory, f'{base_filename}.csv')

        try:
            # Načteme data z Excel souboru s určenou hlavičkou, přeskočíme úvodní řádky
            df = pd.read_excel(filepath, sheet_name=nazev_listu, header=hlavicka_radek, skiprows=range(hlavicka_radek))

            # Přejmenujeme druhý sloupec na 'Měsíc' (pokud existuje)
            if df.shape[1] > 1:
                df = df.rename(columns={df.columns[1]: 'Měsíc'})

                # Přesuneme sloupec 'Měsíc' na první pozici (pokud existuje)
                if 'Měsíc' in df.columns and df.columns[0] != 'Měsíc':
                    mesic_sloupec = df.pop('Měsíc')
                    df.insert(0, 'Měsíc', mesic_sloupec)

            # Odstraníme sloupec 'Unnamed: 0' (pokud existuje)
            if 'Unnamed: 0' in df.columns:
                df = df.drop(columns=['Unnamed: 0'])

            # Ořízneme DataFrame na prvních 12 řádků (leden až prosinec)
            df = df.iloc[:12]

            # Přejmenujeme sloupec '2024 [1]' na '2024' (pokud existuje)
            if '2024\xa0[1]' in df.columns:
                df = df.rename(columns={'2024\xa0[1]': '2024'})
            elif '2024 [1]' in df.columns:
                df = df.rename(columns={'2024 [1]': '2024'})

            # Odstraníme sloupec '2025 [1]' pokud existuje
            df.drop(columns=['2025\xa0[1]'], inplace=True, errors='ignore')
            df.drop(columns=['2025 [1]'], inplace=True, errors='ignore')
            df.drop(columns=['2025'], inplace=True, errors='ignore')

            # Uložíme DataFrame do CSV souboru ve výstupním adresáři
            df.to_csv(output_csv_filepath, index=False, encoding='utf-8')

            print(f"Data pro leden až prosinec z Excel souboru '{filename}', list '{nazev_listu}' byla úspěšně načtena, upravena a uložena do '{output_csv_filepath}'.")

        except FileNotFoundError:
            print(f"Soubor '{filename}' nebyl nalezen.")
        except KeyError:
            print(f"List s názvem '{nazev_listu}' nebyl nalezen v souboru '{filename}'.")
        except Exception as e:
            print(f"Došlo k chybě při načítání Excel souboru '{filename}': {e}")