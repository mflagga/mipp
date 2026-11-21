# TODO — co zostało do zrobienia

Stan: pierwszy szkic (42 slajdy + 5 zapasowych, kompiluje się). Numery = numery slajdów
w stopce PDF. Odhaczaj `[x]` i usuwaj odpowiedni `\sprawdz` z `main.tex`.

## Uzupełnić

- [ ] Imiona i nazwiska prelegentów — `\author{...}` w preambule `main.tex`.
- [ ] Data wystąpienia — `\date{...}` (teraz `\today`).
- [ ] Zamienić „Prelegent A/B” w stopce (`\prelegent`) na imiona — opcjonalnie.

## Fakty do weryfikacji (czerwone `[sprawdzić]` na slajdach)

**Część I (A)**

- [ ] sl. 3 — oś czasu, rok 2026: „Majorana 2” (Pb), spór o TGP i odczyt $C_Q$ (zależy od sl. 39–40).
- [ ] sl. 19 — typowa średnica nanodrutu (~100 nm?).

**Część II (B)**

- [ ] sl. 24 — tabela InSb/InAs ($m^*$, $|g|$ w drutach, $B^*$) — porównać z literaturą.
- [ ] sl. 24 — typowa przerwa topologiczna $\Delta_\mathrm{top}$ (~10–50 μeV?).
- [ ] sl. 26 — tabela półprzewodników ($E_g$, $m^*$, $|g|$; PbTe: anizotropia, $\varepsilon_r$).
- [ ] sl. 26 — pole krytyczne cienkiej warstwy Al w płaszczyźnie (~2 T?).
- [ ] sl. 32 — Mourik 2012: zakres pól, w którym widać ZBP (~0.1–1 T?), wysokość piku (~0.05·2e²/h?).
- [ ] sl. 33 — odnośnik do noty o retrakcji Zhang i in. (Nature, 2021).
- [ ] sl. 34 — numery stron/tomów cytowanych prac (Liu 2017, Vuik 2019, Lee 2012, Pikulin 2012).
- [ ] sl. 36 — Microsoft, Nature 2025: czas przełączania parzystości (≳ 1 ms?), pole (~2 T?), błąd przypisania 1%.
- [ ] sl. 37 — Bordin i in. 2025 (3-węzłowy łańcuch): pełny odnośnik i co dokładnie się poprawia.
- [ ] sl. 38 — tetron, arXiv:2507.08795: tytuł, czy jest już publikacja w czasopiśmie,
      geometria pętli X/Z. **Liczby w tabeli** ($\tau_Z=12.4$ ms, $\tau_X=14.5$ μs, błędy
      0.5% / 16%) są przepisane z planu — potwierdzić w pracy.
- [ ] sl. 39 — krytyka TGP (Legg 2025): numer arXiv (2502.19560?) i główny argument.
- [ ] sl. 39 — **praca w PRB z 17.11.2026** o fałszywych pozytywach odczytu $C_Q$:
      autorzy, tytuł, DOI, główny argument. Na slajdzie jest tylko miejsce na nie.
- [ ] sl. 40 — „Majorana 2” (czerwiec 2026): co to jest i **czego dotyczy „średni czas życia
      20 s”** (parzystość / zatruwanie kwazicząstkami? $T_1$? kubit?). Obecny tekst to tylko
      teza z planu.
- [ ] sl. 40 — PbTe–Pb: dodać konkretne źródło (druty SAG).
- [ ] sl. 40 — Valentini i in., Science 2021: tom/strona.
- [ ] sl. 42 — literatura: uzupełnić pozycje oznaczone `[sprawdzić]`/`[uzupełnić]`.

## Brakujące rysunki

- [ ] sl. 27 — zdjęcie SEM/TEM drutu z epitaksjalnym Al (Krogstrup 2015 albo Gazibegovic 2017).
- [ ] sl. 32 — mapa $dI/dV(B, V)$ z Mourik i in. 2012.
- [ ] Opcjonalnie: sl. 35 — przykład przewodnictwa nielokalnego / danych TGP;
      sl. 36 — schemat urządzenia z pracy Microsoftu zamiast poglądowego.

## Pozostałe

- [ ] Próba czasowa: część A ~28 min, część B ~27 min (czasy per slajd w komentarzach `main.tex`).
- [ ] Ewentualne notatki dla prelegentów (`\note{...}`).
- [ ] Decyzja: separator dziesiętny kropka czy przecinek (patrz `WSPOLPRACA.md`).
- [ ] Wersja końcowa: `grep -n '\\sprawdz' main.tex` zwraca tylko definicję makra.
