import streamlit as st
import numpy as np
import pandas as pd
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import math

# ==============================================================================
# BLOQUE 1: FUNCIONES DE CÁLCULO Y SIMULACIÓN
# ==============================================================================

def calcular_circuito_magnetico(N, I, l_m, S_m2, mu_r):
    mu_0 = 4 * math.pi * 1e-7  
    fmm = N * I
    reluctancia = l_m / (mu_0 * mu_r * S_m2)
    flujo = fmm / reluctancia if reluctancia > 0 else 0
    B = flujo / S_m2 if S_m2 > 0 else 0
    return fmm, reluctancia, flujo, B

def simular_histeresis(B_sat, H_c, a, H_max, H_offset=0):
    H_asc = np.linspace(-H_max + H_offset, H_max + H_offset, 500)
    H_desc = np.linspace(H_max + H_offset, -H_max + H_offset, 500)
    B_asc = B_sat * np.tanh((H_asc - H_c) / a)
    B_desc = B_sat * np.tanh((H_desc + H_c) / a)
    area_asc = np.trapz(B_asc, H_asc)
    area_desc = np.trapz(B_desc, H_desc)
    area_ciclo = np.abs(area_desc - area_asc)
    return H_asc, B_asc, H_desc, B_desc, area_ciclo

# ==============================================================================
# BLOQUE PRINCIPAL: INTERFAZ DE STREAMLIT (APP)
# ==============================================================================

