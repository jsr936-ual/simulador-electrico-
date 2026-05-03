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
    st.header("🧲 TEMA 1: Principios Generales del Electromagnetismo")
    st.caption("Módulo interactivo para el análisis de campos, materiales magnéticos e inducción (Nivel Ingeniería).")

    tab_campo, tab_materiales, tab_circuitos, tab_induccion = st.tabs([
        "1.1 & 1.2 - El Campo Magnético",
        "1.3 - Materiales y Pérdidas",
        "1.4 & 1.5 - Circuitos y Leyes",
        "1.6 & 1.7 - Inducción y Energía"
    ])

    # --------------------------------------------------------------------------
    # PESTAÑA 1: CAMPO MAGNÉTICO (Biot-Savart y Ampère)
    # --------------------------------------------------------------------------
    with tab_campo:
        st.markdown("### 🌐 El Campo Magnético y sus Fuentes")
        col_t1, col_t2 = st.columns([1, 1])
        with col_t1:
            st.markdown("**Ley de Ampère:**")
            st.latex(r"\oint \vec{H} \cdot d\vec{l} = I_{neta}")
            st.markdown("Para un conductor rectilíneo infinito, el campo magnético a una distancia $r$ es:")
            st.latex(r"B = \frac{\mu_0 \cdot I}{2 \pi r}")
        with col_t2:
            st.markdown("#### 📉 Simulación: B vs Distancia")
            I_sim = st.slider("Corriente por el conductor (A)", 10, 500, 100, step=10)
            r_array = np.linspace(0.01, 0.5, 100)
            mu_0 = 4 * math.pi * 1e-7
            B_array = (mu_0 * I_sim) / (2 * math.pi * r_array) * 1000
            fig_campo = go.Figure()
            fig_campo.add_trace(go.Scatter(x=r_array*100, y=B_array, mode='lines', line=dict(color='#00ADB5', width=3)))
            fig_campo.update_layout(title="Atenuación del Campo Magnético", xaxis_title="Distancia al conductor (cm)", yaxis_title="Densidad de Flujo B (mT)", height=300, margin=dict(l=0, r=0, t=40, b=0))
            st.plotly_chart(fig_campo, use_container_width=True)

    # --------------------------------------------------------------------------
    # PESTAÑA 2: MATERIALES MAGNÉTICOS, PÉRDIDAS Y TEMPERATURA
    # --------------------------------------------------------------------------
    with tab_materiales:
        st.markdown("### 🧱 Histéresis, Pérdidas en el Hierro y Calentamiento")
        with st.expander("📖 Base Teórica: Deducción, Pérdidas y Modelo Térmico", expanded=False):
            st.markdown(r"""
            **1. Deducción del Campo Magnético (H) a partir de Excitación AC:**
            Partiendo de la Ley de Ampère para un circuito magnético cerrado de longitud media $l_{eq}$:
            $$ \oint \vec{H} \cdot d\vec{l} = N \cdot I_{neta} \implies H(t) \cdot l_{eq} = N \cdot I(t) $$
            Si excitamos la bobina con una corriente alterna $I(t) = I_{max} \sin(\omega t)$, la intensidad de campo resultante es:
            $$ H(t) = \frac{N \cdot I_{max}}{l_{eq}} \sin(2\pi f t) $$
            **2. Ecuación Térmica en Estado Estacionario:**
            $$ T_{final} = T_{amb} + \Delta T = T_{amb} + (P_{tot} \cdot R_{th}) $$
            """)

        col_mat1, col_mat2 = st.columns([1.2, 2.5])
        with col_mat1:
            tipo_mat = st.radio("Material del Núcleo:", ["Acero al Silicio M4 (Transformadores)", "Acero Estructural (Núcleo Macizo)"])
            if "Silicio" in tipo_mat:
                B_sat, H_c, a, k_f = 1.65, 20, 40, 1.5
            else:
                B_sat, H_c, a, k_f = 1.4, 250, 200, 25.0
            H_max = st.slider("Amplitud AC (H máximo) [A/m]", 50, 1500, 400, step=50)
            H_offset = st.slider("Inyección DC (Bias) [A/m]", -500, 500, 0, step=50)
            freq = st.number_input("Frecuencia de red (Hz)", value=50, step=10)
            V_nucleo = st.number_input("Volumen núcleo (m³)", min_value=0.001, max_value=0.5, value=0.010, format="%.3f")
            R_th = st.number_input("Resist. Térmica Rth (°C/W)", min_value=0.01, max_value=2.0, value=0.15, format="%.2f")

        with col_mat2:
            H_a, B_a, H_d, B_d, area_ciclo = simular_histeresis(B_sat, H_c, a, H_max, H_offset)
            P_hist = area_ciclo * freq * V_nucleo 
            B_max_real = np.max(np.abs(B_a))
            P_fouc = k_f * (freq**2) * (B_max_real**2) * V_nucleo 
            P_tot = P_hist + P_fouc
            T_amb = 40.0 
            Delta_T = P_tot * R_th
            T_final = T_amb + Delta_T
            
            res_c1, res_c2, res_c3, res_c4 = st.columns(4)
            res_c1.metric("Área Ciclo", f"{area_ciclo:,.0f} J/m³")
            res_c2.metric("Pérdidas Histéresis", f"{P_hist:,.1f} W")
            res_c3.metric("Pérdidas Foucault", f"{P_fouc:,.1f} W")
            res_c4.metric("Temp. Máquina", f"{T_final:,.1f} °C", f"+{Delta_T:,.1f} °C (ΔT)", delta_color="inverse")

            fig_bh = go.Figure()
            fig_bh.add_trace(go.Scatter(x=H_a, y=B_a, mode='lines', name='Magnetización', fill='tonexty', fillcolor='rgba(255, 165, 0, 0.1)', line=dict(color='orange')))
            fig_bh.add_trace(go.Scatter(x=H_d, y=B_d, mode='lines', name='Desmagnetización', fill='tonexty', fillcolor='rgba(0, 255, 255, 0.1)', line=dict(color='cyan')))
            fig_bh.add_hline(y=0, line_width=1, line_color="gray")
            fig_bh.add_vline(x=0, line_width=1, line_color="gray")
            fig_bh.add_vline(x=H_offset, line_width=1, line_dash="dash", line_color="red")
            fig_bh.update_layout(title="Ciclo de Histéresis", xaxis_title="Campo H [A/m]", yaxis_title="Inducción B [T]", height=450, margin=dict(l=0, r=0, t=40, b=0))
            st.plotly_chart(fig_bh, use_container_width=True)

    # --------------------------------------------------------------------------
    # PESTAÑA 3: CIRCUITOS MAGNÉTICOS (ESQUEMA CLÁSICO ESTILO FRAILE MORA)
    # --------------------------------------------------------------------------
    with tab_circuitos:
        st.markdown("### 🔄 Resolución de Circuitos Magnéticos por Tramos")
        st.write("Añade piezas a tu circuito magnético en la tabla inferior. El sistema generará el **esquema análogo normalizado** automáticamente.")
        
        col_inputs1, col_inputs2 = st.columns([1, 2])
        
        with col_inputs1:
            st.markdown("**⚡ Excitación (FMM)**")
            N = st.number_input("Número de espiras (N)", min_value=1, value=300, step=10)
            I = st.number_input("Corriente (I) [A]", min_value=0.1, value=3.0, step=0.1)
            mu_r_hierro = st.number_input("Permeabilidad Hierro ($\mu_r$)", min_value=100.0, value=2500.0, step=100.0)

        with col_inputs2:
            st.markdown("**🧱 Configuración de la Malla (Añade tramos)**")
            if "tramos_data" not in st.session_state:
                st.session_state.tramos_data = pd.DataFrame([
                    {"Material": "Hierro", "Longitud (cm)": 40.0, "Sección (cm²)": 30.0},
                    {"Material": "Entrehierro (Aire)", "Longitud (cm)": 0.2, "Sección (cm²)": 31.5}
                ])
            
            edited_df = st.data_editor(
                st.session_state.tramos_data, 
                num_rows="dynamic",
                column_config={
                    "Material": st.column_config.SelectboxColumn("Material", options=["Hierro", "Entrehierro (Aire)"], required=True),
                    "Longitud (cm)": st.column_config.NumberColumn("Long. (cm)", min_value=0.01, format="%.2f"),
                    "Sección (cm²)": st.column_config.NumberColumn("Sec. (cm²)", min_value=0.1, format="%.2f")
                },
                use_container_width=True
            )

        # --- MOTOR DE CÁLCULO ---
        mu_0 = 4 * math.pi * 1e-7
        fmm = N * I
        reluctancia_total = 0.0
        
        for index, row in edited_df.iterrows():
            l_m = row["Longitud (cm)"] / 100.0
            S_m2 = row["Sección (cm²)"] / 10000.0
            mu_r_aplicada = mu_r_hierro if row["Material"] == "Hierro" else 1.0
            if S_m2 > 0:
                reluctancia_total += l_m / (mu_0 * mu_r_aplicada * S_m2)

        flujo = fmm / reluctancia_total if reluctancia_total > 0 else 0

        # --- GENERADOR DE DIAGRAMA SCHEMATIC (SVG) ESTILO CLÁSICO ---
        st.markdown("---")
        st.markdown("**🖥️ Esquema Análogo Magnético**")
        
        num_elements = len(edited_df)
        if num_elements > 0:
            svg_width = 150 + num_elements * 150
            svg_height = 220
            
            # Iniciar SVG
            svg_code = f'<svg width="100%" height="{svg_height}" viewBox="0 0 {svg_width} {svg_height}" xmlns="http://www.w3.org/2000/svg">'
            
            # 1. Dibujar la fuente de FMM (Generador AC clásico con N·I)
            svg_code += '<circle cx="50" cy="115" r="25" stroke="#FFFFFF" stroke-width="2" fill="#1E1E1E" />'
            svg_code += '<text x="50" y="120" fill="#FFFFFF" font-size="22" font-family="serif" text-anchor="middle">~</text>'
            svg_code += '<text x="50" y="80" fill="#FFAA00" font-size="16" font-weight="bold" font-family="sans-serif" text-anchor="middle">N·I</text>'
            
            # Cables de la fuente
            svg_code += '<line x1="50" y1="90" x2="50" y2="40" stroke="#FFFFFF" stroke-width="3" />'
            svg_code += '<line x1="50" y1="140" x2="50" y2="180" stroke="#FFFFFF" stroke-width="3" />'
            
            # Flecha indicadora de flujo (Phi) y definicion de marcador SIN saltos de linea para que Markdown no se rompa
            svg_code += '<defs><marker id="arrow" viewBox="0 0 10 10" refX="5" refY="5" markerWidth="6" markerHeight="6" orient="auto-start-reverse"><path d="M 0 0 L 10 5 L 0 10 z" fill="#00FFFF" /></marker></defs>'
            svg_code += '<line x1="60" y1="30" x2="90" y2="30" stroke="#00FFFF" stroke-width="2" marker-end="url(#arrow)" />'
            svg_code += '<text x="75" y="20" fill="#00FFFF" font-size="16" font-family="serif" font-weight="bold" text-anchor="middle">Φ</text>'

            # Cable horizontal inicial (arriba) y de retorno (abajo)
            svg_code += '<line x1="48" y1="40" x2="100" y2="40" stroke="#FFFFFF" stroke-width="3" />'
            svg_code += f'<line x1="48" y1="180" x2="{100 + num_elements*150}" y2="180" stroke="#FFFFFF" stroke-width="3" />'
            
            # Dibujar Reluctancias y unirlas (Estilo Resistencia IEC - Rectángulo)
            for i, (index, row) in enumerate(edited_df.iterrows()):
                x_offset = 100 + i * 150
                is_iron = row["Material"] == "Hierro"
                
                # Colores según el material
                fill_color = "#00ADB5" if is_iron else "#F9A826"
                text_label = "Fe" if is_iron else "Aire"
                
                # Cálculo de reluctancia individual
                l_m = row["Longitud (cm)"] / 100.0
                S_m2 = row["Sección (cm²)"] / 10000.0
                mu_r_aplicada = mu_r_hierro if is_iron else 1.0
                r_tramo = l_m / (mu_0 * mu_r_aplicada * S_m2) if S_m2 > 0 else 0
                
                # Dibujar el rectángulo
                svg_code += f'<rect x="{x_offset}" y="25" width="80" height="30" stroke="#FFFFFF" stroke-width="2" fill="{fill_color}" rx="3" />'
                # Etiqueta R1, R2...
                svg_code += f'<text x="{x_offset+40}" y="45" fill="#000000" font-size="14" font-weight="bold" font-family="sans-serif" text-anchor="middle">R{i+1}</text>'
                # Info debajo de la reluctancia
                svg_code += f'<text x="{x_offset+40}" y="75" fill="#AAAAAA" font-size="12" font-family="sans-serif" text-anchor="middle">{text_label}</text>'
                svg_code += f'<text x="{x_offset+40}" y="95" fill="#FFFFFF" font-size="12" font-family="sans-serif" text-anchor="middle">{r_tramo:.1e} H⁻¹</text>'
                
                # Cable que conecta a la siguiente reluctancia o al final
                svg_code += f'<line x1="{x_offset+80}" y1="40" x2="{x_offset+150}" y2="40" stroke="#FFFFFF" stroke-width="3" />'

            # Cable vertical derecho que cierra el circuito
            svg_code += f'<line x1="{100 + num_elements*150}" y1="38" x2="{100 + num_elements*150}" y2="182" stroke="#FFFFFF" stroke-width="3" />'
            
            svg_code += '</svg>'
            
            # Mostrar el SVG en Streamlit
            st.markdown(f"<div style='background-color:#161B22; padding:20px; border-radius:10px; text-align:center; border: 1px solid #30363D; overflow-x: auto;'>{svg_code}</div>", unsafe_allow_html=True)
        else:
            st.info("Añade algún tramo en la tabla superior para visualizar el circuito.")

        # --- RESULTADOS NUMÉRICOS ---
        st.markdown("---")
        st.markdown("**📊 Resultados Finales de la Red Magnética**")
        res1, res2, res3 = st.columns(3)
        res1.metric("Reluctancia Equivalente (𝓡_eq)", f"{reluctancia_total:,.0f} H⁻¹")
        res2.metric("Flujo Resultante de la Malla (Φ)", f"{flujo*1000:.3f} mWb")
        res3.metric("FMM Inyectada", f"{fmm:,.0f} A-v")

        st.markdown("**🔍 Verificación de Saturación por Tramo (Densidad de Flujo B)**")
        cols_b = st.columns(len(edited_df) if len(edited_df) > 0 else 1)
        for i, (index, row) in enumerate(edited_df.iterrows()):
            S_m2 = row["Sección (cm²)"] / 10000.0
            B_tramo = flujo / S_m2 if S_m2 > 0 else 0
            
            with cols_b[i]:
                if B_tramo > 1.6 and row["Material"] == "Hierro":
                    st.error(f"**R{i+1}**: {B_tramo:.2f} T (¡Saturado!)")
                else:
                    st.success(f"**R{i+1}**: {B_tramo:.2f} T (Normal)")

    # --------------------------------------------------------------------------
    # PESTAÑA 4: INDUCCIÓN Y LEY DE FARADAY-LENZ
    # --------------------------------------------------------------------------
    with tab_induccion:
        st.markdown("### ⚡ Inducción Electromagnética (Faraday - Lenz)")
        col_f1, col_f2 = st.columns([1, 3])
        with col_f1:
            freq_f = st.slider("Frecuencia AC (Hz)", 10, 100, 50, step=10, key="freq_faraday")
            N_sec = st.number_input("Espiras secundario", value=100, step=10)
            flujo_max_mWb = st.slider("Flujo máx (mWb)", 1.0, 50.0, 15.0)
        with col_f2:
            t = np.linspace(0, 3/freq_f, 300)
            flujo_t = (flujo_max_mWb / 1000) * np.sin(2 * np.pi * freq_f * t)
            e_t = - N_sec * (flujo_max_mWb / 1000) * (2 * np.pi * freq_f) * np.cos(2 * np.pi * freq_f * t)
            fig_faraday = make_subplots(specs=[[{"secondary_y": True}]])
            fig_faraday.add_trace(go.Scatter(x=t*1000, y=flujo_t*1000, name="Flujo Φ (mWb)", line=dict(color="cyan")), secondary_y=False)
            fig_faraday.add_trace(go.Scatter(x=t*1000, y=e_t, name="F.E.M. inducida e(t) (V)", line=dict(color="orange", dash="dash")), secondary_y=True)
            fig_faraday.update_layout(title=f"Desfase 90º entre Flujo y Tensión Inducida ({freq_f} Hz)", xaxis_title="Tiempo (ms)", height=350, margin=dict(l=0, r=0, t=40, b=0))
            st.plotly_chart(fig_faraday, use_container_width=True)

if __name__ == "__main__":
    app()