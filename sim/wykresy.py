#!/usr/bin/env python3
"""Wykresy do prezentacji „Fermiony Majorany i ich realizacja w nanodrutach".

Uruchomienie (z katalogu głównego projektu):  python3 sim/wykresy.py
Wyniki trafiają do fig/:
  kitaev_widmo.pdf          widmo BdG łańcucha Kitaeva (N = 30) w funkcji mu
  kitaev_mody.pdf           |psi|^2 dwóch modów Majorany (mu = 0 oraz mu = 1.5 t)
  kitaev_rozszczepienie.pdf rozszczepienie dE(N) w skali log  ->  dE ~ exp(-L/xi)
  drut_pasma.pdf            pasma drutu z SOC dla rosnącego V_Z (odtworzenie rys. 5a-c)
  drut_bdg.pdf              pasma BdG dla V_Z < V_c, V_Z = V_c, V_Z > V_c (rys. 5d)
  drut_EB.pdf               widmo skończonego drutu InSb/Al w funkcji B
  przerwa_twarda_miekka.pdf schemat DOS: twarda vs miękka przerwa (wzór Dynesa)
"""

from pathlib import Path

import matplotlib as mpl
import matplotlib.pyplot as plt
import numpy as np
from scipy.linalg import eigh

OUT = Path(__file__).resolve().parent.parent / "fig"
OUT.mkdir(exist_ok=True)

CM = 1 / 2.54
C_BLUE = "#1f5fa8"
C_RED = "#c8323c"
C_GREY = "#9a9a9a"
C_GREEN = "#2a8a4a"

mpl.rcParams.update({
    "font.family": "STIX Two Text",
    "mathtext.fontset": "stix",
    "font.size": 9,
    "axes.labelsize": 9,
    "axes.titlesize": 9,
    "legend.fontsize": 8,
    "xtick.labelsize": 8,
    "ytick.labelsize": 8,
    "axes.spines.top": False,
    "axes.spines.right": False,
    "savefig.bbox": "tight",
    "savefig.pad_inches": 0.02,
})

# Macierze Pauliego
s0 = np.eye(2)
sx = np.array([[0, 1], [1, 0]], dtype=complex)
sy = np.array([[0, -1j], [1j, 0]], dtype=complex)
sz = np.array([[1, 0], [0, -1]], dtype=complex)


# ---------------------------------------------------------------------------
# 1. Łańcuch Kitaeva
#    H = -mu sum n_i - sum (t c_i^+ c_{i+1} + Delta c_i c_{i+1} + h.c.)
#    BdG w bazie (c_1..c_N, c_1^+..c_N^+):  H_BdG = [[h, D], [-D, -h]]
# ---------------------------------------------------------------------------
def kitaev_bdg(N, mu, t=1.0, delta=1.0):
    h = -mu * np.eye(N) - t * (np.eye(N, k=1) + np.eye(N, k=-1))
    D = delta * (np.eye(N, k=1) - np.eye(N, k=-1))  # antysymetryczna
    return np.block([[h, D], [-D, -h]])


def kitaev_majorany(N, mu, t=1.0, delta=1.0):
    """Zwraca (E0, |gamma_A|^2, |gamma_B|^2) dla stanu najbliższego E = 0."""
    E, V = np.linalg.eigh(kitaev_bdg(N, mu, t, delta))
    i = np.argmin(np.abs(E))
    u, v = V[:N, i], V[N:, i]
    gA, gB = u + v, u - v  # kombinacje Majorany (H_BdG rzeczywista)
    gA /= np.linalg.norm(gA)
    gB /= np.linalg.norm(gB)
    return abs(E[i]), np.abs(gA) ** 2, np.abs(gB) ** 2


