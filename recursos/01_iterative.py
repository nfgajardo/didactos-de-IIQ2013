import marimo

__generated_with = "0.20.2"
app = marimo.App(width="full")


@app.cell
def _():
    import marimo as mo
    import math
    import numpy as np
    import matplotlib.pyplot as plt
    return mo, math, np, plt


@app.cell
def _(mo):
    mo.md(
        r"""
# 01_iterative — Diseño de ducto con Colebrook-White (iterativo)

Se debe hacer fluir aire caliente a 1 atm y 35°C en un ducto circular de plástico de 150 m de largo, a una razón de 0.35 m³/s. En la parte (a), se pide determinar el diámetro mínimo del ducto para que la pérdida de carga no supere 20 m. En la parte (b), se duplica la longitud del ducto manteniendo el mismo diámetro, y se solicita calcular la caída en la razón de flujo si la pérdida de carga total debe permanecer constante.

Se resolverá con iteraciones sucesivas, mostrando tablas de convergencia.

## Datos del problema

- Fluido: aire a 1 atm y 35°C
- Longitud inicial: $L_1 = 150\ \text{m}$
- Caudal inicial: $Q_1 = 0.35\ \text{m}^3/\text{s}$
- Pérdida de carga máxima: $h_f = 20\ \text{m}$
- Ducto circular de plástico

## Supuestos de propiedades (35°C)

- Viscosidad cinemática del aire: $\nu = 1.65\times 10^{-5}\ \text{m}^2/\text{s}$
- Rugosidad absoluta plástico: $\varepsilon = 1.5\times 10^{-6}\ \text{m}$
- Gravedad: $g = 9.81\ \text{m}/\text{s}^2$

## Ecuaciones utilizadas

Número de Reynolds:

$$
Re = \frac{V D}{\nu}
$$

Ecuación de Darcy-Weisbach:

$$
h_f = f\,\frac{L}{D}\,\frac{V^2}{2g}
$$

Velocidad media a partir de caudal:

$$
V = \frac{4Q}{\pi D^2}
$$

Colebrook-White (factor de fricción de Darcy):

$$
\frac{1}{\sqrt{f}} = -2\log_{10}\left(\frac{\varepsilon/D}{3.7} + \frac{2.51}{Re\sqrt{f}}\right)
$$

Para (a), despejando diámetro con un $f$ supuesto:

$$
D = \left(\frac{8 f L Q^2}{g\pi^2 h_f}\right)^{1/5}
$$

Para (b), con $D$ fijo y $h_f$ fijo, despejando $Q$ con un $f$ supuesto:

$$
Q = \frac{\pi D^2}{4}\sqrt{\frac{2 g h_f D}{f L}}
$$
"""
    )
    return


@app.cell
def _(math):
    def colebrook_f(Re, rel_rough, f0=0.02, n=30):
        f = max(f0, 1e-6)
        Re = max(Re, 1.0)
        rr = max(rel_rough, 1e-12)
        for _ in range(n):
            inv = -2.0 * math.log10(rr / 3.7 + 2.51 / (Re * math.sqrt(f)))
            f = 1.0 / (inv * inv)
        return f

    return colebrook_f


@app.cell
def _(colebrook_f, math):
    # Datos
    Q1 = 0.35
    L1 = 150.0
    h = 20.0
    g = 9.81
    nu = 1.65e-5
    eps = 1.5e-6

    # Iteración parte (a)
    n_iter = 5
    f_guess_a = 0.02
    rows_a = []

    for _i_a in range(1, n_iter + 1):
        D = ((8.0 * f_guess_a * L1 * Q1 * Q1) / (g * math.pi * math.pi * h)) ** (1.0 / 5.0)
        V = 4.0 * Q1 / (math.pi * D * D)
        Re = V * D / nu
        rr = eps / D
        f_corr_a = colebrook_f(Re, rr, f0=f_guess_a, n=35)
        rows_a.append((_i_a, f_guess_a, Re, f_corr_a, D, V))
        f_guess_a = f_corr_a

    D_min = rows_a[-1][4]
    V1 = rows_a[-1][5]
    Re1 = rows_a[-1][2]
    f1 = rows_a[-1][3]

    return D_min, L1, Q1, Re1, V1, f1, g, h, n_iter, nu, eps, rows_a


