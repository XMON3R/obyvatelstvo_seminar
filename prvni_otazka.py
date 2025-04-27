import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# --- Nastavení ---
soubor_csv = './datasets/umrtnost_mesice.csv' # Cesta k tvému CSV souboru
zacatek_obdobi = '2007'
konec_obdobi = '2024'

try:
    # Načteme data z CSV souboru
    df = pd.read_csv(soubor_csv)

    # Zkontrolujeme, zda sloupec 'Měsíc' existuje
    if 'Měsíc' not in df.columns:
        print("Chyba: Sloupec 'Měsíc' nebyl nalezen v CSV souboru.")
    else:
        # Nastavíme sloupec 'Měsíc' jako index pro lepší práci s daty
        df.set_index('Měsíc', inplace=True)

        # Seřadíme index (měsíce) pro správné pořadí na grafu
        mesice_poradi = ['leden', 'únor', 'březen', 'duben', 'květen', 'červen', 'červenec', 'srpen', 'září', 'říjen', 'listopad', 'prosinec']
        df = df.reindex(mesice_poradi)

        # Přepočítáme na průměrnou měsíční úmrtnost za celé období
        df['Průměr'] = df.mean(axis=1, numeric_only=True)

        # --- Vytvoření grafů ---

        # 1. Sloupcový graf průměrné měsíční úmrtnosti
        plt.figure(figsize=(12, 6))
        sns.barplot(x=df.index, y='Průměr', data=df, palette='viridis')
        plt.title('Průměrná měsíční úmrtnost v ČR (dle dostupných let)')
        plt.xlabel('Měsíc')
        plt.ylabel('Průměrný počet zemřelých')
        plt.xticks(rotation=45, ha='right')
        plt.tight_layout()
        plt.show()

        # 2. Čárový graf vývoje úmrtnosti v jednotlivých měsících v průběhu let
        plt.figure(figsize=(14, 8))
        for mesic in df.index:
            # Zajistíme, že vybíráme pouze číselné sloupce pro graf
            ciselne_sloupce = [col for col in df.columns if col != 'Průměr']
            plt.plot(ciselne_sloupce, df.loc[mesic, ciselne_sloupce], marker='o', label=mesic)

        plt.title('Vývoj měsíční úmrtnosti v ČR (dle dostupných let)')
        plt.xlabel('Rok')
        plt.ylabel('Počet zemřelých')
        plt.legend(title='Měsíc', bbox_to_anchor=(1.05, 1), loc='upper left')
        plt.grid(True)
        plt.tight_layout()
        plt.show()


        # 3. Sloupcový graf roční kumulativní úmrtnosti (2020-2022)
        sloupce_obdobi = [col for col in df.columns if zacatek_obdobi <= col[:4] <= konec_obdobi and col != 'Průměr']
        df_kumulativni = df[sloupce_obdobi].sum()

        plt.figure(figsize=(8, 6))
        sns.barplot(x=df_kumulativni.index, y=df_kumulativni.values, palette='magma')
        plt.title(f'Celková roční úmrtnost (březen {zacatek_obdobi} - březen {int(konec_obdobi) + 1})')
        plt.xlabel('Rok')
        plt.ylabel('Celkový počet zemřelých')
        plt.tight_layout()
        plt.show()

except FileNotFoundError:
    print(f"Chyba: Soubor '{soubor_csv}' nebyl nalezen. Zkontrolujte cestu.")
except Exception as e:
    print(f"Došlo k chybě při zpracování dat: {e}")