def wykres_kitaev():
    N, t, delta = 30, 1.0, 0.5
    mus = np.linspace(-3.2, 3.2, 641)
    spec = np.array([np.linalg.eigvalsh(kitaev_bdg(N, m, t, delta)) for m in mus])

    fig, ax = plt.subplots(figsize=(8.0 * CM, 5.6 * CM))
    ax.axvspan(-2 * t, 2 * t, color=C_BLUE, alpha=0.08, lw=0)
    ax.plot(mus, spec, color=C_GREY, lw=0.5)
    # para stanów najbliższych zera – wyróżniona tylko w fazie topologicznej
    order = np.argsort(np.abs(spec), axis=1)[:, :2]
    low = np.take_along_axis(spec, order, axis=1)
    low[np.abs(mus) > 2 * t] = np.nan
    ax.plot(mus, low, color=C_RED, lw=1.6)
    ax.set_xlim(mus[0], mus[-1])
    ax.set_ylim(-3.2, 3.2)
    ax.set_xlabel(r"$\mu/t$")
    ax.set_ylabel(r"$E/t$")
    box = dict(fc="white", ec="none", alpha=0.9, pad=1.0)
    ax.text(0, 2.9, "faza topologiczna " r"$|\mu|<2t$", ha="center", va="top",
            color=C_BLUE, fontsize=8, bbox=box)
    ax.text(0, 0.18, "mody zerowe", ha="center", va="bottom", color=C_RED, fontsize=8,
            bbox=box)
    for x in (-2.65, 2.65):
        ax.text(x, -2.9, "trywialna", ha="center", va="bottom", fontsize=8, color="0.3",
                bbox=box)
    ax.set_title(rf"$N={N}$, $\Delta={delta:g}\,t$", loc="right", fontsize=8)
    fig.savefig(OUT / "kitaev_widmo.pdf")
    plt.close(fig)

    # |psi|^2 modów Majorany
    fig, axs = plt.subplots(1, 2, figsize=(8.0 * CM, 5.6 * CM), sharey=True)
    sites = np.arange(1, N + 1)
    for ax, mu in zip(axs, (0.0, 1.5)):
        E0, gA, gB = kitaev_majorany(N, mu, t, delta)
        ax.bar(sites, gA, width=0.8, color=C_BLUE, label=r"$\gamma_A$")
        ax.bar(sites, gB, width=0.8, color=C_RED, alpha=0.85, label=r"$\gamma_B$")
        ax.set_title(r"$\mu=0$" if mu == 0 else rf"$\mu={mu:g}\,t$", fontsize=8)
        ax.set_xlabel("węzeł $i$")
        ax.set_xlim(0, N + 1)
    axs[0].set_ylabel(r"$|\psi_i|^2$")
    axs[0].legend(frameon=False, loc="upper center")
    fig.tight_layout(w_pad=0.6)
    fig.savefig(OUT / "kitaev_mody.pdf")
    plt.close(fig)

    # rozszczepienie dE(N) dla kilku Delta (mu = t):  dE ~ exp(-N/xi),  xi ~ 1/Delta
    Ns = np.arange(4, 61)
    mu = 1.0
    fig, ax = plt.subplots(figsize=(8.0 * CM, 5.6 * CM))
    for d, c in ((0.2, C_RED), (0.35, C_GREEN), (0.6, C_BLUE)):
        dE = np.array([2 * kitaev_majorany(n, mu, t, d)[0] for n in Ns])
        ok = dE > 1e-12
        xi = -1 / np.polyfit(Ns[ok], np.log(dE[ok]), 1)[0]
        ax.semilogy(Ns[ok], dE[ok], "o-", ms=2, lw=0.8, color=c,
                    label=rf"$\Delta={d:g}\,t$, $\xi\approx{xi:.1f}$")
    ax.set_xlabel(r"długość łańcucha $N$")
    ax.set_ylabel(r"$\delta E / t$")
    ax.set_ylim(1e-16, 5)
    ax.legend(frameon=False, loc="lower left", title=rf"$\mu={mu:g}\,t$",
              title_fontsize=8)
    ax.text(0.55, 0.9, r"$\delta E\propto e^{-N/\xi}$", transform=ax.transAxes, fontsize=10)
    fig.savefig(OUT / "kitaev_rozszczepienie.pdf")
    plt.close(fig)


