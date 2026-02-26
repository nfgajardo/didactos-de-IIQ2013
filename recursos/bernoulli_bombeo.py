import marimo

__generated_with = "0.20.2"
app = marimo.App(width="full", app_title="💧 Bernoulli — Sistema de Bombeo")


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    # 💧 Ecuación de Bernoulli: Sistema de Bombeo de Agua
    ## Análisis gráfico e interactivo — Ingeniería Civil / Mecánica de Fluidos

    ---

    ### 📚 Fundamento Teórico

    La **Ecuación de Bernoulli generalizada** expresa la conservación de energía entre dos puntos de un fluido en movimiento, incluyendo el aporte de una bomba y las pérdidas de carga:

    $$\frac{P_1}{\rho g} + \frac{v_1^2}{2g} + z_1 + H_b = \frac{P_2}{\rho g} + \frac{v_2^2}{2g} + z_2 + h_f$$

    | Término | Nombre | Unidad |
    |---|---|---|
    | $P/\rho g$ | Altura de presión | m |
    | $v^2/2g$ | Altura cinética | m |
    | $z$ | Altura potencial (cota) | m |
    | $H_b$ | Altura de la bomba | m |
    | $h_f$ | Pérdidas de carga | m |

    ### 🔧 Condiciones del problema de bombeo

    - **Punto 1** (superficie estanque): $P_1 = P_{atm}$, $v_1 \approx 0$, $z_1 = 0$ (referencia)
    - **Punto 2** (descarga en el cerro): $P_2 = P_{atm}$, $v_2 = v_{tubería}$, $z_2 = $ altura cerro

    Simplificando con presiones manométricas nulas:

    $$\boxed{H_b = z_2 + \frac{v_2^2}{2g} + h_f}$$

    > 💡 La bomba debe suministrar energía para vencer la **diferencia de cota**, la **energía cinética** y las **pérdidas por fricción**.
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md("""
    ---
    ## 🎛️ Panel de Control — Ajusta los parámetros del sistema
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    slider_z2 = mo.ui.slider(
        start=5, stop=100, step=1, value=30,
        label="🏔️ Altura del cerro  z₂ [m]",
        show_value=True,
    )
    slider_v = mo.ui.slider(
        start=0.1, stop=8.0, step=0.1, value=2.0,
        label="💨 Velocidad en tubería  v [m/s]",
        show_value=True,
    )
    slider_D = mo.ui.slider(
        start=25, stop=300, step=5, value=100,
        label="🔩 Diámetro de tubería  D [mm]",
        show_value=True,
    )
    slider_hf = mo.ui.slider(
        start=0.0, stop=30.0, step=0.5, value=5.0,
        label="⚡ Pérdidas de carga  hf [m]",
        show_value=True,
    )
    mo.vstack([
        mo.hstack([slider_z2, slider_v], justify="start", gap="4rem"),
        mo.hstack([slider_D,  slider_hf], justify="start", gap="4rem"),
    ])
    return slider_D, slider_hf, slider_v, slider_z2


@app.cell(hide_code=True)
def _(mo, np, slider_D, slider_hf, slider_v, slider_z2):
    # ── Parámetros desde sliders ──────────────────────────────
    z2   = slider_z2.value
    v2   = slider_v.value
    D_mm = slider_D.value
    hf   = slider_hf.value

    # ── Constantes físicas ────────────────────────────────────
    g   = 9.81
    rho = 1000.0

    # ── Cálculos hidráulicos ──────────────────────────────────
    z1  = 0.0
    v1  = 0.0
    D   = D_mm / 1000.0
    A   = np.pi * D**2 / 4
    Q   = A * v2
    Q_lps = Q * 1000

    hv1 = v1**2 / (2 * g)
    hv2 = v2**2 / (2 * g)

    Hb    = z2 + hv2 + hf          # altura de la bomba [m]
    Pb    = rho * g * Q * Hb       # potencia hidráulica [W]
    Pb_kW = Pb / 1000

    # ── Líneas de energía (EGL) y piezométrica (HGL) ─────────
    # Puntos: estanque → entrada bomba → salida bomba → cerro
    EGL_0 = z1 + hv1                    # estanque
    EGL_1 = EGL_0 - hf * 0.15          # antes de bomba (pérdidas succión)
    EGL_2 = EGL_1 + Hb                  # después de bomba
    EGL_3 = z2 + hv2                    # cerro

    HGL_0 = EGL_0 - hv1
    HGL_1 = EGL_1 - hv2
    HGL_2 = EGL_2 - hv2
    HGL_3 = EGL_3 - hv2

    # ── Callout con resultados ────────────────────────────────
    resumen = mo.callout(
        mo.md(f"""
        **Resultados de la Ecuación de Bernoulli**

        | Variable | Fórmula | Valor |
        |---|---|---|
        | Altura de la bomba | $H_b = z_2 + v^2/2g + h_f = {z2:.1f} + {hv2:.3f} + {hf:.1f}$ | **{Hb:.2f} m** |
        | Caudal | $Q = A \\cdot v = \\frac{{\\pi ({D_mm:.0f}\\text{{mm}})^2}}{{4}} \\cdot {v2:.1f}$ m/s | **{Q_lps:.3f} L/s** |
        | Potencia hidráulica | $P = \\rho g Q H_b$ | **{Pb_kW:.3f} kW** |
        | Altura cinética | $v^2/2g$ | **{hv2:.4f} m** |
        """),
        kind="info",
    )
    mo.vstack([resumen])
    return (
        D_mm,
        EGL_0,
        EGL_1,
        EGL_2,
        EGL_3,
        HGL_0,
        HGL_1,
        HGL_2,
        HGL_3,
        Hb,
        Pb_kW,
        Q_lps,
        hf,
        hv2,
        v2,
        z2,
    )


@app.cell(hide_code=True)
def _(mo):
    mo.md("""
    ---
    ## 📊 Visualizaciones
    """)
    return


@app.cell(hide_code=True)
def _(
    D_mm,
    EGL_0,
    EGL_1,
    EGL_2,
    EGL_3,
    HGL_0,
    HGL_1,
    HGL_2,
    HGL_3,
    Hb,
    Pb_kW,
    Q_lps,
    hf,
    np,
    plt,
    v2,
    z2,
):
    fig, axes = plt.subplots(1, 2, figsize=(16, 7))
    fig.patch.set_facecolor('#f8f9fa')

    # ══════════════════════════════════════════════════════════
    # PANEL IZQUIERDO — Esquema físico del sistema
    # ══════════════════════════════════════════════════════════
    ax1 = axes[0]
    ax1.set_facecolor('#e8f4f8')
    ax1.set_xlim(-1.2, 11.5)
    ax1.set_ylim(-6, z2 + 10)
    ax1.set_title('📐 Esquema del Sistema de Bombeo', fontsize=13,
                  fontweight='bold', pad=10)
    ax1.set_xlabel('Distancia (esquemática)', fontsize=10)
    ax1.set_ylabel('Cota  z  [m]', fontsize=10)
    ax1.grid(True, alpha=0.25, linestyle='--')

    # Perfil del terreno / cerro
    xT = np.array([0, 2, 3, 4, 5, 6, 7, 8, 9, 10, 10, 0])
    zT = np.array([0, 0, .05, .15, .35, .60, .78, .90, .97, 1, -.05, -.05]) * z2
    ax1.fill(xT, zT, color='#8B7355', alpha=0.65)
    ax1.fill([0, 0, 2, 2], [-6, 0, 0, -6], color='#8B7355', alpha=0.65)
    # Pasto
    ax1.fill_between([0, 2], [0, 0], [0.25, 0.25], color='#4CAF50', alpha=0.7)
    ax1.fill_between(xT[:10], zT[:10], zT[:10] + 0.2, color='#4CAF50', alpha=0.7)

    # Estanque
    eh = min(3.5, z2 * 0.12 + 1.5)
    from matplotlib.patches import FancyBboxPatch
    ax1.add_patch(FancyBboxPatch((-1.0, -eh), 2.0, eh,
                                  boxstyle='square', lw=2,
                                  edgecolor='#1565C0', facecolor='#BBDEFB', alpha=0.85))
    ax1.fill([-0.95, -0.95, 0.9, 0.9],
             [-eh, -0.1, -0.1, -eh], color='#2196F3', alpha=0.55)
    ax1.axhline(0, xmin=0.0, xmax=0.18, color='#1976D2', lw=3, alpha=0.9)
    ax1.text(0, 0.5, 'Nivel libre', ha='center', fontsize=8, color='#1565C0')
    ax1.text(0, -eh - 0.9, 'Estanque\n(Punto 1)', ha='center',
             fontsize=8, color='#1565C0', fontweight='bold')
    ax1.text(0, -eh - 1.7, '$z_1 = 0$ m', ha='center', fontsize=8, color='#1565C0')

    # Tubería
    x_pipe = np.linspace(2.0, 10.0, 200)
    z_pipe = np.linspace(-2.0, z2, 200)
    ax1.plot([0.6, 1.5], [0, 0], color='#37474F', lw=5, zorder=5, solid_capstyle='round')
    ax1.plot([1.5, 1.5], [0, -2], color='#37474F', lw=5, zorder=5)
    ax1.plot(x_pipe, z_pipe, color='#37474F', lw=5, zorder=5, solid_capstyle='round')

    # Flechas de flujo
    for pct in [0.25, 0.5, 0.75]:
        xi = 2 + pct * 8
        zi = -2 + pct * (z2 + 2)
        dz = (z2 + 2) / 8 * 0.6
        ax1.annotate('', xy=(xi + 0.5, zi + dz), xytext=(xi, zi),
                     arrowprops=dict(arrowstyle='->', color='#2196F3', lw=2))

    # Bomba
    bomba_circ = plt.Circle((1.5, -3.0), 0.55, color='#FF5722', zorder=10, ec='#BF360C', lw=2)
    ax1.add_patch(bomba_circ)
    ax1.text(1.5, -3.0, '⚙', fontsize=18, ha='center', va='center', zorder=11)
    ax1.annotate(f'BOMBA\n$H_b = {Hb:.1f}$ m\n$P = {Pb_kW:.2f}$ kW',
                 xy=(1.5, -3.6), fontsize=8, ha='center', fontweight='bold',
                 color='#BF360C',
                 bbox=dict(boxstyle='round,pad=0.35', facecolor='#FFCCBC', alpha=0.9))

    # Punto de llegada
    ax1.plot(10, z2, 'o', color='#E91E63', ms=11, zorder=10, mec='#880E4F', mew=2)
    ax1.annotate(f'Punto 2\n$z_2 = {z2:.0f}$ m',
                 xy=(10, z2), xytext=(8.0, z2 + 2.5),
                 fontsize=9, fontweight='bold', color='#880E4F',
                 arrowprops=dict(arrowstyle='->', color='#880E4F', lw=1.5),
                 bbox=dict(boxstyle='round,pad=0.3', facecolor='#FCE4EC', alpha=0.85))

    # Cotas de referencia
    ax1.axhline(0,  color='#FF9800', ls=':', lw=1.5, alpha=0.8)
    ax1.axhline(z2, color='#9C27B0', ls=':', lw=1.5, alpha=0.8)
    ax1.annotate('', xy=(10.8, z2), xytext=(10.8, 0),
                 arrowprops=dict(arrowstyle='<->', color='#9C27B0', lw=2))
    ax1.text(11.1, z2 / 2, f'$z_2={z2:.0f}$ m', fontsize=9,
             color='#9C27B0', va='center', fontweight='bold')

    # ══════════════════════════════════════════════════════════
    # PANEL DERECHO — Líneas EGL y HGL
    # ══════════════════════════════════════════════════════════
    ax2 = axes[1]
    ax2.set_facecolor('#f0f4e8')
    ax2.set_title('📊 Líneas de Energía (EGL) y Piezométrica (HGL)',
                  fontsize=13, fontweight='bold', pad=10)
    ax2.set_xlabel('Posición en el sistema', fontsize=10)
    ax2.set_ylabel('Altura de energía  [m]', fontsize=10)
    ax2.grid(True, alpha=0.25, linestyle='--')

    X  = [0, 1.5, 1.5, 10]
    Zc = [0, -2,  -2,  z2]   # cotas del eje de la tubería

    # Rellenos por componente de energía
    ax2.fill_between([0, 1.5], [EGL_0, EGL_1], [HGL_0, HGL_1],
                     alpha=0.3, color='#FF9800', label='$v^2/2g$ (cinética)')
    ax2.fill_between([1.5, 10], [EGL_2, EGL_3], [HGL_2, HGL_3],
                     alpha=0.3, color='#FF9800')
    ax2.fill_between([0, 1.5], [HGL_0, HGL_1], [Zc[0], Zc[1]],
                     alpha=0.25, color='#2196F3', label='$P/\\rho g$ (presión)')
    ax2.fill_between([1.5, 10], [HGL_2, HGL_3], [Zc[2], Zc[3]],
                     alpha=0.25, color='#2196F3')
    ax2.fill_between([0, 10], [0, 0], -1,
                     alpha=0.0)   # referencia invisible
    # Cota positiva
    z_pos_0 = max(Zc[0], 0); z_pos_3 = max(Zc[3], 0)
    if z_pos_3 > 0:
        ax2.fill_between([1.5, 10], [Zc[2], Zc[3]], [0, 0],
                         where=[Zc[2] >= 0, Zc[3] >= 0],
                         alpha=0.3, color='#795548', label='$z$ (potencial)')

    # Cota del terreno
    ax2.plot([0, 1.5, 1.5, 10], [0, -2, -2, z2],
             'k--', lw=1.5, alpha=0.45, label='Cota tubería')

    # HGL
    ax2.plot([0, 1.5], [HGL_0, HGL_1], 'b-', lw=2.5, label='HGL (piezométrica)')
    ax2.plot([1.5, 1.5], [HGL_1, HGL_2], 'b-', lw=2.5)
    ax2.plot([1.5, 10], [HGL_2, HGL_3], 'b-', lw=2.5)

    # EGL
    ax2.plot([0, 1.5], [EGL_0, EGL_1], 'r-', lw=2.5, label='EGL (energía total)')
    ax2.plot([1.5, 1.5], [EGL_1, EGL_2], 'r-', lw=2.5)
    ax2.plot([1.5, 10], [EGL_2, EGL_3], 'r-', lw=2.5)

    # Puntos clave
    for xi, ei, hi in zip([0, 1.5, 1.5, 10],
                           [EGL_0, EGL_1, EGL_2, EGL_3],
                           [HGL_0, HGL_1, HGL_2, HGL_3]):
        ax2.plot(xi, ei, 'ro', ms=8, zorder=10)
        ax2.plot(xi, hi, 'bo', ms=8, zorder=10)

    # Flecha de aporte de la bomba
    ax2.annotate('', xy=(1.5, EGL_2), xytext=(1.5, EGL_1),
                 arrowprops=dict(arrowstyle='->', color='#FF5722', lw=2.5))
    ax2.text(1.65, (EGL_1 + EGL_2) / 2, f'$H_b = {Hb:.1f}$ m',
             fontsize=9, color='#BF360C', fontweight='bold')

    # Etiquetas de pérdidas
    perdida_total = EGL_2 - EGL_3
    ax2.annotate('', xy=(10, EGL_3), xytext=(10, EGL_2),
                 arrowprops=dict(arrowstyle='->', color='gray', lw=1.5))
    ax2.text(9.0, (EGL_2 + EGL_3) / 2, f'$h_f={hf:.1f}$ m',
             fontsize=8, color='gray', ha='right')

    ax2.set_xticks([0, 1.5, 10])
    ax2.set_xticklabels(['Estanque (1)', 'Bomba', 'Cerro (2)'], fontsize=10)
    ax2.legend(loc='upper left', fontsize=9, framealpha=0.9)

    fig.suptitle(
        f'💧 Bernoulli — z₂={z2} m  |  v={v2} m/s  |  D={D_mm} mm  |  hf={hf} m'
        f'   →   Hb={Hb:.2f} m  |  Q={Q_lps:.2f} L/s  |  P={Pb_kW:.3f} kW',
        fontsize=11, fontweight='bold', color='#1A237E', y=1.01,
        bbox=dict(boxstyle='round,pad=0.4', facecolor='#E3F2FD', alpha=0.9)
    )
    plt.tight_layout()
    plt.gca()
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md("""
    ---
    ## ⚡ Balance de Energía por Componente
    """)
    return


@app.cell(hide_code=True)
def _(EGL_0, EGL_1, EGL_2, EGL_3, Hb, hf, hv2, np, plt, z2):
    def _():
        fig2, ax3 = plt.subplots(figsize=(10, 5))
        fig2.patch.set_facecolor('#f5f5f5')
        ax3.set_facecolor('#fafafa')

        cats   = ['Estanque (1)', 'Antes\nBomba', 'Después\nBomba', 'Cerro (2)']
        z_v    = np.array([0.0,  -2.0,  -2.0,  z2])
        hv_v   = np.array([0.0,  hv2,   hv2,   hv2])
        # Altura de presión = EGL - z - hv (solo parte positiva para graficar)
        hp_v   = np.array([EGL_0, EGL_1, EGL_2, EGL_3]) - z_v - hv_v
        hp_v   = np.maximum(hp_v, 0)
        z_plot = np.maximum(z_v, 0)

        x = np.arange(len(cats))
        w = 0.5

        ax3.bar(x, z_plot,  w, label='Cota  z [m]',          color='#795548', alpha=0.85)
        ax3.bar(x, hp_v,    w, bottom=z_plot,
                label='Presión  $P/\\rho g$ [m]',             color='#2196F3', alpha=0.8)
        ax3.bar(x, hv_v,    w, bottom=z_plot + hp_v,
                label='Cinética  $v^2/2g$ [m]',               color='#FF9800', alpha=0.8)

        # Línea de energía total
        energias = np.array([EGL_0, EGL_1, EGL_2, EGL_3])
        ax3.plot(x, energias, 'r-o', lw=2.5, ms=9, label='Energía total H [m]', zorder=10)
        for xi, ei in zip(x, energias):
            ax3.text(xi, ei + 0.4, f'{ei:.1f} m', ha='center',
                     fontsize=9, fontweight='bold', color='darkred')

        # Flecha de la bomba
        ax3.annotate('', xy=(x[2], EGL_2), xytext=(x[1], EGL_1),
                     arrowprops=dict(arrowstyle='->', color='#FF5722', lw=2))
        ax3.text(1.5, (EGL_1 + EGL_2) / 2 + 1, f'+{Hb:.1f} m\n(Bomba)',
                 ha='center', fontsize=8, color='#BF360C', fontweight='bold')

        # Flecha de pérdidas
        ax3.annotate('', xy=(x[3], EGL_3), xytext=(x[2], EGL_2),
                     arrowprops=dict(arrowstyle='->', color='gray', lw=1.5))
        ax3.text(2.5, (EGL_2 + EGL_3) / 2 + 1, f'−{hf:.1f} m\n(Pérdidas)',
                 ha='center', fontsize=8, color='gray')

        ax3.set_title('⚡ Desglose de Energía en cada Punto del Sistema',
                      fontsize=12, fontweight='bold', pad=8)
        ax3.set_ylabel('Altura de energía [m]', fontsize=10)
        ax3.set_xticks(x)
        ax3.set_xticklabels(cats, fontsize=11)
        ax3.legend(loc='upper right', fontsize=9, framealpha=0.92)
        ax3.grid(True, axis='y', alpha=0.3, linestyle='--')
        plt.tight_layout()
        return plt.gca()


    _()
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ---
    ## 📝 Ejercicios Propuestos

    Usa los sliders para responder:

    **Ejercicio 1 — Efecto de la altura**
    Con $v = 2$ m/s, $D = 100$ mm y $h_f = 5$ m, varía $z_2$ entre 10 m y 80 m.
    ¿Cómo cambia $H_b$? ¿La relación es lineal? ¿Por qué?

    **Ejercicio 2 — Efecto del diámetro**
    Fija $z_2 = 40$ m y $h_f = 5$ m. Varía el diámetro entre 50 mm y 200 mm con $v = 3$ m/s.
    ¿Cómo afecta el diámetro al caudal $Q$ y a la potencia requerida?

    **Ejercicio 3 — Pérdidas de carga**
    Con $z_2 = 50$ m, $v = 2$ m/s, $D = 150$ mm, incrementa $h_f$ de 0 a 20 m.
    ¿Qué porcentaje de $H_b$ representan las pérdidas cuando $h_f = 20$ m?

    **Ejercicio 4 — Diseño real ⭐**
    Una ciudad requiere abastecer un sector a 65 m de altura con un caudal mínimo de 8 L/s y pérdidas estimadas de 12 m.
    Determina el diámetro adecuado y la potencia mínima de la bomba.
    *(Pista: velocidades entre 0.5 y 3 m/s son recomendables en tuberías de distribución.)*

    ---
    *Notebook desarrollado con Python · Marimo · Matplotlib*
    """)
    return


@app.cell(hide_code=True)
def _():
    import marimo as mo
    import numpy as np
    import matplotlib.pyplot as plt

    return mo, np, plt


if __name__ == "__main__":
    app.run()
