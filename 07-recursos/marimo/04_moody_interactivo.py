import marimo

__generated_with = "0.20.2"
app = marimo.App(width="full")


@app.cell
def _():
    import marimo as mo
    import numpy as np
    import matplotlib.pyplot as plt
    return mo, np, plt


@app.cell
def _(mo):
    mo.md(
        r"""
# Diagrama de Moody interactivo (Marimo) — **Fanning**

El gráfico usa **factor de fricción de Fanning** \(f_F\), no Darcy.

## Ecuaciones usadas

1) Número de Reynolds:
\[
Re = \frac{VD}{\nu}
\]

2) Régimen laminar (Fanning):
\[
f_F = \frac{16}{Re}
\]

3) Régimen turbulento (Colebrook-White en Darcy):
\[
\frac{1}{\sqrt{f_D}} = -2\log_{10}\left(\frac{\varepsilon/D}{3.7} + \frac{2.51}{Re\sqrt{f_D}}\right)
\]

y conversión a Fanning:
\[
f_F = \frac{f_D}{4}
\]

4) Relación con pérdidas por fricción:
\[
\phi = 4f_F\left(\frac{L}{D}\right)\left(\frac{V^2}{2}\right)
\]
"""
    )
    return


@app.cell
def _(np):
    def f_darcy_swamee_jain(Re, rr):
        return 0.25 / (np.log10(rr / 3.7 + 5.74 / (Re**0.9)) ** 2)

    def f_darcy_colebrook(Re, rr, it=35):
        Re = np.asarray(Re, dtype=float)
        fD = np.maximum(f_darcy_swamee_jain(Re, max(rr, 1e-12)), 1e-6)
        for _ in range(it):
            inv = -2 * np.log10(rr / 3.7 + 2.51 / (Re * np.sqrt(fD)))
            fD = 1 / (inv**2)
        return fD

    def f_fanning(Re, rr):
        Re = np.asarray(Re, dtype=float)
        fF = np.empty_like(Re)
        lam = Re < 2300
        fF[lam] = 16 / Re[lam]
        fF[~lam] = f_darcy_colebrook(Re[~lam], rr) / 4
        return fF

    return f_fanning


@app.cell
def _(mo):
    re_slider = mo.ui.slider(1e3, 1e8, value=1e5, step=1000, label="Re (slider)")
    re_manual = mo.ui.number(value=1e5, label="Re (manual)")

    rr_slider = mo.ui.slider(0.000001, 0.05, value=0.001, step=0.000001, label="ε/D (slider)")
    rr_manual = mo.ui.number(value=0.001, label="ε/D (manual)")

    use_manual = mo.ui.switch(value=False, label="Usar entradas manuales")

    mo.vstack(
        [
            use_manual,
            mo.hstack([re_slider, re_manual], widths=[1, 1]),
            mo.hstack([rr_slider, rr_manual], widths=[1, 1]),
        ]
    )
    return re_manual, re_slider, rr_manual, rr_slider, use_manual


@app.cell
def _(f_fanning, np, plt, re_manual, re_slider, rr_manual, rr_slider, use_manual):
    Re_grid = np.logspace(3, 8, 500)
    rr_lines = np.array([1e-5, 1e-4, 1e-3, 1e-2, 3e-2, 5e-2])

    Re0 = float(re_manual.value if use_manual.value else re_slider.value)
    rr0 = float(rr_manual.value if use_manual.value else rr_slider.value)
    Re0 = min(max(Re0, 1e3), 1e8)
    rr0 = min(max(rr0, 1e-6), 0.05)

    fig, ax = plt.subplots(figsize=(11, 7))

    for rrl in rr_lines:
        ax.plot(Re_grid, f_fanning(Re_grid, rrl), lw=1.2, color="steelblue")

    # Línea laminar (Fanning)
    Re_l = np.logspace(2.3, np.log10(2300), 200)
    ax.plot(Re_l, 16 / Re_l, color="black", lw=2.0, label="Laminar: f = 16/Re")

    # Zona sombreada laminar
    ax.axvspan(1e3, 2300, color="#d9d9d9", alpha=0.25, zorder=0)
    ax.text(1300, 0.095, "Régimen laminar", fontsize=11, color="#555555")

    ax.set_xscale("log")
    ax.set_xlim(1e3, 1e8)

    y_min, y_max = 0.0, 0.1
    ax.set_ylim(y_min, y_max)
    y_ticks = np.arange(0.0, 0.101, 0.01)
    ax.set_yticks(y_ticks)
    ax.set_yticklabels([f"{t:.2f}" for t in y_ticks])

    ax.grid(True, which="both", ls="--", alpha=0.3)
    ax.set_title("Diagrama de Moody (Fanning)", fontsize=18, fontweight="bold")
    ax.set_xlabel("Número de Reynolds, Re", fontsize=14)
    ax.set_ylabel("Factor de fricción de Fanning, f", fontsize=14)
    ax.tick_params(axis="both", labelsize=12)

    # Eje derecho: rugosidad relativa en notación científica
    ax2 = ax.twinx()
    fD_right = 1 / (-2 * np.log10(rr_lines / 3.7)) ** 2
    fF_right = fD_right / 4
    m = (fF_right >= y_min) & (fF_right <= y_max)
    ax2.set_ylim(y_min, y_max)
    ax2.set_yticks(fF_right[m])
    ax2.set_yticklabels([f"{r:.1e}" for r in rr_lines[m]], fontsize=12)
    ax2.set_ylabel("Rugosidad relativa, ε/D", fontsize=14)

    # Punto interactivo
    f0 = float(f_fanning(np.array([Re0]), rr0)[0])
    ax.scatter([Re0], [f0], color="#444444", s=90, zorder=6)
    ax.hlines(f0, Re0, ax.get_xlim()[1], colors="#666666", linestyles="--", lw=1.3, zorder=4)
    ax.vlines(Re0, y_min, f0, colors="#666666", linestyles="--", lw=1.3, zorder=4)

    ax.text(
        0.98,
        0.97,
        f"f = {f0:.4f}",
        transform=ax.transAxes,
        ha="right",
        va="top",
        fontsize=14,
        color="#222222",
        fontweight="bold",
    )
    ax.text(
        Re0 * 1.08,
        min(f0 * 1.02, y_max * 0.98),
        f"Re={Re0:.2e}\nε/D={rr0:.4f}",
        color="#333333",
        fontsize=11,
    )

    ax.legend(loc="upper center")
    fig
    return


if __name__ == "__main__":
    app.run()