# ---------------------------------------------------------------------------
# 2. Nanodrut z SOC – jednostki bezwymiarowe:
#    k w k_so = m alpha / hbar^2,  E w E_so = m alpha^2 / (2 hbar^2)
#    H0 = k^2 - mu + 2 k sigma_y + V_Z sigma_z
#    H_BdG = (k^2 - mu + 2 k sigma_y) tau_z + V_Z sigma_z + Delta tau_x
# ---------------------------------------------------------------------------
def h0(k, mu, vz):
    return (k ** 2 - mu) * s0 + 2 * k * sy + vz * sz


def hbdg(k, mu, vz, delta):
    tz = np.diag([1.0, -1.0])
    tx = np.array([[0, 1], [1, 0]])
    return (np.kron(tz, (k ** 2 - mu) * s0 + 2 * k * sy)
            + np.kron(np.eye(2), vz * sz) + delta * np.kron(tx, s0))


def wykres_drut_pasma():
    ks = np.linspace(-2.6, 2.6, 401)
    vzs = (0.0, 1.0, 4.0)
    titles = (r"(a) $V_Z=0$", r"(b) $V_Z=E_\mathrm{so}$", r"(c) $V_Z=4E_\mathrm{so}$")
    fig, axs = plt.subplots(1, 3, figsize=(14.0 * CM, 4.6 * CM), sharey=True)
    for ax, vz, tt in zip(axs, vzs, titles):
        bands, spins = [], []
        for k in ks:
            E, V = np.linalg.eigh(h0(k, 0.0, vz))
            bands.append(E)
            spins.append([[np.real(V[:, j].conj() @ s @ V[:, j]) for s in (sy, sz)]
                          for j in range(2)])
        bands, spins = np.array(bands), np.array(spins)  # spins[k, band, (y,z)]
        for j, c in ((0, C_BLUE), (1, C_RED)):
            ax.plot(ks, bands[:, j], color=c, lw=1.3)
            for kk in (-2.0, 2.0):
                i = np.argmin(np.abs(ks - kk))
                sy_, sz_ = spins[i, j]
                ax.annotate("", xy=(ks[i] + 0.45 * sy_, bands[i, j] + 1.6 * sz_),
                            xytext=(ks[i], bands[i, j]),
                            arrowprops=dict(arrowstyle="-|>", color=c, lw=1.0,
                                            mutation_scale=7))
        ax.axhline(0, color="0.6", lw=0.4)
        ax.set_title(tt, fontsize=8)
        ax.set_xlabel(r"$k/k_\mathrm{so}$")
        ax.set_xlim(ks[0], ks[-1])
        ax.set_ylim(-5.5, 9)
    axs[2].axhline(-1.2, color=C_GREEN, lw=1, ls="--")
    axs[2].text(2.5, -1.0, r"$\mu$", color=C_GREEN, fontsize=9, va="bottom", ha="right")
    axs[0].set_ylabel(r"$E/E_\mathrm{so}$")
    fig.tight_layout(w_pad=0.4)
    fig.savefig(OUT / "drut_pasma.pdf")
    plt.close(fig)


def wykres_drut_bdg():
    ks = np.linspace(-2.6, 2.6, 401)
    delta, mu = 1.0, 0.0
    vc = np.hypot(delta, mu)
    cases = ((0.5 * vc, r"$V_Z=V_c/2$" "\n(trywialna)"),
             (vc, r"$V_Z=V_c$" "\n(zamknięcie przerwy)"),
             (2.0 * vc, r"$V_Z=2V_c$" "\n(topologiczna)"))
    fig, axs = plt.subplots(1, 3, figsize=(14.0 * CM, 4.6 * CM), sharey=True)
    for ax, (vz, tt) in zip(axs, cases):
        E = np.array([np.linalg.eigvalsh(hbdg(k, mu, vz, delta)) for k in ks])
        for j in range(4):
            ax.plot(ks, E[:, j], color=C_BLUE if j in (1, 2) else C_GREY, lw=1.2)
        ax.axhline(0, color="0.6", lw=0.4)
        ax.set_title(tt, fontsize=8)
        ax.set_xlabel(r"$k/k_\mathrm{so}$")
        ax.set_xlim(ks[0], ks[-1])
        ax.set_ylim(-4, 4)
    axs[0].set_ylabel(r"$E/E_\mathrm{so}$")
    fig.text(0.99, 0.01, rf"$\Delta={delta:g}\,E_\mathrm{{so}}$, $\mu=0$",
             ha="right", va="bottom", fontsize=7, color="0.3")
    fig.tight_layout(w_pad=0.4)
    fig.savefig(OUT / "drut_bdg.pdf")
    plt.close(fig)


