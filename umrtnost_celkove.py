import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# --- Nastavení ---
soubor_csv = './datasets/umrtnost_mesice.csv'
zacatek_obdobi = '2011'
konec_obdobi = '2024'

try:
    # data z CSV souboru
    df = pd.read_csv(soubor_csv)

    # Zkontrolujeme, zda sloupec 'Měsíc' existuje
    if 'Měsíc' not in df.columns:
        print("Chyba: Sloupec 'Měsíc' nebyl nalezen v CSV souboru.")
    else:
        # sloupec 'Měsíc' jako index pro lepší práci s daty
        df.set_index('Měsíc', inplace=True)

        # index (měsíce) pro správné pořadí na grafu
        mesice_poradi = ['leden', 'únor', 'březen', 'duben', 'květen', 'červen', 'červenec', 'srpen', 'září', 'říjen', 'listopad', 'prosinec']
        df = df.reindex(mesice_poradi)

        # přepočet na průměrnou měsíční úmrtnost za celé období
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
        palette = sns.color_palette("Paired", n_colors=12)
        ax = plt.gca()
        ax.set_prop_cycle(color=palette)

        mesice = df.index.tolist() # Převedeme index na list pro jistotu
        ciselne_sloupce = [col for col in df.columns if col != 'Průměr']
        for i, mesic in enumerate(mesice):
            ax.plot(ciselne_sloupce, df.loc[mesic, ciselne_sloupce], marker='o', label=mesic)

        plt.title('Vývoj měsíční úmrtnosti v ČR (dle dostupných let)')
        plt.xlabel('Rok')
        plt.ylabel('Počet zemřelých')
        plt.legend(title='Měsíc', bbox_to_anchor=(1.05, 1), loc='upper left')
        plt.grid(True)
        plt.tight_layout()
        plt.show()
        
        # 3. Sloupcový graf roční kumulativní úmrtnosti
        sloupce_obdobi = [col for col in df.columns if zacatek_obdobi <= col[:4] <= konec_obdobi and col != 'Průměr']
        df_kumulativni = df[sloupce_obdobi].sum()

        plt.figure(figsize=(8, 6))
        sns.barplot(x=df_kumulativni.index, y=df_kumulativni.values, palette='magma')
        plt.title(f'Celková roční úmrtnost ({zacatek_obdobi} - {int(konec_obdobi)})')
        plt.xlabel('Rok')
        plt.ylabel('Celkový počet zemřelých')
        plt.tight_layout()
        plt.show()


        # 4. Čárový graf procentuálních změn celkové roční úmrtnosti
        rocni_umrtnost = df[ciselne_sloupce].sum()
        rocni_pct_change = rocni_umrtnost.pct_change() * 100

        fig4, ax4 = plt.subplots(figsize=(10, 6))
        ax4.plot(rocni_pct_change.index, rocni_pct_change.values, marker='o', color='skyblue')
        ax4.set_title('Procentuální změny (meziroční) celkové roční úmrtnosti')
        ax4.set_xlabel('Rok')
        ax4.set_ylabel('Procentuální změna (%)')
        ax4.grid(True, alpha=0.5)
        ax4.axhline(0, color='black', linewidth=0.8, linestyle='--')

        for rok, pct_zmena, pocet_umrti in zip(rocni_pct_change.index, rocni_pct_change.values, rocni_umrtnost.values):
            ax4.annotate(f'{int(pocet_umrti)}', (rok, pct_zmena), textcoords="offset points", xytext=(0, 5), ha='center', fontsize='small')

        plt.tight_layout()
        plt.show()


except FileNotFoundError:
    print(f"Chyba: Soubor '{soubor_csv}' nebyl nalezen. Zkontrolujte cestu.")
except Exception as e:
    print(f"Došlo k chybě při zpracování dat: {e}")