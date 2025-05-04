# obyvatelstvo_seminar
Zápočtový projekt k předmětu: Seminář dobývání znalostí - NAIL121, Šimon Jůza

Tento projekt analyzuje vybraná demografická data České republiky s cílem odpovědět na několik klíčových otázek týkajících se úmrtnosti, porodnosti a migrace. Data byla získána z veřejně dostupných zdrojů Českého statistického úřadu (ČSÚ).

## Přehled grafů

Tento projekt generuje grafy napomáhající k zopodpovězění otázek níže.

## Čárové a sloupcové grafy včetně mapových vizualizací prosím naleznete ve složce /vystup_grafy.

### Pro prohlédnutí odpovědí na otázky prosím otevřete soubor v root adresáři 'zaver.pdf'

## Otázky

**1. Ve kterých oblastech a v jakých měsících či ročních obdobích dochází k nejvyšší úmrtnosti?**

**2. Je klesající trend porodnosti patrný ve všech krajích ČR, nebo existují regionální rozdíly?**

**3. Jak pandemie COVID-19 v letech 2020–2022 ovlivnila nejen porodnost a úmrtnost, ale i migraci – jak mezinárodní, tak v rámci jednotlivých krajů?**

## Použité skripty

* `UMRTNOST_KRAJE.PY`: Skript pro generování mapových vizualizací úmrtnosti po krajích.
* `MIGRACE_13_AZ_23.PY`: Skript pro generování čárových grafů vývoje migrace.
* `PORODNOST_13_AZ_23.PY`: Skript pro generování čárového grafu vývoje porodnosti.
* `UMRTNOST_CELKOVE_11_AZ_24.PY`: Skript pro generování grafů měsíční a roční úmrtnosti v ČR.
* `UMRTNOST_HEATMAP.PY`: Skript pro generování mapové vizualizace úmrtnosti v jednotlivých krajích ČR.

## Zdroje dat

* [Veřejná databáze ČSÚ](https://vdb.czso.cz/vdbvo2/faces/index.jsf?page=statistiky#katalog=30845) 
* [Podmínky pro využívání dat ČSÚ](https://csu.gov.cz/podminky_pro_vyuzivani_a_dalsi_zverejnovani_statistickych_udaju_csu)

## Poznámky

* Grafy jsou uloženy ve složce `vystup/grafy/`.
* Skripty pro generování grafů jsou umístěny v hlavním adresáři repozitáře.
* Pro spuštění skriptů je vyžadována instalace knihoven `pandas` a `matplotlib`. Pro některé skripty může být vyžadována i knihovna `seaborn` a `geopandas`.g