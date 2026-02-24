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
# Diagrama de Moody interactivo (Marimo)

- Eje izquierdo: factor de fricción Darcy, **f**
- Eje derecho: rugosidad relativa, **ε/D**
- Eje inferior: número de Reynolds, **Re**

Incluye **inputs dobles** (slider + entrada manual) para Re y ε/D.
"""
    )
    return


@app.cell
def _(np):
    def f_swamee_jain(Re, rr):
        return 0.25 / (np.log10(rr / 3.7 + 5.74 / (Re**0.9)) ** 2)

    def f_colebrook(Re, rr, it=30):
        Re = np.asarray(Re, dtype=float)
        f = np.maximum(f_swamee_jain(Re, max(rr, 1e-12)), 1e-4)
        for _ in range(it):
            inv = -2 * np.log10(rr / 3.7 + 2.51 / (Re * np.sqrt(f)))
            f = 1 / (inv**2)
        return f

    def f_darcy(Re, rr):
        Re = np.asarray(Re, dtype=float)
        f = np.empty_like(Re)
        lam = Re < 2300
        f[lam] = 64 / Re[lam]
        f[~lam] = f_colebrook(Re[~lam], rr)
        return f

    return f_darcy


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
def _(f_darcy, np, plt, re_manual, re_slider, rr_manual, rr_slider, use_manual):
    Re_grid = np.logspace(3, 8, 500)
    rr_lines = np.array([
        1e-6, 2e-6, 5e-6, 1e-5, 2e-5, 5e-5, 1e-4, 2e-4,
        5e-4, 1e-3, 2e-3, 5e-3, 1e-2, 2e-2, 3e-2, 5e-2,
    ])

    Re0 = float(re_manual.value if use_manual.value else re_slider.value)
    rr0 = float(rr_manual.value if use_manual.value else rr_slider.value)

    Re0 = min(max(Re0, 1e3), 1e8)
    rr0 = min(max(rr0, 1e-6), 0.05)

    fig, ax = plt.subplots(figsize=(11, 7))

    for rrl in rr_lines:
        ax.plot(Re_grid, f_darcy(Re_grid, rrl), lw=1.2, color="steelblue")

    Re_l = np.logspace(2.3, np.log10(2300), 200)
    ax.plot(Re_l, 64 / Re_l, color="black", lw=2.0)

    ax.set_xscale("log")
    ax.set_xlim(1e3, 1e8)

    y_min, y_max = 0.005, 0.1
    ax.set_ylim(y_min, y_max)
    y_ticks = np.linspace(y_min, y_max, 10)
    ax.set_yticks(y_ticks)
    ax.set_yticklabels([f"{t:.4f}" for t in y_ticks])

    ax.grid(True, which="both", ls="--", alpha=0.3)
    ax.set_title("Diagrama de Moody", fontsize=18, fontweight="bold")
    ax.set_xlabel("Número de Reynolds, Re", fontsize=14)
    ax.set_ylabel("Factor de fricción Darcy, f", fontsize=14)
    ax.tick_params(axis="both", labelsize=12)

    ax2 = ax.twinx()
    f_ticks_right = 1 / (-2 * np.log10(rr_lines / 3.7)) ** 2
    m = (f_ticks_right >= y_min) & (f_ticks_right <= y_max)
    ax2.set_ylim(y_min, y_max)
    ax2.set_yticks(f_ticks_right[m])
    ax2.set_yticklabels([f"{r:.6f}".rstrip("0").rstrip(".") for r in rr_lines[m]], fontsize=12)
    ax2.set_ylabel("Rugosidad relativa, ε/D", fontsize=14)

    f0 = float(f_darcy(np.array([Re0]), rr0)[0])
    ax.scatter([Re0], [f0], color="#444444", s=90, zorder=6)
    ax.hlines(f0, Re0, ax.get_xlim()[1], colors="#666666", linestyles="--", lw=1.3, zorder=4)
    ax.vlines(Re0, y_min, f0, colors="#666666", linestyles="--", lw=1.3, zorder=4)

    ax.text(0.98, 0.97, f"f = {f0:.4f}", transform=ax.transAxes,
            ha="right", va="top", fontsize=14, color="#222222", fontweight="bold")
    ax.text(Re0 * 1.08, min(f0 * 1.02, y_max * 0.98), f"Re={Re0:.2e}\nε/D={rr0:.4f}",
            color="#333333", fontsize=11)

    fig
    return


if __name__ == "__main__":
    app.run()
