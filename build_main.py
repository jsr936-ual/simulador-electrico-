import base64, os

brain = r'C:\Users\josea\.gemini\antigravity\brain\87afa5bf-fa3e-4b25-8635-6ffd80d21bb8'

def b64img(fname):
    path = os.path.join(brain, fname)
    with open(path, 'rb') as f:
        return base64.b64encode(f.read()).decode()

imgs = {
    'basic':    b64img('bg_basic_1779045901716.png'),
    'advanced': b64img('bg_advanced_1779046039407.png'),
    'electro':  b64img('bg_electro_1779046671190.png'),
    'async':    b64img('bg_async_1779046684018.png'),
    'dc':       b64img('bg_dc_1779046709202.png'),
}

# Gradientes CSS para los módulos sin imagen
grad_topology = "linear-gradient(135deg, #0A1628 0%, #0D2137 40%, #0A3D2B 100%)"
grad_sync     = "linear-gradient(135deg, #0D1F1A 0%, #0A2E2A 50%, #061A28 100%)"

main_content = '''# LIBRERÍAS EMPLEADAS
import streamlit as st
from modules import basic_calculations, advanced_lines, electromagnetism, topology, asincronous, dc_motors, synchronous_machines

# ─── CONFIGURACIÓN DE PÁGINA ──────────────────────────────────────────────────
st.set_page_config(
    page_title="Electric Design Suite",
    page_icon="⚡",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ─── ESTILOS GLOBALES ────────────────────────────────────────────────────────
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:ital,wght@0,300;0,400;0,500;0,600;1,300&display=swap');

*, *::before, *::after { box-sizing: border-box; }

.stApp {
    background-color: #080808;
    font-family: 'Inter', -apple-system, BlinkMacSystemFont, sans-serif;
    color: #A1A1AA;
}
h1, h2, h3, h4 {
    font-family: 'Inter', sans-serif;
    color: #FAFAFA;
    font-weight: 600;
    letter-spacing: -0.5px;
}

section[data-testid="stSidebar"] {
    background-color: #050505;
    border-right: 1px solid #151515;
}
section[data-testid="stSidebar"] .stButton > button {
    width: 100%;
    height: auto !important;
    min-height: 36px;
    padding: 7px 12px;
    background: transparent;
    border: none;
    border-radius: 6px;
    color: #52525B;
    font-family: 'Inter', sans-serif;
    font-size: 13px;
    font-weight: 400;
    text-align: left;
    justify-content: flex-start;
    transition: all 0.15s ease;
    white-space: nowrap;
}
section[data-testid="stSidebar"] .stButton > button:hover {
    background-color: #111111;
    color: #FAFAFA;
    transform: none;
    box-shadow: none;
}

div.stButton > button {
    width: 100%;
    height: auto;
    padding: 0;
    background: transparent;
    border: none;
    color: transparent;
    font-size: 0;
    transition: none;
    box-shadow: none;
    cursor: pointer;
    position: absolute;
    inset: 0;
    border-radius: 0;
    z-index: 10;
    opacity: 0;
}

hr { border-color: #151515; opacity: 1; }
</style>
""", unsafe_allow_html=True)

# ─── ESTADO ──────────────────────────────────────────────────────────────────
if 'current_section' not in st.session_state:
    st.session_state.current_section = "Home"

def go_home():
    st.session_state.current_section = "Home"
    st.rerun()

def set_section(section):
    st.session_state.current_section = section
    st.rerun()

# ─── SIDEBAR ─────────────────────────────────────────────────────────────────
with st.sidebar:
    st.markdown("""
    <div style="padding:24px 4px 20px 4px;">
        <div style="font-family:'Inter',sans-serif;font-size:15px;font-weight:600;color:#FAFAFA;letter-spacing:-0.3px;">
            ⚡ EDS Pro
        </div>
        <div style="font-family:'Inter',sans-serif;font-size:11px;color:#27272A;margin-top:3px;">
            Electric Design Suite · v1.0
        </div>
    </div>
    """, unsafe_allow_html=True)
    st.markdown("<div style='border-top:1px solid #151515;margin-bottom:12px;'></div>", unsafe_allow_html=True)
    st.markdown("<div style='font-family:Inter,sans-serif;font-size:10px;color:#27272A;letter-spacing:1.5px;text-transform:uppercase;padding:0 4px 8px 4px;'>Módulos</div>", unsafe_allow_html=True)

    nav_items = [
        ("🏠", "Inicio",               "Home"),
        ("📐", "Cálculos Básicos",     "Basic"),
        ("⚡", "Líneas Alta Potencia", "Advanced"),
        ("🌐", "Topología",            "Topology"),
        ("🔌", "Electromagnetismo",    "Electromagnetism"),
        ("🌀", "Motores Asíncronos",   "Asynchronous"),
        ("🔋", "Motores DC",           "DCMotors"),
        ("⚙️", "Máquinas Síncronas",  "Synchronous"),
    ]
    for icon, label, key in nav_items:
        if st.button(f"{icon}  {label}", key=f"nav_{key}"):
            go_home() if key == "Home" else set_section(key)

    st.markdown("<div style='border-top:1px solid #151515;margin-top:20px;padding-top:14px;'></div>", unsafe_allow_html=True)
    st.markdown("<div style='font-family:Inter,sans-serif;font-size:11px;color:#27272A;padding:0 4px;'>© 2025 · Univ. Almería</div>", unsafe_allow_html=True)

# ─── HOME ────────────────────────────────────────────────────────────────────
if st.session_state.current_section == "Home":

    st.markdown("""
    <div style="padding:52px 0 36px 0;">
        <div style="font-family:'Inter',sans-serif;font-size:10px;font-weight:500;color:#27272A;
                    letter-spacing:2.5px;text-transform:uppercase;margin-bottom:14px;">
            Electric Design Suite · Plataforma de Ingeniería
        </div>
        <h1 style="font-family:'Inter',sans-serif;font-size:2.8rem;font-weight:600;
                   color:#FAFAFA;letter-spacing:-1.5px;margin:0 0 14px 0;line-height:1.1;">
            Simulación y diseño<br>de máquinas eléctricas.
        </h1>
        <p style="font-family:'Inter',sans-serif;font-size:0.95rem;color:#3F3F46;
                  font-weight:300;max-width:480px;line-height:1.75;margin:0;">
            Accede a los módulos de cálculo, simulación interactiva y documentación técnica.
        </p>
    </div>
    """, unsafe_allow_html=True)

    # ── TARJETAS TIPO COSENTINO (Expanding Image Cards) ──────────────────────

    IMG = {IMG_DICT}

    modules_data = [
        ("basic",    "📐", "Cálculos<br>Básicos",     "ITC-BT, secciones de cable<br>y protecciones reglamentarias.",   "Basic"),
        ("advanced", "⚡", "Líneas de<br>Alta Potencia","Ampacidad térmica, Blondel<br>y optimización LCC.",            "Advanced"),
        ("topology", "🌐", "Topología &<br>Dimensionado","Redes radiales, anillo,<br>unifilares y perfiles de tensión.", "Topology"),
        ("electro",  "🔌", "Electro-<br>magnetismo",  "Circuitos magnéticos,<br>histéresis B-H y Faraday.",            "Electromagnetism"),
        ("async",    "🌀", "Motores<br>Asíncronos",   "Steinmetz, curva Par-Vel.<br>y Teorema de Ferraris.",            "Asynchronous"),
        ("dc",       "🔋", "Motores<br>DC",            "Excitación, 4 cuadrantes<br>y control de velocidad.",           "DCMotors"),
        ("sync",     "⚙️", "Máquinas<br>Síncronas",   "Reactancia síncrona,<br>curvas en V y estabilidad.",            "Synchronous"),
    ]

    # Construir el HTML de las tarjetas con imágenes reales
    cards_html = []
    for img_key, icon, title, desc, section_key in modules_data:
        if img_key in IMG:
            bg_style = f"background-image: url('data:image/png;base64,{IMG[img_key]}'); background-size: cover; background-position: center;"
        elif img_key == "topology":
            bg_style = f"background: {grad_topology};"
        else:
            bg_style = f"background: {grad_sync};"

        cards_html.append(f"""
        <div class="eds-card" id="card-{section_key}" onclick="document.getElementById('btn-{section_key}').click()">
            <div class="eds-card-bg" style="{bg_style}"></div>
            <div class="eds-card-overlay"></div>
            <div class="eds-card-content">
                <div class="eds-card-icon">{icon}</div>
                <div class="eds-card-title">{title}</div>
                <div class="eds-card-desc">{desc}</div>
            </div>
        </div>
        """)

    st.markdown("""
    <style>
    .eds-gallery {{
        display: flex;
        gap: 6px;
        height: 440px;
        overflow: hidden;
    }}

    .eds-card {{
        position: relative;
        flex: 1;
        border-radius: 12px;
        overflow: hidden;
        cursor: pointer;
        transition: flex 0.55s cubic-bezier(0.4, 0, 0.2, 1);
    }}

    .eds-card:hover {{
        flex: 4.5;
    }}

    .eds-card-bg {{
        position: absolute;
        inset: 0;
        transition: transform 0.55s cubic-bezier(0.4, 0, 0.2, 1);
    }}
    .eds-card:hover .eds-card-bg {{
        transform: scale(1.06);
    }}

    .eds-card-overlay {{
        position: absolute;
        inset: 0;
        background: linear-gradient(
            to top,
            rgba(0,0,0,0.92) 0%,
            rgba(0,0,0,0.55) 40%,
            rgba(0,0,0,0.10) 100%
        );
        transition: opacity 0.4s ease;
    }}

    .eds-card-content {{
        position: absolute;
        bottom: 0; left: 0; right: 0;
        padding: 28px 26px;
        z-index: 2;
    }}

    .eds-card-icon {{
        font-size: 1.8rem;
        margin-bottom: 10px;
        opacity: 0;
        transform: translateY(8px);
        transition: opacity 0.35s ease 0.1s, transform 0.35s ease 0.1s;
    }}
    .eds-card:hover .eds-card-icon {{
        opacity: 1;
        transform: translateY(0);
    }}

    .eds-card-title {{
        font-family: 'Inter', sans-serif;
        font-size: 1.1rem;
        font-weight: 600;
        color: #FAFAFA;
        line-height: 1.25;
        letter-spacing: -0.3px;
        opacity: 0;
        transform: translateY(10px);
        transition: opacity 0.35s ease 0.15s, transform 0.35s ease 0.15s;
        white-space: nowrap;
    }}
    .eds-card:hover .eds-card-title {{
        opacity: 1;
        transform: translateY(0);
    }}

    .eds-card-desc {{
        font-family: 'Inter', sans-serif;
        font-size: 0.78rem;
        font-weight: 300;
        color: #A1A1AA;
        line-height: 1.6;
        margin-top: 8px;
        opacity: 0;
        transform: translateY(10px);
        transition: opacity 0.35s ease 0.22s, transform 0.35s ease 0.22s;
    }}
    .eds-card:hover .eds-card-desc {{
        opacity: 1;
        transform: translateY(0);
    }}

    /* Línea lateral decorativa en hover */
    .eds-card::after {{
        content: '';
        position: absolute;
        bottom: 0; left: 0;
        width: 0;
        height: 2px;
        background: white;
        opacity: 0.4;
        transition: width 0.45s cubic-bezier(0.4, 0, 0.2, 1) 0.1s;
    }}
    .eds-card:hover::after {{
        width: 100%;
    }}

    /* Botones Streamlit ocultos detrás */
    .eds-btn-row div.stButton > button {{
        position: static !important;
        opacity: 1 !important;
        height: 36px !important;
        padding: 6px 14px !important;
        background: #111111 !important;
        border: 1px solid #1C1C1C !important;
        border-radius: 6px !important;
        color: #52525B !important;
        font-size: 12px !important;
        font-weight: 400 !important;
        transition: all 0.15s ease !important;
        white-space: nowrap !important;
    }}
    .eds-btn-row div.stButton > button:hover {{
        border-color: #3F3F46 !important;
        color: #FAFAFA !important;
        background: #161616 !important;
        transform: none !important;
        box-shadow: none !important;
    }}
    </style>
    """ + f'<div class="eds-gallery">{"".join(cards_html)}</div>', unsafe_allow_html=True)

    # Botones funcionales de Streamlit (visibles, compactos, debajo de la galería)
    st.markdown("<div style='height:16px'></div>", unsafe_allow_html=True)
    st.markdown("<div class='eds-btn-row'>", unsafe_allow_html=True)
    st.markdown("<div style='font-family:Inter,sans-serif;font-size:10px;color:#27272A;letter-spacing:1.5px;text-transform:uppercase;margin-bottom:10px;'>Acceso directo</div>", unsafe_allow_html=True)

    bcols = st.columns(7, gap="small")
    btn_map = [
        ("📐 Básicos",      "Basic"),
        ("⚡ Alta Potencia","Advanced"),
        ("🌐 Topología",    "Topology"),
        ("🔌 Electromag.",  "Electromagnetism"),
        ("🌀 Asíncronos",   "Asynchronous"),
        ("🔋 Motores DC",   "DCMotors"),
        ("⚙️ Síncronas",   "Synchronous"),
    ]
    for i, (lbl, sec) in enumerate(btn_map):
        with bcols[i]:
            if st.button(lbl, key=f"direct_{sec}"):
                set_section(sec)
    st.markdown("</div>", unsafe_allow_html=True)

    # Barra de estado
    st.markdown("""
    <div style="margin-top:32px;padding-top:18px;border-top:1px solid #111111;
                display:flex;align-items:center;gap:22px;
                font-family:'Inter',monospace;font-size:11px;color:#27272A;">
        <span>
            <span style="display:inline-block;width:5px;height:5px;border-radius:50%;
                         background:#22C55E;margin-right:6px;box-shadow:0 0 5px #22C55E;"></span>
            Sistema operativo
        </span>
        <span style="color:#151515;">·</span>
        <span>7 módulos activos</span>
        <span style="color:#151515;">·</span>
        <span>Universidad de Almería · 25/26</span>
    </div>
    """, unsafe_allow_html=True)

# ─── ROUTING ─────────────────────────────────────────────────────────────────
elif st.session_state.current_section == "Basic":
    basic_calculations.app()
elif st.session_state.current_section == "Advanced":
    advanced_lines.app()
elif st.session_state.current_section == "Topology":
    topology.app()
elif st.session_state.current_section == "Electromagnetism":
    electromagnetism.app()
elif st.session_state.current_section == "Asynchronous":
    asincronous.app()
elif st.session_state.current_section == "DCMotors":
    dc_motors.app()
elif st.session_state.current_section == "Synchronous":
    synchronous_machines.app()
'''

# Interpolate the image dictionary
img_dict_str = "{\n"
for k, v in imgs.items():
    img_dict_str += f'        "{k}": "{v}",\n'
img_dict_str += "    }"

grad_topology = "linear-gradient(135deg, #0A1628 0%, #0D2137 40%, #0A3D2B 100%)"
grad_sync     = "linear-gradient(135deg, #0D1F1A 0%, #0A2E2A 50%, #061A28 100%)"

final = main_content.replace("{IMG_DICT}", img_dict_str)
final = final.replace("{grad_topology}", grad_topology)
final = final.replace("{grad_sync}", grad_sync)

out_path = r'c:\Users\josea\Desktop\UNIVERSIDAD\UNIVERSIDAD JAIME\3er curso\Segundo Cuatri\MÁQUINAS ELÉCTRICAS\Software Eléctrico COMPLETO\main.py'
with open(out_path, 'w', encoding='utf-8') as f:
    f.write(final)

print(f"Done. Written {len(final)} chars to main.py")
