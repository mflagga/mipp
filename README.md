# Fermiony Majorany i ich realizacja w nanodrutach półprzewodnikowych

Prezentacja (LaTeX/beamer) na przedmiot **„Materiały i przyrządy półprzewodnikowe”**.

- 55 min treści + 5 min pytań, **42 slajdy** + 5 zapasowych, **dwóch prelegentów**.
- Poziom inżynierski: wzory, parametry materiałowe, liczby.
- Gotowy PDF: [`prezentacja.pdf`](prezentacja.pdf).
- Stan: **pierwszy szkic** — otwarte sprawy w [`TODO.md`](TODO.md).
- Jak pracujemy razem (git, konwencje w kodzie): [`WSPOLPRACA.md`](WSPOLPRACA.md).
- **Nowa koncepcja** wg [`plan.txt`](plan.txt) (druga kwantyzacja → Majorany → realizacja → kubit):
  [`slajdy.tex`](slajdy.tex) → [`slajdy.pdf`](slajdy.pdf), budowanie: `make slajdy`.
  Poprzednia wersja (`main.tex`, plan w `src/initial_plan.txt`) zostaje bez zmian.

## Struktura repozytorium

```
.
├── main.tex              # cała prezentacja (beamer, motyw metropolis, 16:9)
├── makefile              # make / make rep / make wykresy / make clean
├── prezentacja.pdf       # wynik kompilacji (commitowany)
├── fig/
│   ├── *.pdf             # własne wykresy — GENEROWANE przez sim/wykresy.py
│   └── ref/rys{1,3,4,5}.png  # rysunki z artykułu bazowego [LF12]
├── sim/
│   └── wykresy.py        # symulacje (numpy) i wszystkie własne wykresy
├── src/
│   └── initial_plan.txt  # plan prezentacji: struktura, czasy, literatura
├── requirements.txt      # zależności Pythona (tylko do wykresów)
├── README.md             # ten plik
├── WSPOLPRACA.md         # workflow i konwencje
└── TODO.md               # lista rzeczy do sprawdzenia/uzupełnienia
```

Katalog `.build/` (pliki pomocnicze LaTeX-a) powstaje przy kompilacji i nie jest w repo.

## Wymagania

**Do kompilacji slajdów** — TeX Live 2022 lub nowszy (sprawdzone na TeX Live 2026) z:

- **LuaLaTeX** i **latexmk** — prezentacja używa `fontspec`, `unicode-math` i `luavlna`,
  więc **nie skompiluje się pdfLaTeX-em**;
- pakietami: `beamer`, `beamertheme-metropolis`, `appendixnumberbeamer`, `babel-polish`,
  `luavlna`, `unicode-math`, `siunitx`, `pgf` (TikZ), `newunicodechar`, `braket`,
  `csquotes`, `listings`, `microtype`, `mathtools`;
- fontami **STIX Two** (`stix2-otf`) i **JetBrains Mono** (`jetbrainsmono-otf`) —
  oba są w dystrybucji TeX Live, nie trzeba ich instalować osobno.

Najprościej: pełna instalacja TeX Live (`scheme-full`; na Fedorze `texlive-scheme-full`,
na Ubuntu/Debianie `texlive-full`). Brakujące pakiety przy mniejszej instalacji:
`tlmgr install <nazwa>`.

**Do generowania wykresów** (opcjonalnie — gotowe PDF-y są w `fig/`):

```sh
pip install -r requirements.txt
```

Wykresy używają czcionki *STIX Two Text* (żeby pasowały do slajdów). Jeśli matplotlib
jej nie widzi w systemie, wypisze ostrzeżenie i użyje czcionki zastępczej — wykresy
i tak powstaną, tylko będą wyglądać trochę inaczej.

## Kompilacja

```sh
make            # main.tex -> prezentacja.pdf (tylko jeśli coś się zmieniło)
make rep        # wymuszona ponowna kompilacja
make wykresy    # python3 sim/wykresy.py -> fig/*.pdf (ok. 30 s)
make clean      # usuwa prezentacja.pdf
```

Bez `make` (np. na Windowsie bez GNU make):

```sh
latexmk -lualatex -interaction=nonstopmode -output-directory=.build main.tex
# wynik: .build/main.pdf
```

`make` celowo ukrywa wyjście LaTeX-a. Przy błędzie zajrzyj do `.build/main.log`
(szukaj linii zaczynających się od `!`).

W edytorze (VS Code + LaTeX Workshop, TeXstudio, …) ustaw silnik **LuaLaTeX** i katalog
wyjściowy `.build`.

## Podział slajdów