# ---------------------------------------------------------------------------
# 3. Skończony drut InSb/Al w funkcji B (model ciasnego wiązania, krok a)
#    parametry orientacyjne – do weryfikacji z literaturą
# ---------------------------------------------------------------------------
HB2_2M0 = 38.0998  # hbar^2 / (2 m0)  [meV nm^2]
MU_B = 0.05788     # magneton Bohra   [meV/T]

PAR_INSB = dict(m=0.014, g=50.0, alpha=20.0, delta=0.25, mu=0.0, L=2000.0, a=10.0)
#              m*/m0, |g|,   alpha [meV nm] (= 0.2 eV A), Delta [meV], mu [meV], L, a [nm]


def drut_bdg_rzeczywisty(B, p):
    N = int(round(p["L"] / p["a"]))
    t = HB2_2M0 / p["m"] / p["a"] ** 2
    vz = 0.5 * p["g"] * MU_B * B
    tz = np.diag([1.0, -1.0])
    tx = np.array([[0.0, 1.0], [1.0, 0.0]])
    onsite = ((2 * t - p["mu"]) * np.kron(tz, s0) + vz * np.kron(np.eye(2), sz)
              + p["delta"] * np.kron(tx, s0))
    hop = -t * np.kron(tz, s0) - 1j * p["alpha"] / (2 * p["a"]) * np.kron(tz, sy)
    H = np.kron(np.eye(N), onsite) + np.kron(np.eye(N, k=1), hop) \
        + np.kron(np.eye(N, k=-1), hop.conj().T)
    return H


def przerwa_objetosciowa(vz, p, ks):
    """min_k E_1(k) dla nieskończonego drutu (model ciągły)."""
    tz = np.diag([1.0, -1.0])
    tx = np.array([[0.0, 1.0], [1.0, 0.0]])
    gaps = []
    for k in ks:
        Hk = (np.kron(tz, (HB2_2M0 / p["m"] * k ** 2 - p["mu"]) * s0 + p["alpha"] * k * sy)
              + vz * np.kron(np.eye(2), sz) + p["delta"] * np.kron(tx, s0))
        gaps.append(np.min(np.abs(np.linalg.eigvalsh(Hk))))
    return min(gaps)


def wykres_drut_EB():
    p = PAR_INSB
    Bs = np.linspace(0.0, 0.6, 181)
    nlev = 6
    lev = []
    for B in Bs:
        E = eigh(drut_bdg_rzeczywisty(B, p), eigvals_only=True,
                 subset_by_value=(-0.6, 0.6))
        E = np.sort(E)
        Epos = np.sort(E[E >= 0])[:nlev]
        lev.append(np.concatenate([Epos, np.full(nlev - len(Epos), np.nan)]))
    lev = np.array(lev)

    vc = np.hypot(p["delta"], p["mu"])
    Bc = vc / (0.5 * p["g"] * MU_B)
    ks = np.linspace(0, 0.08, 801)
    gap = np.array([przerwa_objetosciowa(0.5 * p["g"] * MU_B * B, p, ks) for B in Bs])

    fig, ax = plt.subplots(figsize=(9.0 * CM, 5.8 * CM))
    for j in range(1, nlev):
        ax.plot(Bs, lev[:, j], color=C_GREY, lw=0.8)
        ax.plot(Bs, -lev[:, j], color=C_GREY, lw=0.8)
    ax.plot(Bs, lev[:, 0], color=C_RED, lw=1.4, label="najniższy stan skończonego drutu")
    ax.plot(Bs, -lev[:, 0], color=C_RED, lw=1.4)
    ax.plot(Bs, gap, "--", color=C_BLUE, lw=1.0, label="przerwa objętościowa ($L\\to\\infty$)")
    ax.plot(Bs, -gap, "--", color=C_BLUE, lw=1.0)
    ax.axvline(Bc, color="k", lw=0.6, ls=":")
    ax.text(Bc + 0.005, 0.52, rf"$B^*\approx{Bc:.2f}$ T" "\n" r"$V_Z=\sqrt{\Delta^2+\mu^2}$",
            fontsize=8, va="top")
    ax.set_xlim(Bs[0], Bs[-1])
    ax.set_ylim(-0.55, 0.55)
    ax.set_xlabel(r"$B$ [T]")
    ax.set_ylabel(r"$E$ [meV]")
    ax.legend(loc="lower left", fontsize=7, framealpha=0.95, edgecolor="none")
    ax.set_title(rf"InSb/Al: $m^*={p['m']}\,m_0$, $g={p['g']:g}$, "
                 rf"$\alpha={p['alpha'] / 100:g}$ eV$\cdot$Å, $\Delta={p['delta']}$ meV, "
                 rf"$\mu={p['mu']:g}$, $L={p['L'] / 1000:g}\,\mu$m",
                 fontsize=7, color="0.3", loc="left")
    fig.savefig(OUT / "drut_EB.pdf")
    plt.close(fig)
    print(f"drut_EB: B* = {Bc:.3f} T, t = {HB2_2M0 / p['m'] / p['a'] ** 2:.2f} meV")