def app():
    st.header("Principios Generales del Electromagnetismo")
    st.caption("Módulo interactivo para el análisis de campos, materiales magnéticos e inducción (Nivel Ingeniería).")

    tab_campo, tab_materiales, tab_circuitos = st.tabs([
        "1 - El Campo Magnético",
        "2 - Materiales y Pérdidas",
        "3 - Circuitos y Leyes"
    ])

    # --------------------------------------------------------------------------
    # PESTAÑA 1: CAMPO MAGNÉTICO (Biot-Savart y Ampère)
    # --------------------------------------------------------------------------
    with tab_campo:
        st.markdown("### El Campo Magnético y sus Fuentes")

        # =====================================================================
        # SECCIÓN 1: FUNDAMENTO TEÓRICO COMPLETO DE LA LEY DE AMPÈRE
        # =====================================================================
        with st.expander("📖 Fundamento Teórico Completo: Ley de Ampère", expanded=True):
            col_teoria1, col_teoria2 = st.columns([1.1, 1])

            with col_teoria1:
                st.markdown(r"""
                #### 1. Enunciado y Formulación Integral

                La **Ley de Ampère** (André-Marie Ampère, 1826) es una de las cuatro ecuaciones de Maxwell y establece
                la relación cuantitativa entre las **corrientes eléctricas** y el **campo magnético** que generan.

                > *«La circulación del vector intensidad de campo magnético $\vec{H}$ a lo largo de cualquier
                curva cerrada (amperiana) es igual a la corriente neta que atraviesa la superficie delimitada
                por dicha curva.»*

                $$\boxed{\oint_C \vec{H} \cdot d\vec{l} = I_{enc} = \iint_S \vec{J} \cdot d\vec{S}}$$

                Donde:
                - $\vec{H}$ — Intensidad de campo magnético [A/m]
                - $d\vec{l}$ — Elemento diferencial de longitud sobre la curva $C$
                - $I_{enc}$ — Corriente total encerrada por la curva
                - $\vec{J}$ — Densidad de corriente [A/m²]
                - $d\vec{S}$ — Elemento diferencial de superficie

                La **relación constitutiva** liga $\vec{B}$ con $\vec{H}$ a través de la permeabilidad del medio:

                $$\vec{B} = \mu \, \vec{H} = \mu_0 \, \mu_r \, \vec{H}$$

                con $\mu_0 = 4\pi \times 10^{-7}$ H/m (permeabilidad del vacío).

                ---

                #### 2. Forma Diferencial (Local)

                Mediante el teorema de Stokes, la forma integral se transforma en la **ecuación diferencial** (forma puntual):

                $$\boxed{\nabla \times \vec{H} = \vec{J}}$$

                Esto indica que las **corrientes de conducción** son las fuentes del rotacional del campo magnético.
                En cualquier punto donde no circule corriente ($\vec{J} = 0$), el campo $\vec{H}$ es irrotacional.
                """)

            with col_teoria2:
                st.markdown(r"""
                #### 3. Corrección de Maxwell (Corriente de Desplazamiento)

                En régimen variable (campos que cambian con el tiempo), Maxwell añadió la **corriente de
                desplazamiento** $\vec{J}_D$ para garantizar la continuidad de la ecuación:

                $$\oint_C \vec{H} \cdot d\vec{l} = I_{enc} + \frac{\partial}{\partial t}\iint_S \vec{D} \cdot d\vec{S}$$

                O en forma diferencial:

                $$\nabla \times \vec{H} = \vec{J} + \frac{\partial \vec{D}}{\partial t}$$

                Esta corrección es fundamental para explicar la **propagación de ondas electromagnéticas**
                y cierra las ecuaciones de Maxwell.

                ---

                #### 4. Aplicación Clásica: Conductor Rectilíneo Infinito

                Consideremos un conductor recto de longitud infinita por el que circula una corriente $I$.
                Por simetría cilíndrica, $\vec{H}$ es tangencial y constante sobre cualquier
                circunferencia concéntrica de radio $r$:

                $$H \cdot (2\pi r) = I \implies \boxed{H = \frac{I}{2\pi r}}$$

                Y la densidad de flujo magnético resulta:

                $$\boxed{B = \frac{\mu_0 \, I}{2\pi r}}$$

                **Dirección:** La regla de la mano derecha determina el sentido de $\vec{B}$: si el pulgar
                apunta en la dirección de $I$, los dedos curvados indican el sentido de las líneas de campo.

                ---

                #### 5. Importancia en Máquinas Eléctricas

                - Cálculo de la **FMM** en entrehierros y circuitos magnéticos.
                - Diseño de **bobinas**, **solenoides** y **electroimanes**.
                - Base de los **circuitos equivalentes magnéticos** (Ley de Hopkinson).
                - Determinación del **par electromagnético** en motores y generadores.
                """)

        st.markdown("---")

        # =====================================================================
        # SECCIÓN 2: ANIMACIÓN 2D INTERACTIVA — LEY DE AMPÈRE
        # =====================================================================
        st.markdown("""
        <div style="background-color: #0D1117; border-left: 4px solid #FCD34D; padding: 16px; border-radius: 6px; border: 1px solid #30363D; margin-bottom: 20px;">
            <h4 style="margin-top: 0; color: #FCD34D; font-size: 16px; margin-bottom: 8px;">🎬 Animación 2D — Ley de Ampère en Acción</h4>
            <p style="margin-bottom: 0; color: #C9D1D9; font-size: 14px;">Visualización interactiva del campo magnético generado por un conductor rectilíneo.
            Ajusta la corriente y el número de líneas de campo para explorar cómo varía la distribución del campo <b>H</b>.
            La animación muestra el avance de los vectores de campo sobre la trayectoria amperiana.</p>
        </div>
        """, unsafe_allow_html=True)

        col_anim_ctrl, col_anim_vis = st.columns([1, 2.8])

        with col_anim_ctrl:
            st.markdown("**⚙️ Parámetros de la Animación**")
            I_anim = st.slider("Corriente I (A)", 10, 500, 150, step=10, key="I_ampere_anim")
            n_field_lines = st.slider("Líneas de campo concéntricas", 3, 10, 6, key="n_lines_ampere")
            r_ampere = st.slider("Radio trayectoria amperiana (cm)", 3, 25, 10, key="r_ampere_loop")
            n_vectors = st.slider("Nº de vectores H sobre el lazo", 6, 24, 12, key="n_vec_ampere")
            sentido_I = st.radio("Sentido de la corriente", ["⊙ Sale del plano (hacia ti)", "⊗ Entra en el plano (alejándose)"], key="sentido_ampere")
            sale = "Sale" in sentido_I

            # Cálculos informativos
            mu_0_val = 4 * math.pi * 1e-7
            r_amp_m = r_ampere / 100.0
            H_en_lazo = I_anim / (2 * math.pi * r_amp_m)
            B_en_lazo = mu_0_val * H_en_lazo
            circulacion = H_en_lazo * 2 * math.pi * r_amp_m  # = I

            st.markdown("---")
            st.markdown("**📊 Resultados en la Trayectoria Amperiana**")
            st.metric("H en r = {} cm".format(r_ampere), f"{H_en_lazo:.2f} A/m")
            st.metric("B en r = {} cm".format(r_ampere), f"{B_en_lazo*1000:.4f} mT")
            st.metric("∮ H·dl (Circulación)", f"{circulacion:.1f} A")

            st.markdown("""
            <div style="background-color: #112211; border: 1px solid #2EB85C; border-radius: 6px; padding: 10px; margin-top: 8px;">
                <span style="color: #2EB85C; font-size: 13px;">✅ <b>Verificación:</b> ∮H·dl = I<sub>enc</sub> = {} A</span>
            </div>
            """.format(I_anim), unsafe_allow_html=True)

        with col_anim_vis:
            # =================================================================
            # GENERAR FRAMES DE LA ANIMACIÓN
            # =================================================================
            n_frames = 30
            fig_anim = go.Figure()

            # --- Colores y estilo ---
            color_conductor = "#FCD34D" if sale else "#FF6B6B"
            color_field_lines = "#00ADB5"
            color_ampere_loop = "#FF6B6B"
            color_vectors = "#FFFFFF"
            color_bg = "#0D1117"

            # --- Datos estáticos: Líneas de campo concéntricas ---
            theta_circle = np.linspace(0, 2 * np.pi, 120)
            radii = np.linspace(2, 28, n_field_lines)

            for k, r_fl in enumerate(radii):
                opacity_fl = max(0.08, 0.35 - k * 0.03)
                fig_anim.add_trace(go.Scatter(
                    x=r_fl * np.cos(theta_circle), y=r_fl * np.sin(theta_circle),
                    mode='lines', line=dict(color=color_field_lines, width=1.2, dash='dot'),
                    opacity=opacity_fl, showlegend=False, hoverinfo='skip'
                ))

            # --- Flechas de dirección sobre las líneas de campo (estáticas) ---
            for k, r_fl in enumerate(radii):
                n_arrows_on_line = max(3, 8 - k)
                for j in range(n_arrows_on_line):
                    angle_arrow = (2 * math.pi * j / n_arrows_on_line)
                    sign = 1 if sale else -1
                    ax = r_fl * math.cos(angle_arrow)
                    ay = r_fl * math.sin(angle_arrow)
                    # Tangent direction (perpendicular to radial, CCW if current exits)
                    dx = -sign * math.sin(angle_arrow) * 1.5
                    dy = sign * math.cos(angle_arrow) * 1.5
                    fig_anim.add_annotation(
                        x=ax + dx, y=ay + dy, ax=ax, ay=ay,
                        xref="x", yref="y", axref="x", ayref="y",
                        showarrow=True, arrowhead=2, arrowsize=1.2, arrowwidth=1.5,
                        arrowcolor=color_field_lines, opacity=max(0.15, 0.4 - k * 0.04)
                    )

            # --- Conductor en el centro (sección transversal) ---
            theta_cond = np.linspace(0, 2 * np.pi, 60)
            r_cond = 1.5
            fig_anim.add_trace(go.Scatter(
                x=r_cond * np.cos(theta_cond), y=r_cond * np.sin(theta_cond),
                fill='toself', fillcolor=color_conductor, line=dict(color='#FFFFFF', width=2),
                mode='lines', showlegend=False, hoverinfo='skip'
            ))
            # Símbolo de corriente: ⊙ (sale) o ⊗ (entra)
            if sale:
                # Punto central para ⊙
                fig_anim.add_trace(go.Scatter(
                    x=[0], y=[0], mode='markers',
                    marker=dict(size=10, color='#000000', symbol='circle'),
                    showlegend=False, hoverinfo='skip'
                ))
            else:
                # Cruz para ⊗
                fig_anim.add_trace(go.Scatter(
                    x=[-0.7, 0.7, None, -0.7, 0.7], y=[-0.7, 0.7, None, 0.7, -0.7],
                    mode='lines', line=dict(color='#000000', width=3),
                    showlegend=False, hoverinfo='skip'
                ))

            # --- Trayectoria Amperiana (círculo destacado) ---
            r_amp_plot = r_ampere  # en cm (el plot usa cm como unidad visual)
            fig_anim.add_trace(go.Scatter(
                x=r_amp_plot * np.cos(theta_circle), y=r_amp_plot * np.sin(theta_circle),
                mode='lines', line=dict(color=color_ampere_loop, width=2.5, dash='dash'),
                opacity=0.85, showlegend=False, hoverinfo='skip',
                name='Trayectoria Amperiana'
            ))

            # --- Etiqueta de la trayectoria amperiana ---
            fig_anim.add_annotation(
                x=r_amp_plot * math.cos(math.pi / 4) + 2,
                y=r_amp_plot * math.sin(math.pi / 4) + 2,
                text="<b>Trayectoria<br>Amperiana C</b>",
                showarrow=True,
                ax=r_amp_plot * math.cos(math.pi / 4),
                ay=r_amp_plot * math.sin(math.pi / 4),
                axref="x", ayref="y",
                arrowhead=2, arrowcolor=color_ampere_loop,
                font=dict(color=color_ampere_loop, size=11),
                bgcolor="rgba(13,17,23,0.8)", borderpad=4
            )

            # --- Etiqueta del radio ---
            fig_anim.add_trace(go.Scatter(
                x=[0, r_amp_plot * math.cos(-math.pi / 6)],
                y=[0, r_amp_plot * math.sin(-math.pi / 6)],
                mode='lines', line=dict(color='#888888', width=1, dash='dot'),
                showlegend=False, hoverinfo='skip'
            ))
            fig_anim.add_annotation(
                x=r_amp_plot * 0.5 * math.cos(-math.pi / 6) + 1,
                y=r_amp_plot * 0.5 * math.sin(-math.pi / 6) - 1.5,
                text=f"<b>r = {r_ampere} cm</b>",
                showarrow=False, font=dict(color='#AAAAAA', size=11),
                bgcolor="rgba(13,17,23,0.8)", borderpad=3
            )

            # =================================================================
            # FRAMES DE ANIMACIÓN: Vectores H rotando sobre la trayectoria
            # =================================================================
            frames = []
            sign = 1 if sale else -1
            vec_length = min(3.5, 1.0 + I_anim / 100.0)  # Proporcional a I

            for f_idx in range(n_frames):
                offset_angle = sign * (2 * math.pi * f_idx / n_frames)
                frame_data = []

                # Vectores H tangenciales sobre la trayectoria amperiana
                vec_x = []
                vec_y = []
                for v in range(n_vectors):
                    theta_v = (2 * math.pi * v / n_vectors) + offset_angle
                    # Base del vector
                    bx = r_amp_plot * math.cos(theta_v)
                    by = r_amp_plot * math.sin(theta_v)
                    # Dirección tangencial
                    tx = -sign * math.sin(theta_v) * vec_length
                    ty = sign * math.cos(theta_v) * vec_length
                    # Dibujar como segmento
                    vec_x.extend([bx, bx + tx, None])
                    vec_y.extend([by, by + ty, None])

                frame_data.append(go.Scatter(
                    x=vec_x, y=vec_y,
                    mode='lines', line=dict(color='#FFDD57', width=2.5),
                    showlegend=False, hoverinfo='skip'
                ))

                # Puntas de flechas (marcadores al final del vector)
                arrow_x = []
                arrow_y = []
                for v in range(n_vectors):
                    theta_v = (2 * math.pi * v / n_vectors) + offset_angle
                    bx = r_amp_plot * math.cos(theta_v)
                    by = r_amp_plot * math.sin(theta_v)
                    tx = -sign * math.sin(theta_v) * vec_length
                    ty = sign * math.cos(theta_v) * vec_length
                    arrow_x.append(bx + tx)
                    arrow_y.append(by + ty)

                frame_data.append(go.Scatter(
                    x=arrow_x, y=arrow_y,
                    mode='markers',
                    marker=dict(size=7, color='#FFDD57', symbol='arrow',
                                angle=[math.degrees(math.atan2(
                                    sign * math.cos((2 * math.pi * v / n_vectors) + offset_angle),
                                    -sign * math.sin((2 * math.pi * v / n_vectors) + offset_angle)
                                )) - 90 for v in range(n_vectors)]),
                    showlegend=False, hoverinfo='skip'
                ))

                # dl elements (small segments on the Amperian path)
                dl_x = []
                dl_y = []
                for v in range(n_vectors):
                    theta_v = (2 * math.pi * v / n_vectors) + offset_angle
                    # Pequeño segmento dl centrado
                    dl_half = math.pi / n_vectors * 0.5
                    t1 = theta_v - dl_half
                    t2 = theta_v + dl_half
                    dl_x.extend([r_amp_plot * math.cos(t1), r_amp_plot * math.cos(t2), None])
                    dl_y.extend([r_amp_plot * math.sin(t1), r_amp_plot * math.sin(t2), None])

                frame_data.append(go.Scatter(
                    x=dl_x, y=dl_y,
                    mode='lines', line=dict(color='#FF6B6B', width=4),
                    opacity=0.7, showlegend=False, hoverinfo='skip'
                ))

                frames.append(go.Frame(data=frame_data, name=str(f_idx)))

            # Añadir primer frame como datos iniciales
            if frames:
                for trace in frames[0].data:
                    fig_anim.add_trace(trace)

            fig_anim.frames = frames

            # --- Layout de la animación ---
            axis_range = 33
            fig_anim.update_layout(
                title=dict(
                    text=f"<b>Ley de Ampère</b> — Campo H alrededor de un conductor (I = {I_anim} A)",
                    font=dict(size=15, color='#FAFAFA')
                ),
                xaxis=dict(
                    range=[-axis_range, axis_range], scaleanchor="y", scaleratio=1,
                    showgrid=False, zeroline=False, showticklabels=False, visible=False
                ),
                yaxis=dict(
                    range=[-axis_range, axis_range],
                    showgrid=False, zeroline=False, showticklabels=False, visible=False
                ),
                plot_bgcolor=color_bg, paper_bgcolor=color_bg,
                height=550, margin=dict(l=10, r=10, t=50, b=10),
                showlegend=False,
                updatemenus=[dict(
                    type="buttons",
                    showactive=False,
                    x=0.02, y=-0.02,
                    xanchor="left", yanchor="top",
                    buttons=[
                        dict(
                            label="▶ Animar",
                            method="animate",
                            args=[None, dict(
                                frame=dict(duration=80, redraw=True),
                                fromcurrent=True, mode="immediate",
                                transition=dict(duration=30)
                            )]
                        ),
                        dict(
                            label="⏸ Pausar",
                            method="animate",
                            args=[[None], dict(
                                frame=dict(duration=0, redraw=False),
                                mode="immediate",
                                transition=dict(duration=0)
                            )]
                        )
                    ],
                    font=dict(color="#FAFAFA", size=12),
                    bgcolor="#1E1E2E",
                    bordercolor="#30363D",
                    borderwidth=1
                )],
                # Leyenda visual con anotaciones
                annotations=[
                    dict(x=0.01, y=0.99, xref="paper", yref="paper",
                         text="<b style='color:#FFDD57'>━━</b> Vectores H (tangenciales)",
                         showarrow=False, font=dict(size=11, color="#AAAAAA"),
                         bgcolor="rgba(13,17,23,0.85)", borderpad=4, xanchor="left"),
                    dict(x=0.01, y=0.93, xref="paper", yref="paper",
                         text=f"<b style='color:{color_field_lines}'>····</b> Líneas de campo B",
                         showarrow=False, font=dict(size=11, color="#AAAAAA"),
                         bgcolor="rgba(13,17,23,0.85)", borderpad=4, xanchor="left"),
                    dict(x=0.01, y=0.87, xref="paper", yref="paper",
                         text=f"<b style='color:{color_ampere_loop}'>- -</b> Trayectoria Amperiana C",
                         showarrow=False, font=dict(size=11, color="#AAAAAA"),
                         bgcolor="rgba(13,17,23,0.85)", borderpad=4, xanchor="left"),
                    dict(x=0.01, y=0.81, xref="paper", yref="paper",
                         text=f"<b style='color:#FF6B6B'>━━</b> Elementos dl",
                         showarrow=False, font=dict(size=11, color="#AAAAAA"),
                         bgcolor="rgba(13,17,23,0.85)", borderpad=4, xanchor="left"),
                    # Ecuación principal
                    dict(x=0.99, y=0.02, xref="paper", yref="paper",
                         text="<b>∮ H · dl = I<sub>enc</sub></b>",
                         showarrow=False, font=dict(size=18, color="#FCD34D"),
                         bgcolor="rgba(13,17,23,0.9)", bordercolor="#FCD34D",
                         borderwidth=1, borderpad=8, xanchor="right"),
                ]
            )

            st.plotly_chart(fig_anim, use_container_width=True, key="ampere_animation")

        # =====================================================================
        # SECCIÓN 3: GRÁFICA CLÁSICA B vs DISTANCIA (preservada)
        # =====================================================================
        st.markdown("---")
        st.markdown("#### Atenuación de B con la Distancia")
        st.markdown(r"""
        La densidad de flujo magnético $B$ generada por un conductor rectilíneo decae de forma hiperbólica,
        siendo inversamente proporcional a la distancia radial $r$ al centro del conductor:

        $$\boxed{B(r) = \frac{\mu_0 \cdot I}{2\pi r}}$$

        Esto implica que la **mayor parte de la energía magnética** se concentra en la **vecindad inmediata**
        del conductor. A medida que nos alejamos radialmente, el campo experimenta una atenuación rápida,
        lo que demuestra la importancia del blindaje magnético y el diseño compacto en máquinas eléctricas y transformadores.
        """)

    # --------------------------------------------------------------------------
    # PESTAÑA 2: MATERIALES MAGNÉTICOS, PÉRDIDAS Y TEMPERATURA
    # --------------------------------------------------------------------------
    with tab_materiales:
        st.markdown("### Histéresis, Pérdidas en el Hierro y Calentamiento")
        with st.expander("📖 Base Teórica: Propiedades Magnéticas, Pérdidas y Modelo Térmico", expanded=False):
            st.markdown(r"""
            **1. Ciclo de Histéresis y Curva de Magnetización:**
            Los materiales ferromagnéticos presentan una relación no lineal entre $B$ y $H$. Al aplicar un campo alterno, la magnetización se retrasa respecto al campo inductor.
            - **Inducción Remanente ($B_r$):** Magnetización residual al retirar la excitación ($H=0$).
            - **Fuerza Coercitiva ($H_c$):** Campo necesario para anular la magnetización ($B=0$).

            **2. Excitación AC y Generación del Campo:**
            Partiendo de la Ley de Ampère para un circuito de longitud media $l_{eq}$:
            $$ \oint \vec{H} \cdot d\vec{l} = N \cdot I \implies H(t) = \frac{N \cdot I_{max}}{l_{eq}} \sin(2\pi f t) $$

            **3. Pérdidas en el Hierro (Núcleo):**
            Las pérdidas totales en el núcleo ($P_{Fe}$) se componen de:
            - **Histéresis ($P_H$):** Proporcionales al área del ciclo y la frecuencia ($f$). $P_H = k_h \cdot f \cdot B_{max}^n$.
            - **Corrientes de Foucault ($P_F$):** Debidas a corrientes inducidas en el núcleo. $P_F = k_f \cdot f^2 \cdot B_{max}^2$.

            **4. Modelo Térmico Estacionario:**
            $$ T_{final} = T_{amb} + (P_{tot} \cdot R_{th}) $$
            """)

        import streamlit.components.v1 as components
        hyst_html = r"""<!DOCTYPE html>
<html><head><meta charset="UTF-8">
<style>
*{margin:0;padding:0;box-sizing:border-box;}
html,body{background:#0D1117;overflow:hidden;width:100%;height:100%;font-family:'Segoe UI',system-ui,-apple-system,sans-serif;}
canvas{display:block;width:100%;height:100%;}
</style>
</head><body>
<canvas id="C"></canvas>
<script>
(function(){
const cv=document.getElementById('C'),c=cv.getContext('2d');
const MATS=[
{name:'Acero al Silicio M4',Bsat:1.65,Hc:20,a:40,kf:1.5,col:'#F59E0B'},
{name:'Acero Estructural (Macizo)',Bsat:1.4,Hc:250,a:200,kf:25.0,col:'#EF4444'},
{name:'Ferrita Mn-Zn (Electrónica)',Bsat:0.45,Hc:12,a:18,kf:0.3,col:'#8B5CF6'},
{name:'Hierro Puro (Referencia)',Bsat:2.1,Hc:80,a:90,kf:5.0,col:'#10B981'},
{name:'Acero M19 (Motores)',Bsat:1.56,Hc:40,a:55,kf:2.2,col:'#3B82F6'},
{name:'Permalloy 80 (Alta perm.)',Bsat:0.75,Hc:2,a:8,kf:0.8,col:'#EC4899'}
];
let mi=0;
let sl=[
{lb:'H max (A/m)',mn:50,mx:1500,v:400,st:10},
{lb:'Bias DC (A/m)',mn:-500,mx:500,v:0,st:10},
{lb:'Frecuencia (Hz)',mn:10,mx:400,v:50,st:5},
{lb:'Vol. nucleo (dm3)',mn:1,mx:500,v:10,st:1},
{lb:'Rth (C/W) x100',mn:1,mx:200,v:15,st:1}
];
let drag=-1,hov=-1,W=0,H=0,dpr=1,aT=0,paused=false;
let Z={},mBtns=[];

function resize(){
  dpr=window.devicePixelRatio||1;
  W=document.documentElement.clientWidth||window.innerWidth||cv.clientWidth;
  H=680;
  if(W<10){setTimeout(resize,100);return;}
  cv.width=W*dpr;cv.height=H*dpr;
  cv.style.width=W+'px';cv.style.height=H+'px';
  c.setTransform(dpr,0,0,dpr,0,0);
  var p=16,cW=Math.min(250,W*0.21);
  Z.ct={x:p,y:56,w:cW,h:H-70};
  Z.ch={x:cW+p*2,y:56,w:W-cW-p*3-210,h:H-110};
  Z.pn={x:W-200,y:56,w:188,h:H-70};
}
window.addEventListener('resize',resize);

function loop(m,Hm,Ho){
  var N=300,Ha=[],Ba=[],Hd=[],Bd=[];
  for(var i=0;i<N;i++){
    var t=i/(N-1);
    var ha=(-Hm+Ho)+2*Hm*t,hd=(Hm+Ho)-2*Hm*t;
    Ha.push(ha);Ba.push(m.Bsat*Math.tanh((ha-m.Hc)/m.a));
    Hd.push(hd);Bd.push(m.Bsat*Math.tanh((hd+m.Hc)/m.a));
  }
  var aA=0,aD=0;
  for(var i=0;i<N-1;i++){
    aA+=.5*(Ba[i]+Ba[i+1])*(Ha[i+1]-Ha[i]);
    aD+=.5*(Bd[i]+Bd[i+1])*(Hd[i+1]-Hd[i]);
  }
  var area=Math.abs(aD-aA);
  var BrA=m.Bsat*Math.tanh((Ho-m.Hc)/m.a);
  var BrD=m.Bsat*Math.tanh((Ho+m.Hc)/m.a);
  var Br=.5*(Math.abs(BrD)+Math.abs(BrA));
  var Bx=0;for(var i=0;i<N;i++){Bx=Math.max(Bx,Math.abs(Ba[i]),Math.abs(Bd[i]));}
  return{Ha:Ha,Ba:Ba,Hd:Hd,Bd:Bd,area:area,Br:Br,Bx:Bx,BrA:BrA,BrD:BrD};
}

function rr(x,y,w,h,r,f,s){
  c.beginPath();c.moveTo(x+r,y);c.lineTo(x+w-r,y);c.quadraticCurveTo(x+w,y,x+w,y+r);
  c.lineTo(x+w,y+h-r);c.quadraticCurveTo(x+w,y+h,x+w-r,y+h);c.lineTo(x+r,y+h);
  c.quadraticCurveTo(x,y+h,x,y+h-r);c.lineTo(x,y+r);c.quadraticCurveTo(x,y,x+r,y);
  c.closePath();if(f){c.fillStyle=f;c.fill();}
  if(s){c.strokeStyle=s;c.lineWidth=1;c.stroke();}
}

function dSlider(s,idx,x,y,w){
  var h=7,kr=6,rat=(s.v-s.mn)/(s.mx-s.mn),kx=x+rat*w;
  var ih=(hov===idx),id=(drag===idx);
  c.fillStyle=ih?'#E5E7EB':'#9CA3AF';c.font='11px "Segoe UI"';c.textAlign='left';
  c.fillText(s.lb,x,y-9);
  var dv=s.v;
  if(idx===3)dv=(s.v/1000).toFixed(3)+' m3';
  else if(idx===4)dv=(s.v/100).toFixed(2)+' C/W';
  else dv=''+s.v;
  c.textAlign='right';c.fillStyle='#FCD34D';c.font='bold 11px "Segoe UI"';
  c.fillText(dv,x+w,y-9);
  rr(x,y-h/2,w,h,3,'#1E293B','#334155');
  var g=c.createLinearGradient(x,0,x+w,0);
  g.addColorStop(0,'#0EA5E9');g.addColorStop(1,'#6366F1');
  if(rat>0)rr(x,y-h/2,Math.max(4,rat*w),h,3,g,null);
  c.beginPath();c.arc(kx,y,id?kr+2:kr,0,Math.PI*2);
  c.fillStyle=id?'#FFF':'#E5E7EB';c.fill();
  c.strokeStyle='#6366F1';c.lineWidth=2;c.stroke();
  s._x=x;s._y=y;s._w=w;s._kr=kr+6;
}

function dMat(x,y,w){
  c.fillStyle='#C9D1D9';c.font='bold 11px "Segoe UI"';c.textAlign='left';
  c.fillText('Material del Nucleo',x,y);
  mBtns=[];
  var bh=21,gap=2;
  for(var i=0;i<MATS.length;i++){
    var by=y+8+i*(bh+gap),sel=(i===mi);
    rr(x,by,w,bh,4,sel?'#1E293B':'#0D1117',sel?MATS[i].col:'#30363D');
    c.fillStyle=sel?MATS[i].col:'#8B949E';c.font=(sel?'bold ':'')+' 10px "Segoe UI"';
    c.textAlign='left';c.fillText(MATS[i].name,x+7,by+14);
    mBtns.push({x:x,y:by,w:w,h:bh,i:i});
  }
  return y+8+MATS.length*(bh+gap)+6;
}

function dChart(z,lp,m){
  var pl=52,pr=16,pt=38,pb=36;
  var x0=z.x+pl,y0=z.y+pt,cw=z.w-pl-pr,ch=z.h-pt-pb;
  rr(z.x,z.y,z.w,z.h,8,'#0D1117','#21262D');
  c.fillStyle='#E5E7EB';c.font='bold 14px "Segoe UI"';c.textAlign='center';
  c.fillText('Ciclo de Histeresis B-H',z.x+z.w/2,z.y+20);
  c.fillStyle='#6B7280';c.font='11px "Segoe UI"';
  c.fillText(m.name,z.x+z.w/2,z.y+34);
  var Hax=sl[0].v+Math.abs(sl[1].v)+50;
  var Bax=Math.min(m.Bsat*1.35,2.5);
  function mH(h){return x0+(h+Hax)/(2*Hax)*cw;}
  function mB(b){return y0+ch-(b+Bax)/(2*Bax)*ch;}
  c.strokeStyle='#1E293B';c.lineWidth=.5;
  for(var i=0;i<=8;i++){
    var hv=-Hax+i*2*Hax/8,px=mH(hv);
    c.beginPath();c.moveTo(px,y0);c.lineTo(px,y0+ch);c.stroke();
    c.fillStyle='#4B5563';c.font='9px "Segoe UI"';c.textAlign='center';
    c.fillText(Math.round(hv),px,y0+ch+13);
  }
  for(var i=0;i<=6;i++){
    var bv=-Bax+i*2*Bax/6,py=mB(bv);
    c.beginPath();c.moveTo(x0,py);c.lineTo(x0+cw,py);c.stroke();
    c.fillStyle='#4B5563';c.font='9px "Segoe UI"';c.textAlign='right';
    c.fillText(bv.toFixed(2),x0-5,py+3);
  }
  c.strokeStyle='#4B5563';c.lineWidth=1;
  c.beginPath();c.moveTo(mH(0),y0);c.lineTo(mH(0),y0+ch);c.stroke();
  c.beginPath();c.moveTo(x0,mB(0));c.lineTo(x0+cw,mB(0));c.stroke();
  c.fillStyle='#9CA3AF';c.font='11px "Segoe UI"';c.textAlign='center';
  c.fillText('H (A/m)',z.x+z.w/2,z.y+z.h-2);
  c.save();c.translate(z.x+10,z.y+z.h/2);c.rotate(-Math.PI/2);
  c.fillText('B (T)',0,0);c.restore();
  // Fill loop area
  c.save();c.beginPath();
  for(var i=0;i<lp.Ha.length;i++){var px=mH(lp.Ha[i]),py=mB(lp.Ba[i]);i===0?c.moveTo(px,py):c.lineTo(px,py);}
  for(var i=0;i<lp.Hd.length;i++){c.lineTo(mH(lp.Hd[i]),mB(lp.Bd[i]));}
  c.closePath();c.fillStyle='rgba(245,158,11,0.07)';c.fill();c.restore();
  // Ascending
  c.beginPath();
  for(var i=0;i<lp.Ha.length;i++){var px=mH(lp.Ha[i]),py=mB(lp.Ba[i]);i===0?c.moveTo(px,py):c.lineTo(px,py);}
  var ga=c.createLinearGradient(x0,y0+ch,x0,y0);
  ga.addColorStop(0,'#F59E0B');ga.addColorStop(1,'#FBBF24');
  c.strokeStyle=ga;c.lineWidth=2.5;c.stroke();
  // Descending
  c.beginPath();
  for(var i=0;i<lp.Hd.length;i++){var px=mH(lp.Hd[i]),py=mB(lp.Bd[i]);i===0?c.moveTo(px,py):c.lineTo(px,py);}
  var gd=c.createLinearGradient(x0,y0+ch,x0,y0);
  gd.addColorStop(0,'#06B6D4');gd.addColorStop(1,'#22D3EE');
  c.strokeStyle=gd;c.lineWidth=2.5;c.stroke();
  // Animated dot
  var tot=lp.Ha.length+lp.Hd.length;
  var di=Math.floor(aT*tot)%tot;
  var dx,dy;
  if(di<lp.Ha.length){dx=mH(lp.Ha[di]);dy=mB(lp.Ba[di]);}
  else{var j=di-lp.Ha.length;dx=mH(lp.Hd[j]);dy=mB(lp.Bd[j]);}
  var gl=c.createRadialGradient(dx,dy,0,dx,dy,14);
  gl.addColorStop(0,'rgba(255,255,255,0.5)');gl.addColorStop(1,'rgba(255,255,255,0)');
  c.fillStyle=gl;c.fillRect(dx-14,dy-14,28,28);
  c.beginPath();c.arc(dx,dy,5,0,Math.PI*2);c.fillStyle='#FFF';c.fill();
  c.strokeStyle='#FCD34D';c.lineWidth=2;c.stroke();
  // Br annotations
  var Ho=sl[1].v;
  var brPx=mH(Ho),brPyD=mB(lp.BrD),brPyA=mB(lp.BrA);
  c.beginPath();c.arc(brPx,brPyD,4,0,Math.PI*2);c.fillStyle='#10B981';c.fill();
  c.font='bold 10px "Segoe UI"';c.textAlign='left';
  c.fillText('Br='+lp.BrD.toFixed(2)+' T',brPx+8,brPyD-4);
  c.beginPath();c.arc(brPx,brPyA,4,0,Math.PI*2);c.fillStyle='#10B981';c.fill();
  c.fillText('Br='+lp.BrA.toFixed(2)+' T',brPx+8,brPyA+12);
  // Hc points
  var HcA=m.Hc+Ho,HcD=-m.Hc+Ho;
  if(Math.abs(HcA)<Hax){
    c.beginPath();c.arc(mH(HcA),mB(0),4,0,Math.PI*2);c.fillStyle='#EF4444';c.fill();
    c.font='bold 10px "Segoe UI"';c.textAlign='center';c.fillText('Hc',mH(HcA),mB(0)+16);
  }
  if(Math.abs(HcD)<Hax){
    c.beginPath();c.arc(mH(HcD),mB(0),4,0,Math.PI*2);c.fillStyle='#EF4444';c.fill();
    c.font='bold 10px "Segoe UI"';c.textAlign='center';c.fillText('-Hc',mH(HcD),mB(0)+16);
  }
  // Bsat lines
  c.setLineDash([4,4]);c.strokeStyle='rgba(139,92,246,0.4)';c.lineWidth=1;
  c.beginPath();c.moveTo(x0,mB(m.Bsat));c.lineTo(x0+cw,mB(m.Bsat));c.stroke();
  c.beginPath();c.moveTo(x0,mB(-m.Bsat));c.lineTo(x0+cw,mB(-m.Bsat));c.stroke();
  c.setLineDash([]);
  c.fillStyle='#8B5CF6';c.font='9px "Segoe UI"';c.textAlign='left';
  c.fillText('Bsat='+m.Bsat.toFixed(2)+' T',x0+4,mB(m.Bsat)-4);
  c.fillText('-Bsat',x0+4,mB(-m.Bsat)+12);
  // DC bias line
  if(Ho!==0){
    c.setLineDash([3,5]);c.strokeStyle='rgba(239,68,68,0.35)';c.lineWidth=1;
    c.beginPath();c.moveTo(mH(Ho),y0);c.lineTo(mH(Ho),y0+ch);c.stroke();
    c.setLineDash([]);
    c.fillStyle='#EF4444';c.font='9px "Segoe UI"';c.textAlign='center';
    c.fillText('DC Bias',mH(Ho),y0-4);
  }
  // Legend
  var lx=x0+8,ly=y0+10;
  c.fillStyle='#F59E0B';c.fillRect(lx,ly,14,3);
  c.fillStyle='#9CA3AF';c.font='10px "Segoe UI"';c.textAlign='left';
  c.fillText('Magnetizacion (asc.)',lx+18,ly+4);
  c.fillStyle='#06B6D4';c.fillRect(lx,ly+14,14,3);
  c.fillStyle='#9CA3AF';c.fillText('Desmagnetizacion (desc.)',lx+18,ly+18);
}

function dPanel(z,lp,m){
  rr(z.x,z.y,z.w,z.h,8,'#0D1117','#21262D');
  var px=z.x+10,py=z.y+14;
  c.fillStyle='#E5E7EB';c.font='bold 12px "Segoe UI"';c.textAlign='left';
  c.fillText('Panel de Ingenieria',px,py);py+=6;
  var Hm=sl[0].v,Ho=sl[1].v,fr=sl[2].v;
  var Vn=sl[3].v/1000,Rt=sl[4].v/100;
  var Ph=lp.area*fr*Vn;
  var Pf=m.kf*(fr*fr)*(lp.Bx*lp.Bx)*Vn;
  var Pt=Ph+Pf;
  var Ta=40,dT=Pt*Rt,Tf=Ta+dT;
  var mu=(lp.Bx/(4*Math.PI*1e-7*Hm))||0;
  function mc(lb,vl,un,cl,yp){
    rr(px,yp,z.w-20,32,4,'#161B22','#30363D');
    c.fillStyle='#8B949E';c.font='10px "Segoe UI"';c.textAlign='left';
    c.fillText(lb,px+6,yp+12);
    c.fillStyle=cl;c.font='bold 12px "Segoe UI"';c.textAlign='right';
    c.fillText(vl+' '+un,px+z.w-28,yp+25);
    return yp+36;
  }
  py+=8;
  py=mc('Area del Ciclo',lp.area.toFixed(1),'J/m3','#F59E0B',py);
  py=mc('Bmax Real',lp.Bx.toFixed(3),'T','#06B6D4',py);
  py=mc('Br (Remanente)',lp.Br.toFixed(3),'T','#10B981',py);
  py=mc('ur efectiva',mu.toFixed(0),'','#8B5CF6',py);
  py+=6;
  c.fillStyle='#E5E7EB';c.font='bold 11px "Segoe UI"';c.textAlign='left';
  c.fillText('Desglose de Perdidas',px,py);py+=8;
  var bW=z.w-20,bH=15,mP=Math.max(Pt,1);
  rr(px,py,bW,bH,3,'#1E293B','#30363D');
  rr(px,py,Math.max(2,(Ph/mP)*bW),bH,3,'#F59E0B',null);
  c.fillStyle='#000';c.font='bold 9px "Segoe UI"';c.textAlign='left';
  c.fillText('Histeresis: '+Ph.toFixed(1)+' W',px+4,py+11);
  py+=bH+3;
  rr(px,py,bW,bH,3,'#1E293B','#30363D');
  rr(px,py,Math.max(2,(Pf/mP)*bW),bH,3,'#3B82F6',null);
  c.fillStyle='#FFF';c.font='bold 9px "Segoe UI"';c.textAlign='left';
  c.fillText('Foucault: '+Pf.toFixed(1)+' W',px+4,py+11);
  py+=bH+3;
  rr(px,py,bW,bH,3,'#1E293B',null);
  rr(px,py,bW,bH,3,null,'#EF4444');
  c.fillStyle='#EF4444';c.font='bold 9px "Segoe UI"';c.textAlign='center';
  c.fillText('TOTAL: '+Pt.toFixed(1)+' W',px+bW/2,py+11);
  py+=bH+12;
  c.fillStyle='#E5E7EB';c.font='bold 11px "Segoe UI"';c.textAlign='left';
  c.fillText('Modelo Termico',px,py);py+=10;
  rr(px,py,z.w-20,66,6,'#161B22','#30363D');
  var gx=px+8,gy=py+10,gw=z.w-36,gh=12;
  rr(gx,gy,gw,gh,4,'#1E293B',null);
  var tG=c.createLinearGradient(gx,0,gx+gw,0);
  tG.addColorStop(0,'#10B981');tG.addColorStop(0.4,'#F59E0B');tG.addColorStop(0.7,'#EF4444');tG.addColorStop(1,'#7F1D1D');
  var tR=Math.min(1,Tf/200);
  c.save();c.beginPath();c.rect(gx,gy,gw*tR,gh);c.clip();
  rr(gx,gy,gw,gh,4,tG,null);c.restore();
  rr(gx,gy,gw,gh,4,null,'#4B5563');
  var tc=Tf<80?'#10B981':Tf<130?'#F59E0B':'#EF4444';
  c.fillStyle=tc;c.font='bold 17px "Segoe UI"';c.textAlign='center';
  c.fillText(Tf.toFixed(1)+' C',gx+gw/2,gy+gh+20);
  c.fillStyle='#6B7280';c.font='10px "Segoe UI"';
  c.fillText('Tamb=40C | dT='+dT.toFixed(1)+'C',gx+gw/2,gy+gh+34);
  if(Tf>155){py+=72;rr(px,py,z.w-20,20,4,'rgba(239,68,68,0.15)','#EF4444');c.fillStyle='#EF4444';c.font='bold 10px "Segoe UI"';c.textAlign='center';c.fillText('TEMP. CRITICA',px+(z.w-20)/2,py+14);}
  else if(Tf>120){py+=72;rr(px,py,z.w-20,20,4,'rgba(245,158,11,0.15)','#F59E0B');c.fillStyle='#F59E0B';c.font='bold 10px "Segoe UI"';c.textAlign='center';c.fillText('Sobretemperatura',px+(z.w-20)/2,py+14);}
  py+=28;
  if(py+40<z.y+z.h){
    c.fillStyle='#4B5563';c.font='italic 9px "Segoe UI"';c.textAlign='left';
    c.fillText('P_H = Area x f x V',px+4,py);py+=12;
    c.fillText('P_F = kf x f2 x B2max x V',px+4,py);py+=12;
    c.fillText('T = Tamb + Ptot x Rth',px+4,py);
  }
}

function draw(){
  if(W<10){
    requestAnimationFrame(draw);
    return;
  }
  c.clearRect(0,0,W,H);
  c.fillStyle='#0D1117';c.fillRect(0,0,W,H);
  rr(0,0,W,H,10,null,'#21262D');
  // Title
  c.fillStyle='#E5E7EB';c.font='bold 15px "Segoe UI"';c.textAlign='left';
  c.fillText('Simulador de Ciclo de Histeresis y Perdidas en el Hierro',16,26);
  c.fillStyle='#6B7280';c.font='11px "Segoe UI"';
  c.fillText('B = Bsat tanh((H +/- Hc) / a)  |  Analisis de perdidas y termico',16,42);
  // Play/Pause
  var bx=W-85,by=6,bw=68,bh=26;
  rr(bx,by,bw,bh,6,paused?'#1E293B':'#065F46',paused?'#6B7280':'#10B981');
  c.fillStyle=paused?'#9CA3AF':'#10B981';c.font='bold 11px "Segoe UI"';c.textAlign='center';
  c.fillText(paused?'Play':'Pausa',bx+bw/2,by+17);
  Z.pb={x:bx,y:by,w:bw,h:bh};
  // Controls
  var cy=Z.ct.y+6;
  cy=dMat(Z.ct.x,cy,Z.ct.w);cy+=4;
  for(var i=0;i<sl.length;i++){dSlider(sl[i],i,Z.ct.x,cy,Z.ct.w);cy+=40;}
  // Compute
  var m=MATS[mi];
  var lp=loop(m,sl[0].v,sl[1].v);
  dChart(Z.ch,lp,m);
  dPanel(Z.pn,lp,m);
  if(!paused){aT+=0.003;if(aT>=1)aT=0;}
  requestAnimationFrame(draw);
}

function gp(e){var r=cv.getBoundingClientRect();return{x:e.clientX-r.left,y:e.clientY-r.top};}

cv.addEventListener('mousedown',function(e){
  var p=gp(e);
  if(Z.pb&&p.x>=Z.pb.x&&p.x<=Z.pb.x+Z.pb.w&&p.y>=Z.pb.y&&p.y<=Z.pb.y+Z.pb.h){paused=!paused;return;}
  for(var b=0;b<mBtns.length;b++){var bt=mBtns[b];if(p.x>=bt.x&&p.x<=bt.x+bt.w&&p.y>=bt.y&&p.y<=bt.y+bt.h){mi=bt.i;return;}}
  for(var i=0;i<sl.length;i++){
    var s=sl[i];if(!s._x)continue;
    var rat=(s.v-s.mn)/(s.mx-s.mn),kx=s._x+rat*s._w;
    if(Math.sqrt((p.x-kx)*(p.x-kx)+(p.y-s._y)*(p.y-s._y))<s._kr+4){drag=i;return;}
    if(p.x>=s._x&&p.x<=s._x+s._w&&Math.abs(p.y-s._y)<12){
      var nv=s.mn+(p.x-s._x)/s._w*(s.mx-s.mn);
      s.v=Math.round(nv/s.st)*s.st;s.v=Math.max(s.mn,Math.min(s.mx,s.v));drag=i;return;
    }
  }
});
cv.addEventListener('mousemove',function(e){
  var p=gp(e);
  if(drag>=0){var s=sl[drag];var nv=s.mn+(p.x-s._x)/s._w*(s.mx-s.mn);s.v=Math.round(nv/s.st)*s.st;s.v=Math.max(s.mn,Math.min(s.mx,s.v));return;}
  hov=-1;
  for(var i=0;i<sl.length;i++){var s=sl[i];if(!s._x)continue;if(p.x>=s._x&&p.x<=s._x+s._w&&Math.abs(p.y-s._y)<14){hov=i;cv.style.cursor='pointer';return;}}
  for(var b=0;b<mBtns.length;b++){var bt=mBtns[b];if(p.x>=bt.x&&p.x<=bt.x+bt.w&&p.y>=bt.y&&p.y<=bt.y+bt.h){cv.style.cursor='pointer';return;}}
  if(Z.pb&&p.x>=Z.pb.x&&p.x<=Z.pb.x+Z.pb.w&&p.y>=Z.pb.y&&p.y<=Z.pb.y+Z.pb.h){cv.style.cursor='pointer';return;}
  cv.style.cursor='default';
});
cv.addEventListener('mouseup',function(){drag=-1;});
cv.addEventListener('mouseleave',function(){drag=-1;hov=-1;});
cv.addEventListener('touchstart',function(e){e.preventDefault();var t=e.touches[0];cv.dispatchEvent(new MouseEvent('mousedown',{clientX:t.clientX,clientY:t.clientY}));},{passive:false});
cv.addEventListener('touchmove',function(e){e.preventDefault();var t=e.touches[0];cv.dispatchEvent(new MouseEvent('mousemove',{clientX:t.clientX,clientY:t.clientY}));},{passive:false});
cv.addEventListener('touchend',function(){cv.dispatchEvent(new MouseEvent('mouseup'));});

resize();
requestAnimationFrame(draw);
})();
</script>
</body></html>"""
        components.html(hyst_html, height=700, scrolling=False)

    # --------------------------------------------------------------------------
    # PESTAÑA 3: CIRCUITOS Y LEYES
    # --------------------------------------------------------------------------
    with tab_circuitos:
        st.markdown("### Siemens M-CAD - Simulador de Circuitos Magnéticos")
        st.markdown("""
        Visualizador y resolvedor de circuitos magnéticos interactivo. 
        Añade ramas de hierro, bobinas excitadoras o entrehierros de aire haciendo clic y seleccionando las herramientas en el panel de la izquierda. 
        Ajusta parámetros geométricos y magnéticos interactuando con el panel de propiedades a la derecha.
        """)

        import streamlit.components.v1 as components
        circuit_html = r"""<!DOCTYPE html>
<html><head><meta charset="UTF-8">
<style>
*{margin:0;padding:0;box-sizing:border-box;}
html,body{background:#0D1117;overflow:hidden;width:100%;height:100%;font-family:'Segoe UI',system-ui,-apple-system,sans-serif;}
canvas{display:block;width:100%;height:100%;}
</style>
</head><body>
<canvas id="C"></canvas>
<script>
(function(){
const cv=document.getElementById('C'),c=cv.getContext('2d');
let W=0,H=0,dpr=1,aT=0,paused=false;
let activeTool = 'select'; // 'select', 'iron', 'coil', 'gap', 'eraser'
let selBrId = 0; // selected branch ID
let dragSlider = -1;

const MATS = [
  { name: 'Hierro Silicio', mur: 2500 },
  { name: 'Acero Dulce', mur: 1200 },
  { name: 'Ferrita MnZn', mur: 4000 }
];

// 12 nodes grid (4 columns, 3 rows)
// Branches database
const branches = [
  { id: 0, u: 0, v: 1, type: 1, l: 15, S: 25, mur: 2000, N: 300, I: 2.0, dir: 1, g: 0.5, label: "R1" },
  { id: 1, u: 1, v: 2, type: 3, l: 15, S: 25, mur: 2000, N: 300, I: 2.0, dir: 1, g: 0.8, label: "R2" }, // Air Gap
  { id: 2, u: 2, v: 3, type: 1, l: 15, S: 25, mur: 2000, N: 300, I: 2.0, dir: 1, g: 0.5, label: "R3" },
  { id: 3, u: 4, v: 5, type: 0, l: 15, S: 25, mur: 2000, N: 300, I: 2.0, dir: 1, g: 0.5, label: "R4" },
  { id: 4, u: 5, v: 6, type: 0, l: 15, S: 25, mur: 2000, N: 300, I: 2.0, dir: 1, g: 0.5, label: "R5" },
  { id: 5, u: 6, v: 7, type: 0, l: 15, S: 25, mur: 2000, N: 300, I: 2.0, dir: 1, g: 0.5, label: "R6" },
  { id: 6, u: 8, v: 9, type: 1, l: 15, S: 25, mur: 2000, N: 300, I: 2.0, dir: 1, g: 0.5, label: "R7" },
  { id: 7, u: 9, v: 10, type: 1, l: 15, S: 25, mur: 2000, N: 300, I: 2.0, dir: 1, g: 0.5, label: "R8" },
  { id: 8, u: 10, v: 11, type: 1, l: 15, S: 25, mur: 2000, N: 300, I: 2.0, dir: 1, g: 0.5, label: "R9" },
  // Vertical
  { id: 9, u: 0, v: 4, type: 2, l: 12, S: 25, mur: 2000, N: 400, I: 3.0, dir: 1, g: 0.5, label: "R10" }, // Coil
  { id: 10, u: 4, v: 8, type: 1, l: 12, S: 25, mur: 2000, N: 300, I: 2.0, dir: 1, g: 0.5, label: "R11" },
  { id: 11, u: 1, v: 5, type: 0, l: 12, S: 25, mur: 2000, N: 300, I: 2.0, dir: 1, g: 0.5, label: "R12" },
  { id: 12, u: 5, v: 9, type: 0, l: 12, S: 25, mur: 2000, N: 300, I: 2.0, dir: 1, g: 0.5, label: "R13" },
  { id: 13, u: 2, v: 6, type: 0, l: 12, S: 25, mur: 2000, N: 300, I: 2.0, dir: 1, g: 0.5, label: "R14" },
  { id: 14, u: 6, v: 10, type: 0, l: 12, S: 25, mur: 2000, N: 300, I: 2.0, dir: 1, g: 0.5, label: "R15" },
  { id: 15, u: 3, v: 7, type: 1, l: 12, S: 25, mur: 2000, N: 300, I: 2.0, dir: 1, g: 0.5, label: "R16" },
  { id: 16, u: 7, v: 11, type: 1, l: 12, S: 25, mur: 2000, N: 300, I: 2.0, dir: 1, g: 0.5, label: "R17" }
];

// Particle state
branches.forEach(br => {
  br.particles = [0.15, 0.45, 0.75];
});

let computedReq = 0, computedFluxMax = 0, computedFMM = 0;
let statusMessage = "NOMINAL";
let statusColor = "#10B981";

function resize(){
  dpr=window.devicePixelRatio||1;
  W=document.documentElement.clientWidth||window.innerWidth||cv.clientWidth;
  H=680;
  if(W<10){setTimeout(resize,100);return;}
  cv.width=W*dpr;cv.height=H*dpr;
  cv.style.width=W+'px';cv.style.height=H+'px';
  c.setTransform(dpr,0,0,dpr,0,0);
}
window.addEventListener('resize',resize);

function getNodeCoords(nodeIdx) {
  let r = Math.floor(nodeIdx / 4);
  let c_ = nodeIdx % 4;
  let padX = 150;
  let padY = 80;
  let gridW = W - padX - 250;
  let gridH = H - padY - 150;
  return {
    x: padX + c_ * (gridW / 3),
    y: padY + r * (gridH / 2)
  };
}

function solveCircuit() {
  const M = 12;
  const A = Array.from({ length: M }, () => new Float64Array(M));
  const B = new Float64Array(M);
  const mu0 = 4 * Math.PI * 1e-7;

  computedFMM = 0;

  // 1. Reluctances and permeances
  branches.forEach(br => {
    br.flux = 0;
    br.B = 0;
    if (br.type === 0) {
      br.R = Infinity;
      br.P = 0;
      br.fmm = 0;
    } else if (br.type === 1) {
      const l_m = br.l / 100.0;
      const S_m2 = br.S / 10000.0;
      br.R = l_m / (mu0 * br.mur * S_m2);
      br.P = 1.0 / br.R;
      br.fmm = 0;
    } else if (br.type === 2) {
      const l_m = br.l / 100.0;
      const S_m2 = br.S / 10000.0;
      br.R = l_m / (mu0 * br.mur * S_m2);
      br.P = 1.0 / br.R;
      br.fmm = br.N * br.I * br.dir;
      computedFMM += Math.abs(br.fmm);
    } else if (br.type === 3) {
      const g_m = br.g / 1000.0;
      const S_m2 = br.S / 10000.0;
      br.R = g_m / (mu0 * S_m2);
      br.P = 1.0 / br.R;
      br.fmm = 0;
    }
  });

  // 2. Assemble Nodal Matrix
  branches.forEach(br => {
    if (br.type === 0) return;
    const u = br.u;
    const v = br.v;
    const P = br.P;
    
    A[u][u] += P;
    A[v][v] += P;
    A[u][v] -= P;
    A[v][u] -= P;

    const seq = P * br.fmm;
    B[u] -= seq;
    B[v] += seq;
  });

  // 3. Ground Node (Reference at left-bottom node = 8)
  const refNode = 8;
  for (let c_ = 0; c_ < M; c_++) {
    A[refNode][c_] = 0;
  }
  A[refNode][refNode] = 1.0;
  B[refNode] = 0.0;

  // 4. Gauss solver
  const x = solveGauss(A, B);

  // 5. Calculate results
  computedFluxMax = 0;
  let activeIronCount = 0;
  let saturatedCount = 0;
  let criticalCount = 0;

  branches.forEach(br => {
    if (br.type === 0) return;
    const u = br.u;
    const v = br.v;
    br.flux = br.P * (x[u] - x[v] + br.fmm);
    const S_m2 = br.S / 10000.0;
    br.B = Math.abs(br.flux) / S_m2;

    computedFluxMax = Math.max(computedFluxMax, Math.abs(br.flux));

    if (br.type === 1 || br.type === 2) {
      activeIronCount++;
      if (br.B > 2.0) criticalCount++;
      else if (br.B > 1.6) saturatedCount++;
    }
  });

  if (computedFluxMax > 1e-9) {
    computedReq = computedFMM / computedFluxMax;
  } else {
    computedReq = 0;
  }

  // Diagnostics console state
  if (activeIronCount === 0 || computedFluxMax < 1e-9) {
    statusMessage = "SIN EXCITACIÓN / CIRCUITO MAGNÉTICO ABIERTO";
    statusColor = "#6B7280";
  } else if (criticalCount > 0) {
    statusMessage = "CRÍTICO: EXCESIVA SATURACIÓN MAGNÉTICA (B > 2.0 T)";
    statusColor = "#EF4444";
  } else if (saturatedCount > 0) {
    statusMessage = "ADVERTENCIA: SATURACIÓN DETECTADA (B > 1.6 T)";
    statusColor = "#F59E0B";
  } else {
    statusMessage = "SISTEMA NOMINAL - FLUJO MAGNÉTICO OPTIMIZADO";
    statusColor = "#10B981";
  }
}

function solveGauss(A, B) {
  const n = B.length;
  const a = Array.from({ length: n }, (_, i) => new Float64Array(A[i]));
  const b = new Float64Array(B);

  for (let i = 0; i < n; i++) {
    let maxEl = Math.abs(a[i][i]);
    let maxRow = i;
    for (let k = i + 1; k < n; k++) {
      if (Math.abs(a[k][i]) > maxEl) {
        maxEl = Math.abs(a[k][i]);
        maxRow = k;
      }
    }
    for (let k = i; k < n; k++) {
      const tmp = a[maxRow][k];
      a[maxRow][k] = a[i][k];
      a[i][k] = tmp;
    }
    const tmp = b[maxRow];
    b[maxRow] = b[i];
    b[i] = tmp;

    for (let k = i + 1; k < n; k++) {
      const factor = a[k][i] / (a[i][i] || 1e-12);
      for (let j = i; j < n; j++) {
        a[k][j] -= factor * a[i][j];
      }
      b[k] -= factor * b[i];
    }
  }

  const x = new Float64Array(n);
  for (let i = n - 1; i >= 0; i--) {
    let sum = 0.0;
    for (let k = i + 1; k < n; k++) {
      sum += a[i][k] * x[k];
    }
    x[i] = (b[i] - sum) / (a[i][i] || 1e-12);
  }
  return x;
}

function rr(x,y,w,h,r,f,s){
  c.beginPath();c.moveTo(x+r,y);c.lineTo(x+w-r,y);c.quadraticCurveTo(x+w,y,x+w,y+r);
  c.lineTo(x+w,y+h-r);c.quadraticCurveTo(x+w,y+h,x+w-r,y+h);c.lineTo(x+r,y+h);
  c.quadraticCurveTo(x,y+h,x,y+h-r);c.lineTo(x,y+r);c.quadraticCurveTo(x,y,x+r,y);
  c.closePath();if(f){c.fillStyle=f;c.fill();}
  if(s){c.strokeStyle=s;c.lineWidth=1;c.stroke();}
}

function drawSidebar() {
  c.fillStyle = '#090D14';
  c.fillRect(0, 0, 120, H);
  c.strokeStyle = '#21262D';
  c.lineWidth = 1;
  c.beginPath();c.moveTo(120, 0);c.lineTo(120, H);c.stroke();

  c.fillStyle = '#00E5FF';
  c.font = 'bold 13px "Segoe UI"';
  c.textAlign = 'center';
  c.fillText('SIEMENS', 60, 24);
  c.fillStyle = '#566573';
  c.font = '9px "Segoe UI"';
  c.fillText('M-CAD Studio', 60, 36);

  const tools = [
    { id: 'select', label: 'Seleccionar', desc: 'Edita/Mira' },
    { id: 'iron', label: 'Hierro', desc: 'Núcleo' },
    { id: 'coil', label: 'Bobina FMM', desc: 'Excitación' },
    { id: 'gap', label: 'Entrehierro', desc: 'Corte Aire' },
    { id: 'eraser', label: 'Borrador', desc: 'Limpia' }
  ];

  tools.forEach((t, i) => {
    let y = 60 + i * 54;
    let isSel = activeTool === t.id;
    rr(8, y, 104, 46, 4, isSel ? '#1A293E' : '#111721', isSel ? '#00E5FF' : '#30363D');
    
    // Draw icon representation inside button
    c.fillStyle = isSel ? '#00E5FF' : '#C9D1D9';
    c.font = 'bold 10px "Segoe UI"';
    c.fillText(t.label, 60, y + 20);
    c.fillStyle = '#8B949E';
    c.font = '8px "Segoe UI"';
    c.fillText(t.desc, 60, y + 34);
  });
}

function blendColors(c1, c2, t) {
  let r1 = parseInt(c1.substring(1,3), 16);
  let g1 = parseInt(c1.substring(3,5), 16);
  let b1 = parseInt(c1.substring(5,7), 16);
  let r2 = parseInt(c2.substring(1,3), 16);
  let g2 = parseInt(c2.substring(3,5), 16);
  let b2 = parseInt(c2.substring(5,7), 16);
  let r = Math.round(r1 + (r2 - r1) * t);
  let g = Math.round(g1 + (g2 - g1) * t);
  let b = Math.round(b1 + (b2 - b1) * t);
  return '#' + [r,g,b].map(x => {
    let s = x.toString(16);
    return s.length === 1 ? '0' + s : s;
  }).join('');
}

function drawCircuit() {
  // Draw nodes
  for (let i = 0; i < 12; i++) {
    let coord = getNodeCoords(i);
    c.beginPath();
    c.arc(coord.x, coord.y, 4, 0, Math.PI * 2);
    c.fillStyle = '#30363D';
    c.fill();
  }

  // Draw branches
  branches.forEach(br => {
    let uCoords = getNodeCoords(br.u);
    let vCoords = getNodeCoords(br.v);
    let xc = (uCoords.x + vCoords.x) / 2;
    let yc = (uCoords.y + vCoords.y) / 2;
    let isHoriz = Math.abs(uCoords.y - vCoords.y) < 2;
    let thick = 16;
    let isSelected = selBrId === br.id;

    if (br.type === 0) {
      // Empty slot
      c.strokeStyle = isSelected ? 'rgba(0, 229, 255, 0.4)' : '#1E293B';
      c.lineWidth = 2;
      c.setLineDash([4, 4]);
      c.beginPath();c.moveTo(uCoords.x, uCoords.y);c.lineTo(vCoords.x, vCoords.y);c.stroke();
      c.setLineDash([]);
      
      // Clickable label in Select mode
      c.fillStyle = '#4B5563';
      c.font = '8px monospace';
      c.textAlign = 'center';
      c.fillText('(Vacío)', xc, yc + 4);
      return;
    }

    // Material Core Color based on Saturation
    let baseCol = '#1E2D3D'; // steel core
    if (br.B > 1.6) {
      let t = Math.min(1.0, (br.B - 1.6) / 0.8);
      baseCol = blendColors('#1E2D3D', '#7F1D1D', t); // saturates to red
    }

    let borderCol = isSelected ? '#00E5FF' : '#30363D';
    c.lineWidth = isSelected ? 2 : 1;

    // Draw main core rect
    if (isHoriz) {
      rr(uCoords.x - 2, yc - thick/2, (vCoords.x - uCoords.x) + 4, thick, 2, baseCol, borderCol);
    } else {
      rr(xc - thick/2, uCoords.y - 2, thick, (vCoords.y - uCoords.y) + 4, 2, baseCol, borderCol);
    }

    // Overlay specifics
    if (br.type === 2) {
      // Coil
      c.fillStyle = '#D35400'; // copper
      if (isHoriz) {
        for (let i = -3; i <= 3; i++) {
          rr(xc + i * 8 - 3, yc - 12, 6, 24, 1, '#E67E22', '#A04000');
        }
        // Direction arrow
        c.fillStyle = '#00E5FF';
        c.font = 'bold 9px Arial';
        c.fillText(br.dir > 0 ? '▶' : '◀', xc, yc + 3);
      } else {
        for (let i = -3; i <= 3; i++) {
          rr(xc - 12, yc + i * 8 - 3, 24, 6, 1, '#E67E22', '#A04000');
        }
        c.fillStyle = '#00E5FF';
        c.font = 'bold 9px Arial';
        c.fillText(br.dir > 0 ? '▼' : '▲', xc, yc + 3);
      }
    } else if (br.type === 3) {
      // Air Gap
      c.fillStyle = '#0D1117'; // cut
      if (isHoriz) {
        c.fillRect(xc - 3, yc - 9, 6, 18);
        c.fillStyle = '#FFA000'; // air gap glow
        c.fillRect(xc - 1, yc - 9, 2, 18);
      } else {
        c.fillRect(xc - 9, yc - 3, 18, 6);
        c.fillStyle = '#FFA000';
        c.fillRect(xc - 9, yc - 1, 18, 2);
      }
    }

    // Branch Label & B value
    c.fillStyle = '#8B949E';
    c.font = '9px Arial';
    c.textAlign = 'center';
    
    let brLabel = br.type === 1 ? 'Núcleo' : br.type === 2 ? 'Bobina' : 'Aire';
    let labelY = isHoriz ? yc - 16 : yc;
    let labelX = isHoriz ? xc : xc + 28;
    
    if (!isHoriz) c.textAlign = 'left';
    c.fillText(brLabel + ` [${br.B.toFixed(2)}T]`, labelX, labelY);
    c.font = '8px monospace';
    c.fillStyle = '#00E5FF';
    c.fillText(`${(br.flux * 1000).toFixed(3)} mWb`, labelX, labelY + 10);
    c.textAlign = 'center';

    // Particle Flow Animation
    if (Math.abs(br.flux) > 1e-7 && !paused) {
      let speed = Math.abs(br.flux) * 450 * (1.0 / br.l);
      c.fillStyle = '#00E5FF';
      br.particles.forEach((p, idx) => {
        if (br.flux > 0) {
          br.particles[idx] += speed;
          if (br.particles[idx] > 1) br.particles[idx] -= 1;
        } else {
          br.particles[idx] -= speed;
          if (br.particles[idx] < 0) br.particles[idx] += 1;
        }
        // compute position
        let px = uCoords.x + (vCoords.x - uCoords.x) * br.particles[idx];
        let py = uCoords.y + (vCoords.y - uCoords.y) * br.particles[idx];
        c.beginPath();
        c.arc(px, py, 2.5, 0, Math.PI * 2);
        c.shadowColor = '#00E5FF';
        c.shadowBlur = 4;
        c.fill();
        c.shadowBlur = 0; // reset
      });
    }
  });
}

function getDistToSegment(px, py, x1, y1, x2, y2) {
  let dx = x2 - x1;
  let dy = y2 - y1;
  let lenSq = dx*dx + dy*dy;
  if (lenSq === 0) return Math.sqrt((px-x1)*(px-x1) + (py-y1)*(py-y1));
  let t = ((px - x1) * dx + (py - y1) * dy) / lenSq;
  t = Math.max(0, Math.min(1, t));
  let projX = x1 + t * dx;
  let projY = y1 + t * dy;
  return Math.sqrt((px-projX)*(px-projX) + (py-projY)*(py-projY));
}

function drawPropertiesPanel() {
  let x = W - 240;
  c.fillStyle = '#090D14';
  c.fillRect(x, 0, 240, H);
  c.strokeStyle = '#21262D';
  c.lineWidth = 1;
  c.beginPath();c.moveTo(x, 0);c.lineTo(x, H);c.stroke();

  c.fillStyle = '#C9D1D9';
  c.font = 'bold 12px "Segoe UI"';
  c.textAlign = 'left';
  c.fillText('PANEL DE PROPIEDADES', x + 16, 24);

  if (selBrId < 0) {
    c.fillStyle = '#566573';
    c.font = '11px "Segoe UI"';
    c.fillText('Haz clic en un componente', x + 16, 60);
    c.fillText('del circuito para editarlo.', x + 16, 76);
    return;
  }

  let br = branches.find(b => b.id === selBrId);
  c.fillStyle = '#00E5FF';
  c.font = 'bold 11px monospace';
  let typeLabels = ['Vacío', 'Núcleo Hierro', 'Bobina FMM', 'Entrehierro'];
  c.fillText(`RAMA ${br.id+1} - ${typeLabels[br.type]}`, x + 16, 52);

  // Parameter Sliders based on Type
  let sliders = [];
  if (br.type === 1) {
    sliders = [
      { key: 'l', lb: 'Longitud Núcleo (cm)', min: 5, max: 100, val: br.l, fmt: v=>v+' cm' },
      { key: 'S', lb: 'Sección Transv. (cm2)', min: 2, max: 150, val: br.S, fmt: v=>v+' cm²' },
      { key: 'mur', lb: 'Permeabilidad (mur)', min: 100, max: 8000, val: br.mur, fmt: v=>v }
    ];
  } else if (br.type === 2) {
    sliders = [
      { key: 'N', lb: 'Número de Espiras (N)', min: 10, max: 1500, val: br.N, fmt: v=>v },
      { key: 'I', lb: 'Corriente Exc. (I)', min: 0.1, max: 15.0, val: br.I, fmt: v=>v.toFixed(1)+' A' },
      { key: 'mur', lb: 'Permeabilidad (mur)', min: 100, max: 8000, val: br.mur, fmt: v=>v }
    ];
  } else if (br.type === 3) {
    sliders = [
      { key: 'g', lb: 'Espesor de Entrehierro', min: 0.1, max: 8.0, val: br.g, fmt: v=>v.toFixed(1)+' mm' },
      { key: 'S', lb: 'Sección Transv. (cm2)', min: 2, max: 150, val: br.S, fmt: v=>v+' cm²' }
    ];
  }

  // Draw Sliders
  sliders.forEach((sl, idx) => {
    let sy = 80 + idx * 56;
    c.fillStyle = '#8B949E';
    c.font = '10px "Segoe UI"';
    c.fillText(sl.lb, x + 16, sy + 14);

    c.fillStyle = '#FCD34D';
    c.font = 'bold 10px monospace';
    c.textAlign = 'right';
    c.fillText(sl.fmt(sl.val), x + 224, sy + 14);
    c.textAlign = 'left';

    // Slider Line
    rr(x + 16, sy + 24, 208, 6, 3, '#1F2937', null);
    let rat = (sl.val - sl.min) / (sl.max - sl.min);
    rr(x + 16, sy + 24, rat * 208, 6, 3, '#00E5FF', null);

    // Knob
    let kx = x + 16 + rat * 208;
    c.beginPath();
    c.arc(kx, sy + 27, 6, 0, Math.PI * 2);
    c.fillStyle = '#FFF';
    c.fill();
    c.strokeStyle = '#00E5FF';
    c.lineWidth = 1.5;
    c.stroke();

    // Store slider interactions hitboxes
    sl.x = x + 16;
    sl.y = sy + 27;
    sl.w = 208;
    sl.idx = idx;
    sl.brRef = br;
  });

  br._sliders = sliders;

  // Extra button for Coil Polarities
  if (br.type === 2) {
    let by = 260;
    rr(x + 16, by, 208, 28, 4, '#1E293B', '#30363D');
    c.fillStyle = '#FFF';
    c.font = 'bold 10px "Segoe UI"';
    c.textAlign = 'center';
    c.fillText('INVERTIR DIRECCIÓN COIL', x + 120, by + 17);
    br._dirBtn = { x: x + 16, y: by, w: 208, h: 28 };
    c.textAlign = 'left';
  }
}

function drawDiagnosticsConsole() {
  let cx_ = 140;
  let cy_ = H - 120;
  let cw_ = W - 140 - 250;
  let ch_ = 100;

  rr(cx_, cy_, cw_, ch_, 6, '#090D14', '#1E293B');

  c.fillStyle = '#8B949E';
  c.font = 'bold 10px "Segoe UI"';
  c.fillText('SIEMENS - DIAGNÓSTICO EN TIEMPO REAL', cx_ + 14, cy_ + 18);

  // Siemens values
  function mc(lb, vl, un, px, py) {
    c.fillStyle = '#4B5563';
    c.font = '9px "Segoe UI"';
    c.fillText(lb, px, py);
    c.fillStyle = '#E5E7EB';
    c.font = 'bold 12px monospace';
    c.fillText(vl + ' ' + un, px, py + 16);
  }

  mc('FMM Total Inyectada', computedFMM.toFixed(0), 'A-v', cx_ + 14, cy_ + 42);
  mc('Reluctancia Equiv. Loop', computedReq > 0 ? computedReq.toExponential(2) : '---', 'H⁻¹', cx_ + 150, cy_ + 42);
  mc('Flujo Máx de Malla', (computedFluxMax*1000).toFixed(3), 'mWb', cx_ + 290, cy_ + 42);

  // Diagnostics status indicator
  c.fillStyle = '#4B5563';
  c.font = '9px "Segoe UI"';
  c.fillText('ESTADO DE LA RED', cx_ + 430, cy_ + 42);

  rr(cx_ + 430, cy_ + 48, cw_ - 444, 28, 4, statusColor + '1E', statusColor);
  c.fillStyle = statusColor;
  c.font = 'bold 9px "Segoe UI"';
  c.textAlign = 'center';
  c.fillText(statusMessage, cx_ + 430 + (cw_ - 444)/2, cy_ + 65);
  c.textAlign = 'left';
}

function draw(){
  if(W<10){
    requestAnimationFrame(draw);
    return;
  }
  c.clearRect(0,0,W,H);
  c.fillStyle='#0A0F17';c.fillRect(0,0,W,H);

  // Siemens border style
  rr(0,0,W,H,10,null,'#1F2937');

  drawSidebar();
  drawCircuit();
  drawPropertiesPanel();
  drawDiagnosticsConsole();

  requestAnimationFrame(draw);
}

function gp(e){var r=cv.getBoundingClientRect();return{x:e.clientX-r.left,y:e.clientY-r.top};}

cv.addEventListener('mousedown',function(e){
  var p=gp(e);

  // Sidebar Tool Palette Click
  if (p.x <= 120) {
    const tools = ['select', 'iron', 'coil', 'gap', 'eraser'];
    tools.forEach((t, i) => {
      let y = 60 + i * 54;
      if (p.x >= 8 && p.x <= 112 && p.y >= y && p.y <= y + 46) {
        activeTool = t;
      }
    });
    return;
  }

  // Properties Panel Click
  if (p.x >= W - 240) {
    if (selBrId >= 0) {
      let br = branches.find(b => b.id === selBrId);
      // Check Sliders Click
      if (br._sliders) {
        br._sliders.forEach(sl => {
          if (p.y >= sl.y - 12 && p.y <= sl.y + 12 && p.x >= sl.x && p.x <= sl.x + sl.w) {
            dragSlider = sl.idx;
          }
        });
      }
      // Check direction invert button
      if (br._dirBtn && p.x >= br._dirBtn.x && p.x <= br._dirBtn.x + br._dirBtn.w && p.y >= br._dirBtn.y && p.y <= br._dirBtn.y + br._dirBtn.h) {
        br.dir = -br.dir;
        solveCircuit();
      }
    }
    return;
  }

  // Grid/Branch interaction click
  let bestDist = 15;
  let clickedBr = null;
  branches.forEach(br => {
    let uCoords = getNodeCoords(br.u);
    let vCoords = getNodeCoords(br.v);
    let dist = getDistToSegment(p.x, p.y, uCoords.x, uCoords.y, vCoords.x, vCoords.y);
    if (dist < bestDist) {
      bestDist = dist;
      clickedBr = br;
    }
  });

  if (clickedBr) {
    selBrId = clickedBr.id;
    if (activeTool === 'iron') {
      clickedBr.type = 1;
      clickedBr.mur = 2000;
    } else if (activeTool === 'coil') {
      clickedBr.type = 2;
      clickedBr.mur = 2000;
    } else if (activeTool === 'gap') {
      clickedBr.type = 3;
    } else if (activeTool === 'eraser') {
      clickedBr.type = 0;
    }
    solveCircuit();
  } else {
    // click in empty grid resets selection if no branch clicked
    if (p.x > 120 && p.x < W - 240 && p.y < H - 120) {
      selBrId = -1;
    }
  }
});

cv.addEventListener('mousemove',function(e){
  var p=gp(e);

  // If dragging a properties slider
  if (dragSlider >= 0 && selBrId >= 0) {
    let br = branches.find(b => b.id === selBrId);
    let sl = br._sliders[dragSlider];
    let rat = (p.x - sl.x) / sl.w;
    rat = Math.max(0, Math.min(1, rat));
    let val = sl.min + rat * (sl.max - sl.min);
    
    // adjust parameters based on slider keys
    if (sl.key === 'l' || sl.key === 'S' || sl.key === 'N') {
      br[sl.key] = Math.round(val);
    } else if (sl.key === 'I' || sl.key === 'g') {
      br[sl.key] = Math.round(val * 10) / 10;
    } else if (sl.key === 'mur') {
      br[sl.key] = Math.round(val / 100) * 100;
    }
    solveCircuit();
    return;
  }

  // Cursor change styling based on hover targets
  let isHover = false;
  if (p.x <= 120) {
    const tools = ['select', 'iron', 'coil', 'gap', 'eraser'];
    tools.forEach((t, i) => {
      let y = 60 + i * 54;
      if (p.x >= 8 && p.x <= 112 && p.y >= y && p.y <= y + 46) isHover = true;
    });
  } else if (p.x >= W - 240) {
    if (selBrId >= 0) {
      let br = branches.find(b => b.id === selBrId);
      if (br._sliders) {
        br._sliders.forEach(sl => {
          if (p.y >= sl.y - 12 && p.y <= sl.y + 12 && p.x >= sl.x && p.x <= sl.x + sl.w) isHover = true;
        });
      }
      if (br._dirBtn && p.x >= br._dirBtn.x && p.x <= br._dirBtn.x + br._dirBtn.w && p.y >= br._dirBtn.y && p.y <= br._dirBtn.y + br._dirBtn.h) isHover = true;
    }
  } else {
    // Hover grid branches
    branches.forEach(br => {
      let uCoords = getNodeCoords(br.u);
      let vCoords = getNodeCoords(br.v);
      let dist = getDistToSegment(p.x, p.y, uCoords.x, uCoords.y, vCoords.x, vCoords.y);
      if (dist < 15) isHover = true;
    });
  }

  cv.style.cursor = isHover ? 'pointer' : 'default';
});

cv.addEventListener('mouseup',function(){
  dragSlider = -1;
});
cv.addEventListener('mouseleave',function(){
  dragSlider = -1;
});

// Setup touch events
cv.addEventListener('touchstart',function(e){e.preventDefault();var t=e.touches[0];cv.dispatchEvent(new MouseEvent('mousedown',{clientX:t.clientX,clientY:t.clientY}));},{passive:false});
cv.addEventListener('touchmove',function(e){e.preventDefault();var t=e.touches[0];cv.dispatchEvent(new MouseEvent('mousemove',{clientX:t.clientX,clientY:t.clientY}));},{passive:false});
cv.addEventListener('touchend',function(){cv.dispatchEvent(new MouseEvent('mouseup'));});

resize();
solveCircuit();
requestAnimationFrame(draw);
})();
</script>
</body></html>"""
        components.html(circuit_html, height=710, scrolling=False)



if __name__ == "__main__":
    app()