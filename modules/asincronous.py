import streamlit as st
import numpy as np
import pandas as pd
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import math

# ==============================================================================
# BLOQUE 1: MOTOR DE CÁLCULO (FÍSICA DEL MOTOR ASÍNCRONO)
# ==============================================================================

def calcular_parametros_motor(U_linea, f, p, R1, X1, R2_prim, X2_prim, Xm, s):
    """
    Calcula el comportamiento del motor para un deslizamiento 's' dado.
    Utiliza el circuito equivalente por fase (Modelo de Steinmetz).
    """
    # Frecuencia angular y velocidad de sincronismo
    omega_s = 2 * math.pi * f
    n_sync = (60 * f) / p
    
    # Tensión de fase (suponiendo conexión en Estrella)
    U_fase = U_linea / math.sqrt(3)
    
    if s == 0: return 0, 0, n_sync # Evitar división por cero en vacío
    
    # Fórmula simplificada del par (Kloss o similar para la plantilla)
    omega_m_sync = (2 * math.pi * n_sync) / 60
    V_th = U_fase 
    I2_prim = V_th / math.sqrt((R1 + R2_prim/s)**2 + (X1 + X2_prim)**2)
    Par = (3 * I2_prim**2 * R2_prim) / (s * omega_m_sync)
    
    n_rotor = n_sync * (1 - s)
    
    return Par, I2_prim, n_rotor

# ==============================================================================
# BLOQUE PRINCIPAL: INTERFAZ DE STREAMLIT (APP)
# ==============================================================================

def app():
    st.header("⚙️ TEMA 2: Máquinas Asíncronas (Motores de Inducción)")
    st.caption("Análisis del motor de jaula de ardilla y rotor devanado según la metodología de Fraile Mora.")

