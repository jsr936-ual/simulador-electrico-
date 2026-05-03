import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go

#+++++++++++++++LIBRERÍAS EMPLEADAS:+++++++++++++++++++++++++++++++
#Streamlit para crear webs de forma sencilla.
#Pandas para manejo de datos en tablas.
#Numpy para cálculos numéricos y vectores.
#Plotly para gráficos interactivos y dinámicos. En particular "Plotly Express" para gráficos rápidos,
#y Graph Objects para gráficos más personalizados.
#+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++

#En primer lugar definimos la función APP, que contiene todas las funciones y el código para
#el funcionamiento de un módulo. En el caso de este primer archivo BASIC_CALCULATIONS.PY, lo definimos
#al principio, sin embargo en el resto de módulos DEFINIMOS APP AL FINAL. 
def app():
    st.header("Line Classification & Basic Calculations")
    st.caption("Module for fundamental analysis, material selection and rules.")

    #Aquí definimos las distintas pestañas que tiene nuestro primer módulo. Para ello
    #empleamos la función TABS de Streamlit.
    tab_projects, tab_materials, tab_insulation, tab_calc, tab_wizard = st.tabs([
        "Proyectos y estadísticas",
        "Análisis de conductores",
        "Aislamiento de los conductores (PVC vs XLPE)",
        "Laboratorio de cálculo",
        "Asistente de diseño"
    ])

    # ==============================================================================
    # TAB 1: DEFINIMOS LOS PROYECTOS Y ESTADÍSTICAS, Y LOS COMPARAMOS, ASÍ
    # NOMBRAMOS SU TOPOLOGÍA PERMITIDA
    # ==============================================================================
    with tab_projects:
        st.subheader("Base de datos y clasificación normativa de proyectos")
        
        #USAMOS DATAFRAMES: ESTRUCTURAS BIDIMENSIONALES DE DATOS (SIMILARES A TABLAS DE EXCEL)
        # 1. DATOS ENRIQUECIDOS
        data_proyectos = [
            {
                "Proyecto": "Instalación Industrial", 
                "Tensión (V)": 20000, 
                "Nivel": "MT (Alta Tensión)", 
                "Topología": "Mixta", 
                "Conductor": "Cobre (XLPE)",
                "Norma": "RAT + ITC-LAT 06",
                "Cantidad": 1
            },
            {
                "Proyecto": "Complejo Residencial", 
                "Tensión (V)": 400, 
                "Nivel": "BT (Baja Tensión)", 
                "Topología": "Subterránea", 
                "Conductor": "Cobre (PVC)",
                "Norma": "REBT ITC-BT-07",
                "Cantidad": 1
            },
            {
                "Proyecto": "Centro Comercial (Línea MT)", 
                "Tensión (V)": 20000, 
                "Nivel": "MT (Alta Tensión)", 
                "Topología": "Aérea", 
                "Conductor": "Aluminio (XLPE)",
                "Norma": "RAT + ITC-LAT 07",
                "Cantidad": 1
            },
            {
                "Proyecto": "Centro Comercial (Interior)", 
                "Tensión (V)": 400, 
                "Nivel": "BT (Baja Tensión)", 
                "Topología": "Interior/Entubada", 
                "Conductor": "Cobre (XLPE)",
                "Norma": "REBT ITC-BT-19/28",
                "Cantidad": 1
            }
        ]
        df_projects = pd.DataFrame(data_proyectos)
        
        # VISUALIZACIÓN DEL DATAFRAME
        st.dataframe(
            df_projects, 
            column_config={
                "Tensión (V)": st.column_config.NumberColumn(format="%d V"),
                "Norma": st.column_config.TextColumn(help="Reglamento aplicable")
            },
            use_container_width=True
        )
        
        col1, col2 = st.columns([1, 1])
        
        with col1:
            st.markdown("##### 📊 Comparativa de Niveles de Tensión")
            fig_bar = px.bar(
                df_projects, 
                x="Proyecto", 
                y="Tensión (V)", 
                color="Nivel",
                color_discrete_map={"MT (Alta Tensión)": "#FF4B4B", "BT (Baja Tensión)": "#00CC96"},
                text_auto=True
            )
            fig_bar.update_layout(showlegend=False, xaxis_title=None)
            st.plotly_chart(fig_bar, use_container_width=True)
            
        with col2:
            st.markdown("##### 🎯 Clasificación de Normativa y Topología")
            fig_sun = px.sunburst(
                df_projects, 
                path=['Nivel', 'Topología', 'Conductor'], 
                values='Cantidad',
                color='Nivel',
                color_discrete_map={"MT (Alta Tensión)": "#FF4B4B", "BT (Baja Tensión)": "#00CC96"},
            )
            fig_sun.update_traces(textinfo="label+percent entry")
            fig_sun.update_layout(margin=dict(t=0, l=0, r=0, b=0))
            st.plotly_chart(fig_sun, use_container_width=True)
            
        st.info("💡 Con este gráfico circular separamos visualmente el ámbito de la Alta Tensión de la Baja Tensión y sus respectivas topologías permitidas.")

        # --- SECCIÓN DE BIBLIOGRAFÍA Y VERIFICACIÓN ---
        st.divider()
        st.markdown("##### 📚 Bibliografía y Marco Legal de Referencia")
        st.write("Utilice los siguientes enlaces oficiales para verificar los límites de tensión, topologías y métodos de instalación empleados en estos cálculos:")

        c_link1, c_link2 = st.columns(2)
        with c_link1:
            st.link_button(
                "📜 REBT (Baja Tensión) - BOE", 
                "https://www.boe.es/buscar/act.php?id=BOE-A-2002-18099",
                use_container_width=True,
                help="Real Decreto 842/2002: Reglamento Electrotécnico para Baja Tensión."
            )
        with c_link2:
            st.link_button(
                "⚡ RAT (Alta Tensión) - BOE", 
                "https://www.boe.es/buscar/act.php?id=BOE-A-2014-6084",
                use_container_width=True,
                help="Real Decreto 337/2014: Reglamento de condiciones técnicas y garantías de seguridad en instalaciones eléctricas de alta tensión."
            )
        
        st.caption("Nota: Las clasificaciones ITC-BT e ITC-LAT mostradas en la tabla corresponden a las Instrucciones Técnicas Complementarias de los reglamentos arriba citados.")
    # ==============================================================================
    # TAB 2: ANÁLISIS DE MATERIALES
    # ==============================================================================
    with tab_materials:
        st.subheader("Propiedades Físicas y Eléctricas") #La función subheader es para el título del
        #encabezado de la sección.
        
        #A continuación definimos un DataFrame, que es como una
        #tabla con las propiedades de los materiales.

        #NOTA: los valores de las conductividades de los materiales
        #y los costes estimados son aproximados para fines educativos, pero
        #en la realidad fluctúan según el fabricante y las condiciones del mercado.

        #NOTA: En el caso de la propiedad de Resistencia a la Tracción y Módulo de Young, 
        #DEPENDE DEL TRATAMIENTO que se le aplique al material, arrojan un valor u otro.
        #Por ejemplo, para el cobre, si se aplica un recocido en tiras, el valor de resistencia
        #de tracción puede ser de 220 Mpa. Sin embargo, si se le aplica un revenido de resorte,
        #su valor asciende a los 379 Mpa. 
        
        materials_data = {
            "Material": ["Cobre", "Aluminio (AAC)", "Aluminio-Acero (ACSR)"],
            "Conductividad a temperatura de 20ºC (m/Ωmm²)": [56.0, 36.0, 34.0],
            "Coste Estimado (€/km)": [1200, 700, 850],
            "Resistencia Tracción Max (MPa)": [450, 160, 1500],
            "Módulo Young Max (GPa)": [125, 70, 75]
        }
        df_mat = pd.DataFrame(materials_data)
        
        #Usamos "st.dataframe(...)"" para mostrar el DataFrame.
        st.dataframe(df_mat.style.highlight_max(axis=0, color="#2c5e2e"), use_container_width=True)
        
        #A continuación, por columnas, dos gráficos distintos. 
        #En el primero comparamos la RESISTENCIA A LA TRACCIÓN MECÁNICA, MIENTRAS
        #QUE EN EL SEGUNDO COMPARAREMOS LA CONDUCTIVIDAD ELÉCTRICA.
        #Para ello usamos las funciones PLOTLY_CHART Y PX.BAR.
        c1, c2 = st.columns(2)
        with c1:
            fig_tensile = px.bar(df_mat, x="Material", y="Resistencia Tracción Max (MPa)", 
                                 color="Material", title="Resistencia a la Tracción Mecánica")
            st.plotly_chart(fig_tensile, use_container_width=True)
        with c2:
            fig_cond = px.bar(df_mat, x="Material", y="Conductividad a temperatura de 20ºC (m/Ωmm²)", 
                              color="Material", title="Conductividad Eléctrica")
            st.plotly_chart(fig_cond, use_container_width=True)

        st.divider()
        
      #SIMULADOR BÁSICO DE CÁLCULOS DE LÍNEA:
      
      #INTRODUCIMOS EL ELEMENTO DE LOS CONTROLES:
      #Son las casillas donde el usuario introduce los datos. 
      #y luego usamos la función NUMBER_INPUT para que el usuario pueda introducir los datos.

        col_sim1, col_sim2, col_sim3 = st.columns(3)
        load_va = col_sim1.number_input("Carga Aparente (VA)", value=1000)
        voltage_sys = col_sim2.number_input("Tensión Sistema (V)", value=400) # <--- DEFINICIÓN
        section_sim = col_sim3.number_input("Sección (mm²)", value=2.5)

        #CÁLCULOS BASE
        dist_km = np.linspace(0, 2, 100) 
        dist_m = dist_km * 1000
        current_load = load_va / (np.sqrt(3) * voltage_sys)

        #GENERACIÓN DEL DATAFRAME
        df_sim_list = []

        #El usuario puede elegir entre tres apartados, que 
        #DEFINIMOS COMO COLUMNAS. 

        for index, row in df_mat.iterrows():
            mat_name = row["Material"]
            sigma = row["Conductividad a temperatura de 20ºC (m/Ωmm²)"]
            cost_unit = row["Coste Estimado (€/km)"]
            
            R_vec = dist_m / (sigma * section_sim)
            V_drop = np.sqrt(3) * current_load * R_vec
            Power_loss = 3 * (current_load**2) * R_vec
            Cost_total = cost_unit * dist_km
            
            df_temp = pd.DataFrame({
                "Distancia (km)": dist_km,
                "Caída Tensión (V)": V_drop,
                "Pérdida Potencia (W)": Power_loss,
                "Coste (€)": Cost_total,
                "Material": mat_name
            })
            df_sim_list.append(df_temp)

        df_simu_final = pd.concat(df_sim_list) # <--- DEFINICIÓN FINAL

        #PARA MOSTRAR LAS FÓRMULAS LATEX
        plot_type = st.radio("Seleccione variable a analizar:", 
                            ["Caída Tensión (V)", "Pérdida Potencia (W)", "Coste (€)"], 
                            horizontal=True)

        with st.expander("Ver base matemática del cálculo", expanded=True):
            st.latex(r"I = \frac{S}{\sqrt{3} \cdot V_{sys}}")
            if plot_type == "Caída Tensión (V)":
                st.latex(r"\Delta V = \sqrt{3} \cdot I \cdot R \quad ; \quad R = \frac{L}{\sigma \cdot S}")
            elif plot_type == "Pérdida Potencia (W)":
                st.latex(r"P_{loss} = 3 \cdot I^2 \cdot R")
            else:
                st.latex(r"Coste = C_{u} \cdot L")

        #REPRESENTAMOS COMO GRÁFICA FINAL
        fig_sim = px.line(df_simu_final, x="Distancia (km)", y=plot_type, color="Material",
                        title=f"Evolución de {plot_type} según Distancia")

        if plot_type == "Caída Tensión (V)":
            limit_v = voltage_sys * 0.05
            fig_sim.add_hline(y=limit_v, line_dash="dash", line_color="red", 
                            annotation_text=f"Límite REBT 5% ({limit_v:.1f}V)")

        st.plotly_chart(fig_sim, use_container_width=True)

        st.info("💡 Debe añadirse que los valores de los costes son estimados, por lo que supone información meramente educativa.")

        # --- NUEVA SECCIÓN DE BIBLIOGRAFÍA Y ENLACES REALES ---
        st.divider()
        st.markdown("### 📚 Verificación de Datos y Bibliografía")
        st.write("Para contrastar los valores de conductividad, propiedades mecánicas y costes actuales, puede consultar las siguientes fuentes oficiales:")

        # Organizamos los enlaces en columnas para una estética 10/10
        c_ref1, c_ref2, c_ref3 = st.columns(3)

        with c_ref1:
            st.link_button(
                "📈 Precios del Cobre (LME)", 
                "https://www.lme.com/en/Metals/Non-ferrous/LME-Copper",
                use_container_width=True,
                help="Consulta el precio real del Cobre en el London Metal Exchange"
            )
        
        with c_ref2:
            st.link_button(
                "📉 Precios del Aluminio (LME)", 
                "https://www.lme.com/en/Metals/Non-ferrous/LME-Aluminium",
                use_container_width=True,
                help="Consulta el precio real del Aluminio en el London Metal Exchange"
            )

        with c_ref3:
            st.link_button(
                "📜 Norma UNE 20003", 
                "https://www.une.org/encuentra-tu-norma/busca-tu-norma/norma?c=N0003058",
                use_container_width=True,
                help="Norma sobre el valor normalizado de la conductividad del Cobre"
            )

        with st.expander("📖 Referencias Bibliográficas Técnicas"):
            st.markdown("""
            **Fuentes empleadas para el desarrollo de este módulo:**
            1. **García Trasancos, J.** (2018). *Instalaciones Eléctricas en Media y Baja Tensión*. Ed. Paraninfo. (Referencia principal para conductividad y cálculos de línea).
            2. **Standard IACS** (International Annealed Copper Standard): Define el valor de conductividad del cobre recocido ($58 \\, MS/m$ a 20°C como 100% IACS).
            3. **ASTM B1, B2, B231/B232**: Estándares para la resistencia a la tracción y propiedades de conductores de aluminio (AAC) y reforzados con acero (ACSR).
            4. **Reglamento Electrotécnico para Baja Tensión (REBT)**: Real Decreto 842/2002, Instrucción Técnica Complementaria **ITC-BT-07** e **ITC-BT-06** para el cálculo de líneas.
            """)

   # =================================================================================
    # TAB 3: AISLAMIENTOS (Mejorada con Normativa REBT). SECCIÓN MERAMENTE INFORMATIVA
    # =================================================================================

    with tab_insulation:
        st.subheader("Comparativa Técnica: PVC vs XLPE")
        
        col_text, col_plot = st.columns([1, 1.5])
        
        with col_text:
            st.info("💡 **Contexto:** La elección del aislamiento del cable es crucial " \
                    "para la seguridad y eficiencia de las instalaciones eléctricas.")
            
            st.markdown("""
            ### 🌡️ Diferencias Térmicas
            * **PVC (Termoplástico):** Se ablanda con el calor. Límite **70°C**.
            * **XLPE (Termoestable):** Mantiene estructura. Límite **90°C**.
            
            ### 🔥 Comportamiento al Fuego
            * **PVC:** Emite humo negro y ácido (Corrosivo).
            * **XLPE (Libre de Halógenos):** Humo blanco, no tóxico.
            """)
            
            # --- BLOQUE DE NORMATIVA CON TABLA OFICIAL ---
            with st.expander("📜 Ver Normativa REBT Asociada"):
                st.markdown("""
                **1. ITC-BT-19 (Instalaciones Interiores):**
                * El **XLPE (90°C)** permite aproximadamente un **22% más de capacidad** de carga que el **PVC (70°C)**.
                """)

                rebt_data = {
                    "Sección (mm²)": [1.5, 2.5, 4, 6, 10, 16, 25, 35, 50, 70, 95, 120, 150, 185, 240],
                    "PVC 70°C (A)": [15, 21, 28, 36, 50, 68, 89, 110, 134, 171, 207, 239, 272, 310, 364],
                    "XLPE 90°C (A)": [18, 26, 34, 44, 61, 82, 108, 135, 164, 211, 254, 294, 335, 382, 453]
                }
                df_rebt = pd.DataFrame(rebt_data)
                st.write("**Intensidades Admisibles (A) - Referencia: Cobre, Método C**")
                st.table(df_rebt) 
                st.caption("Valores según norma UNE 20460-5-523.")

            # --- NUEVA SECCIÓN DE BIBLIOGRAFÍA ---
            st.divider()
            st.markdown("### 📚 Bibliografía y Verificación")
            st.write("Consulte las fuentes oficiales para contrastar estos datos:")
            
            c_link1, c_link2 = st.columns(2)
            with c_link1:
                st.link_button("📄 REBT ITC-BT-19 (BOE)", 
                            "https://industria.gob.es/Calidad-Industrial/seguridadindustrial/instalacionesindustriales/baja-tension/Documents/bt/guia_bt_19_feb09R2.pdf")
            with c_link2:
                st.link_button("📘 Modelo degradación térmica Arrhenius (pág 15, forma logarítmica)", 
                            "http://www.scielo.org.co/pdf/rium/v12n23/v12n23a10.pdf")

        with col_plot:
            # --- EXPLICACIÓN MATEMÁTICA ---
            st.markdown("##### Modelo de Degradación Térmica")
            st.latex(r"R(T) = R_0 \cdot e^{-\alpha \cdot (T - T_{ref})}")
            
            # 

            st.info("Empleamos la curva exponencial para modelar la degradación de la resistencia de aislamiento con la temperatura.")
            
            temp_range = np.arange(20, 120, 5)
            R0 = 1000 
            R_pvc = R0 * np.exp(-0.045 * (temp_range - 20))
            R_xlpe = R0 * np.exp(-0.035 * (temp_range - 20))
            
            df_iso = pd.DataFrame({
                "Temperatura (°C)": np.concatenate([temp_range, temp_range]),
                "Resistencia Aislamiento (Relativa)": np.concatenate([R_pvc, R_xlpe]),
                "Tipo": ["PVC (70°C Max)", "XLPE (90°C Max)"] * len(temp_range)
            })
            
            fig_iso = px.line(df_iso, x="Temperatura (°C)", y="Resistencia Aislamiento (Relativa)", 
                            color="Tipo", title="Resistencia de Aislamiento vs Temperatura",
                            color_discrete_map={"PVC (70°C Max)": "#EF553B", "XLPE (90°C Max)": "#00CC96"})
            
            fig_iso.add_vrect(x0=70, x1=120, fillcolor="red", opacity=0.1, 
                            annotation_text="Fallo PVC", annotation_position="top left")
            fig_iso.add_vline(x=90, line_dash="dash", line_color="green", annotation_text="Límite XLPE")

            st.plotly_chart(fig_iso, use_container_width=True)
            st.info("💡 **Conclusión:** La menor pendiente del XLPE indica mayor estabilidad dieléctrica frente al calor.")

    
    # ==============================================================================
    # TAB 4: LABORATORIO DE CÁLCULO (Actualizado con Bibliografía)
    # ==============================================================================
    with tab_calc:
        st.subheader("Cálculo de Escenarios (Alumnos A, B, C)")

        st.info("Bienvenido al laboratorio de cálculo. En este laboratorio podrá calcular distintos parámetros relativos a sus líneas"
                " eléctricas así como consultar en una tabla la comparación cuantitativa de las corrientes.")
        
        # --- EXPLICACIÓN TÉCNICA (LaTeX) ---
        with st.expander("📖 Ver fórmulas de cálculo empleadas"):
            st.markdown("Para el análisis de estas líneas se han empleado las siguientes ecuaciones fundamentales:")

            st.markdown("**1. Resistencia Óhmica del Conductor ($R$):**")
            st.latex(r"R = \frac{L}{\sigma \cdot S} \quad [\Omega]")
            
            st.markdown("**2. Intensidad de Corriente Trifásica ($I$):**")
            st.latex(r"I = \frac{P \cdot 1000}{\sqrt{3} \cdot V_{line} \cdot \cos(\phi)} \quad [A]")
            
            st.markdown("**3. Caída de Tensión por Fase ($\Delta V_{fase}$):**")
            st.latex(r"\Delta V_{fase} = I \cdot R \quad [V]")
            
            st.caption("Donde: L=Longitud(m), σ=Conductividad(m/Ωmm²), S=Sección(mm²), P=Potencia(kW), V=Tensión(V).")

        st.divider()

        # --- PARÁMETROS GLOBALES ---
        col_params1, col_params2 = st.columns(2)
        v_line = col_params1.number_input("Tensión de Línea del Sistema (V)", value=400, help="Tensión entre fases (U)")
        s_cond = col_params2.number_input("Sección del Conductor Seleccionada (mm²)", value=95, step=1)
        sigma_cu = 56.0  # Conductividad del Cobre a 20°C

        # --- TABLA EDITABLE ---
        st.markdown("##### 📝 Datos de entrada por escenario")
        st.write("Puede modificar o añadir filas directamente en la tabla:")
        
        default_data = pd.DataFrame([
            {"Alumno": "A", "Longitud (m)": 500.0, "Potencia (kW)": 50.0, "Cos phi": 0.80},
            {"Alumno": "B", "Longitud (m)": 1200.0, "Potencia (kW)": 150.0, "Cos phi": 0.90},
            {"Alumno": "C", "Longitud (m)": 2500.0, "Potencia (kW)": 300.0, "Cos phi": 0.85},
        ])
        
        edited_df = st.data_editor(default_data, num_rows="dynamic", use_container_width=True)
        
        if st.button("🚀 Ejecutar Cálculos de Laboratorio"):
            results_df = edited_df.copy()
            
            # Cálculos internos
            results_df["R (Ω)"] = results_df["Longitud (m)"] / (sigma_cu * s_cond)
            results_df["I (A)"] = (results_df["Potencia (kW)"] * 1000) / (np.sqrt(3) * v_line * results_df["Cos phi"])
            results_df["Caída V (Fase)"] = results_df["I (A)"] * results_df["R (Ω)"]
            v_phase = v_line / np.sqrt(3)
            results_df["% dU"] = (results_df["Caída V (Fase)"] / v_phase) * 100

            st.success("✅ Cálculos realizados con éxito")
            
            st.dataframe(results_df.style.format({
                "Longitud (m)": "{:.1f}", "Potencia (kW)": "{:.1f}", "Cos phi": "{:.2f}",
                "R (Ω)": "{:.4f}", "I (A)": "{:.2f}", "Caída V (Fase)": "{:.2f} V", "% dU": "{:.2f} %"
            }), use_container_width=True)
            
            fig = px.bar(results_df, x="Alumno", y="I (A)", color="Alumno", 
                         title="Comparativa de la corriente circulante por escenario", text_auto='.2f')
            st.plotly_chart(fig, use_container_width=True)

        # --- NUEVA SECCIÓN DE BIBLIOGRAFÍA TÉCNICA ---
        st.divider()
        st.markdown("### 📚 Bibliografía y Referencias Técnicas")
        st.write("Para validar la precisión de estos cálculos y las fórmulas trifásicas empleadas, puede consultar la siguiente bibliografía de referencia:")

        c_bib1, c_bib2 = st.columns(2)
        with c_bib1:
            st.link_button(
                "📘 Circuitos Eléctricos de Jesús Fraile Mora", 
                "https://www.amazon.es/Circuitos-el%C3%A9ctricos-Jes%C3%BAs-Mora-Fraile/dp/8483227959/ref=sr_1_6?adgrpid=1307319760186315&dib=eyJ2IjoiMSJ9.KFQOcft10JCAJnUhA8jpkW9S64dGJBYu1lsNgRpU-HJExDkzYx5sXt10urwzqAf0Hq6nGgPpRZFrN9sCjA5knkMvQsy0Ins3aumuGA836cag_aD5-DloiI_4smiAXd_B.46ejHI1VxjfotA4kkHB2AchCrvbPEsGZd5iGl4Wlg-A&dib_tag=se&hvadid=81707573597660&hvbmt=be&hvdev=c&hvlocphy=164439&hvnetw=o&hvqmt=e&hvtargid=kwd-81707719375523%3Aloc-170&hydadcr=21565_1856291&keywords=circuitos+electricos+jesus+fraile+mora&mcid=4961cba1a0d137a882b4f0cc5f19c446&msclkid=8e68e9e0cded18aa096e80de683fc91d&qid=1765713388&sr=8-6",
                use_container_width=True,
                help="Libro de cabecera en ingeniería para el cálculo de líneas eléctricas."
            )
        
        st.caption("Nota: Las fórmulas empleadas corresponden al modelo de línea de transporte corta (parámetros concentrados) despreciando el efecto capacitivo, estándar en cálculos de Baja Tensión.")

    # ==============================================================================
    # TAB 5: ASISTENTE DE DISEÑO (Optimizado con Base Teórica)
    # ==============================================================================
    # ==============================================================================
    # TAB 5: ASISTENTE DE DISEÑO (Actualizado con Bibliografía Real)
    # ==============================================================================
    with tab_wizard:
        st.subheader("Asistente Inteligente de Selección de Línea")
        st.markdown("""
        Este módulo actúa como un sistema experto preliminar. Evalúa la viabilidad técnica y 
        económica basándose en la normativa vigente y el análisis de ciclo de vida.
        """)

        # --- SECCIÓN DE TEORÍA APLICADA ---
        with st.expander("📖 Fundamentos de Selección (Criterios de Ingeniería)"):
            col_t1, col_t2 = st.columns(2)
            with col_t1:
                st.markdown("**Criterio de Material (Económico-Técnico):**")
                st.write("""
                La elección entre Cobre (Cu) y Aluminio (Al) no es solo de coste inicial. 
                El Cu tiene menor resistividad, lo que reduce las pérdidas por efecto Joule:
                """)
                st.latex(r"P_{pérdidas} = 3 \cdot I^2 \cdot \frac{L}{\sigma \cdot S}")
                st.info("A largo plazo (>30 años), el ahorro en pérdidas del Cobre suele compensar su mayor precio inicial.")
            
            with col_t2:
                st.markdown("**Criterio de Topología (Seguridad y Entorno):**")
                st.write("""
                La normativa distingue entre líneas de Media Tensión (MT > 1kV) y Baja Tensión (BT ≤ 1kV).
                La elección aérea vs. subterránea depende de la densidad de carga y el coste:
                """)
                st.markdown("- **Aérea:** Mayor disipación térmica, menor coste ($\sim 1/3$ del subterráneo).")
                st.markdown("- **Subterránea:** Mayor seguridad, menor impacto visual (Obligatorio en zonas urbanas según REBT).")

        st.divider()

        # --- INTERFAZ DE ENTRADA ---
        st.markdown("##### ⚙️ Parámetros del Proyecto")
        c_wiz1, c_wiz2, c_wiz3 = st.columns(3)
        
        voltage_wiz = c_wiz1.number_input("Tensión de operación (V)", value=400, step=100, help="Define si aplica REBT o RAT")
        lifetime_wiz = c_wiz2.number_input("Vida útil del proyecto (años)", value=30, help="Influye en el Análisis de Ciclo de Vida")
        app_type = c_wiz3.selectbox("Tipo de Aplicación:", 
                            ["Alimentador Principal (Subestación -> Distribución)", 
                             "Distribución Local (Urbana/Interior)"])
        
        location_code = "main_feeder" if "Alimentador" in app_type else "local_distribution"
        
        if st.button("🚀 Generar Informe de Recomendación"):
            # --- LÓGICA DE RECOMENDACIÓN ---
            # 1. Justificación del Material
            if lifetime_wiz > 30:
                rec_material = "Cobre (Cu)"
                just_mat = "Debido a la larga vida útil, la alta conductividad del Cobre minimiza los costes operativos por pérdidas de energía."
                icon_mat = "💎"
            else:
                rec_material = "Aluminio (Al)"
                just_mat = "Para proyectos temporales o de corta duración, el Aluminio ofrece el menor tiempo de retorno de inversión (ROI)."
                icon_mat = "💰"
                
            # 2. Justificación de la Topología
            if voltage_wiz > 1000:
                nivel = "Media Tensión (MT)"
                if location_code == "main_feeder":
                    rec_topology = "Línea Aérea sobre Apoyos"
                    just_top = "Optimiza la disipación de calor por convección natural y reduce drásticamente el CAPEX en grandes distancias."
                else:
                    rec_topology = "Subterránea en Zanja"
                    just_top = "Necesaria por requerimientos de seguridad y protección ambiental en zonas de acceso público."
            else:
                nivel = "Baja Tensión (BT)"
                if location_code == "local_distribution":
                    rec_topology = "Subterránea (Bajo Tubo/Enterrada)"
                    just_top = "Cumplimiento con ITC-BT-07. Maximiza la seguridad ciudadana y estética urbana."
                else:
                    rec_topology = "Aérea Trenzada (Postes/Fachada)"
                    just_top = "Solución económica para electrificación rural o industrial de baja densidad."

            # --- RESULTADO VISUAL ---
            st.success("### ✅ Propuesta Técnica de Diseño")
            
            res_col1, res_col2 = st.columns(2)
            with res_col1:
                st.metric("Material Sugerido", rec_material)
                st.write(f"**Justificación:** {just_mat}")
            
            with res_col2:
                st.metric("Topología Sugerida", rec_topology)
                st.write(f"**Justificación:** {just_top}")
            
            st.divider()
            
            # --- NOTAS NORMATIVAS ---
            st.warning(f"**Nota Normativa:** Este proyecto se clasifica como una instalación de **{nivel}**. " + 
                       ("Debe cumplir con el Reglamento de Alta Tensión (RAT)." if voltage_wiz > 1000 else "Debe cumplir con el Reglamento Electrotécnico de Baja Tensión (REBT)."))

        # --- SECCIÓN FINAL DE BIBLIOGRAFÍA (Enlace Externo) ---
        st.markdown("---")
        st.markdown("### 📚 Bibliografía y Marco Legal")
        st.write("Para verificar los criterios de diseño, límites de tensión y propiedades de materiales, consulte la documentación oficial:")
        
        c_link1, c_link2 = st.columns(2)
        with c_link1:
            st.link_button("📜 REBT (Baja Tensión) - BOE", "https://www.boe.es/buscar/act.php?id=BOE-A-2002-18099")
            st.caption("Real Decreto 842/2002: Referencia para topologías subterráneas (ITC-BT-07) y aéreas (ITC-BT-06).")
        
        with c_link2:
            st.link_button("⚡ RAT (Alta Tensión) - BOE", "https://www.boe.es/buscar/act.php?id=BOE-A-2014-6084")
            st.caption("Real Decreto 337/2014: Criterios para líneas de Media y Alta Tensión.")

        with st.expander("🔍 Ver Referencias Bibliográficas Técnicas"):
            st.markdown("""
            1. **García Trasancos, J.** (2018). *Instalaciones Eléctricas en Media y Baja Tensión*. Ed. Paraninfo.
            2. **Gil Carrillo, F.** (2015). *Líneas Eléctricas*. Universidad de Almería.
            3. **Leonardo Energy / European Copper Institute**: *Guide to high-efficiency conductor sizing*.
            """)