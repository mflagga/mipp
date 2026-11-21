# Współpraca — jak pracujemy nad prezentacją

## Git

1. **Przed rozpoczęciem pracy:** `git pull --rebase`.
2. **Każdy edytuje głównie swoją część `main.tex`** — wtedy konflikty są rzadkie:
   - prelegent A: od znacznika `CZĘŚĆ I — Prelegent A` do `CZĘŚĆ II — Prelegent B`,
   - prelegent B: od `CZĘŚĆ II — Prelegent B` do `SLAJDY ZAPASOWE`,
   - preambuła (pakiety, kolory, makra) jest wspólna — zmiany w niej najpierw uzgadniamy.
3. Małe commity z opisem po polsku, np. `sl. 32: dodany wykres dI/dV z Mourik 2012`.
4. Przed `git push` sprawdź, że `make` przechodzi bez błędów.

### PDF w repo

`prezentacja.pdf` jest commitowany, żeby każdy mógł obejrzeć aktualną wersję bez
kompilacji. Commituj go **razem ze zmianami w źródle**, zbudowany z aktualnego `main.tex`.

Pliku binarnego git nie umie scalić. Przy konflikcie na `prezentacja.pdf` po prostu
przebuduj go po rozwiązaniu konfliktów w `main.tex`:

```sh
make rep                # wymuszona kompilacja (zwykłe `make` mogłoby uznać PDF za aktualny)
git add prezentacja.pdf
```

Tak samo z `fig/*.pdf`: zamiast scalać, uruchom ponownie `make wykresy`.

### `.gitignore` działa jak biała lista

Domyślnie ignorowane jest **wszystko**, a do repo trafia tylko to, co wypisano
w `.gitignore` z `!`. Dzięki temu pliki pomocnicze LaTeX-a i `__pycache__` nie zaśmiecają
repo, ale:

> **Nowy plik (np. `notatki.md`, nowy skrypt) trzeba dopisać do `.gitignore`**,
> np. `!notatki.md`, inaczej `git add` go pominie.

Wyjątki, które już są obsłużone: wszystko w `fig/` (`!fig/**`), pliki `sim/*.py`.
Sprawdzenie, czy plik jest ignorowany i przez którą regułę: `git check-ignore -v <plik>`.

## Konwencje w `main.tex`

### Numeracja slajdów

Przed każdym slajdem jest komentarz z numerem i czasem:

```latex
% --- 14 (~1 min) -------------------------------------------------------------
\begin{frame}{Rozszczepienie modów: $\delta E\propto e^{-L/\xi}$}
```

Numer = numer w stopce PDF = numer w planie (`src/initial_plan.txt`) i w tabeli w README.
**Po dodaniu/usunięciu slajdu** popraw numery w komentarzach i odwołania w treści —
obecnie są na sl. 37–39 (`slajdu~10`, `slajdzie~15`, `sl.~36`, `sl.~39`, `sl.~41`).
Znajdziesz je przez:

```sh
grep -nE 'slajd(zie|u)?~[0-9]|sl\.~[0-9]' main.tex
```

### Makra

| Makro | Do czego |
|-------|----------|
| `\zrodlo{...}` | źródło w prawym dolnym rogu slajdu. **Każdy cudzy rysunek, wzór z artykułu i liczba z literatury musi je mieć.** |
| `\sprawdz` / `\sprawdz[tekst]` | czerwony znacznik `[sprawdzić]` / `[tekst]` przy niezweryfikowanym fakcie. W wersji końcowej nie może go być — patrz niżej. |
| `\LF` | skrót cytowania `[LF12]` (artykuł bazowy). |
| `\prelegent` | tekst w stopce; przełączany `\renewcommand` na granicy części. |
| `\hc`, `\eV` | $\mathrm{h.c.}$, jednostka eV. |

Pozostałe znaczniki `[sprawdzić]` w źródle:

```sh
grep -n '\\sprawdz' main.tex     # w wersji końcowej powinna zostać tylko definicja makra
```

Żeby na chwilę ukryć znaczniki (np. do próby), w preambule zamień definicję na
`\newcommand{\sprawdz}[1][]{}`.

### Styl

- **Kolory:** `mBlue`, `mRed`, `mGreen`, `mDark` — te same co na wykresach z `sim/wykresy.py`.
  `\alert{...}` daje czerwony (`mRed`).
- **Jednostki:** zawsze przez `siunitx`: `\qty{0.2}{\milli\electronvolt}`,
  `\unit{\micro\metre}`.
- **Separator dziesiętny:** na razie kropka (ustawienie w `\sisetup` w preambule
  i domyślne w matplotlib). Jeśli zmieniamy na przecinek — w obu miejscach naraz.
- **Strzałki i symbole w tekście:** `→`, `⇒`, `≈` można pisać wprost (są zmapowane przez
  `newunicodechar`, bo STIX Two Text ich nie ma). Jeśli inny znak Unicode znika z PDF,
  w `.build/main.log` pojawi się `Missing character` — dodaj mapowanie
  `\newunicodechar{…}{\ensuremath{…}}` albo napisz go w trybie matematycznym.
- **Gęstość treści:** slajd 16:9, czcionka 10 pt. Jeśli w logu jest
  `Overfull \vbox` przy danym slajdzie, tekst wychodzi poza slajd — skróć go,
  zamiast zmniejszać czcionkę.

## Wykresy

- Wszystkie własne wykresy powstają w `sim/wykresy.py`. **Nie edytuj `fig/*.pdf` ręcznie** —
  zmień skrypt, uruchom `make wykresy`, zacommituj skrypt i nowe PDF-y razem.
- Każdy wykres ma własną funkcję (`wykres_kitaev`, `wykres_drut_pasma`, `wykres_drut_bdg`,
  `wykres_drut_EB`, `wykres_przerwa`); parametry drutu są w słowniku `PAR_INSB`.
- Rozmiary (`figsize` w cm) są dobrane do miejsca na slajdzie, żeby czcionka na wykresie
  (~8–9 pt) pasowała do slajdu. Przy zmianie rozmiaru na slajdzie zmień też `figsize`.
- `drut_EB.pdf` diagonalizuje macierz 800×800 dla 181 wartości $B$ — to najwolniejsza część
  (kilkadziesiąt sekund).

## Rysunki z literatury

- Wrzucamy do `fig/ref/`, nazwa opisowa (np. `mourik2012_dIdV.png`).
- Na slajdzie zawsze `\zrodlo{Rys.: autor i in., czasopismo tom, strona (rok)}`.
- Wycinanie rysunku z PDF: `pdfimages -list plik.pdf` (lista obrazów), potem
  `pdfimages -f <strona> -l <strona> -png plik.pdf fig/ref/nazwa`. Rysunki wektorowe:
  `pdftoppm -r 300 -f <strona> -l <strona> -png` + przycięcie.