| #  | Część                              | Slajdy | Czas    | Prelegent |
|----|------------------------------------|--------|---------|-----------|
| 1  | Motywacja                          | 1–3    | 4 min   | A         |
| 2  | Majorana w ciele stałym            | 4–8    | 6 min   | A         |
| 3  | Łańcuch Kitaeva (+ własna symulacja) | 9–14 | 8 min   | A         |
| 4  | Parzystość, nieabelowość, kubit    | 15–18  | 5 min   | A         |
| 5a | Nanodrut — model                   | 19–22  | 5 min   | A         |
| 5b | Nanodrut — inżynieria              | 23–25  | 5 min   | B         |
| 6  | Materiały i technologia            | 26–30  | 7 min   | B         |
| 7  | Pomiary i pułapki                  | 31–36  | 8 min   | B         |
| 8  | Stan na 2026                       | 37–40  | 5 min   | B         |
| 9  | Podsumowanie i literatura          | 41–42  | 2 min   | B         |
| —  | Zapasowe: BdG/Nambu, argument Kramersa, kod, parametry symulacji, oryginalny rys. 5 | po 42 | — | — |

Prelegent A: ~28 min (sl. 1–22), prelegent B: ~27 min (sl. 23–42). Numery slajdów
w tabeli = numery w stopce PDF = numery w komentarzach `% --- N (~X min) ---` w `main.tex`.
Stopka każdego slajdu pokazuje, czyja to część.

## Własne wykresy (`sim/wykresy.py`)

| Plik w `fig/`                 | Slajd | Co pokazuje |
|-------------------------------|-------|-------------|
| `kitaev_widmo.pdf`            | 13    | widmo BdG łańcucha Kitaeva ($N=30$, $\Delta=0.5t$) w funkcji $\mu$ |
| `kitaev_mody.pdf`             | 13    | $\lvert\psi\rvert^2$ dwóch modów Majorany dla $\mu=0$ i $\mu=1.5t$ |
| `kitaev_rozszczepienie.pdf`   | 14    | rozszczepienie $\delta E(N)$ w skali log, $\xi\propto1/\Delta$ |
| `drut_pasma.pdf`              | 20    | pasma drutu z SOC dla rosnącego $V_Z$ (odtworzenie rys. 5a–c z [LF12]) |
| `drut_bdg.pdf`                | 21    | pasma BdG dla $V_Z<V_c$, $V_Z=V_c$, $V_Z>V_c$ |
| `drut_EB.pdf`                 | 22    | widmo skończonego drutu InSb/Al ($L=2\,\mu$m) w funkcji $B$ |
| `przerwa_twarda_miekka.pdf`   | 28    | schemat: twarda vs miękka przerwa (gęstość stanów Dynesa) |

Parametry drutu InSb/Al (`PAR_INSB` w skrypcie): $m^*=0.014\,m_0$, $g=50$,
$\alpha=0.2$ eV·Å, $\Delta=0.25$ meV, $\mu=0$, $L=2\,\mu$m, krok sieci $a=10$ nm.
Wynik: $B^*\approx0.17$ T; w tym modelu $\xi\approx0.3$–$0.8\,\mu$m dla $B=0.25$–$0.5$ T.

## Źródła

- Materiał bazowy **[LF12]**: M. Leijnse, K. Flensberg, *Introduction to topological
  superconductivity and Majorana fermions*, Semicond. Sci. Technol. **27**, 124003 (2012),
  [arXiv:1206.1736](https://arxiv.org/abs/1206.1736). Pokrywa teorię do 2012 r.
  PDF nie jest w repo (prawa autorskie) — w razie potrzeby pobierz go z arXiv
  do `src/ref2.pdf` (ten plik jest ignorowany przez gita).
- `fig/ref/rys{1,3,4,5}.png` — rysunki 1, 3, 4, 5 wycięte z [LF12] (`pdfimages`),
  na slajdach zawsze z podanym źródłem.
- Część eksperymentalna i stan na 2026 — nowsza literatura, pełna lista na slajdzie 42.

### Znane niespójności w [LF12] (uwzględnione na slajdach)

- Równ. (51)–(53): w (51) człon Zeemana to $\tfrac12\tilde B\sigma_z$, w (52)–(53) już
  $\tilde B$. Na slajdach konsekwentnie $V_Z=\tfrac12 g\mu_B B$ = współczynnik przy $\sigma_z$,
  warunek topologiczny $V_Z>\sqrt{\Delta^2+\mu^2}$.
- Równ. (31)–(32): znak wykładnika nie zgadza się z (22)–(25); na slajdzie 16
  poprawione na $e^{+i\pi\sigma/4}$.
- Podpis rys. 1: indeksy końcowych Majoran zamienione względem tekstu
  (niesparowane są $\gamma_{1,1}$ i $\gamma_{N,2}$).
