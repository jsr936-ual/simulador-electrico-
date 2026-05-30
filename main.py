import streamlit as st
from modules import basic_calculations, advanced_lines, electromagnetism, topology, asincronous, dc_motors, synchronous_machines

st.set_page_config(page_title="Electric Design Suite", page_icon="⚡", layout="wide", initial_sidebar_state="collapsed")

# ── ESTADO & NAVEGACIÓN ───────────────────────────────────────────────────────
if 'nav' in st.query_params:
    nav = st.query_params['nav']
    st.session_state.current_section = nav
    st.query_params.clear()

if "current_section" not in st.session_state:
    st.session_state.current_section = "Home"

def set_section(s):
    st.session_state.current_section = s
    st.rerun()

# ── ESTILOS GLOBALES ──────────────────────────────────────────────────────────
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600&display=swap');
*,*::before,*::after{box-sizing:border-box;}
.stApp{background:#080808;font-family:'Inter',sans-serif;color:#71717A;}
h1,h2,h3{font-family:'Inter',sans-serif;color:#FAFAFA;font-weight:600;letter-spacing:-0.5px;}
#MainMenu,footer,header{visibility:hidden;}
section[data-testid="stSidebar"],[data-testid="collapsedControl"]{display:none!important;}

/* TOP NAV BUTTONS */
div[data-testid="stHorizontalBlock"] div.stButton>button{
    width:100%!important;height:34px!important;padding:0 6px!important;
    background:transparent!important;border:none!important;
    border-bottom:1px solid transparent!important;border-radius:0!important;
    color:#3F3F46!important;font-family:'Inter',sans-serif!important;
    font-size:13px!important;font-weight:400!important;
    transition:color .15s ease,border-color .15s ease!important;
    box-shadow:none!important;transform:none!important;white-space:nowrap!important;
}
div[data-testid="stHorizontalBlock"] div.stButton>button:hover{
    color:#E4E4E7!important;border-bottom:1px solid #3F3F46!important;
    background:transparent!important;box-shadow:none!important;transform:none!important;
}
hr{border-color:#141414;opacity:1;}
</style>
""", unsafe_allow_html=True)

# ── TOP NAV ───────────────────────────────────────────────────────────────────
st.markdown("""
<div style="display:flex;align-items:center;justify-content:space-between;
            height:52px;border-bottom:1px solid #111;">
  <div style="font-family:'Inter',sans-serif;font-size:14px;font-weight:600;color:#FAFAFA;letter-spacing:-0.2px;">
    Electric Design Suite
  </div>
  <div style="font-family:'Inter',sans-serif;font-size:11px;color:#27272A;">
    v1.0 &nbsp;·&nbsp; Universidad de Almería
  </div>
</div>
""", unsafe_allow_html=True)

nav_cols = st.columns([1,1,1,1,1,1,1,1,4])
nav_map = [
    ("Inicio","Home"),("Cálculos","Basic"),("Líneas","Advanced"),
    ("Topología","Topology"),("Electromag.","Electromagnetism"),
    ("Asíncronos","Asynchronous"),("Motores DC","DCMotors"),("Síncronas","Synchronous"),
]
for i,(lbl,key) in enumerate(nav_map):
    with nav_cols[i]:
        if st.button(lbl, key=f"tnav_{key}"):
            set_section(key)

st.markdown("<div style='border-bottom:1px solid #111;'></div>", unsafe_allow_html=True)

# ── HOME ─────────────────────────────────────────────────────────────────────
if st.session_state.current_section == "Home":

    st.markdown("""
    <div style="padding:52px 0 36px 0;">
      <div style="font-size:10px;font-weight:500;color:#27272A;letter-spacing:2.5px;
                  text-transform:uppercase;margin-bottom:14px;font-family:'Inter',sans-serif;">
        Plataforma de Ingeniería Eléctrica
      </div>
      <h1 style="font-size:2.7rem;font-weight:600;color:#FAFAFA;letter-spacing:-1.6px;
                 margin:0 0 14px 0;line-height:1.1;">
        Simulación y diseño<br>de máquinas eléctricas.
      </h1>
      <p style="font-size:0.95rem;color:#3F3F46;font-weight:300;max-width:440px;
                line-height:1.8;margin:0;font-family:'Inter',sans-serif;">
        Selecciona un módulo para acceder al motor de cálculo,
        los simuladores y la documentación técnica.
      </p>
    </div>
    """, unsafe_allow_html=True)

    gallery_html = """
<div class="eds-gallery">
  <a href="?nav=Basic" target="_self" class="eds-card" style="--accent:#8AB4F8">
    <div class="card-bg" style="background:linear-gradient(160deg,#0B1E3A,#0D2954,#071833)"></div>
    <div class="card-overlay"></div>
    <div class="card-num">01</div>
    <div class="card-label-v">CÁLCULOS</div>
    <div class="card-content">
      <div class="card-title">Cálculos Básicos</div>
      <div class="card-desc">ITC-BT, secciones de cable,<br>protecciones y normativa.</div>
    </div>
    <div class="card-line"></div>
  </a>

  <a href="?nav=Advanced" target="_self" class="eds-card" style="--accent:#FDBA74">
    <div class="card-bg" style="background:linear-gradient(160deg,#1A0A00,#2D1200,#3D2000)"></div>
    <div class="card-overlay"></div>
    <div class="card-num">02</div>
    <div class="card-label-v">LÍNEAS</div>
    <div class="card-content">
      <div class="card-title">Líneas Alta Potencia</div>
      <div class="card-desc">Ampacidad térmica, Blondel<br>y optimización LCC.</div>
    </div>
    <div class="card-line"></div>
  </a>

  <a href="?nav=Topology" target="_self" class="eds-card" style="--accent:#6EE7B7">
    <div class="card-bg" style="background:linear-gradient(160deg,#061A10,#0A2E1E,#082514)"></div>
    <div class="card-overlay"></div>
    <div class="card-num">03</div>
    <div class="card-label-v">TOPOLOGÍA</div>
    <div class="card-content">
      <div class="card-title">Topología y Dimensionado</div>
      <div class="card-desc">Redes radiales, anillo<br>y perfiles de tensión.</div>
    </div>
    <div class="card-line"></div>
  </a>

  <a href="?nav=Electromagnetism" target="_self" class="eds-card" style="--accent:#FCD34D">
    <div class="card-bg" style="background:linear-gradient(160deg,#1A1400,#2A2000,#1E1800)"></div>
    <div class="card-overlay"></div>
    <div class="card-num">04</div>
    <div class="card-label-v">ELECTROMAG</div>
    <div class="card-content">
      <div class="card-title">Electromagnetismo</div>
      <div class="card-desc">Circuitos magnéticos,<br>histéresis B-H y Faraday.</div>
    </div>
    <div class="card-line"></div>
  </a>

  <a href="?nav=Asynchronous" target="_self" class="eds-card" style="--accent:#C4B5FD">
    <div class="card-bg" style="background:linear-gradient(160deg,#0E0818,#190D2E,#0F0520)"></div>
    <div class="card-overlay"></div>
    <div class="card-num">05</div>
    <div class="card-label-v">ASÍNCRONOS</div>
    <div class="card-content">
      <div class="card-title">Motores Asíncronos</div>
      <div class="card-desc">Steinmetz, curva Par-Vel.<br>y Teorema de Ferraris.</div>
    </div>
    <div class="card-line"></div>
  </a>

  <a href="?nav=DCMotors" target="_self" class="eds-card" style="--accent:#FCA5A5">
    <div class="card-bg" style="background:linear-gradient(160deg,#1A0505,#2A0808,#1E0404)"></div>
    <div class="card-overlay"></div>
    <div class="card-num">06</div>
    <div class="card-label-v">MOTORES DC</div>
    <div class="card-content">
      <div class="card-title">Motores DC</div>
      <div class="card-desc">Excitación, 4 cuadrantes<br>y control de velocidad.</div>
    </div>
    <div class="card-line"></div>
  </a>

  <a href="?nav=Synchronous" target="_self" class="eds-card" style="--accent:#5EEAD4">
    <div class="card-bg" style="background:linear-gradient(160deg,#021612,#042620,#031A15)"></div>
    <div class="card-overlay"></div>
    <div class="card-num">07</div>
    <div class="card-label-v">SÍNCRONAS</div>
    <div class="card-content">
      <div class="card-title">Máquinas Síncronas</div>
      <div class="card-desc">Reactancia síncrona,<br>curvas en V y estabilidad.</div>
    </div>
    <div class="card-line"></div>
  </a>
</div>
"""

    st.markdown("""
    <style>
    .eds-gallery {
        display: flex;
        gap: 4px;
        height: 430px;
        border-radius: 12px;
        overflow: hidden;
    }
    .eds-card {
        position: relative;
        flex: 1;
        border-radius: 8px;
        overflow: hidden;
        transition: flex 0.6s cubic-bezier(0.4, 0, 0.2, 1);
        min-width: 44px;
        text-decoration: none !important;
        color: inherit !important;
        display: block;
        cursor: pointer;
    }
    .eds-gallery:hover .eds-card { flex: 0.35; }
    .eds-gallery .eds-card:hover { flex: 5 !important; }

    .card-bg {
        position: absolute; inset: 0;
        transition: transform 0.6s cubic-bezier(0.4, 0, 0.2, 1);
    }
    .eds-card:hover .card-bg { transform: scale(1.04); }

    .card-overlay {
        position: absolute; inset: 0;
        background: linear-gradient(to top,
            rgba(0,0,0,0.9) 0%,
            rgba(0,0,0,0.35) 45%,
            rgba(0,0,0,0.06) 100%);
    }
    .card-num {
        position: absolute; top: 18px; right: 18px;
        font-family: 'Inter', monospace;
        font-size: 10px; letter-spacing: 1px;
        color: rgba(255,255,255,0.15);
        z-index: 5; opacity: 0;
        transition: opacity 0.3s ease 0.12s;
    }
    .eds-card:hover .card-num { opacity: 1; }

    .card-label-v {
        position: absolute;
        bottom: 24px; left: 50%;
        transform: translateX(-50%) rotate(-90deg);
        font-family: 'Inter', sans-serif;
        font-size: 9px; font-weight: 500;
        letter-spacing: 2px; text-transform: uppercase;
        color: rgba(255,255,255,0.22);
        white-space: nowrap;
        transition: opacity 0.25s ease;
        z-index: 3;
    }
    .eds-card:hover .card-label-v { opacity: 0; }

    .card-content {
        position: absolute;
        bottom: 0; left: 0; right: 0;
        padding: 28px 24px 30px 24px;
        z-index: 4;
    }
    .card-title {
        font-family: 'Inter', sans-serif;
        font-size: 1.05rem; font-weight: 600;
        color: #FAFAFA; line-height: 1.25;
        letter-spacing: -0.3px;
        opacity: 0; transform: translateY(14px);
        transition: opacity 0.3s ease 0.18s, transform 0.3s ease 0.18s;
        white-space: nowrap;
    }
    .card-desc {
        font-family: 'Inter', sans-serif;
        font-size: 0.76rem; font-weight: 300;
        color: #9CA3AF; line-height: 1.65;
        margin-top: 10px;
        opacity: 0; transform: translateY(10px);
        transition: opacity 0.28s ease 0.26s, transform 0.28s ease 0.26s;
    }
    .eds-card:hover .card-title,
    .eds-card:hover .card-desc { opacity: 1; transform: translateY(0); }

    .card-line {
        position: absolute; bottom: 0; left: 0;
        height: 1.5px; width: 0;
        background: var(--accent, #fff);
        opacity: 0.45;
        transition: width 0.5s cubic-bezier(0.4, 0, 0.2, 1) 0.08s;
    }
    .eds-card:hover .card-line { width: 100%; }
    </style>
    """, unsafe_allow_html=True)

    st.markdown(gallery_html, unsafe_allow_html=True)

    # Barra de estado
    st.markdown("""
    <div style="margin-top:28px;padding-top:18px;border-top:1px solid #111;
                display:flex;align-items:center;gap:22px;
                font-family:'Inter',monospace;font-size:11px;color:#222;">
      <span>
        <span style="display:inline-block;width:5px;height:5px;border-radius:50%;
                     background:#22C55E;margin-right:7px;box-shadow:0 0 5px #22C55E;"></span>
        Sistema operativo
      </span>
      <span style="color:#1A1A1A;">·</span>
      <span>7 módulos activos</span>
      <span style="color:#1A1A1A;">·</span>
      <span>Universidad de Almería · 25/26</span>
    </div>
    
    <div style="margin-top:40px; padding:20px 0; border-top:1px solid rgba(255,255,255,0.05); text-align:center;">
      <div style="font-family:'Inter', sans-serif; font-size:13px; font-weight:400; color:rgba(255,255,255,0.6); letter-spacing:0.5px;">
        Desarrollado por <span style="color:#FAFAFA; font-weight:600; letter-spacing:0px;">Jaime Salinas Reche</span> y <span style="color:#FAFAFA; font-weight:600; letter-spacing:0px;">Enrique Antonio Raudales Rodríguez</span>
      </div>
    </div>
    """, unsafe_allow_html=True)

# ── ROUTING ───────────────────────────────────────────────────────────────────
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