# Definición de Pestañas (Asegúrate de que hay 9 variables y 9 textos)
    tab_fundamentos, tab_circuito, tab_curvas, tab_ensayos, tab_arranque, tab_balance, tab_placa, tab_factores, tab_ferraris = st.tabs([
        "2.1 - Fundamentos",
        "2.2 - Circuito",
        "2.3 - Curva Par-Vel.",
        "2.4 - Ensayos",
        "2.5 - Arranque",
        "2.6 - Balance",
        "2.7 - Placa",
        "2.8 - Factores 'K'",
        "2.9 - Teorema de Ferraris"
    ])

    # --------------------------------------------------------------------------
    # PESTAÑA 2.1: FUNDAMENTOS
    # --------------------------------------------------------------------------
    with tab_fundamentos:
        st.markdown("### ⚡ Principio de Funcionamiento: Inducción Electromagnética")
        st.write("El motor asíncrono no recibe corriente eléctrica directamente en el rotor. Su funcionamiento se basa enteramente en la inducción electromagnética, gobernada por las leyes de **Faraday y Lenz**.")
        
        col_teoria1, col_teoria2 = st.columns(2)
        
        with col_teoria1:
            st.markdown("#### 1. Flujo Magnético y Ley de Faraday")
            st.write("El flujo magnético ($\Phi$) que atraviesa una superficie $S$ debido a un campo magnético de densidad $\vec{B}$ se define como:")
            st.latex(r"\Phi = \iint_S \vec{B} \cdot d\vec{S}")
            
            st.write("La **Ley de Faraday** establece que cualquier variación temporal del flujo magnético que atraviesa un circuito induce una Fuerza Electromotriz (f.e.m. o tensión) en él. La **Ley de Lenz** añade el signo negativo, indicando que la f.e.m. inducida se opone a la causa que la produce:")
            st.latex(r"e(t) = -N \frac{d\Phi(t)}{dt}")
            st.caption("Donde $N$ es el número de espiras del devanado.")

        with col_teoria2:
            st.markdown("#### 2. Ecuación Fundamental de las Máquinas de C.A.")
            st.write("Si asumimos que el flujo en el entrehierro varía de forma senoidal en el tiempo (debido al campo giratorio creado por el estator):")
            st.latex(r"\Phi(t) = \Phi_{max} \cdot \cos(\omega t)")
            
            st.write("Derivando para encontrar la f.e.m. instantánea:")
            st.latex(r"e(t) = -N \frac{d}{dt} [\Phi_{max} \cos(\omega t)] = N \cdot \omega \cdot \Phi_{max} \cdot \sin(\omega t)")
            
            st.write("El valor eficaz (RMS) de esta tensión se obtiene dividiendo la amplitud entre $\sqrt{2}$. Sabiendo que $\omega = 2\pi f$:")
            st.latex(r"E = \frac{N \cdot 2\pi f \cdot \Phi_{max}}{\sqrt{2}} \approx 4.44 \cdot f \cdot N \cdot \Phi_{max}")

        st.markdown("---")
        
        # NUEVA SECCIÓN EXTENSA SOLICITADA
        st.markdown("### 🌀 Cinemática del Motor: Sincronismo, Rotor y Deslizamiento")
        st.write("Para entender cómo se produce el movimiento en un motor asíncrono, es fundamental analizar la relación entre la velocidad del campo magnético (generado eléctricamente) y la velocidad de giro físico del rotor. En esta interacción reside la esencia de su funcionamiento.")

        st.markdown("#### 1. Velocidad de Sincronismo ($n_s$)")
        st.write("El **Teorema de Ferraris** demuestra que al aplicar un sistema trifásico equilibrado de corrientes a un conjunto de bobinas desfasadas 120º geométricamente en el estator, se crea un **campo magnético de amplitud constante que gira** continuamente. La velocidad a la que rota este campo invisible se denomina **Velocidad de Sincronismo**.")
        st.latex(r"n_s = \frac{60 \cdot f_1}{p} \quad [\text{rpm}]")
        
        st.write("Donde:")
        st.markdown("""
        * $f_1$: Frecuencia de la red eléctrica que alimenta al estator (ej. 50 Hz).
        * $p$: Número de pares de polos magnéticos (depende de cómo se bobinó el motor en fábrica).
        * $60$: Factor para convertir la velocidad de revoluciones por segundo (Hz) a revoluciones por minuto (rpm).
        """)
        st.write("En unidades del Sistema Internacional (rad/s), la velocidad angular síncrona se expresa como:")
        st.latex(r"\omega_s = \frac{2\pi \cdot n_s}{60} = \frac{2\pi \cdot f_1}{p} \quad [\text{rad/s}]")

        st.markdown("#### 2. Velocidad Mecánica del Rotor ($n$)")
        st.write("Es la velocidad física a la que gira el eje del motor acoplado a nuestra carga. En un motor asíncrono en funcionamiento como motor, **el rotor nunca puede alcanzar la velocidad de sincronismo** ($n < n_s$).")
        st.info("**¿Por qué es imposible que $n = n_s$?**\n\nLas barras o el devanado del rotor giran para intentar 'alcanzar' al campo magnético. Si el rotor girase exactamente a la velocidad del campo ($n_s$), ambas partes viajarían juntas y solidarias. El campo magnético ya no 'cortaría' las barras del rotor. Sin este corte continuo de líneas de flujo, la variación de flujo sería cero ($d\Phi/dt = 0$), la f.e.m. inducida desaparecería, no habría corrientes rotóricas y, por ende, el **par electromagnético caería a cero**. El motor necesita esa diferencia de velocidad para seguir empujando.")

        st.markdown("#### 3. El Deslizamiento ($s$)")
        st.write("A esta diferencia o retraso vital entre la velocidad del campo y la del rotor se la conoce como **Deslizamiento**. Es el puente de unión en todas las ecuaciones entre el mundo eléctrico y el mecánico.")
        
        col_desl1, col_desl2 = st.columns(2)
        with col_desl1:
            st.write("**Deslizamiento Absoluto:**")
            st.write("Es simplemente la diferencia en rpm entre el campo y el rotor.")
            st.latex(r"n_{deslizamiento} = n_s - n \quad [\text{rpm}]")
        with col_desl2:
            st.write("**Deslizamiento Relativo ($s$):**")
            st.write("Es el valor porcentual o *per unit* (p.u.) de esa pérdida de velocidad respecto a la velocidad teórica.")
            st.latex(r"s = \frac{n_s - n}{n_s}")

        st.write("A partir de la fórmula del deslizamiento, podemos despejar matemáticamente la **Velocidad Mecánica del Rotor** ($n$) en función del deslizamiento del punto de trabajo:")
        st.latex(r"n = n_s \cdot (1 - s)")
        st.latex(r"\omega_m = \omega_s \cdot (1 - s) \quad [\text{rad/s}]")

        st.markdown("#### ⚡ Consecuencia Analítica: La Frecuencia Rotórica ($f_2$)")
        st.write("Dado que el rotor gira a $n$ rpm y el campo a $n_s$ rpm, el devanado rotórico percibe que el campo magnético le adelanta a una velocidad relativa de $n_s - n$. Esta velocidad relativa es la que determina la **frecuencia de las corrientes que circularán por el rotor ($f_2$)**.")
        st.latex(r"f_2 = \frac{p \cdot (n_s - n)}{60}")
        st.write("Si sustituimos la expresión del deslizamiento ($n_s - n = s \cdot n_s$) en esta ecuación:")
        st.latex(r"f_2 = \frac{p \cdot (s \cdot n_s)}{60} = s \cdot \left(\frac{p \cdot n_s}{60}\right)")
        st.write("Recordando la fórmula de $n_s$, el término entre paréntesis es exactamente la frecuencia de red ($f_1$). Esto nos da la relación fundamental de frecuencias de la máquina asíncrona:")
        st.latex(r"f_2 = s \cdot f_1")
        
        st.success("**Ejemplo Práctico:**\nEn el instante del **arranque** (motor parado, $n=0$), el deslizamiento es máximo ($s=1$). Por tanto, $f_2 = f_1$ (50 Hz). El motor se comporta temporalmente como un transformador estático. Cuando el motor alcanza su **régimen de trabajo nominal**, el deslizamiento suele ser minúsculo ($s \approx 0.02$ a $0.05$). Esto significa que en condiciones normales, las corrientes que circulan por el rotor oscilan a bajísimas frecuencias ($f_2 \approx 1$ a $2.5 \text{ Hz}$).")


    # --------------------------------------------------------------------------
    # PESTAÑA 2.2: CIRCUITO EQUIVALENTE
    # --------------------------------------------------------------------------
    with tab_circuito:
        st.markdown("### 💡 Modelo Analítico de Steinmetz (Por fase)")
        st.write("""
        El motor asíncrono puede estudiarse analógicamente como un **transformador cuyo secundario está en cortocircuito y gira**. 
        Sin embargo, al girar, la frecuencia de las corrientes del rotor ($f_2 = s \cdot f_1$) es distinta a la del estator. 
        Para poder unir ambos circuitos eléctricamente, se reducen las magnitudes del rotor al estator (multiplicando por la relación de transformación efectiva) y se divide la impedancia rotórica entre el deslizamiento ($s$).
        """)

        st.markdown("---")

        col_exacto, col_aprox = st.columns(2)

        with col_exacto:
            st.markdown("#### 1️⃣ Circuito Equivalente Exacto")
            st.write("Representa fielmente el motor conectando la rama en derivación (magnetización y pérdidas en el hierro) en el medio de la red, tras la caída de tensión en la impedancia del estator.")
            st.code("""
      I1        R1       jX1       I'2      jX'2      R'2/s
 U1 >----->----[  ]-----[  ]---+----->-----[  ]------[  ]----o
                               |                             |
                               +--[  ]-- RFe                 |
                               |                             |
                               +--[  ]-- jXm                 |
                               |                             |
    >--------------------------+-----------------------------o
            """, language="text")
            
            st.markdown("**Ecuaciones de malla:**")
            st.latex(r"\vec{U}_1 = \vec{I}_1 (R_1 + jX_1) + \vec{E}_1")
            st.latex(r"\vec{E}_1 = \vec{I}'_2 \left( \frac{R'_2}{s} + jX'_2 \right)")
            st.latex(r"\vec{I}_1 = \vec{I}_0 + \vec{I}'_2")

        with col_aprox:
            st.markdown("#### 2️⃣ Circuito Equivalente Aproximado")
            st.write("Para simplificar cálculos manuales, se traslada la rama transversal a la entrada. El error cometido es mínimo (especialmente en motores grandes) ya que la caída de tensión estatórica debida a la corriente de vacío ($I_0$) es muy pequeña.")
            st.code("""
                I0                 I1 ≈ I'2   R1+R'2/s   j(X1+X'2)
 U1 >-----+-----+-------------------->-------[   ]------[   ]----o
          |     |                                                |
          +-[ ]-+ RFe                                            |
          |     |                                                |
          +-[ ]-+ jXm                                            |
          |                                                      |
    >-----+------------------------------------------------------o
            """, language="text")
            
            st.markdown("**Simplificación (Impedancia de cortocircuito):**")
            st.latex(r"\vec{Z}_{cc} = (R_1 + \frac{R'_2}{s}) + j(X_1 + X'_2)")
            st.latex(r"\vec{I}'_2 \approx \frac{\vec{U}_1}{\vec{Z}_{cc}}")

        st.markdown("---")
        st.markdown("#### 🧩 Desdoblamiento de la Resistencia Rotórica")
        st.write("""
        En el circuito equivalente, la resistencia rotórica reducida al estator aparece afectada por el deslizamiento ($R'_2/s$). Físicamente, esta resistencia ficticia se encarga de disipar tanto las **pérdidas por efecto Joule** en el rotor como la **potencia mecánica útil** que el motor entrega por el eje.
        
        Para visualizar esto explícitamente, la resistencia se desdobla en la suma de dos términos:
        """)
        
        st.latex(r"\frac{R'_2}{s} = R'_2 + R'_2 \left( \frac{1 - s}{s} \right)")
        
        col_r1, col_r2 = st.columns(2)
        with col_r1:
            st.info("**$R'_2$ (Resistencia real):**\nRepresenta el devanado del rotor. La potencia que consume representa las **Pérdidas en el Cobre del Rotor ($P_{Cu2}$)**.")
        with col_r2:
            st.success("**$R'_2 \\frac{1-s}{s}$ (Carga mecánica):**\nResistencia ficticia variable con la velocidad. La potencia que consume representa la **Potencia Mecánica Interna ($P_{mi}$)** transformada en el eje.")

    # --------------------------------------------------------------------------
    # PESTAÑA 2.3: CARACTERÍSTICA PAR-VELOCIDAD
    # --------------------------------------------------------------------------
    with tab_curvas:
        st.markdown("### 📈 Análisis de la Curva Característica Par-Velocidad")
        st.write("La curva de Par-Velocidad (o Par-Deslizamiento) es la huella dactilar del motor asíncrono. Nos permite comprender visualmente cuánta fuerza rotatoria es capaz de ejercer el motor desde el instante en que recibe corriente hasta que alcanza su régimen de trabajo continuo.")

        col_exp1, col_exp2 = st.columns([1.1, 1])

        with col_exp1:
            st.markdown("#### 🔍 Zonas de Funcionamiento Clave")
            st.markdown("""
            A lo largo de la curva podemos identificar hitos vitales para la operación de la máquina:
            
            * **1. Punto de Arranque ($s=1, n=0$):** El rotor está completamente quieto. El campo magnético gira a máxima velocidad relativa, cortando las barras del rotor. Se induce mucha f.e.m. y enormes corrientes, pero debido a la alta reactancia del rotor a esta frecuencia ($50$ Hz), el factor de potencia es pésimo y el **Par de Arranque** no es el máximo posible.
            * **2. Zona Inestable:** Abarca desde el arranque hasta el pico de la curva. Si acoplamos una carga mecánica que exija un par mayor al que el motor da en esta zona, el motor es incapaz de acelerar y se "cala".
            * **3. Par Máximo o Crítico ($M_{max}$):** Es el punto más alto de la montaña. Ocurre a un deslizamiento específico ($s_k$). Determina la capacidad máxima de sobrecarga del motor antes de detenerse abruptamente.
            * **4. Zona Estable (Régimen Nominal):** Es la ladera que cae de forma casi recta hacia la derecha. Aquí, si la carga frena ligeramente al motor (aumenta $s$), el motor responde entregando más par, alcanzando rápidamente un nuevo equilibrio. **Aquí trabaja el motor en la vida real**.
            * **5. Sincronismo ($s=0, n=n_s$):** El rotor gira exactamente a la misma velocidad que el campo magnético. No hay corte de líneas de flujo, no hay corriente inducida y el motor entrega **0 N·m de par**.
            """)

        with col_exp2:
            st.markdown("#### 📐 Desarrollo Analítico")
            st.write("Resolviendo el circuito equivalente exacto (mediante el Teorema de Thévenin), la ecuación fundamental del par electromagnético es:")
            
            st.latex(r"M = \frac{3 \cdot U_1^2 \cdot \frac{R'_2}{s}}{\omega_s \left[ \left(R_1 + \frac{R'_2}{s}\right)^2 + (X_1 + X'_2)^2 \right]}")
            
            st.info("""
            **Análisis de Límites (Comportamiento Asintótico):**
            * **Cerca del sincronismo (ZONA ESTABLE):** El deslizamiento $s$ es muy pequeño (ej: $0.02$). El término $R'_2/s$ se hace dominante en el denominador. Simplificando, el par queda directamente proporcional al deslizamiento: $M \propto s$. Esto explica por qué la curva es una **línea recta** al final.
            * **En el arranque (ZONA INESTABLE):** El deslizamiento $s$ es grande (cercano a 1). El denominador queda dominado por las reactancias. Simplificando, el par es inversamente proporcional al deslizamiento: $M \propto \frac{1}{s}$. Esto explica la forma de **hipérbola**.
            """)
            
            st.error("**⚠️ Regla de Oro:** Fíjate en el numerador. El par electromagnético es **proporcional al cuadrado de la tensión de red ($U_1^2$)**. Si en una fábrica la tensión cae un **10%**, ¡el motor perderá un **19%** de su capacidad de empuje!")

        st.markdown("---")
        st.markdown("#### 🕹️ Simulador de Curva en Tiempo Real")
        st.write("Modifica los parámetros eléctricos y de red en el panel izquierdo para ver cómo se transforma la curva Par-Velocidad instantáneamente.")

        c_in, c_plot = st.columns([1, 2.5])
        with c_in:
            st.markdown("**Datos de Placa y Red:**")
            u_l = st.number_input("Tensión Línea (V)", value=400, step=10)
            freq = st.number_input("Frecuencia (Hz)", value=50, step=5)
            pares_polos = st.slider("Pares de polos (p)", 1, 4, 1)
            
            st.markdown("**Parámetros del Rotor (Ω):**")
            r2_p = st.number_input("Resistencia R'2", value=0.4, step=0.1)
            x2_p = st.number_input("Reactancia X'2", value=1.2, step=0.1)
            
            st.markdown("**Parámetros del Estator (Ω):**")
            r1 = st.number_input("Resistencia R1", value=0.5, step=0.1)
            x1 = st.number_input("Reactancia X1", value=1.5, step=0.1)
            xm = 50.0 # Magnetización fija para este modelo didáctico
            
        with c_plot:
            # Generar array de deslizamientos (de s=1 a s=0)
            s_vec = np.linspace(0.001, 1.0, 300)
            curva_data = [calcular_parametros_motor(u_l, freq, pares_polos, r1, x1, r2_p, x2_p, xm, s) for s in s_vec]
            
            par_vec = [c[0] for c in curva_data]
            n_vec = [c[2] for c in curva_data]
            
            # Encontrar puntos críticos
            par_max = max(par_vec)
            idx_max = par_vec.index(par_max)
            n_max = n_vec[idx_max]
            par_arranque = par_vec[-1]
            n_sync_val = (60 * freq) / pares_polos

            fig = go.Figure()
            
            # Curva principal
            fig.add_trace(go.Scatter(x=n_vec, y=par_vec, name="Curva Par-Velocidad", line=dict(color="#00ADB5", width=4)))
            
            # Puntos clave
            fig.add_trace(go.Scatter(x=[0], y=[par_arranque], mode="markers+text", name="Arranque", 
                                     marker=dict(color="#F9A826", size=12), text=["Arranque"], textposition="top right"))
            fig.add_trace(go.Scatter(x=[n_max], y=[par_max], mode="markers+text", name="Par Máximo", 
                                     marker=dict(color="#FF4B4B", size=12), text=["Par Máximo"], textposition="top center"))
            fig.add_trace(go.Scatter(x=[n_sync_val], y=[0], mode="markers+text", name="Sincronismo", 
                                     marker=dict(color="#30363D", size=12), text=["Sincronismo"], textposition="top left"))

            # Sombreado de la zona estable
            fig.add_vrect(x0=n_max, x1=n_sync_val, fillcolor="#00ADB5", opacity=0.1, layer="below", line_width=0, annotation_text="Zona Estable", annotation_position="top right")

            fig.update_layout(
                title=f"Curva Par-Velocidad (Velocidad de Sincronismo: {n_sync_val:.0f} rpm)", 
                xaxis_title="Velocidad del Rotor (rpm)", 
                yaxis_title="Par Electromagnético (N·m)", 
                xaxis=dict(autorange="reversed"), # Invierte el eje X para que s vaya de 1 a 0 de izquierda a derecha
                legend=dict(yanchor="top", y=0.99, xanchor="left", x=0.01),
                margin=dict(t=50, b=40, l=40, r=40)
            ) 
            st.plotly_chart(fig, use_container_width=True)

    # --------------------------------------------------------------------------
    # PESTAÑA 2.4: ENSAYOS
    # --------------------------------------------------------------------------
    with tab_ensayos:
        st.markdown("### 🧪 Determinación de Parámetros")
        st.write("Cálculo de impedancias mediante el ensayo de vacío y el ensayo de rotor frenado (cortocircuito).")

    # --------------------------------------------------------------------------
    # PESTAÑA 2.5: ARRANQUE ESTRELLA-TRIÁNGULO
    # --------------------------------------------------------------------------
    with tab_arranque:
        st.markdown("### 🔄 Arranque Estrella-Triángulo (Y-Δ)")
        st.write("Mitigación de la corriente de inserción transitoria conectando inicialmente en Estrella y pasando a Triángulo en régimen.")
        st.info("Recordatorio: Corriente de línea y Par de arranque se reducen a 1/3 respecto a la conexión directa en Triángulo.")

    # --------------------------------------------------------------------------
    # PESTAÑA 2.6: BALANCE DE POTENCIAS
    # --------------------------------------------------------------------------
    with tab_balance:
        st.markdown("### ⚖️ Balance de Potencias en el Motor de Inducción")
        st.write("El diagrama de flujo de potencia ilustra cómo la energía eléctrica absorbida de la red se transforma, sufre pérdidas en el estator y rotor, y finalmente se entrega como energía mecánica en el eje. Este análisis es fundamental para determinar el **rendimiento ($ \eta $)** de la máquina.")

        col_b1, col_b2 = st.columns([1, 1])

        with col_b1:
            st.markdown("#### 📝 Ecuaciones del Flujo (Fraile Mora)")
            st.markdown("**1. Potencia Eléctrica Absorbida (Estator):**")
            st.latex(r"P_1 = \sqrt{3} \cdot U_L \cdot I_L \cdot \cos\varphi")
            
            st.markdown("**2. Potencia Electromagnética (Síncrona o del Entrehierro):**")
            st.write("Es la potencia que cruza el entrehierro tras restar las pérdidas en el cobre y hierro del estator.")
            st.latex(r"P_{ag} = P_1 - P_{Cu1} - P_{Fe} = 3 \cdot R'_2 \cdot \frac{I'^2_2}{s}")
            
            st.markdown("**3. Pérdidas en el Cobre del Rotor ($P_{Cu2}$):**")
            st.write("Dependen directamente del **deslizamiento ($s$)**. A mayor deslizamiento, mayores pérdidas en el rotor.")
            st.latex(r"P_{Cu2} = s \cdot P_{ag} = 3 \cdot R'_2 \cdot I'^2_2")
            
            st.markdown("**4. Potencia Mecánica Interna ($P_{mi}$):**")
            st.latex(r"P_{mi} = P_{ag} - P_{Cu2} = (1 - s) \cdot P_{ag}")
            
            st.markdown("**5. Potencia Útil en el Eje ($P_u$) y Rendimiento:**")
            st.write("Se restan las pérdidas mecánicas (rozamiento y ventilación) a la potencia interna.")
            st.latex(r"P_u = P_{mi} - P_{mec} \quad \implies \quad \eta = \frac{P_u}{P_1}")

        with col_b2:
            st.markdown("#### 📊 Simulador de Flujo (Diagrama Waterfall)")
            st.write("Observa la degradación de potencia con un ejemplo en tiempo real:")
            
            # Entradas para la simulación
            p1_in = st.number_input("Potencia Absorbida P1 (W)", value=10000, step=500)
            s_in = st.slider("Deslizamiento (s) ", 0.01, 0.10, 0.03, step=0.01, format="%.2f")
            p_cu1_in = st.number_input("Pérdidas Cobre Estator (W)", value=400, step=50)
            p_fe_in = st.number_input("Pérdidas Hierro (W)", value=300, step=50)
            p_mec_in = st.number_input("Pérdidas Mecánicas (W)", value=200, step=50)

            # Cálculos de balance
            p_ag_calc = p1_in - p_cu1_in - p_fe_in
            p_cu2_calc = s_in * p_ag_calc
            p_mi_calc = p_ag_calc - p_cu2_calc
            p_util_calc = p_mi_calc - p_mec_in
            rendimiento = (p_util_calc / p1_in) * 100 if p1_in > 0 else 0

            # Gráfico Waterfall de Plotly
            fig_waterfall = go.Figure(go.Waterfall(
                name = "Balance", orientation = "v",
                measure = ["absolute", "relative", "relative", "total", "relative", "total", "relative", "total"],
                x = ["P. Abs. (P1)", "P. Cu1", "P. Fe", "P. Entrehierro", "P. Cu2", "P. Mec. Int.", "P. Roz", "P. Útil"],
                textposition = "outside",
                text = [f"{p1_in}W", f"-{p_cu1_in}W", f"-{p_fe_in}W", f"{p_ag_calc}W", f"-{p_cu2_calc:.0f}W", f"{p_mi_calc:.0f}W", f"-{p_mec_in}W", f"{p_util_calc:.0f}W"],
                y = [p1_in, -p_cu1_in, -p_fe_in, 0, -p_cu2_calc, 0, -p_mec_in, 0],
                connector = {"line":{"color":"#30363D", "width":2}},
                decreasing = {"marker":{"color":"#FF4B4B"}},
                increasing = {"marker":{"color":"#00ADB5"}},
                totals = {"marker":{"color":"#F9A826"}}
            ))
            fig_waterfall.update_layout(
                title=f"Rendimiento del Motor: {rendimiento:.1f}%",
                showlegend=False,
                height=450,
                margin=dict(l=0, r=0, t=40, b=0),
                paper_bgcolor="rgba(0,0,0,0)",
                plot_bgcolor="rgba(0,0,0,0)"
            )
            st.plotly_chart(fig_waterfall, use_container_width=True)
            
    # --------------------------------------------------------------------------
    # PESTAÑA 2.7: PLACA DE CARACTERÍSTICAS
    # --------------------------------------------------------------------------
    with tab_placa:
        st.markdown("### 📋 Interpretación de la Placa de Características")
        st.write("""
        La placa de características contiene la información mínima necesaria para instalar y operar el motor de forma segura. 
        Ignorar estos datos puede provocar desde un rendimiento deficiente hasta la destrucción del aislamiento por sobrecalentamiento.
        """)

        # Simulación visual de una placa
        st.markdown("""
        <div style="border: 2px solid #555; padding: 20px; border-radius: 10px; background-color: #f0f2f6; color: #111; font-family: monospace;">
            <center><b>TRES-PHASE INDUCTION MOTOR</b></center><br>
            <b>TYPE:</b> MS 100L-4 &nbsp;&nbsp; <b>NO:</b> 2024-001 &nbsp;&nbsp; <b>IP:</b> 55 <br>
            <b>kW:</b> 3.0 &nbsp;&nbsp; <b>CV:</b> 4.0 &nbsp;&nbsp; <b>Hz:</b> 50 &nbsp;&nbsp; <b>IC:</b> F <br>
            <b>V:</b> 230Δ / 400Y &nbsp;&nbsp; <b>A:</b> 11.2 / 6.5 <br>
            <b>min⁻¹:</b> 1440 &nbsp;&nbsp; <b>cos φ:</b> 0.82 &nbsp;&nbsp; <b>S1</b> <br>
            <b>IE3:</b> 87.7%
        </div>
        """, unsafe_allow_html=True)
        
        st.caption("Ejemplo de disposición de datos en una placa normalizada.")

        # Desglose didáctico
        st.markdown("#### 🔍 Análisis de los parámetros principales")

        col_p1, col_p2 = st.columns(2)

        with col_p1:
            with st.expander("⚡ Tensión y Conexión (V)", expanded=True):
                st.write("**¿Qué significa?**")
                st.write("Indica las tensiones que soportan los devanados. El valor más bajo (230V) es lo máximo que admite cada fase del motor.")
                st.warning("**Regla de Oro:** Si tu red es de 400V entre fases, DEBES conectar en **Estrella (Y)**. Si conectas en Triángulo (Δ), aplicarás 400V a una bobina de 230V y el motor se quemará en segundos.")
            
            with st.expander("🐎 Potencia Nominal (kW / CV)"):
                st.write("**¿Qué significa?**")
                st.write("Es la **Potencia Útil ($P_u$)** que el motor entrega en el eje. No es la potencia que consume de la red (que siempre es mayor debido a las pérdidas).")
                st.latex(r"1 \text{ CV} \approx 0.736 \text{ kW} \quad | \quad 1 \text{ HP} \approx 0.746 \text{ kW}")

            with st.expander("🌀 Velocidad Nominal (min⁻¹ o rpm)"):
                st.write("**¿Qué significa?**")
                st.write("Es la velocidad real de giro a plena carga. Como es un motor asíncrono, siempre será menor a la de sincronismo.")
                st.info("💡 **Dato Didáctico:** Si ves 1440 rpm en la placa, sabes automáticamente que el motor es de 4 polos (sincronismo = 1500 rpm) y que su deslizamiento nominal es del 4%.")

        with col_p2:
            with st.expander("🔌 Corriente Nominal (A)"):
                st.write("**¿Qué significa?**")
                st.write("Es la intensidad que circula por la línea cuando el motor trabaja a su potencia nominal. Se dan dos valores asociados a la tensión: el mayor para la conexión Δ y el menor para Y.")
                st.write("Sirve para calibrar el **relé térmico** de protección.")

            with st.expander("📐 Factor de Potencia (cos φ)"):
                st.write("**¿Qué significa?**")
                st.write("Indica qué parte de la corriente absorbida se convierte en trabajo útil frente a la corriente reactiva necesaria para crear los campos magnéticos.")
                st.write("Un valor de 0.82 es típico. Cuanto más bajo, más 'penaliza' la compañía eléctrica por consumo de reactiva.")

            with st.expander("🌡️ Clase de Aislamiento (IC)"):
                st.write("**¿Qué significa?**")
                st.write("Indica la temperatura máxima que soporta el barniz de las bobinas sin degradarse. Las más comunes son:")
                st.markdown("- **Clase B:** 130°C\n- **Clase F:** 155°C (Estándar industrial)\n- **Clase H:** 180°C")

        st.markdown("---")
        st.markdown("#### 🛡️ Datos de Protección y Servicio")
        
        col_s1, col_s2, col_s3 = st.columns(3)
        
        with col_s1:
            st.markdown("**Grado IP (Ingress Protection)**")
            st.write("El primer dígito es protección contra **polvo** (0-6) y el segundo contra **agua** (0-8).")
            st.caption("Ej: IP55 significa protegido contra polvo y chorros de agua.")

        with col_s2:
            st.markdown("**Régimen de Servicio**")
            st.write("Indica si el motor puede trabajar sin parar (**S1**) o si es para usos intermitentes (**S2, S3...**) donde necesita enfriarse entre arranques.")

        with col_s3:
            st.markdown("**Clase de Eficiencia (IE)**")
            st.write("Normativa internacional (IEC) sobre eficiencia energética:")
            st.markdown("- **IE1:** Estándar\n- **IE2:** Alta\n- **IE3:** Premium\n- **IE4:** Super Premium")
    # --------------------------------------------------------------------------
    # PESTAÑA 2.8: FACTORES K Y RENDIMIENTO (¡NUEVO!)
    # --------------------------------------------------------------------------
    with tab_factores:
        st.markdown("### 📐 Los 'Factores K': Diseño Físico y Eficiencia")
        st.write("""
        En la teoría básica, imaginamos las bobinas del motor como hilos ideales perfectamente concentrados. En la realidad de la ingeniería, los devanados se diseñan con ciertas deformaciones deliberadas (Factores de Devanado) para **limpiar la onda de los armónicos perjudiciales**. 
        Aunque esto reduce ligeramente la tensión inducida (f.e.m.), el beneficio en el **rendimiento** (al eliminar calentamientos parásitos y ruidos) es enorme.
        """)

        

        col_k1, col_k2 = st.columns(2)

        with col_k1:
            st.markdown("#### 1. Factor de Distribución ($K_d$)")
            st.write("Las bobinas de una fase no se meten en una sola ranura, sino que se distribuyen en varias ($q$ ranuras por polo y fase). Al estar desfasadas geométricamente, sus f.e.m.s no están en fase temporal. La suma vectorial es menor que la suma aritmética directa.")
            st.latex(r"K_d = \frac{\text{Suma Vectorial}}{\text{Suma Aritmética}} = \frac{\sin(q \cdot \alpha/2)}{q \cdot \sin(\alpha/2)}")
            st.caption("Donde $\\alpha$ es el ángulo eléctrico entre ranuras contiguas. Típicamente $K_d \approx 0.95$.")

        with col_k2:
            st.markdown("#### 2. Factor de Acortamiento o Paso ($K_p$)")
            st.write("El paso de la bobina (distancia entre sus dos lados) se suele hacer intencionadamente más pequeño que el paso polar (la distancia entre el Polo N y el S). Se hace para anular **armónicos específicos** (como el 5º o el 7º) que frenan al motor.")
            st.latex(r"K_p = \sin\left(\frac{\rho}{2}\right) = \cos\left(\frac{\epsilon}{2}\right)")
            st.caption("Donde $\\rho$ es el ángulo de paso real y $\\epsilon$ es el ángulo de acortamiento. Típicamente $K_p \approx 0.96$.")

        st.info("**Ecuación Fundamental Real de la Máquina:**\nSe unifican ambos en el **Factor de Devanado** ($K_w = K_d \cdot K_p$). La f.e.m. inducida real queda corregida como:  $E = 4.44 \cdot f \cdot N \cdot \Phi_{max} \cdot \mathbf{K_w}$")

        st.markdown("---")
        
        st.markdown("#### 📊 El Factor de Carga ($k$) y la Curva de Rendimiento")
        st.write("""
        Más allá del diseño físico, el rendimiento del motor operando en una fábrica depende del **Factor de Carga ($k$)**, también llamado índice de carga. Es la relación entre la potencia que se le está exigiendo en ese instante y su potencia nominal de placa: $k = P / P_{nominal}$.
        """)
        
        col_r1, col_r2 = st.columns([1, 1.5])
        
        with col_r1:
            st.markdown("**Teorema del Rendimiento Máximo**")
            st.write("Las pérdidas de un motor se dividen en dos familias:")
            st.markdown("""
            * **Fijas ($P_{Fe}$ + $P_{mec}$):** Rozamiento y magnetización. No cambian aunque cambie la carga.
            * **Variables ($P_{Cu}$):** Efecto Joule. Evolucionan con el cuadrado de la carga ($k^2$).
            """)
            st.write("Matemáticamente, si derivamos la ecuación del rendimiento respecto a $k$ e igualamos a cero, demostramos que el **rendimiento máximo se alcanza cuando las pérdidas variables igualan a las fijas:**")
            st.latex(r"P_{fijas} = k_{opt}^2 \cdot P_{Cu_{nominal}} \implies k_{opt} = \sqrt{\frac{P_{fijas}}{P_{Cu_{nominal}}}}")

        with col_r2:
            st.markdown("**🕹️ Simulador de Rendimiento según Carga ($k$)**")
            p_fijas_sim = st.slider("Pérdidas Fijas (Hierro+Mec) [W]", 100, 1000, 300, step=50)
            p_var_sim = st.slider("Pérdidas Variables (Cobre a plena carga) [W]", 100, 1000, 600, step=50)
            p_nom_sim = 10000 # 10 kW fijos para simulación
            
            # Generar curva de rendimiento
            k_array = np.linspace(0.1, 1.25, 100) # De 10% a 125% de carga
            rend_array = []
            for k_val in k_array:
                p_util = k_val * p_nom_sim
                p_perdidas = p_fijas_sim + (k_val**2 * p_var_sim)
                rend = (p_util / (p_util + p_perdidas)) * 100
                rend_array.append(rend)
                
            k_optimo = math.sqrt(p_fijas_sim / p_var_sim)
            rend_optimo = max(rend_array) if k_optimo <= 1.25 else 0
            
            fig_rend = go.Figure()
            fig_rend.add_trace(go.Scatter(x=k_array*100, y=rend_array, mode='lines', name='Rendimiento (%)', line=dict(color='#F9A826', width=4)))
            
            if k_optimo <= 1.25:
                fig_rend.add_vline(x=k_optimo*100, line_width=2, line_dash="dash", line_color="red")
                fig_rend.add_annotation(x=k_optimo*100, y=rend_optimo, text=f"Máx: {rend_optimo:.1f}% a {k_optimo*100:.0f}% carga", showarrow=True, arrowhead=2)
                
            fig_rend.update_layout(
                title="Evolución del Rendimiento",
                xaxis_title="Factor de Carga (k) [%]",
                yaxis_title="Rendimiento (η) [%]",
                height=300, margin=dict(l=0, r=0, t=40, b=0)
            )
            st.plotly_chart(fig_rend, use_container_width=True)
    # --------------------------------------------------------------------------
    # PESTAÑA 2.9: TEOREMA DE FERRARIS (CAMPO GIRATORIO)
    # --------------------------------------------------------------------------
    with tab_ferraris:
        st.markdown("### 🌀 El Corazón del Motor AC: El Teorema de Ferraris")
        st.write("""
        El físico italiano Galileo Ferraris descubrió en 1885 el principio que hace posible todos los motores de corriente alterna modernos: **cómo crear movimiento rotativo a partir de piezas completamente estáticas**.
        """)
        
        

        col_teo1, col_teo2 = st.columns([1, 1])

        with col_teo1:
            st.markdown("#### 📐 1. Las Premisas del Sistema")
            st.write("Para generar un campo magnético giratorio necesitamos dos condiciones que se cruzan simultáneamente (Desfase Espacial + Desfase Temporal):")
            st.markdown("""
            * **Desfase Espacial:** Tenemos 3 bobinas (fases U, V, W) distribuidas en el estator separadas físicamente por **120º geométricos** ($2\pi/3$ rad).
            * **Desfase Temporal:** Inyectamos un sistema trifásico de corrientes, donde cada corriente está desfasada **120º eléctricos** en el tiempo.
            """)
            
            st.write("Las corrientes instantáneas que entran al motor son:")
            st.latex(r"i_U(t) = I_{max} \cdot \cos(\omega t)")
            st.latex(r"i_V(t) = I_{max} \cdot \cos(\omega t - 120^\circ)")
            st.latex(r"i_W(t) = I_{max} \cdot \cos(\omega t - 240^\circ)")

        with col_teo2:
            st.markdown("#### 🧲 2. Campos Magnéticos Pulsantes")
            st.write("Cada bobina genera un campo magnético ($B$) en su propio eje estático. Su magnitud sube y baja al ritmo de su corriente (campo pulsante):")
            st.latex(r"\vec{B}_U(t) = B_{max} \cos(\omega t) \angle 0^\circ")
            st.latex(r"\vec{B}_V(t) = B_{max} \cos(\omega t - 120^\circ) \angle 120^\circ")
            st.latex(r"\vec{B}_W(t) = B_{max} \cos(\omega t - 240^\circ) \angle 240^\circ")
            
            st.info("⚠️ **Nota:** Fíjate que en cada ecuación, el ángulo aparece dos veces: restando dentro del coseno (retraso en el tiempo) y como el ángulo del vector (posición física de la bobina).")

        st.markdown("---")
        st.markdown("#### 🔬 3. Demostración Matemática (Suma Vectorial)")
        st.write("Según el Principio de Superposición, el campo magnético total en el centro del motor es la suma vectorial instantánea de los tres campos. Descomponemos en los ejes X e Y:")

        st.latex(r"B_x = B_U \cos(0^\circ) + B_V \cos(120^\circ) + B_W \cos(240^\circ)")
        st.latex(r"B_y = B_U \sin(0^\circ) + B_V \sin(120^\circ) + B_W \sin(240^\circ)")

        st.write("Sustituyendo los valores de $\cos(120^\circ) = -1/2$ y $\cos(240^\circ) = -1/2$, y aplicando las identidades trigonométricas de transformación de productos a sumas (ej. $\cos A \cdot \cos B$), la suma colapsa mágicamente a un resultado increíblemente limpio:")

        col_res1, col_res2 = st.columns(2)
        with col_res1:
            st.latex(r"B_x = \frac{3}{2} B_{max} \cdot \cos(\omega t)")
            st.latex(r"B_y = \frac{3}{2} B_{max} \cdot \sin(\omega t)")
        with col_res2:
            st.success("**El Vector Resultante:**\nRepresenta un vector de **módulo constante** igual a $1.5 \cdot B_{max}$ que **rota en el espacio** con velocidad angular $\omega$. ¡Hemos creado un imán virtual que da vueltas sin partes móviles!")

        st.markdown("---")
        st.markdown("#### 🕹️ Simulador del Teorema de Ferraris")
        st.write("Mueve el deslizador del tiempo ($\omega t$) para ver cómo los tres campos pulsantes (estáticos en su eje) crecen y decrecen, y cómo su suma vectorial (rojo) resulta en un vector que gira perfectamente en círculo.")

        # Simulador Interactivo
        c_slider, c_grafico = st.columns([1, 2])
        
        with c_slider:
            st.write("<br><br>", unsafe_allow_html=True)
            wt_deg = st.slider("Instante de tiempo (ωt en grados)", 0, 360, 0, step=5)
            wt = math.radians(wt_deg)
            
            # Cálculos instantáneos
            B_max = 1.0
            
            # Magnitudes pulsantes
            Bu_mag = B_max * math.cos(wt)
            Bv_mag = B_max * math.cos(wt - 2*math.pi/3)
            Bw_mag = B_max * math.cos(wt - 4*math.pi/3)
            
            # Componentes X, Y de cada vector
            Bu_x = Bu_mag * 1.0
            Bu_y = 0.0
            
            Bv_x = Bv_mag * math.cos(2*math.pi/3)
            Bv_y = Bv_mag * math.sin(2*math.pi/3)
            
            Bw_x = Bw_mag * math.cos(4*math.pi/3)
            Bw_y = Bw_mag * math.sin(4*math.pi/3)
            
            # Vector resultante
            B_res_x = Bu_x + Bv_x + Bw_x
            B_res_y = Bu_y + Bv_y + Bw_y
            
            st.metric("Módulo Vector Total", f"{math.sqrt(B_res_x**2 + B_res_y**2):.2f} B_max")
            st.metric("Ángulo Vector Total", f"{wt_deg}°")

        with c_grafico:
            fig_ferraris = go.Figure()
            
            # Círculo de la trayectoria resultante (Módulo 1.5)
            fig_ferraris.add_shape(type="circle", x0=-1.5, y0=-1.5, x1=1.5, y1=1.5, line_color="rgba(255, 75, 75, 0.3)", line_dash="dash")
            
            # Función auxiliar para dibujar flechas
            def add_arrow(fig, x_end, y_end, name, color, width=3):
                fig.add_annotation(
                    x=x_end, y=y_end, ax=0, ay=0, xref="x", yref="y", axref="x", ayref="y",
                    showarrow=True, arrowhead=2, arrowsize=1.5, arrowwidth=width, arrowcolor=color
                )
                # Punto oculto para leyenda
                fig.add_trace(go.Scatter(x=[x_end], y=[y_end], mode='lines', name=name, marker=dict(color=color)))

            # Añadir vectores de fase
            add_arrow(fig_ferraris, Bu_x, Bu_y, "Fase U (0º)", "#00ADB5", 3)
            add_arrow(fig_ferraris, Bv_x, Bv_y, "Fase V (120º)", "#F9A826", 3)
            add_arrow(fig_ferraris, Bw_x, Bw_y, "Fase W (240º)", "#9B59B6", 3)
            
            # Añadir vector Resultante
            add_arrow(fig_ferraris, B_res_x, B_res_y, "Campo Resultante", "#FF4B4B", 5)

            fig_ferraris.update_layout(
                xaxis=dict(range=[-2, 2], showgrid=False, zeroline=True, zerolinewidth=2, zerolinecolor='gray'),
                yaxis=dict(range=[-2, 2], showgrid=False, zeroline=True, zerolinewidth=2, zerolinecolor='gray', scaleanchor="x", scaleratio=1),
                title="Suma Vectorial del Campo Giratorio",
                height=450, margin=dict(l=0, r=0, t=40, b=0),
                showlegend=True, legend=dict(yanchor="top", y=0.99, xanchor="left", x=0.01)
            )
            st.plotly_chart(fig_ferraris, use_container_width=True)
if __name__ == "__main__":
    app()