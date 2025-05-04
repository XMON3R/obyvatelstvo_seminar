# obyvatelstvo_seminar
Zápočtový projekt k předmětu: Seminář dobývání znalostí - NAIL121, Šimon Jůza

Tento projekt analyzuje vybraná demografická data České republiky s cílem odpovědět na několik klíčových otázek týkajících se úmrtnosti, porodnosti a migrace. Data byla získána z veřejně dostupných zdrojů Českého statistického úřadu (ČSÚ).

## Přehled grafů

Tento projekt generuje 8 grafů, které vizualizují odpovědi na zadané otázky:

Tento projekt generuje grafy, které vizualizují odpovědi na zadané otázky:

1.  **Průměrná měsíční úmrtnost v ČR:** Čárový graf zobrazující průměrný počet zemřelých v jednotlivých měsících (dle dostupných let). *(Vygenerováno skriptem `UMRTNOST_MESICNI_ROCNI.PY`, uložen jako `grafy/line_mesice.png`)*
2.  **Celková roční úmrtnost v ČR:** Sloupcový graf zobrazující celkový počet zemřelých v jednotlivých letech. *(Vygenerováno skriptem `UMRTNOST_MESICNI_ROCNI.PY`, uložen jako `grafy/umrtnost_celkove_roky.png`)*
3.  **Procentuální úmrtnost vůči celkovému počtu obyvatel:** Sloupcový graf zobrazující podíl úmrtí na celkovém počtu obyvatel v jednotlivých letech. *(Vygenerováno skriptem `UMRTNOST_PROCENTA.PY`, uložen jako `grafy/procenta_celkove_umrtnost.png`)*
4.  **Úmrtnost krajů (nejnižší):** Mapová vizualizace zobrazující kraje s nejnižší úmrtností. *(Vygenerováno skriptem `UMRTNOST_KRAJE.PY`, uložen jako `grafy/umrtnost_kraje_nejnizsi.png`)*
5.  **Úmrtnost krajů (nejvyšší):** Mapová vizualizace zobrazující kraje s nejvyšší úmrtností. *(Vygenerováno skriptem `UMRTNOST_KRAJE.PY`, uložen jako `grafy/umrtnost_kraje_nejvyssi.png`)*
6.  **Vývoj migrace (2013–2023):** Čárový graf zobrazující vývoj migrace (přistěhovalí a vystěhovalí) v letech 2013–2023. *(Vygenerováno skriptem `MIGRACE.PY`, uložen jako `grafy/migrace_2013_az_2023.png`)*
7.  **Vývoj porodnosti (2013–2023):** Čárový graf zobrazující vývoj porodnosti (počet živě narozených) v letech 2013–2023. *(Vygenerováno skriptem `PORODNOST.PY`, uložen jako `grafy/porodnost_2013_az_2023.png`)*
8.  **Vývoj migrace (2018–2023):** Čárový graf zobrazující vývoj migrace (přistěhovalí a vystěhovalí) v letech 2018–2023. *(Vygenerováno skriptem `MIGRACE.PY`, uložen jako `grafy/migrace_2018_az_2023.png`)*

## Odpovědi na zadané otázky

**1. Ve kterých oblastech a v jakých měsících či ročních obdobích dochází k nejvyšší úmrtnosti?**

* **Měsíce:** Graf 1 (`line_mesice.png`) vizualizuje průměrnou měsíční úmrtnost v ČR, což umožňuje identifikovat měsíce s nejvyšším počtem úmrtí.
* **Oblasti:** Grafy 4 (`umrtnost_kraje_nejnizsi.png`) a 5 (`umrtnost_kraje_nejvyssi.png`) zobrazují mapy krajů s nejnižší a nejvyšší úmrtností. Graf 3 (`procenta_celkove_umrtnost.png`) poskytuje pohled na procentuální podíl úmrtí v rámci celkové populace.

**2. Je klesající trend porodnosti patrný ve všech krajích ČR, nebo existují regionální rozdíly?**

* Graf 7 (`porodnost_2013_az_2023.png`) zobrazuje vývoj porodnosti za delší časové období, konkrétně 2013 až 2023.

**3. Jak pandemie COVID-19 v letech 2020–2022 ovlivnila nejen porodnost a úmrtnost, ale i migraci – jak mezinárodní, tak v rámci jednotlivých krajů?**

* **Úmrtnost:** Graf 1 a 2 (pokud zahrnují roky 2020-2022) a Graf 3 ukazují vývoj úmrtnosti během pandemie.
* **Porodnost:** Graf 7 (`porodnost_2013_az_2023.png`) zobrazuje vývoj porodnosti v letech 2020-2022 v kontextu delšího období. Pro detailnější pohled na kraje by byl vhodný graf specificky pro toto období (jak jsme dříve generovali).
* **Migrace:** Grafy 6 (`migrace_2013_az_2023.png`) a 8 (`migrace_2018_az_2023.png`) zobrazují vývoj celkové migrace v letech 2020-2022 v kontextu delšího období. Pro analýzu mezinárodní vs. vnitrostátní migrace by bylo třeba specifické grafy, pokud jsi tato data zpracoval.

## Použité skripty

* `UMRTNOST_KRAJE.PY`: Skript pro generování mapových vizualizací úmrtnosti po krajích.
* `MIGRACE.PY`: Skript pro generování čárových grafů vývoje migrace.
* `PORODNOST.PY`: Skript pro generování čárového grafu vývoje porodnosti.
* `UMRTNOST_MESICNI_ROCNI.PY`: Skript pro generování grafů měsíční a roční úmrtnosti v ČR.
* `UMRTNOST_PROCENTA.PY`: Skript pro generování sloupcového grafu procentuální úmrtnosti.

## Zdroje dat

* [Veřejná databáze ČSÚ](https://vdb.czso.cz/vdbvo2/faces/index.jsf?page=statistiky#katalog=30845)
* [Podmínky pro využívání dat ČSÚ](https://csu.gov.cz/podminky_pro_vyuzivani_a_dalsi_zverejnovani_statistickych_udaju_csu)

## Poznámky

* Grafy jsou uloženy ve složce `vystup/grafy/`.
* Skripty pro generování grafů jsou umístěny v hlavním adresáři repozitáře.
* Pro spuštění skriptů je vyžadována instalace knihoven `pandas` a `matplotlib`. Pro některé skripty může být vyžadována i knihovna `seaborn` a `geopandas`.g