@app.cell
def _(D_min, L1, Q1, Re1, V1, f1, mo, rows_a):
    table_a = [
        "| iteración | f (suposición) | Re | f (corregido) |",
        "|---:|---:|---:|---:|",
    ]
    for _i, _fg, _re, _fc, _, _ in rows_a:
        table_a.append(f"| {_i} | {_fg:.6f} | {_re:.3e} | {_fc:.6f} |")

    mo.md(
        fr"""
## (a) Diámetro mínimo del ducto — iteración paso a paso

En esta primera parte buscamos el diámetro mínimo del ducto que permita transportar el caudal especificado sin superar la pérdida de carga máxima. Para ello, se inicia con una suposición del factor de fricción, se calcula un diámetro candidato con Darcy-Weisbach, luego se obtiene la velocidad promedio y el número de Reynolds asociado, y finalmente se corrige el factor de fricción usando Colebrook-White. Este ciclo se repite de forma iterativa hasta estabilizar los valores, permitiendo observar claramente la convergencia entre la suposición inicial y el factor corregido.

{chr(10).join(table_a)}

**Valores convergidos (iteración {rows_a[-1][0]}):**

- $D_{{\min}} \approx {D_min:.4f}\ \text{{m}}$
- $V \approx {V1:.3f}\ \text{{m/s}}$
- $Re \approx {Re1:.3e}$
- $f \approx {f1:.5f}$

Interpretación: el ducto mínimo para cumplir $h_f\le 20\,\text{{m}}$ a $Q=0.35\,\text{{m}}^3/\text{{s}}$ es de aproximadamente **{D_min*1000:.0f} mm**.
"""
    )
    return


@app.cell
def _(D_min, Q1, colebrook_f, g, h, math, nu, eps):
    # Parte (b): L se duplica, D constante, h constante -> hallar Q2
    L2 = 300.0
    n_iter_b = 5
    f_guess_b = 0.02
    rows_b = []

    for _i_b in range(1, n_iter_b + 1):
        Q2 = (math.pi * D_min * D_min / 4.0) * math.sqrt((2.0 * g * h * D_min) / (f_guess_b * L2))
        V2 = 4.0 * Q2 / (math.pi * D_min * D_min)
        Re2 = V2 * D_min / nu
        rr2 = eps / D_min
        f_corr_b = colebrook_f(Re2, rr2, f0=f_guess_b, n=35)
        rows_b.append((_i_b, f_guess_b, Re2, f_corr_b, Q2, V2))
        f_guess_b = f_corr_b

    Q2_final = rows_b[-1][4]
    drop = Q1 - Q2_final
    drop_pct = 100.0 * drop / Q1

    return L2, Q2_final, drop, drop_pct, rows_b


@app.cell
def _(L2, Q2_final, drop, drop_pct, mo, rows_b):
    table_b = [
        "| iteración | f (suposición) | Re | f (corregido) |",
        "|---:|---:|---:|---:|",
    ]
    for _i, _fg, _re, _fc, _, _ in rows_b:
        table_b.append(f"| {_i} | {_fg:.6f} | {_re:.3e} | {_fc:.6f} |")

    mo.md(
        fr"""
## (b) Duplicando longitud del ducto, con $D$ constante y $h_f$ constante

Se usa $L_2 = {L2:.0f}\,\text{{m}}$ y se itera para encontrar el nuevo caudal.

{chr(10).join(table_b)}

**Resultado convergido:**

- Nuevo caudal: $Q_2 \approx {Q2_final:.4f}\ \text{{m}}^3/\text{{s}}$
- Caída de caudal: $\Delta Q = Q_1 - Q_2 \approx {drop:.4f}\ \text{{m}}^3/\text{{s}}$
- Disminución porcentual: **{drop_pct:.2f}%**
"""
    )
    return


@app.cell
def _(np, plt, rows_a, rows_b):
    it_a = np.array([r[0] for r in rows_a])
    fg_a = np.array([r[1] for r in rows_a])
    fc_a = np.array([r[3] for r in rows_a])

    it_b = np.array([r[0] for r in rows_b])
    fg_b = np.array([r[1] for r in rows_b])
    fc_b = np.array([r[3] for r in rows_b])

    fig, ax = plt.subplots(1, 2, figsize=(12, 4.5), constrained_layout=True)

    ax[0].plot(it_a, fg_a, "o--", label="f suposición")
    ax[0].plot(it_a, fc_a, "s-", label="f corregido")
    ax[0].set_title("Convergencia de f — parte (a)")
    ax[0].set_xlabel("Iteración")
    ax[0].set_ylabel("f")
    ax[0].grid(alpha=0.3)
    ax[0].legend()

    ax[1].plot(it_b, fg_b, "o--", label="f suposición")
    ax[1].plot(it_b, fc_b, "s-", label="f corregido")
    ax[1].set_title("Convergencia de f — parte (b)")
    ax[1].set_xlabel("Iteración")
    ax[1].set_ylabel("f")
    ax[1].grid(alpha=0.3)
    ax[1].legend()

    fig
    return


if __name__ == "__main__":
    app.run()