# ---------------------------------------------------------------------------
# 4. Twarda vs miękka przerwa – schemat (gęstość stanów Dynesa)
#    N(E)/N0 = Re[(E + i Gamma) / sqrt((E + i Gamma)^2 - Delta^2)]
# ---------------------------------------------------------------------------
def wykres_przerwa():
    E = np.linspace(-2.5, 2.5, 2001)
    fig, ax = plt.subplots(figsize=(7.0 * CM, 5.0 * CM))
    for gam, c, lab in ((0.003, C_BLUE, "twarda (epitaksjalny Al)"),
                        (0.25, C_RED, "miękka (zła granica faz)")):
        z = E + 1j * gam
        dos = np.real(z / np.sqrt(z ** 2 - 1.0 + 0j) * np.sign(E + 1e-12))
        dos = np.abs(dos)
        ax.plot(E, dos, color=c, lw=1.2, label=lab)
    ax.set_yscale("log")
    ax.set_ylim(1e-3, 30)
    ax.set_xlim(E[0], E[-1])
    ax.set_xlabel(r"$eV/\Delta$")
    ax.set_ylabel(r"$dI/dV$ (j. wzgl.)")
    ax.legend(frameon=False, loc="lower left", fontsize=7)
    fig.savefig(OUT / "przerwa_twarda_miekka.pdf")
    plt.close(fig)


# ---------------------------------------------------------------------------
# 5. Wykresy do slajdy.tex (wersja finalna, wspólna z częścią kolegi)
#    Paleta i czcionka (Inter) jak na slajdach kolegi, przezroczyste tło
#    (slajdy mają kremowe tło).  Wyniki: fig/final/*.pdf
#    Samo to:  python3 -c "import sys; sys.path.insert(0, 'sim'); import wykresy; wykresy.wykresy_final()"
# ---------------------------------------------------------------------------
F_NAVY = "#172033"
F_BLUE = "#2d5baa"
F_RUST = "#a64b16"
F_GREEN = "#1f7a5a"
F_PURPLE = "#6b3fa0"
F_GREY = "#5a6170"
F_LINE = "#b9b3a6"


def _styl_final():
    """rcParams dla wykresów w stylu slajdów finalnych (czcionka Inter z TeX Live)."""
    from matplotlib import font_manager as fm
    for d in ("/usr/share/texlive/texmf-dist/fonts/opentype/public/inter",
              "/usr/local/texlive/2026/texmf-dist/fonts/opentype/public/inter"):
        for name in ("Inter-Regular.otf", "Inter-Italic.otf", "Inter-Medium.otf"):
            p = Path(d) / name
            if p.exists():
                fm.fontManager.addfont(str(p))
    return {
        "font.family": "Inter",
        "mathtext.fontset": "custom",
        "mathtext.rm": "Inter",
        "mathtext.it": "Inter:italic",
        "font.size": 7.5,
        "axes.labelsize": 7.5,
        "axes.titlesize": 7.5,
        "xtick.labelsize": 6.5,
        "ytick.labelsize": 6.5,
        "legend.fontsize": 7,
        "text.color": F_NAVY,
        "axes.labelcolor": F_NAVY,
        "axes.edgecolor": F_GREY,
        "xtick.color": F_GREY,
        "ytick.color": F_GREY,
        "axes.linewidth": 0.6,
        "xtick.major.width": 0.6,
        "ytick.major.width": 0.6,
        "savefig.transparent": True,
    }


