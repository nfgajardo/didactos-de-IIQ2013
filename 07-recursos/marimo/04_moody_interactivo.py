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
def _(mo):
    mo.md(
        r"""
## Ejercicio resuelto: régimen de flujo

**Enunciado**  
¿Cuál es el régimen de flujo en una tubería de 10 in de diámetro nominal 
\((D = 254.5\ \text{mm})\) cuando circula \(Q = 0.1\ \text{m}^3/\text{s}\) de agua?

**Supuesto para agua a temperatura ambiente:**  
\(\nu \approx 1.0\times10^{-6}\ \text{m}^2/\text{s}\)

**Ecuaciones:**
\[
A = \frac{\pi D^2}{4},\qquad V = \frac{Q}{A},\qquad Re = \frac{VD}{\nu}
\]

Criterio:
- Laminar: \(Re < 2300\)
- Transición: \(2300 \le Re \le 4000\)
- Turbulento: \(Re > 4000\)
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
def _(mo, np):
    Q = 0.1
    D = 0.2545
    nu = 1.0e-6
    eps = 0.046e-3   # acero comercial (m)
    L = 100.0

    A = np.pi * D**2 / 4
    V = Q / A
    Re_ex = V * D / nu
    rr_ex = eps / D

    if Re_ex < 2300:
        regime = "Laminar"
    elif Re_ex <= 4000:
        regime = "Transición"
    else:
        regime = "Turbulento"

    # Colebrook (Darcy) para el caso del ejercicio
    fD = 0.25 / (np.log10(rr_ex / 3.7 + 5.74 / (Re_ex**0.9)) ** 2)
    for _ in range(35):
        inv = -2 * np.log10(rr_ex / 3.7 + 2.51 / (Re_ex * np.sqrt(fD)))
        fD = 1 / (inv**2)

    fF = fD / 4.0  # Fanning

    # phi = 4*fF*(L/D)*(V^2/2)
    phi = 4 * fF * (L / D) * (V**2 / 2)
    hf = phi / 9.81

    mo.md(
        fr"""
### Resultado del ejercicio

- Área: **A = {A:.5f} m²**
- Velocidad media: **V = {V:.3f} m/s**
- Reynolds: **Re = {Re_ex:.2e}**
- **Régimen: {regime}**

**Segunda parte (usando Moody, acero comercial):**
- Rugosidad relativa: **ε/D = {rr_ex:.2e}**
- Factor de fricción de **Fanning**: **f = {fF:.4f}** (aprox.)
- Factor de fricción de **Darcy** (referencia): **f_D = {fD:.4f}**
- \(\phi = 4f\,(L/D)\,(V^2/2)\): **φ = {phi:.2f} m²/s²**
- Equivalente en pérdida de carga: **h_f \approx {hf:.2f} m** (para L=100 m)

Conclusión: para este caudal y diámetro, el flujo está en régimen **{regime.lower()}**.
"""
    )
    return


@app.cell
def _(f_darcy, np, plt, re_manual, re_slider, rr_manual, rr_slider, use_manual):
    Re_grid = np.logspace(3, 8, 500)
    rr_lines = np.array([1e-5, 1e-4, 1e-3, 1e-2, 3e-2, 5e-2])

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

    y_min, y_max = 0.0, 0.1
    ax.set_ylim(y_min, y_max)
    y_ticks = np.arange(0.0, 0.101, 0.01)
    ax.set_yticks(y_ticks)
    ax.set_yticklabels([f"{t:.2f}" for t in y_ticks])

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
    ax2.set_yticklabels([f"{r:.1e}" for r in rr_lines[m]], fontsize=12)
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
