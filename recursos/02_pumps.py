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
# 02_pumps — Curvas características de bomba centrífuga (interactivo)

Este recurso muestra en un solo gráfico (mismo eje X) las curvas típicas de una bomba:

- **Carga-capacidad** $H(Q)$
- **Eficiencia** $\eta(Q)$
- **Potencia al eje** $P(Q)$
- **NPSHr**

## Ecuaciones base (modelo didáctico)

1) Curva de carga (aproximada):

$$
H(Q) = H_0 - aQ - bQ^2
$$

2) Curva de eficiencia (tipo campana):

$$
\eta(Q) = \eta_{max} - k\,(Q-Q_{BEP})^2
$$

3) Potencia hidráulica:

$$
P_h = \rho g Q H
$$

Potencia al eje (considerando eficiencia hidráulica y mecánica):

$$
P_{eje} = \frac{\rho g Q H}{\eta_h\,\eta_m}
$$

4) NPSHr (aprox. creciente con caudal):

$$
NPSHr(Q) = N_0 + cQ^2
$$

## Leyes de afinidad por cambio de diámetro (misma velocidad)

Con $r_D = D/D_{ref}$:

$$
Q \propto D \Rightarrow Q' = Q\,r_D
$$

$$
H \propto D^2 \Rightarrow H' = H\,r_D^2
$$

$$
P \propto D^3 \Rightarrow P' = P\,r_D^3
$$

## Variables de entrada recomendadas

- Geometría/operación: $D_{ref}$, $D$, rango de caudal
- Curva base: $H_0$, $a$, $b$
- Eficiencia: $\eta_{max}$, $Q_{BEP}$, $k$
- Fluido/sistema: $\rho$, $g$, $\eta_m$
- NPSHr: $N_0$, $c$
"""
    )
    return


@app.cell
def _(mo):
    D_ref = mo.ui.number(value=250.0, label="D_ref (mm)")
    D = mo.ui.slider(start=150.0, stop=350.0, step=5.0, value=250.0, label="D (mm)")

    Qmax_ref = mo.ui.number(value=320.0, label="Q_max ref (m³/h)")

    H0 = mo.ui.number(value=62.0, label="H0 (m)")
    a = mo.ui.number(value=0.06, label="a (m/(m³/h))")
    b = mo.ui.number(value=0.00035, label="b (m/(m³/h)²)")

    eta_max = mo.ui.number(value=0.82, label="η_max (0-1)")
    Qbep_ref = mo.ui.number(value=180.0, label="Q_BEP ref (m³/h)")
    k_eta = mo.ui.number(value=7.5e-6, label="k_eta")
    eta_m = mo.ui.number(value=0.95, label="η_mec (0-1)")

    rho = mo.ui.number(value=998.0, label="ρ (kg/m³)")
    npsh0 = mo.ui.number(value=2.0, label="NPSHr0 (m)")
    c_npsh = mo.ui.number(value=1.5e-4, label="c_NPSHr")

    mo.vstack([
        mo.hstack([D_ref, D, Qmax_ref], widths=[1, 1, 1]),
        mo.hstack([H0, a, b], widths=[1, 1, 1]),
        mo.hstack([eta_max, Qbep_ref, k_eta, eta_m], widths=[1, 1, 1, 1]),
        mo.hstack([rho, npsh0, c_npsh], widths=[1, 1, 1]),
    ])

    return D_ref, D, Qmax_ref, H0, a, b, eta_max, Qbep_ref, k_eta, eta_m, rho, npsh0, c_npsh


@app.cell
def _(np, D_ref, D, Qmax_ref, H0, a, b, eta_max, Qbep_ref, k_eta, eta_m, rho, npsh0, c_npsh):
    g = 9.81

    rD = max(D.value / D_ref.value, 1e-6)

    Q_ref = np.linspace(0.0, Qmax_ref.value, 240)  # m3/h
    H_ref = H0.value - a.value * Q_ref - b.value * (Q_ref**2)

    eta_ref = eta_max.value - k_eta.value * (Q_ref - Qbep_ref.value) ** 2
    eta_ref = np.clip(eta_ref, 0.05, 0.9)

    NPSHr_ref = npsh0.value + c_npsh.value * (Q_ref**2)

    # Escalado por diámetro
    Q = Q_ref * rD
    H = H_ref * (rD**2)
    eta = eta_ref  # aproximación didáctica
    NPSHr = NPSHr_ref * (rD**2)

    # Potencia eje
    Q_m3s = Q / 3600.0
    P_eje_W = rho.value * g * Q_m3s * np.maximum(H, 0.0) / np.clip(eta * eta_m.value, 0.05, 1.0)
    P_eje_kW = P_eje_W / 1000.0

    mask = H > 0
    Q, H, eta, NPSHr, P_eje_kW = Q[mask], H[mask], eta[mask], NPSHr[mask], P_eje_kW[mask]

    return Q, H, eta, NPSHr, P_eje_kW, rD


@app.cell
def _(plt, Q, H, eta, NPSHr, P_eje_kW, rD):
    fig, ax1 = plt.subplots(figsize=(11, 6.5))

    # Eje principal: H y NPSHr
    l1 = ax1.plot(Q, H, color="#1f77b4", lw=2.5, label="H-Q (m)")
    l2 = ax1.plot(Q, NPSHr, color="#17becf", lw=2.0, ls="--", label="NPSHr (m)")
    ax1.set_xlabel("Capacidad, Q (m³/h)", fontsize=12)
    ax1.set_ylabel("Carga / NPSHr (m)", fontsize=12)
    ax1.grid(True, ls="--", alpha=0.3)

    # Eje derecho: eficiencia
    ax2 = ax1.twinx()
    l3 = ax2.plot(Q, 100 * eta, color="#2ca02c", lw=2.2, label="Eficiencia (%)")
    ax2.set_ylabel("Eficiencia (%)", color="#2ca02c", fontsize=12)
    ax2.tick_params(axis="y", colors="#2ca02c")

    # Tercer eje derecho: potencia
    ax3 = ax1.twinx()
    ax3.spines["right"].set_position(("outward", 65))
    l4 = ax3.plot(Q, P_eje_kW, color="#d62728", lw=2.2, label="Potencia eje (kW)")
    ax3.set_ylabel("Potencia eje (kW)", color="#d62728", fontsize=12)
    ax3.tick_params(axis="y", colors="#d62728")

    lines = l1 + l2 + l3 + l4
    labels = [ln.get_label() for ln in lines]
    ax1.legend(lines, labels, loc="upper right", fontsize=10)

    ax1.set_title(f"Curvas de bomba centrífuga (escala por diámetro: D/D_ref = {rD:.3f})", fontsize=14, fontweight="bold")
    fig
    return


if __name__ == "__main__":
    app.run()