def _mody_kitaeva(N, mu, t, delta):
    """|psi|^2 dwóch Majoran z podprzestrzeni dwóch stanów najbliższych E = 0.

    Wektor BdG (u, v) = (phi, phi) to jedna Majorana, (psi, -psi) druga; dowolna
    kombinacja daje je z powrotem jako u + v oraz u - v.  Bierzemy oba wektory
    własne najbliższe zera, żeby nie trafić na czystą Majoranę (wtedy u - v = 0).
    """
    E, V = np.linalg.eigh(kitaev_bdg(N, mu, t, delta))
    idx = np.argsort(np.abs(E))[:2]
    A = [V[:N, i] + V[N:, i] for i in idx]
    B = [V[:N, i] - V[N:, i] for i in idx]
    gA = max(A, key=np.linalg.norm)
    gB = max(B, key=np.linalg.norm)
    gA, gB = gA / np.linalg.norm(gA), gB / np.linalg.norm(gB)
    if np.argmax(np.abs(gA)) > N // 2:  # gamma_A zawsze na lewym końcu
        gA, gB = gB, gA
    return np.abs(gA) ** 2, np.abs(gB) ** 2


def wykresy_final():
    out = OUT / "final"
    out.mkdir(exist_ok=True)
    with mpl.rc_context(_styl_final()):
        _final_kitaev(out)
        _final_bogolubow(out)
        _final_przerwa(out)
        _final_opor(out)
    print("Zapisano do", out)


def _final_kitaev(out):
    # widmo BdG skończonego łańcucha w funkcji mu
    N, t, delta = 30, 1.0, 0.5
    mus = np.linspace(-3.2, 3.2, 641)
    spec = np.array([np.linalg.eigvalsh(kitaev_bdg(N, m, t, delta)) for m in mus])
    fig, ax = plt.subplots(figsize=(6.6 * CM, 4.6 * CM))
    ax.axvspan(-2 * t, 2 * t, color=F_BLUE, alpha=0.08, lw=0)
    ax.plot(mus, spec, color=F_LINE, lw=0.45)
    order = np.argsort(np.abs(spec), axis=1)[:, :2]
    low = np.take_along_axis(spec, order, axis=1)
    low[np.abs(mus) > 2 * t] = np.nan
    ax.plot(mus, low, color=F_RUST, lw=1.6)
    ax.set_xlim(mus[0], mus[-1])
    ax.set_ylim(-3.2, 3.2)
    ax.set_xticks([-3, -2, -1, 0, 1, 2, 3])
    ax.set_xlabel(r"$\mu/t$")
    ax.set_ylabel(r"$E/t$")
    ax.spines[["top", "right"]].set_visible(False)
    ax.text(0, 3.3, "faza topologiczna", ha="center", va="bottom", color=F_BLUE, fontsize=7,
            clip_on=False)
    ax.text(0, 0.22, r"mody $E=0$", ha="center", va="bottom", color=F_RUST, fontsize=7)
    for x in (-2.6, 2.6):
        ax.text(x, 3.3, "trywialna", ha="center", va="bottom", color=F_GREY, fontsize=6.5,
                clip_on=False)
    fig.savefig(out / "kitaev_widmo.pdf")
    plt.close(fig)

    # |psi|^2 Majoran: punkt specjalny i mu = 1.5 t
    fig, axs = plt.subplots(1, 2, figsize=(6.8 * CM, 4.6 * CM), sharey=True)
    sites = np.arange(1, N + 1)
    for ax, (mu, d, tyt) in zip(axs, ((0.0, 1.0, r"$\mu=0,\ \Delta=t$"),
                                       (1.5, 0.5, r"$\mu=1.5t,\ \Delta=0.5t$"))):
        gA, gB = _mody_kitaeva(N, mu, t, d)
        ax.bar(sites, gA, width=0.8, color=F_BLUE, lw=0)
        ax.bar(sites, gB, width=0.8, color=F_RUST, lw=0)
        ax.set_title(tyt, fontsize=7)
        ax.set_xlabel(r"węzeł $i$")
        ax.set_xlim(0, N + 1)
        ax.set_xticks([1, 15, 30])
        ax.spines[["top", "right"]].set_visible(False)
    axs[0].set_ylabel(r"$|\psi_i|^2$")
    axs[0].set_ylim(0, 1.05)
    axs[0].set_yticks([0, 0.5, 1])
    fig.tight_layout(w_pad=0.8)
    fig.savefig(out / "kitaev_mody.pdf")
    plt.close(fig)


def _final_bogolubow(out):
    """E(xi) = ±sqrt(xi^2 + Delta^2), kolor = udział elektronu |u|^2; obok |u|^2, |v|^2."""
    from matplotlib.collections import LineCollection
    from matplotlib.colors import LinearSegmentedColormap
    cmap = LinearSegmentedColormap.from_list("eh", [F_RUST, F_PURPLE, F_BLUE])
    xi = np.linspace(-4, 4, 801)
    E = np.sqrt(xi ** 2 + 1)
    u2 = 0.5 * (1 + xi / E)

    fig, (ax, bx) = plt.subplots(1, 2, figsize=(12.0 * CM, 4.6 * CM),
                                 gridspec_kw=dict(width_ratios=[1.15, 1]))
    for sgn, w in ((1, u2), (-1, 1 - u2)):  # gałąź -E: udział elektronu = |v|^2
        pts = np.column_stack([xi, sgn * E]).reshape(-1, 1, 2)
        seg = np.concatenate([pts[:-1], pts[1:]], axis=1)
        lc = LineCollection(seg, cmap=cmap, norm=plt.Normalize(0, 1), lw=1.8)
        lc.set_array(0.5 * (w[:-1] + w[1:]))
        ax.add_collection(lc)
    ax.plot(xi, xi, ls=(0, (3, 2)), lw=0.7, color=F_BLUE, alpha=0.6)
    ax.plot(xi, -xi, ls=(0, (3, 2)), lw=0.7, color=F_RUST, alpha=0.6)
    ax.annotate("", xy=(0, 1), xytext=(0, -1),
                arrowprops=dict(arrowstyle="<->", lw=0.7, color=F_NAVY, shrinkA=0, shrinkB=0))
    ax.text(-0.15, 0.25, r"$2\Delta$", ha="right", va="center", fontsize=7.5)
    ax.text(3.2, 2.2, "elektron", color=F_BLUE, ha="center", fontsize=7)
    ax.text(-3.2, 2.2, "dziura", color=F_RUST, ha="center", fontsize=7)
    ax.annotate("pół na pół", xy=(0.08, 1.02), xytext=(1.25, 0.35), color=F_PURPLE,
                fontsize=7, va="center",
                arrowprops=dict(arrowstyle="-", lw=0.5, color=F_PURPLE, shrinkA=1, shrinkB=1))
    ax.text(0.15, 4.2, r"$E/\Delta$", va="top", fontsize=7.5)
    ax.set_xlim(-4, 4)
    ax.set_ylim(-4.2, 4.2)
    ax.set_xlabel(r"$\xi_k/\Delta$  (energia liczona od $E_F$)")
    for s in ("left", "bottom"):
        ax.spines[s].set_position("zero")
    ax.spines[["top", "right"]].set_visible(False)
    ax.set_xticks([-4, -2, 2, 4])
    ax.set_yticks([])
    ax.xaxis.set_label_coords(0.5, -0.06)

    bx.plot(xi, u2, color=F_BLUE, lw=1.6)
    bx.plot(xi, 1 - u2, color=F_RUST, lw=1.6)
    bx.axhline(0.5, color=F_LINE, lw=0.5)
    bx.axvline(0, color=F_LINE, lw=0.5)
    bx.text(2.3, 0.72, r"$|u_k|^2$  elektron", color=F_BLUE, ha="center", fontsize=7)
    bx.text(-2.3, 0.72, r"$|v_k|^2$  dziura", color=F_RUST, ha="center", fontsize=7)
    bx.set_xlim(-4, 4)
    bx.set_ylim(0, 1.02)
    bx.set_yticks([0, 0.5, 1])
    bx.set_xlabel(r"$\xi_k/\Delta$")
    bx.spines[["top", "right"]].set_visible(False)
    fig.tight_layout(w_pad=1.5)
    fig.savefig(out / "bogolubow.pdf")
    plt.close(fig)


def _final_przerwa(out):
    """Charakterystyka I(V) złącza tunelowego: metal–izolator–metal vs metal–izolator–nadprzewodnik (T = 0)."""
    v = np.linspace(-3, 3, 1201)
    i_nis = np.sign(v) * np.sqrt(np.clip(v ** 2 - 1, 0, None))
    fig, ax = plt.subplots(figsize=(6.0 * CM, 4.6 * CM))
    ax.axvspan(-1, 1, color=F_RUST, alpha=0.09, lw=0)
    ax.plot(v, v, color=F_GREY, lw=1.0, ls=(0, (3, 2)))
    ax.plot(v, i_nis, color=F_BLUE, lw=1.7)
    for s in ("left", "bottom"):
        ax.spines[s].set_position("zero")
    ax.spines[["top", "right"]].set_visible(False)
    ax.set_xticks([-1, 1])
    ax.set_xticklabels(["", ""])
    ax.text(1, -0.25, r"$\Delta/e$", ha="center", va="top", fontsize=7, color=F_GREY)
    ax.text(-1, 0.25, r"$-\Delta/e$", ha="center", va="bottom", fontsize=7, color=F_GREY)
    ax.set_yticks([])
    ax.set_xlim(-3, 3)
    ax.set_ylim(-3, 3)
    ax.text(3.0, -0.3, r"$V$", ha="right", va="top", fontsize=7.5)
    ax.text(0.12, 2.95, r"$I$", ha="left", va="top", fontsize=7.5)
    ax.text(2.1, 2.75, "metal", color=F_GREY, fontsize=7, ha="right")
    ax.text(1.55, 0.55, "nadprzewodnik", color=F_BLUE, fontsize=7)
    ax.text(0, -2.6, r"$I=0$", color=F_RUST, ha="center", fontsize=7)
    fig.savefig(out / "przerwa_IV.pdf")
    plt.close(fig)


def _final_opor(out):
    """Schemat R(T) rtęci (Onnes 1911): skok do zera przy T_c ≈ 4.2 K."""
    T = np.linspace(4.0, 4.45, 901)
    Tc = 4.2
    R = np.where(T > Tc, 0.110 + 0.08 * (T - Tc), 0.0)
    fig, ax = plt.subplots(figsize=(6.0 * CM, 4.6 * CM))
    ax.plot(T, R, color=F_BLUE, lw=1.7)
    ax.axvline(Tc, color=F_LINE, lw=0.6, ls=(0, (3, 2)))
    ax.text(Tc + 0.01, 0.06, r"$T_c$", fontsize=7.5)
    ax.text(4.03, 0.02, r"$R = 0$", color=F_RUST, fontsize=7.5)
    ax.text(4.03, 0.135, "rtęć (Hg)", color=F_GREY, fontsize=7)
    ax.set_xlim(T[0], T[-1])
    ax.set_ylim(-0.005, 0.15)
    ax.set_xlabel(r"$T$ (K)")
    ax.set_ylabel(r"$R$ ($\Omega$)")
    ax.spines[["top", "right"]].set_visible(False)
    fig.savefig(out / "opor_T.pdf")
    plt.close(fig)


if __name__ == "__main__":
    wykres_kitaev()
    wykres_drut_pasma()
    wykres_drut_bdg()
    wykres_drut_EB()
    wykres_przerwa()
    wykresy_final()
    print("Zapisano do", OUT)
