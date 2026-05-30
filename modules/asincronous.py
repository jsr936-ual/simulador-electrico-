import streamlit as st
import numpy as np
import pandas as pd
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import math
import streamlit.components.v1 as components

# ==============================================================================
# ANIMACIÓN 2D PROFESIONAL - MOTOR ASÍNCRONO (SECCIÓN TRANSVERSAL)
# ==============================================================================
ASYNC_MOTOR_ANIMATION_HTML = """
<link href="https://fonts.googleapis.com/css2?family=Inter:wght@400;600;700&display=swap" rel="stylesheet">
<style>*{margin:0;padding:0;}body{background:transparent;overflow:hidden;}</style>
<canvas id="asm" width="780" height="520" style="display:block;margin:0 auto;border-radius:10px;"></canvas>
<script>
(function(){
var c=document.getElementById('asm'),g=c.getContext('2d');
var W=780,H=520,cx=300,cy=225,t=0;
var SR=168,SI=158,RR=105,RI=15,NB=28;
var SLIP=0.04, FIELD_SPEED=1, ROTOR_SPEED=FIELD_SPEED*(1-SLIP);
var phaseColors=['#EF4444','#F9A826','#818CF8'];
var phaseNames=['U','V','W'];
var phaseAngles=[0, 2*Math.PI/3, 4*Math.PI/3];

function rr(x,y,w,h,r){g.beginPath();g.moveTo(x+r,y);g.arcTo(x+w,y,x+w,y+h,r);g.arcTo(x+w,y+h,x,y+h,r);g.arcTo(x,y+h,x,y,r);g.arcTo(x,y,x+w,y,r);g.closePath();}
function arw(x,y,ang,col,sz){g.save();g.translate(x,y);g.rotate(ang);g.beginPath();g.moveTo(0,0);g.lineTo(-sz,-sz*0.4);g.lineTo(-sz,sz*0.4);g.closePath();g.fillStyle=col;g.fill();g.restore();}

function drawCoil(a1,a2,col,label){
  var mr=(SI+SR)/2, r2=(SR-SI)/2-1;
  var ma=(a1+a2)/2;
  g.beginPath();g.arc(cx,cy,SI,a1,a2);g.arc(cx,cy,SR,a2,a1,true);g.closePath();
  var grad=g.createRadialGradient(cx,cy,SI,cx,cy,SR);
  grad.addColorStop(0,col+'33');grad.addColorStop(1,col+'88');
  g.fillStyle=grad;g.fill();
  g.strokeStyle=col;g.lineWidth=1;g.stroke();
  g.font='bold 11px Inter,sans-serif';g.fillStyle='#FFF';g.textAlign='center';g.textBaseline='middle';
  g.fillText(label,cx+mr*Math.cos(ma),cy+mr*Math.sin(ma));
}

function draw(){
  g.clearRect(0,0,W,H);
  g.fillStyle='#0D1117';g.fillRect(0,0,W,H);
  rr(0,0,W,H,10);g.strokeStyle='#21262D';g.lineWidth=1;g.stroke();

  // Title
  g.font='600 13px Inter,sans-serif';g.fillStyle='#8B949E';g.textAlign='center';
  g.fillText('MOTOR AS\u00cdNCRONO TRIF\u00c1SICO \u2014 SECCI\u00d3N TRANSVERSAL ANIMADA',cx,20);

  // === STATOR YOKE ===
  g.beginPath();g.arc(cx,cy,SR+12,0,2*Math.PI);g.arc(cx,cy,SR,0,2*Math.PI,true);
  var sg=g.createRadialGradient(cx,cy,SR,cx,cy,SR+12);
  sg.addColorStop(0,'#2D333B');sg.addColorStop(1,'#21262D');
  g.fillStyle=sg;g.fill();
  g.beginPath();g.arc(cx,cy,SR+12,0,2*Math.PI);g.strokeStyle='#444C56';g.lineWidth=2;g.stroke();

  // === STATOR SLOTS (inner ring) ===
  g.beginPath();g.arc(cx,cy,SR,0,2*Math.PI);g.arc(cx,cy,SI,0,2*Math.PI,true);
  g.fillStyle='#1C2128';g.fill();
  g.beginPath();g.arc(cx,cy,SI,0,2*Math.PI);g.strokeStyle='#30363D';g.lineWidth=1;g.stroke();

  // === STATOR COILS (6 slots, 3 phases, each with 2 coil sides) ===
  var coilSpan = Math.PI/6;
  for(var i=0;i<3;i++){
    var a = phaseAngles[i];
    // Positive side
    drawCoil(a - coilSpan/2, a + coilSpan/2, phaseColors[i], phaseNames[i]+'+');
    // Negative side (opposite)
    drawCoil(a + Math.PI - coilSpan/2, a + Math.PI + coilSpan/2, phaseColors[i], phaseNames[i]+'-');
  }

  // === AIR GAP ===
  g.beginPath();g.arc(cx,cy,SI,0,2*Math.PI);g.arc(cx,cy,RR+2,0,2*Math.PI,true);
  g.fillStyle='rgba(6,182,212,0.03)';g.fill();

  // === ROTATING MAGNETIC FIELD (dashed lines + vector) ===
  var fieldAngle = t * FIELD_SPEED;
  g.save();g.globalAlpha=0.2;g.strokeStyle='#06B6D4';g.lineWidth=1;
  g.setLineDash([4,4]);
  for(var i=-3;i<=3;i++){
    var off=i*12;
    var perpA=fieldAngle+Math.PI/2;
    var sx=cx+off*Math.cos(perpA), sy=cy+off*Math.sin(perpA);
    g.beginPath();
    g.moveTo(sx+(SI-4)*Math.cos(fieldAngle), sy+(SI-4)*Math.sin(fieldAngle));
    g.lineTo(sx+(SI-4)*Math.cos(fieldAngle+Math.PI), sy+(SI-4)*Math.sin(fieldAngle+Math.PI));
    g.stroke();
  }
  g.setLineDash([]);g.globalAlpha=1;g.restore();

  // Big rotating B-field arrow
  var bLen=SI-8;
  var bx1=cx+bLen*Math.cos(fieldAngle), by1=cy+bLen*Math.sin(fieldAngle);
  var bx0=cx+30*Math.cos(fieldAngle+Math.PI), by0=cy+30*Math.sin(fieldAngle+Math.PI);
  g.strokeStyle='#06B6D4';g.lineWidth=3;g.globalAlpha=0.7;
  g.beginPath();g.moveTo(bx0,by0);g.lineTo(bx1,by1);g.stroke();
  arw(bx1,by1,fieldAngle,'#06B6D4',10);
  g.globalAlpha=1;
  // B label
  g.font='italic bold 16px Georgia,serif';g.fillStyle='#06B6D4';g.textAlign='center';g.textBaseline='middle';
  var blx=cx+(bLen*0.55)*Math.cos(fieldAngle)+14*Math.cos(fieldAngle+Math.PI/2);
  var bly=cy+(bLen*0.55)*Math.sin(fieldAngle)+14*Math.sin(fieldAngle+Math.PI/2);
  g.fillText('B',blx,bly);

  // === ROTOR ===
  var rotorAngle = t * ROTOR_SPEED;
  g.save();g.translate(cx,cy);g.rotate(rotorAngle);

  // Rotor core
  var rg=g.createRadialGradient(0,0,RI,0,0,RR);
  rg.addColorStop(0,'#1C2128');rg.addColorStop(0.7,'#161B22');rg.addColorStop(1,'#21262D');
  g.beginPath();g.arc(0,0,RR,0,2*Math.PI);g.fillStyle=rg;g.fill();
  g.strokeStyle='#373E47';g.lineWidth=1.5;g.stroke();

  // Lamination lines
  g.strokeStyle='rgba(255,255,255,0.025)';g.lineWidth=0.5;
  for(var i=0;i<36;i++){var la=(i/36)*2*Math.PI;g.beginPath();g.moveTo((RI+2)*Math.cos(la),(RI+2)*Math.sin(la));g.lineTo((RR-2)*Math.cos(la),(RR-2)*Math.sin(la));g.stroke();}

  // Squirrel cage bars
  var barR=(RR+RI)/2+12;
  for(var i=0;i<NB;i++){
    var ba=(i/NB)*2*Math.PI;
    var bx=barR*Math.cos(ba), by=barR*Math.sin(ba);
    // Compute effective angle in stator frame to determine induced current direction
    var absA=ba+rotorAngle;
    var relToField=absA-fieldAngle;
    relToField=relToField%(2*Math.PI); if(relToField<0) relToField+=2*Math.PI;
    var isOut=relToField<Math.PI;
    var currentMag=Math.abs(Math.sin(relToField));

    // Slot hole
    g.beginPath();g.arc(bx,by,5.5,0,2*Math.PI);g.fillStyle='#0D1117';g.fill();
    // Bar conductor
    var barAlpha=0.3+0.7*currentMag;
    g.beginPath();g.arc(bx,by,4,0,2*Math.PI);
    g.fillStyle=isOut?('rgba(249,163,22,'+barAlpha+')'):'rgba(96,165,250,'+barAlpha+')';
    g.fill();g.strokeStyle='rgba(255,255,255,0.15)';g.lineWidth=0.6;g.stroke();
    // Current symbol
    if(currentMag>0.3){
      if(isOut){g.beginPath();g.arc(bx,by,1.5,0,2*Math.PI);g.fillStyle='#FFF';g.fill();}
      else{g.strokeStyle='rgba(255,255,255,'+(0.4+0.6*currentMag)+')';g.lineWidth=1;g.beginPath();g.moveTo(bx-2.5,by-2.5);g.lineTo(bx+2.5,by+2.5);g.moveTo(bx+2.5,by-2.5);g.lineTo(bx-2.5,by+2.5);g.stroke();}
    }
  }

  // End rings
  g.beginPath();g.arc(0,0,barR+6,0,2*Math.PI);
  g.strokeStyle='rgba(212,160,23,0.15)';g.lineWidth=3;g.stroke();
  g.beginPath();g.arc(0,0,barR-6,0,2*Math.PI);
  g.strokeStyle='rgba(212,160,23,0.15)';g.lineWidth=3;g.stroke();

  // Shaft
  var shg=g.createRadialGradient(0,0,0,0,0,RI);
  shg.addColorStop(0,'#4D555E');shg.addColorStop(1,'#3D444D');
  g.beginPath();g.arc(0,0,RI,0,2*Math.PI);g.fillStyle=shg;g.fill();
  g.strokeStyle='#555D66';g.lineWidth=1;g.stroke();
  g.fillStyle='#2D333B';g.fillRect(-2,-RI,4,RI*2);

  g.restore();

  // === LORENTZ FORCE ARROWS on rotor bars ===
  for(var i=0;i<NB;i++){
    var ba=(i/NB)*2*Math.PI+rotorAngle;
    var relToField2=ba-fieldAngle;
    relToField2=relToField2%(2*Math.PI); if(relToField2<0)relToField2+=2*Math.PI;
    var fMag=Math.sin(relToField2);
    if(Math.abs(fMag)>0.5){
      var px=cx+barR*Math.cos(ba), py=cy+barR*Math.sin(ba);
      var fa=ba+(fMag>0?Math.PI/2:-Math.PI/2);
      var fl=14*Math.abs(fMag);
      var fx=px+fl*Math.cos(fa), fy=py+fl*Math.sin(fa);
      g.strokeStyle='rgba(16,185,129,0.7)';g.lineWidth=1.8;
      g.beginPath();g.moveTo(px,py);g.lineTo(fx,fy);g.stroke();
      arw(fx,fy,fa,'rgba(16,185,129,0.7)',5);
    }
  }

  // === EM GLOW ===
  var ga=0.06+0.03*Math.sin(t*3);
  g.beginPath();g.arc(cx,cy,RR+3,0,2*Math.PI);
  g.strokeStyle='rgba(6,182,212,'+ga.toFixed(3)+')';g.lineWidth=4;g.stroke();

  // === ROTOR TORQUE ARROW ===
  g.beginPath();g.arc(cx,cy,RI+8,-2.5,1.3);g.strokeStyle='#10B981';g.lineWidth=2.5;g.stroke();
  arw(cx+(RI+8)*Math.cos(1.3),cy+(RI+8)*Math.sin(1.3),1.3+Math.PI/2,'#10B981',7);
  g.font='italic bold 14px Georgia,serif';g.fillStyle='#10B981';g.textAlign='center';g.textBaseline='middle';
  g.fillText('\u03c9',cx,cy);

  // === STATOR LABELS ===
  g.font='600 10px Inter,sans-serif';g.fillStyle='#8B949E';g.textAlign='center';
  g.fillText('EST\u00c1TOR (3\u03c6)',cx,cy-SR-20);
  g.fillText('ROTOR (Jaula de Ardilla)',cx,cy+RR+22);

  // Air gap label
  var gx=cx+(SI+RR+2)/2*Math.cos(-0.35), gy=cy+(SI+RR+2)/2*Math.sin(-0.35);
  g.font='9px Inter,sans-serif';g.fillStyle='#555D66';g.textAlign='left';
  g.fillText('\u03b4 (entrehierro)',gx+4,gy-2);
  g.strokeStyle='#555D66';g.lineWidth=0.7;
  g.beginPath();g.moveTo(cx+SI*Math.cos(-0.35),cy+SI*Math.sin(-0.35));
  g.lineTo(cx+(RR+2)*Math.cos(-0.35),cy+(RR+2)*Math.sin(-0.35));g.stroke();

  // === SINE WAVE PANEL (3 phases) ===
  var px0=W-215, py0=35, pw=195, ph=100;
  rr(px0,py0,pw,ph,6);g.fillStyle='rgba(13,17,23,0.92)';g.fill();g.strokeStyle='#30363D';g.lineWidth=1;g.stroke();
  g.font='600 10px Inter,sans-serif';g.fillStyle='#E6EDF3';g.textAlign='left';
  g.fillText('CORRIENTES ESTATOR\u00cdCAS',px0+8,py0+14);
  // Axes
  var wOx=px0+10, wOy=py0+55, wW=pw-20, wH=32;
  g.strokeStyle='#30363D';g.lineWidth=0.5;
  g.beginPath();g.moveTo(wOx,wOy);g.lineTo(wOx+wW,wOy);g.stroke();
  // Draw 3 sine waves
  for(var p2=0;p2<3;p2++){
    g.strokeStyle=phaseColors[p2];g.lineWidth=1.5;g.beginPath();
    for(var x=0;x<wW;x++){
      var tLocal=t*3 + (x/wW)*4*Math.PI - phaseAngles[p2];
      var yy=wOy - wH*Math.cos(tLocal);
      if(x===0) g.moveTo(wOx+x,yy); else g.lineTo(wOx+x,yy);
    }
    g.stroke();
  }
  // Phase labels
  g.font='bold 9px Inter,sans-serif';
  for(var p2=0;p2<3;p2++){
    g.fillStyle=phaseColors[p2];
    g.fillText(phaseNames[p2],px0+10+p2*25,py0+ph-6);
  }

  // === LIVE DATA PANEL ===
  var dx0=px0, dy0=py0+ph+14, dw=pw, dh=128;
  rr(dx0,dy0,dw,dh,6);g.fillStyle='rgba(13,17,23,0.92)';g.fill();g.strokeStyle='#30363D';g.lineWidth=1;g.stroke();
  g.font='600 10px Inter,sans-serif';g.fillStyle='#E6EDF3';g.textAlign='left';
  g.fillText('PAR\u00c1METROS EN TIEMPO REAL',dx0+8,dy0+14);

  var ns=1500, n=Math.round(ns*(1-SLIP)), s_pct=(SLIP*100).toFixed(1), f2=(SLIP*50).toFixed(1);
  var items=[
    ['n\u209B (sincronis.)',ns+' rpm','#06B6D4'],
    ['n  (rotor)',n+' rpm','#10B981'],
    ['s  (deslizam.)',s_pct+' %','#F9A826'],
    ['f\u2082 (frec. rotor)',f2+' Hz','#818CF8'],
    ['p  (pares polos)','2','#9CA3AF']
  ];
  g.font='11px Inter,sans-serif';
  for(var i=0;i<items.length;i++){
    var iy=dy0+30+i*19;
    g.fillStyle='#6E7681';g.textAlign='left';g.fillText(items[i][0],dx0+10,iy);
    g.fillStyle=items[i][2];g.textAlign='right';g.font='bold 11px Inter,sans-serif';g.fillText(items[i][1],dx0+dw-10,iy);
    g.font='11px Inter,sans-serif';
  }

  // === LEGEND ===
  var lx0=px0, ly0=dy0+dh+14, lw2=pw, lh2=120;
  rr(lx0,ly0,lw2,lh2,6);g.fillStyle='rgba(13,17,23,0.92)';g.fill();g.strokeStyle='#30363D';g.lineWidth=1;g.stroke();
  g.font='600 10px Inter,sans-serif';g.fillStyle='#E6EDF3';g.textAlign='left';
  g.fillText('LEYENDA',lx0+8,ly0+14);
  g.font='10px Inter,sans-serif';var yl=ly0+30;

  // Rotating field
  g.strokeStyle='#06B6D4';g.lineWidth=2;g.beginPath();g.moveTo(lx0+10,yl);g.lineTo(lx0+24,yl);g.stroke();
  arw(lx0+24,yl,0,'#06B6D4',5);
  g.fillStyle='#8B949E';g.fillText('Campo B giratorio',lx0+30,yl+4);yl+=18;

  // Current out
  g.beginPath();g.arc(lx0+17,yl,4,0,2*Math.PI);g.fillStyle='#F9A826';g.fill();
  g.beginPath();g.arc(lx0+17,yl,1.5,0,2*Math.PI);g.fillStyle='#FFF';g.fill();
  g.fillStyle='#8B949E';g.fillText('Corriente inducida \u2299',lx0+30,yl+4);yl+=18;

  // Current in
  g.beginPath();g.arc(lx0+17,yl,4,0,2*Math.PI);g.fillStyle='#60A5FA';g.fill();
  g.strokeStyle='#FFF';g.lineWidth=1;g.beginPath();g.moveTo(lx0+14,yl-3);g.lineTo(lx0+20,yl+3);g.moveTo(lx0+20,yl-3);g.lineTo(lx0+14,yl+3);g.stroke();
  g.fillStyle='#8B949E';g.fillText('Corriente inducida \u2297',lx0+30,yl+4);yl+=18;

  // Lorentz force
  g.strokeStyle='#10B981';g.lineWidth=2;g.beginPath();g.moveTo(lx0+10,yl);g.lineTo(lx0+24,yl);g.stroke();
  arw(lx0+24,yl,0,'#10B981',5);
  g.fillStyle='#8B949E';g.fillText('Fuerza F = I \u00d7 B',lx0+30,yl+4);yl+=18;

  // Torque
  g.beginPath();g.arc(lx0+17,yl,5,-2,0.8);g.strokeStyle='#10B981';g.lineWidth=1.5;g.stroke();
  g.fillStyle='#8B949E';g.fillText('Par motor (\u03c9)',lx0+30,yl+4);

  // === EQUATIONS PANEL ===
  var ex0=px0, ey0=ly0+lh2+14, ew2=pw, eh2=75;
  rr(ex0,ey0,ew2,eh2,6);g.fillStyle='rgba(13,17,23,0.92)';g.fill();g.strokeStyle='#30363D';g.lineWidth=1;g.stroke();
  g.font='600 10px Inter,sans-serif';g.fillStyle='#E6EDF3';g.textAlign='left';
  g.fillText('ECUACIONES CLAVE',ex0+8,ey0+14);
  g.font='italic 12px Georgia,serif';g.fillStyle='#C9D1D9';
  g.fillText('n\u209B = 60\u00b7f / p',ex0+12,ey0+34);
  g.fillText('s = (n\u209B \u2212 n) / n\u209B',ex0+12,ey0+52);
  g.fillText('f\u2082 = s \u00b7 f\u2081',ex0+12,ey0+68);

  t+=0.012;requestAnimationFrame(draw);}
  draw();
})();
</script>
"""

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
    st.header("Máquinas Asíncronas (Motores de Inducción)")
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

        components.html(ASYNC_MOTOR_ANIMATION_HTML, height=540)

        with st.expander("🛠️ Paso a Paso: Desde la Alimentación hasta el Movimiento", expanded=True):
            st.markdown(r"""
            Para entender cómo una máquina estática, sin contacto eléctrico en el rotor, se convierte en un potente motor rotativo, debemos seguir la cadena de fenómenos físicos paso a paso:
            
            1.  **Inyección Trifásica:** Se inyecta un sistema equilibrado de corrientes alternas trifásicas en los devanados fijos del estator.
            2.  **Campo Magnético Giratorio (Teorema de Ferraris):** Estas corrientes generan tres campos magnéticos pulsantes que, al sumarse geométricamente en el entrehierro, crean un único **campo magnético rotativo** de amplitud constante. Este campo invisible gira como un imán a una velocidad exacta llamada velocidad de sincronismo ($n_s$).
            3.  **Inducción Magnética (Ley de Faraday):** En el instante inicial, el rotor está completamente quieto. Las líneas del campo magnético giratorio "barren" y cortan a gran velocidad las barras conductoras de la jaula de ardilla del rotor, induciendo en ellas una Fuerza Electromotriz (FEM o tensión).
            4.  **Corrientes Rotóricas:** Como las barras del rotor están cortocircuitadas en sus extremos (por los anillos), esta tensión inducida provoca que comiencen a circular **altísimas corrientes eléctricas** masivas por el interior del rotor.
            5.  **Fuerza de Lorentz:** Ahora tenemos conductores con corriente (las barras del rotor) inmersos dentro de un fuerte campo magnético externo (el del estator). Automáticamente, sobre cada barra aparece una fuerza mecánica ($\vec{F} = I \cdot \vec{L} \times \vec{B}$).
            6.  **Giro y Deslizamiento (Ley de Lenz):** La suma de las fuerzas sobre todas las barras conforma el **Par Motor**, obligando al rotor a girar persiguiendo al campo del estator. Intenta "alcanzarlo" para anular el corte de líneas (Lenz). Sin embargo, nunca lo logra: si lo alcanzara, cesaría la inducción, la corriente caería a cero y el motor se pararía. Esta eterna persecución genera el **deslizamiento ($s$)**.
            """)
            
        col_teoria1, col_teoria2 = st.columns(2)
        
        with col_teoria1:
            st.markdown("#### Flujo Magnético y Ley de Faraday")
            st.write(r"El flujo magnético ($\Phi$) que atraviesa una superficie $S$ debido a un campo magnético de densidad $\vec{B}$ se define como:")
            st.latex(r"\Phi = \iint_S \vec{B} \cdot d\vec{S}")
            
            st.write("La **Ley de Faraday** establece que cualquier variación temporal del flujo magnético que atraviesa un circuito induce una Fuerza Electromotriz (f.e.m. o tensión) en él. La **Ley de Lenz** añade el signo negativo, indicando que la f.e.m. inducida se opone a la causa que la produce:")
            st.latex(r"e(t) = -N \frac{d\Phi(t)}{dt}")
            st.caption("Donde $N$ es el número de espiras del devanado.")

        with col_teoria2:
            st.markdown("#### Ecuación Fundamental de las Máquinas de C.A.")
            st.write("Si asumimos que el flujo en el entrehierro varía de forma senoidal en el tiempo (debido al campo giratorio creado por el estator):")
            st.latex(r"\Phi(t) = \Phi_{max} \cdot \cos(\omega t)")
            
            st.write("Derivando para encontrar la f.e.m. instantánea:")
            st.latex(r"e(t) = -N \frac{d}{dt} [\Phi_{max} \cos(\omega t)] = N \cdot \omega \cdot \Phi_{max} \cdot \sin(\omega t)")
            
            st.write(r"El valor eficaz (RMS) de esta tensión se obtiene dividiendo la amplitud entre $\sqrt{2}$. Sabiendo que $\omega = 2\pi f$:")
            st.latex(r"E = \frac{N \cdot 2\pi f \cdot \Phi_{max}}{\sqrt{2}} \approx 4.44 \cdot f \cdot N \cdot \Phi_{max}")

        st.markdown("---")
        
        # NUEVA SECCIÓN EXTENSA SOLICITADA
        st.markdown("### Cinemática del Motor: Sincronismo, Rotor y Deslizamiento")
        st.write("Para entender cómo se produce el movimiento en un motor asíncrono, es fundamental analizar la relación entre la velocidad del campo magnético (generado eléctricamente) y la velocidad de giro físico del rotor. En esta interacción reside la esencia de su funcionamiento.")

        st.markdown("#### Velocidad de Sincronismo ($n_s$)")
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

        st.markdown("#### Velocidad Mecánica del Rotor ($n$)")
        st.write("Es la velocidad física a la que gira el eje del motor acoplado a nuestra carga. En un motor asíncrono en funcionamiento como motor, **el rotor nunca puede alcanzar la velocidad de sincronismo** ($n < n_s$).")
        st.info(r"""**¿Por qué es imposible que $n = n_s$?**

Las barras o el devanado del rotor giran para intentar 'alcanzar' al campo magnético. Si el rotor girase exactamente a la velocidad del campo ($n_s$), ambas partes viajarían juntas y solidarias. El campo magnético ya no 'cortaría' las barras del rotor. Sin este corte continuo de líneas de flujo, la variación de flujo sería cero ($d\Phi/dt = 0$), la f.e.m. inducida desaparecería, no habría corrientes rotóricas y, por ende, el **par electromagnético caería a cero**. El motor necesita esa diferencia de velocidad para seguir empujando.""")

        st.markdown("#### El Deslizamiento ($s$)")
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

        st.markdown("#### Consecuencia Analítica: La Frecuencia Rotórica ($f_2$)")
        st.write("Dado que el rotor gira a $n$ rpm y el campo a $n_s$ rpm, el devanado rotórico percibe que el campo magnético le adelanta a una velocidad relativa de $n_s - n$. Esta velocidad relativa es la que determina la **frecuencia de las corrientes que circularán por el rotor ($f_2$)**.")
        st.latex(r"f_2 = \frac{p \cdot (n_s - n)}{60}")
        st.write(r"Si sustituimos la expresión del deslizamiento ($n_s - n = s \cdot n_s$) en esta ecuación:")
        st.latex(r"f_2 = \frac{p \cdot (s \cdot n_s)}{60} = s \cdot \left(\frac{p \cdot n_s}{60}\right)")
        st.write("Recordando la fórmula de $n_s$, el término entre paréntesis es exactamente la frecuencia de red ($f_1$). Esto nos da la relación fundamental de frecuencias de la máquina asíncrona:")
        st.latex(r"f_2 = s \cdot f_1")
        
        st.success(r"""**Ejemplo Práctico:**
En el instante del **arranque** (motor parado, $n=0$), el deslizamiento es máximo ($s=1$). Por tanto, $f_2 = f_1$ (50 Hz). El motor se comporta temporalmente como un transformador estático. Cuando el motor alcanza su **régimen de trabajo nominal**, el deslizamiento suele ser minúsculo ($s \approx 0.02$ a $0.05$). Esto significa que en condiciones normales, las corrientes que circulan por el rotor oscilan a bajísimas frecuencias ($f_2 \approx 1$ a $2.5 \text{ Hz}$).""")


    # --------------------------------------------------------------------------
    # PESTAÑA 2.2: CIRCUITO EQUIVALENTE
    # --------------------------------------------------------------------------
    with tab_circuito:
        st.markdown("### Modelo Analítico de Steinmetz (Por fase)")
        st.write("""
        El motor asíncrono puede estudiarse analógicamente como un **transformador cuyo secundario está en cortocircuito y gira**. 
        Sin embargo, al girar, la frecuencia de las corrientes del rotor ($f_2 = s \cdot f_1$) es distinta a la del estator. 
        Para poder unir ambos circuitos eléctricamente, se reducen las magnitudes del rotor al estator (multiplicando por la relación de transformación efectiva) y se divide la impedancia rotórica entre el deslizamiento ($s$).
        """)

        st.markdown("---")

        col_exacto, col_aprox = st.columns(2)

        with col_exacto:
            st.markdown("#### Circuito Equivalente Exacto")
            st.write("Representa fielmente el motor conectando la rama en derivación (magnetización y pérdidas en el hierro) en el medio de la red, tras la caída de tensión en la impedancia del estator.")
            
            st.markdown("""
            <div style="background:#0E1117; border:1px solid #2a2a3a; border-radius:10px; padding:18px 10px 10px 10px; margin-bottom:10px;">
            <svg viewBox="0 0 680 210" xmlns="http://www.w3.org/2000/svg" style="width:100%;font-family:'monospace',sans-serif;">
              <!-- Estilos -->
              <defs>
                <marker id="arr" markerWidth="8" markerHeight="8" refX="6" refY="3" orient="auto">
                  <path d="M0,0 L0,6 L8,3 z" fill="#9CA3AF"/>
                </marker>
              </defs>

              <!-- Rail superior -->
              <line x1="30" y1="50" x2="650" y2="50" stroke="#4B5563" stroke-width="1.5" stroke-dasharray="4,3"/>
              <!-- Rail inferior -->
              <line x1="30" y1="170" x2="650" y2="170" stroke="#4B5563" stroke-width="1.5" stroke-dasharray="4,3"/>

              <!-- Fuente U1 izquierda -->
              <circle cx="30" cy="110" r="20" fill="none" stroke="#00ADB5" stroke-width="2"/>
              <text x="30" y="114" text-anchor="middle" fill="#00ADB5" font-size="11" font-weight="bold">U₁</text>
              <line x1="30" y1="50" x2="30" y2="90" stroke="#00ADB5" stroke-width="2"/>
              <line x1="30" y1="130" x2="30" y2="170" stroke="#00ADB5" stroke-width="2"/>

              <!-- Resistencia R1 -->
              <line x1="50" y1="50" x2="90" y2="50" stroke="#9CA3AF" stroke-width="2"/>
              <rect x="90" y="40" width="50" height="20" rx="3" fill="none" stroke="#F9A826" stroke-width="2"/>
              <text x="115" y="33" text-anchor="middle" fill="#F9A826" font-size="11">R₁</text>
              <line x1="140" y1="50" x2="190" y2="50" stroke="#9CA3AF" stroke-width="2"/>

              <!-- Reactancia jX1 -->
              <rect x="190" y="40" width="50" height="20" rx="3" fill="none" stroke="#818CF8" stroke-width="2"/>
              <text x="215" y="33" text-anchor="middle" fill="#818CF8" font-size="11">jX₁</text>
              <line x1="240" y1="50" x2="290" y2="50" stroke="#9CA3AF" stroke-width="2"/>

              <!-- Nudo central -->
              <circle cx="290" cy="50" r="3" fill="#9CA3AF"/>
              <line x1="290" y1="50" x2="290" y2="90" stroke="#9CA3AF" stroke-width="1.5"/>

              <!-- Rama shunt: RFe -->
              <rect x="270" y="90" width="40" height="18" rx="3" fill="none" stroke="#EF4444" stroke-width="1.8"/>
              <text x="256" y="103" text-anchor="end" fill="#EF4444" font-size="10">Rᶠᴇ</text>
              <line x1="290" y1="108" x2="290" y2="125" stroke="#9CA3AF" stroke-width="1.5"/>

              <!-- Rama shunt: jXm -->
              <rect x="270" y="125" width="40" height="18" rx="3" fill="none" stroke="#A78BFA" stroke-width="1.8"/>
              <text x="256" y="138" text-anchor="end" fill="#A78BFA" font-size="10">jXm</text>
              <line x1="290" y1="143" x2="290" y2="170" stroke="#9CA3AF" stroke-width="1.5"/>

              <!-- Linea central-derecha -->
              <line x1="290" y1="50" x2="340" y2="50" stroke="#9CA3AF" stroke-width="2"/>

              <!-- Reactancia jX'2 -->
              <rect x="340" y="40" width="50" height="20" rx="3" fill="none" stroke="#818CF8" stroke-width="2"/>
              <text x="365" y="33" text-anchor="middle" fill="#818CF8" font-size="11">jX'₂</text>
              <line x1="390" y1="50" x2="440" y2="50" stroke="#9CA3AF" stroke-width="2"/>

              <!-- Resistencia R'2/s -->
              <rect x="440" y="40" width="60" height="20" rx="3" fill="none" stroke="#34D399" stroke-width="2"/>
              <text x="470" y="33" text-anchor="middle" fill="#34D399" font-size="11">R'₂/s</text>
              <line x1="500" y1="50" x2="530" y2="50" stroke="#9CA3AF" stroke-width="2"/>

              <!-- Terminal salida -->
              <circle cx="530" cy="50" r="4" fill="#34D399"/>
              <text x="545" y="45" fill="#34D399" font-size="10">+</text>
              <line x1="530" y1="50" x2="530" y2="170" stroke="#34D399" stroke-width="1.5" stroke-dasharray="4,2"/>
              <circle cx="530" cy="170" r="4" fill="#34D399"/>
              <text x="545" y="174" fill="#34D399" font-size="10">−</text>

              <!-- Etiqueta I1 -->
              <text x="65" y="43" fill="#9CA3AF" font-size="10">→ I₁</text>
              <!-- Etiqueta I'2 -->
              <text x="360" y="43" fill="#9CA3AF" font-size="10">→ I'₂</text>
              <!-- Etiqueta I0 -->
              <text x="297" y="90" fill="#9CA3AF" font-size="10">↓ I₀</text>

              <!-- Etiqueta E1 -->
              <text x="295" y="175" fill="#6EE7B7" font-size="9" text-anchor="middle">E₁</text>

              <!-- Secciones coloreadas estator/rotor -->
              <text x="165" y="195" text-anchor="middle" fill="#F9A826" font-size="10" font-weight="bold">ESTATOR</text>
              <line x1="80" y1="190" x2="250" y2="190" stroke="#F9A826" stroke-width="1" stroke-dasharray="2,2"/>
              <text x="440" y="195" text-anchor="middle" fill="#34D399" font-size="10" font-weight="bold">ROTOR (reducido al estator)</text>
              <line x1="340" y1="190" x2="540" y2="190" stroke="#34D399" stroke-width="1" stroke-dasharray="2,2"/>
            </svg>
            </div>
            """, unsafe_allow_html=True)
            
            st.markdown("**Ecuaciones de malla:**")
            st.latex(r"\vec{U}_1 = \vec{I}_1 (R_1 + jX_1) + \vec{E}_1")
            st.latex(r"\vec{E}_1 = \vec{I}'_2 \left( \frac{R'_2}{s} + jX'_2 \right)")
            st.latex(r"\vec{I}_1 = \vec{I}_0 + \vec{I}'_2")

        with col_aprox:
            st.markdown("#### Circuito Equivalente Aproximado")
            st.write("Para simplificar cálculos manuales, se traslada la rama transversal a la entrada. El error cometido es mínimo (especialmente en motores grandes) ya que la caída de tensión estatórica debida a la corriente de vacío ($I_0$) es muy pequeña.")

            st.markdown("""
            <div style="background:#0E1117; border:1px solid #2a2a3a; border-radius:10px; padding:18px 10px 10px 10px; margin-bottom:10px;">
            <svg viewBox="0 0 680 210" xmlns="http://www.w3.org/2000/svg" style="width:100%;font-family:'monospace',sans-serif;">

              <!-- Rails -->
              <line x1="30" y1="50" x2="650" y2="50" stroke="#4B5563" stroke-width="1.5" stroke-dasharray="4,3"/>
              <line x1="30" y1="170" x2="650" y2="170" stroke="#4B5563" stroke-width="1.5" stroke-dasharray="4,3"/>

              <!-- Fuente U1 -->
              <circle cx="30" cy="110" r="20" fill="none" stroke="#00ADB5" stroke-width="2"/>
              <text x="30" y="114" text-anchor="middle" fill="#00ADB5" font-size="11" font-weight="bold">U₁</text>
              <line x1="30" y1="50" x2="30" y2="90" stroke="#00ADB5" stroke-width="2"/>
              <line x1="30" y1="130" x2="30" y2="170" stroke="#00ADB5" stroke-width="2"/>

              <!-- Nudo de shunt (al inicio, circuito aprox) -->
              <circle cx="80" cy="50" r="3" fill="#9CA3AF"/>
              <line x1="80" y1="50" x2="80" y2="90" stroke="#9CA3AF" stroke-width="1.5"/>

              <!-- Rama shunt: RFe -->
              <rect x="60" y="90" width="40" height="18" rx="3" fill="none" stroke="#EF4444" stroke-width="1.8"/>
              <text x="46" y="103" text-anchor="end" fill="#EF4444" font-size="10">Rᶠᴇ</text>
              <line x1="80" y1="108" x2="80" y2="125" stroke="#9CA3AF" stroke-width="1.5"/>

              <!-- Rama shunt: jXm -->
              <rect x="60" y="125" width="40" height="18" rx="3" fill="none" stroke="#A78BFA" stroke-width="1.8"/>
              <text x="46" y="138" text-anchor="end" fill="#A78BFA" font-size="10">jXm</text>
              <line x1="80" y1="143" x2="80" y2="170" stroke="#9CA3AF" stroke-width="1.5"/>

              <!-- Linea principal tras shunt -->
              <line x1="80" y1="50" x2="140" y2="50" stroke="#9CA3AF" stroke-width="2"/>

              <!-- Resistencia R1+R'2/s combinada -->
              <rect x="140" y="40" width="70" height="20" rx="3" fill="none" stroke="#F9A826" stroke-width="2"/>
              <text x="175" y="33" text-anchor="middle" fill="#F9A826" font-size="10">R₁+R'₂/s</text>
              <line x1="210" y1="50" x2="270" y2="50" stroke="#9CA3AF" stroke-width="2"/>

              <!-- Reactancia j(X1+X'2) combinada -->
              <rect x="270" y="40" width="75" height="20" rx="3" fill="none" stroke="#818CF8" stroke-width="2"/>
              <text x="307" y="33" text-anchor="middle" fill="#818CF8" font-size="10">j(X₁+X'₂)</text>
              <line x1="345" y1="50" x2="390" y2="50" stroke="#9CA3AF" stroke-width="2"/>

              <!-- Terminal salida -->
              <circle cx="390" cy="50" r="4" fill="#34D399"/>
              <text x="405" y="45" fill="#34D399" font-size="10">+</text>
              <line x1="390" y1="50" x2="390" y2="170" stroke="#34D399" stroke-width="1.5" stroke-dasharray="4,2"/>
              <circle cx="390" cy="170" r="4" fill="#34D399"/>
              <text x="405" y="174" fill="#34D399" font-size="10">−</text>

              <!-- Etiquetas de corriente -->
              <text x="95" y="43" fill="#9CA3AF" font-size="10">→ I₁≈I'₂</text>
              <text x="87" y="90" fill="#9CA3AF" font-size="10">↓ I₀</text>

              <!-- Etiquetas secciones -->
              <text x="50" y="195" text-anchor="middle" fill="#A78BFA" font-size="10" font-weight="bold">SHUNT</text>
              <text x="265" y="195" text-anchor="middle" fill="#F9A826" font-size="10" font-weight="bold">SERIE (Estator + Rotor reducido)</text>
              <line x1="55" y1="190" x2="110" y2="190" stroke="#A78BFA" stroke-width="1" stroke-dasharray="2,2"/>
              <line x1="130" y1="190" x2="400" y2="190" stroke="#F9A826" stroke-width="1" stroke-dasharray="2,2"/>
            </svg>
            </div>
            """, unsafe_allow_html=True)
            
            st.markdown("**Simplificación (Impedancia de cortocircuito):**")
            st.latex(r"\vec{Z}_{cc} = (R_1 + \frac{R'_2}{s}) + j(X_1 + X'_2)")
            st.latex(r"\vec{I}'_2 \approx \frac{\vec{U}_1}{\vec{Z}_{cc}}")

        st.markdown("---")
        st.markdown("#### Desdoblamiento de la Resistencia Rotórica")
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
        st.markdown("### Análisis de la Curva Característica Par-Velocidad")
        st.write("La curva de Par-Velocidad (o Par-Deslizamiento) es la huella dactilar del motor asíncrono. Nos permite comprender visualmente cuánta fuerza rotatoria es capaz de ejercer el motor desde el instante en que recibe corriente hasta que alcanza su régimen de trabajo continuo.")

        col_exp1, col_exp2 = st.columns([1.1, 1])

        with col_exp1:
            st.markdown("#### Zonas de Funcionamiento Clave")
            st.markdown("""
            A lo largo de la curva podemos identificar hitos vitales para la operación de la máquina:
            
            * **1. Punto de Arranque ($s=1, n=0$):** El rotor está completamente quieto. El campo magnético gira a máxima velocidad relativa, cortando las barras del rotor. Se induce mucha f.e.m. y enormes corrientes, pero debido a la alta reactancia del rotor a esta frecuencia ($50$ Hz), el factor de potencia es pésimo y el **Par de Arranque** no es el máximo posible.
            * **2. Zona Inestable:** Abarca desde el arranque hasta el pico de la curva. Si acoplamos una carga mecánica que exija un par mayor al que el motor da en esta zona, el motor es incapaz de acelerar y se "cala".
            * **3. Par Máximo o Crítico ($M_{max}$):** Es el punto más alto de la montaña. Ocurre a un deslizamiento específico ($s_k$). Determina la capacidad máxima de sobrecarga del motor antes de detenerse abruptamente.
            * **4. Zona Estable (Régimen Nominal):** Es la ladera que cae de forma casi recta hacia la derecha. Aquí, si la carga frena ligeramente al motor (aumenta $s$), el motor responde entregando más par, alcanzando rápidamente un nuevo equilibrio. **Aquí trabaja el motor en la vida real**.
            * **5. Sincronismo ($s=0, n=n_s$):** El rotor gira exactamente a la misma velocidad que el campo magnético. No hay corte de líneas de flujo, no hay corriente inducida y el motor entrega **0 N·m de par**.
            """)

        with col_exp2:
            st.markdown("#### Desarrollo Analítico")
            st.write("Resolviendo el circuito equivalente exacto (mediante el Teorema de Thévenin), la ecuación fundamental del par electromagnético es:")
            
            st.latex(r"M = \frac{3 \cdot U_1^2 \cdot \frac{R'_2}{s}}{\omega_s \left[ \left(R_1 + \frac{R'_2}{s}\right)^2 + (X_1 + X'_2)^2 \right]}")
            
            st.info("""
            **Análisis de Límites (Comportamiento Asintótico):**
            * **Cerca del sincronismo (ZONA ESTABLE):** El deslizamiento $s$ es muy pequeño (ej: $0.02$). El término $R'_2/s$ se hace dominante en el denominador. Simplificando, el par queda directamente proporcional al deslizamiento: $M \propto s$. Esto explica por qué la curva es una **línea recta** al final.
            * **En el arranque (ZONA INESTABLE):** El deslizamiento $s$ es grande (cercano a 1). El denominador queda dominado por las reactancias. Simplificando, el par es inversamente proporcional al deslizamiento: $M \propto \frac{1}{s}$. Esto explica la forma de **hipérbola**.
            """)
            
            st.error("**⚠️ Regla de Oro:** Fíjate en el numerador. El par electromagnético es **proporcional al cuadrado de la tensión de red ($U_1^2$)**. Si en una fábrica la tensión cae un **10%**, ¡el motor perderá un **19%** de su capacidad de empuje!")

        st.markdown("---")
        st.markdown("#### Simulador Interactivo: Curva Par-Velocidad en Tiempo Real")
        st.write("Modifica cualquier parámetro en los controles integrados y observa cómo la curva característica del motor evoluciona instantáneamente.")

        # ==================================================================
        # SIMULADOR PROFESIONAL — CURVA PAR-VELOCIDAD
        # HTML5 Canvas con controles integrados estilo ingeniería
        # ==================================================================
        TORQUE_SPEED_HTML = """
        <link href="https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800&display=swap" rel="stylesheet">
        <style>
          *{margin:0;padding:0;box-sizing:border-box;}
          body{background:transparent;overflow:hidden;}
          #tw{
            font-family:'Inter',sans-serif;
            background:linear-gradient(145deg,#060a10,#0b1018,#080d14);
            border:1px solid rgba(255,255,255,0.08);
            border-radius:14px;position:relative;overflow:hidden;
          }
          #tw::before{content:'';position:absolute;top:0;left:0;right:0;height:1px;
            background:linear-gradient(90deg,transparent,rgba(0,173,181,0.5),transparent);}
          .th{display:flex;align-items:center;justify-content:space-between;padding:14px 22px;
            background:rgba(255,255,255,0.02);border-bottom:1px solid rgba(255,255,255,0.06);}
          .th .tt{font-size:14px;font-weight:700;color:#e5e7eb;letter-spacing:0.5px;}
          .th .tt span{color:#00ADB5;font-weight:800;}
          .tp{display:flex;gap:0;padding:0;border-bottom:1px solid rgba(255,255,255,0.06);}
          .tp .pc{flex:1;padding:12px 14px;border-right:1px solid rgba(255,255,255,0.04);}
          .tp .pc:last-child{border-right:none;}
          .tp .pc label{display:block;font-size:9px;color:#6b7280;text-transform:uppercase;
            letter-spacing:1px;margin-bottom:5px;font-weight:600;}
          .tp .pc input[type=range]{width:100%;accent-color:#00ADB5;height:6px;margin:0;}
          .tp .pc .sv{font-size:15px;font-weight:800;margin-top:3px;}
          .tp .pc .sv.cyan{color:#00ADB5;}
          .tp .pc .sv.red{color:#ef4444;}
          .tp .pc .sv.purple{color:#a78bfa;}
          .tp .pc .sv.amber{color:#f59e0b;}
          canvas#tc{display:block;width:100%;}
          .tr{display:flex;gap:0;border-top:1px solid rgba(255,255,255,0.06);}
          .tr .rc{flex:1;text-align:center;padding:11px 6px;
            border-right:1px solid rgba(255,255,255,0.04);}
          .tr .rc:last-child{border-right:none;}
          .tr .rc .rl{font-size:9px;color:#6b7280;text-transform:uppercase;letter-spacing:1px;margin-bottom:2px;}
          .tr .rc .rv{font-size:18px;font-weight:800;}
          .tr .rc .rv.cyan{color:#00ADB5;}
          .tr .rc .rv.red{color:#ef4444;}
          .tr .rc .rv.amber{color:#f59e0b;}
          .tr .rc .rv.green{color:#34d399;}
          .tr .rc .ru{font-size:9px;color:#4b5563;margin-top:1px;}
        </style>
        <div id="tw">
          <div class="th">
            <div class="tt"><span>⚙</span> Curva Característica Par-Velocidad — Motor Asíncrono Trifásico</div>
          </div>
          <div class="tp">
            <div class="pc">
              <label>Tensión de Línea U<sub>L</sub> (V)</label>
              <input type="range" id="sl_ul" min="100" max="690" value="400" step="10">
              <div class="sv cyan" id="v_ul">400</div>
            </div>
            <div class="pc">
              <label>Resistencia Rotor R'₂ (Ω)</label>
              <input type="range" id="sl_r2" min="0.1" max="5" value="0.4" step="0.1">
              <div class="sv amber" id="v_r2">0.4</div>
            </div>
            <div class="pc">
              <label>Reactancia Total X₁+X'₂ (Ω)</label>
              <input type="range" id="sl_xt" min="0.5" max="10" value="2.7" step="0.1">
              <div class="sv purple" id="v_xt">2.7</div>
            </div>
            <div class="pc">
              <label>R₁ Estator (Ω)</label>
              <input type="range" id="sl_r1" min="0.1" max="3" value="0.5" step="0.1">
              <div class="sv" style="color:#9ca3af" id="v_r1">0.5</div>
            </div>
            <div class="pc">
              <label>Pares de Polos p</label>
              <input type="range" id="sl_pp" min="1" max="4" value="1" step="1">
              <div class="sv red" id="v_pp">1</div>
            </div>
          </div>
          <canvas id="tc"></canvas>
          <div class="tr">
            <div class="rc"><div class="rl">n<sub>s</sub></div><div class="rv cyan" id="r_ns">3000</div><div class="ru">rpm</div></div>
            <div class="rc"><div class="rl">M<sub>max</sub></div><div class="rv red" id="r_mmax">0</div><div class="ru">N·m</div></div>
            <div class="rc"><div class="rl">s<sub>k</sub></div><div class="rv amber" id="r_sk">0</div><div class="ru">—</div></div>
            <div class="rc"><div class="rl">n @ M<sub>max</sub></div><div class="rv green" id="r_nmmax">0</div><div class="ru">rpm</div></div>
            <div class="rc"><div class="rl">M<sub>arr</sub></div><div class="rv amber" id="r_marr">0</div><div class="ru">N·m</div></div>
            <div class="rc"><div class="rl">M<sub>max</sub>/M<sub>arr</sub></div><div class="rv" style="color:#818cf8" id="r_ratio">0</div><div class="ru">—</div></div>
          </div>
        </div>
        <script>
        (function(){
        var cv=document.getElementById('tc'),g=cv.getContext('2d');
        var W,H;
        var sl_ul=document.getElementById('sl_ul'),sl_r2=document.getElementById('sl_r2');
        var sl_xt=document.getElementById('sl_xt'),sl_r1=document.getElementById('sl_r1');
        var sl_pp=document.getElementById('sl_pp');

        function resize(){
          var wrap=document.getElementById('tw');
          W=wrap.clientWidth;
          if(W<10){requestAnimationFrame(resize);return;}
          H=Math.min(460,W*0.52);
          cv.width=W*2;cv.height=H*2;cv.style.height=H+'px';
          g.setTransform(2,0,0,2,0,0);draw();
        }
        requestAnimationFrame(resize);window.addEventListener('resize',resize);

        var ML=65,MR=25,MT=25,MB=50;
        var PI=Math.PI;

        function draw(){
          var UL=parseFloat(sl_ul.value),R2=parseFloat(sl_r2.value);
          var Xt=parseFloat(sl_xt.value),R1=parseFloat(sl_r1.value);
          var pp=parseInt(sl_pp.value);
          var Uf=UL/Math.sqrt(3);
          var ns=3000/pp, ws=2*PI*ns/60;
          var freq=50;

          document.getElementById('v_ul').textContent=UL;
          document.getElementById('v_r2').textContent=R2.toFixed(1);
          document.getElementById('v_xt').textContent=Xt.toFixed(1);
          document.getElementById('v_r1').textContent=R1.toFixed(1);
          document.getElementById('v_pp').textContent=pp;

          /* Compute curve */
          var N=500,sArr=new Float64Array(N),mArr=new Float64Array(N),nArr=new Float64Array(N);
          var Mmax=0,skIdx=0,Marr=0;
          for(var i=0;i<N;i++){
            var s=0.001+(i/(N-1))*0.999;
            sArr[i]=s;
            nArr[i]=ns*(1-s);
            var denom=(R1+R2/s)*(R1+R2/s)+Xt*Xt;
            var I2sq=Uf*Uf/denom;
            var M=3*I2sq*R2/(s*ws);
            mArr[i]=M;
            if(M>Mmax){Mmax=M;skIdx=i;}
          }
          Marr=mArr[N-1];
          var sk=sArr[skIdx], nMmax=nArr[skIdx];
          var ratio=Marr>0?Mmax/Marr:0;

          /* HUD */
          document.getElementById('r_ns').textContent=ns.toFixed(0);
          document.getElementById('r_mmax').textContent=Mmax.toFixed(1);
          document.getElementById('r_sk').textContent=sk.toFixed(3);
          document.getElementById('r_nmmax').textContent=nMmax.toFixed(0);
          document.getElementById('r_marr').textContent=Marr.toFixed(1);
          document.getElementById('r_ratio').textContent=ratio.toFixed(2);

          g.clearRect(0,0,W,H);

          var cW=W-ML-MR, cH=H-MT-MB;
          var maxN=ns*1.05, maxM=Mmax*1.25;

          function xPx(n){return ML+n/maxN*cW;}
          function yPx(m){return MT+cH-m/maxM*cH;}

          /* === Zone fills === */
          /* Unstable zone */
          g.fillStyle='rgba(239,68,68,0.04)';
          g.fillRect(ML,MT,xPx(nMmax)-ML,cH);
          /* Stable zone */
          g.fillStyle='rgba(0,173,181,0.04)';
          g.fillRect(xPx(nMmax),MT,xPx(ns)-xPx(nMmax),cH);

          /* Grid */
          g.strokeStyle='rgba(255,255,255,0.04)';g.lineWidth=0.5;
          var nStep=ns<=1500?250:500;
          for(var gn=0;gn<=maxN;gn+=nStep){
            var xx=xPx(gn);g.beginPath();g.moveTo(xx,MT);g.lineTo(xx,MT+cH);g.stroke();
          }
          for(var i=0;i<=5;i++){
            var yy=MT+cH*i/5;g.beginPath();g.moveTo(ML,yy);g.lineTo(ML+cW,yy);g.stroke();
          }

          /* Axes */
          g.strokeStyle='rgba(255,255,255,0.15)';g.lineWidth=1.5;
          g.beginPath();g.moveTo(ML,MT);g.lineTo(ML,MT+cH);g.lineTo(ML+cW,MT+cH);g.stroke();

          /* X labels */
          g.font='600 10px Inter,sans-serif';g.fillStyle='rgba(255,255,255,0.3)';g.textAlign='center';
          for(var gn=0;gn<=maxN;gn+=nStep){
            g.fillText(gn.toFixed(0),xPx(gn),MT+cH+16);
          }
          g.fillText('Velocidad n (rpm)',ML+cW/2,MT+cH+40);

          /* Y labels */
          g.textAlign='right';g.fillStyle='rgba(255,255,255,0.3)';
          for(var i=0;i<=5;i++){
            var val=maxM*i/5;
            g.fillText(val.toFixed(0),ML-8,MT+cH-cH*i/5+4);
          }
          g.save();g.translate(14,MT+cH/2);g.rotate(-PI/2);
          g.textAlign='center';g.font='600 11px Inter,sans-serif';g.fillStyle='rgba(255,255,255,0.4)';
          g.fillText('Par M (N·m)',0,0);g.restore();

          /* Synchronous speed vertical line */
          var xns=xPx(ns);
          g.beginPath();g.moveTo(xns,MT);g.lineTo(xns,MT+cH);
          g.strokeStyle='rgba(255,255,255,0.12)';g.lineWidth=1;g.setLineDash([6,4]);g.stroke();g.setLineDash([]);
          g.font='600 10px Inter,sans-serif';g.fillStyle='rgba(255,255,255,0.3)';g.textAlign='center';
          g.fillText('n_s = '+ns.toFixed(0)+' rpm',xns,MT-6);

          /* === Main curve === */
          /* Glow pass */
          g.beginPath();
          for(var i=0;i<N;i++){
            var xx=xPx(nArr[i]),yy=yPx(mArr[i]);
            if(i===0)g.moveTo(xx,yy);else g.lineTo(xx,yy);
          }
          g.strokeStyle='rgba(0,173,181,0.15)';g.lineWidth=12;g.lineCap='round';g.stroke();

          /* Fill under curve */
          g.beginPath();g.moveTo(xPx(nArr[0]),yPx(0));
          for(var i=0;i<N;i++){g.lineTo(xPx(nArr[i]),yPx(mArr[i]));}
          g.lineTo(xPx(nArr[N-1]),yPx(0));g.closePath();
          var grd=g.createLinearGradient(0,MT,0,MT+cH);
          grd.addColorStop(0,'rgba(0,173,181,0.12)');grd.addColorStop(1,'rgba(0,173,181,0.01)');
          g.fillStyle=grd;g.fill();

          /* Solid curve */
          g.beginPath();
          for(var i=0;i<N;i++){
            var xx=xPx(nArr[i]),yy=yPx(mArr[i]);
            if(i===0)g.moveTo(xx,yy);else g.lineTo(xx,yy);
          }
          g.strokeStyle='#00ADB5';g.lineWidth=3;g.lineCap='round';g.stroke();

          /* === Zone labels === */
          g.font='bold 12px Inter,sans-serif';g.globalAlpha=0.25;g.textAlign='center';
          g.fillStyle='#ef4444';g.fillText('ZONA INESTABLE',xPx(nMmax/2),yPx(maxM*0.3));
          g.fillStyle='#00ADB5';g.fillText('ZONA ESTABLE',xPx((nMmax+ns)/2),yPx(maxM*0.3));
          g.globalAlpha=1;

          /* === M_max point === */
          var xMm=xPx(nMmax),yMm=yPx(Mmax);
          g.beginPath();g.arc(xMm,yMm,10,0,2*PI);g.fillStyle='rgba(239,68,68,0.15)';g.fill();
          g.beginPath();g.arc(xMm,yMm,6,0,2*PI);g.fillStyle='#ef4444';g.fill();
          g.strokeStyle='rgba(255,255,255,0.6)';g.lineWidth=2;g.stroke();
          /* Label */
          g.font='bold 12px Inter,sans-serif';g.fillStyle='#fca5a5';g.textAlign='left';
          g.fillText('M_max = '+Mmax.toFixed(1)+' N·m',xMm+14,yMm-4);
          g.font='600 10px Inter,sans-serif';g.fillStyle='rgba(252,165,165,0.5)';
          g.fillText('s_k = '+sk.toFixed(3)+' | n = '+nMmax.toFixed(0)+' rpm',xMm+14,yMm+12);

          /* Horizontal dashed from M_max to Y axis */
          g.beginPath();g.moveTo(ML,yMm);g.lineTo(xMm,yMm);
          g.strokeStyle='rgba(239,68,68,0.25)';g.lineWidth=1;g.setLineDash([4,4]);g.stroke();g.setLineDash([]);

          /* === Startup point (s=1, n=0) === */
          var xArr=xPx(0),yArr=yPx(Marr);
          g.beginPath();g.arc(xArr,yArr,9,0,2*PI);g.fillStyle='rgba(249,168,38,0.15)';g.fill();
          g.beginPath();g.arc(xArr,yArr,5,0,2*PI);g.fillStyle='#f59e0b';g.fill();
          g.strokeStyle='rgba(255,255,255,0.5)';g.lineWidth=2;g.stroke();
          g.font='bold 12px Inter,sans-serif';g.fillStyle='#fbbf24';g.textAlign='left';
          g.fillText('M_arr = '+Marr.toFixed(1)+' N·m',xArr+14,yArr-2);
          g.font='600 10px Inter,sans-serif';g.fillStyle='rgba(251,191,36,0.5)';
          g.fillText('Arranque (s=1)',xArr+14,yArr+14);

          /* Horizontal dashed from M_arr to Y axis */
          g.beginPath();g.moveTo(ML,yArr);g.lineTo(xArr+5,yArr);
          g.strokeStyle='rgba(249,168,38,0.25)';g.lineWidth=1;g.setLineDash([4,4]);g.stroke();g.setLineDash([]);

          /* === Formula badge === */
          var bx=ML+cW*0.55, by=MT+8;
          g.fillStyle='rgba(0,0,0,0.55)';
          g.beginPath();var bw=220,bh=42,br=8;
          g.moveTo(bx+br,by);g.arcTo(bx+bw,by,bx+bw,by+bh,br);
          g.arcTo(bx+bw,by+bh,bx,by+bh,br);g.arcTo(bx,by+bh,bx,by,br);
          g.arcTo(bx,by,bx+bw,by,br);g.closePath();g.fill();
          g.strokeStyle='rgba(0,173,181,0.3)';g.lineWidth=1;g.stroke();
          g.font='600 10px Inter,sans-serif';g.fillStyle='rgba(0,173,181,0.6)';g.textAlign='left';
          g.fillText('M = 3·U²f·(R₂/s) / [ωs·((R₁+R₂/s)²+X²t)]',bx+10,by+16);
          g.font='700 13px Inter,sans-serif';g.fillStyle='#00ADB5';
          g.fillText('Motor '+pp*2+' polos | '+ns.toFixed(0)+' rpm síncronos',bx+10,by+34);
        }

        [sl_ul,sl_r2,sl_xt,sl_r1,sl_pp].forEach(function(el){el.addEventListener('input',draw);});
        draw();
        })();
        </script>
        """

        components.html(TORQUE_SPEED_HTML, height=620, scrolling=False)

        # --- ANÁLISIS FÍSICO DE LOS EFECTOS ---
        with st.expander("Análisis Físico: Efecto de cada Parámetro sobre la Curva", expanded=False):
            st.markdown(r"""
            La forma de la curva Par-Velocidad es el resultado directo de los parámetros eléctricos del motor. Aquí se detalla el efecto de cada uno:

            | Parámetro | Efecto sobre el Par Máximo $M_{max}$ | Efecto sobre el Deslizamiento Crítico $s_k$ | Efecto sobre el Par de Arranque $M_{arr}$ |
            |---|---|---|---|
            | **↑ Tensión** $U_1$ | Aumenta $\propto U_1^2$. Gran sensibilidad. | **No cambia** (no depende de $U_1$). | Aumenta $\propto U_1^2$. |
            | **↑ Resistencia Rotórica** $R'_2$ | **No cambia** (el máximo es siempre el mismo). | Aumenta proporcionalmente ($s_k \propto R'_2$). La curva se "desplaza" hacia la derecha. | Aumenta (en motores de rotor bobinado, esta es la técnica de arranque). |
            | **↑ Reactancias** $X_1, X'_2$ | Disminuye (las reactancias limitan la corriente inducida). | Disminuye (el pico se desplaza hacia $s=0$, hacia la derecha en velocidad). | Disminuye. |
            | **↑ Resistencia Estatórica** $R_1$ | Disminuye ligeramente. | Disminuye ligeramente. | Disminuye. |
            | **↑ Pares de polos** $p$ | No cambia (en valor p.u.). | No cambia (en p.u.). | La $n_s$ se reduce a la mitad por cada par de polos adicional, escalando toda la curva horizontalmente. |

            > **Regla de Oro:** El par electromagnético es **proporcional al cuadrado de la tensión** ($M \propto U_1^2$). Una caída de tensión del 10% en la red reduce el par disponible un **19%**, pudiendo calar el motor si trabaja cerca de su límite de carga.
            """)


    # --------------------------------------------------------------------------
    # PESTAÑA 2.4: ENSAYOS
    # --------------------------------------------------------------------------
    with tab_ensayos:
        st.markdown("### Determinación de Parámetros del Circuito Equivalente")
        st.write(r"""
        Los parámetros del circuito equivalente ($R_1$, $X_1$, $R_{Fe}$, $X_m$, $R'_2$, $X'_2$) no pueden conocerse por inspección visual del motor.
        Para determinarlos experimentalmente, se realizan dos ensayos normalizados: el **ensayo de vacío** y el **ensayo de cortocircuito** (rotor frenado), análogos a los del transformador.
        """)

        tab_vacio, tab_cc = st.tabs(["Ensayo de Vacío (Sin carga)", "Ensayo de Cortocircuito (Rotor Frenado)"])

        # ======================================================================
        # ENSAYO DE VACÍO
        # ======================================================================
        with tab_vacio:
            st.markdown("#### Ensayo de Vacío")
            st.write(r"""
            El motor funciona **sin ninguna carga mecánica en el eje** ($M = 0$), a tensión nominal y frecuencia nominal.
            El rotor gira casi a velocidad de sincronismo, por lo que el deslizamiento es prácticamente nulo ($s \approx 0$).
            """)

            col_v1, col_v2 = st.columns([1.1, 1])

            with col_v1:
                st.markdown("##### Circuito Equivalente en Vacío")
                st.markdown(r"""
                <div style="background:#0E1117; border:1px solid #2a2a3a; border-radius:10px; padding:18px 10px 14px 10px; margin-bottom:12px;">
                <svg viewBox="0 0 680 220" xmlns="http://www.w3.org/2000/svg" style="width:100%;font-family:'monospace',sans-serif;">

                  <!-- Rails de guía -->
                  <line x1="30" y1="50" x2="650" y2="50" stroke="#2D3748" stroke-width="1.5" stroke-dasharray="4,3"/>
                  <line x1="30" y1="185" x2="650" y2="185" stroke="#2D3748" stroke-width="1.5" stroke-dasharray="4,3"/>

                  <!-- Fuente -->
                  <circle cx="30" cy="117" r="22" fill="none" stroke="#00ADB5" stroke-width="2.5"/>
                  <text x="30" y="121" text-anchor="middle" fill="#00ADB5" font-size="12" font-weight="bold">U₁</text>
                  <line x1="30" y1="50" x2="30" y2="95" stroke="#00ADB5" stroke-width="2.5"/>
                  <line x1="30" y1="139" x2="30" y2="185" stroke="#00ADB5" stroke-width="2.5"/>

                  <!-- Resistencia R1 -->
                  <line x1="52" y1="50" x2="95" y2="50" stroke="#9CA3AF" stroke-width="2"/>
                  <rect x="95" y="39" width="55" height="22" rx="3" fill="none" stroke="#F9A826" stroke-width="2"/>
                  <text x="122" y="31" text-anchor="middle" fill="#F9A826" font-size="12">R₁</text>
                  <line x1="150" y1="50" x2="200" y2="50" stroke="#9CA3AF" stroke-width="2"/>

                  <!-- Reactancia jX1 -->
                  <rect x="200" y="39" width="55" height="22" rx="3" fill="none" stroke="#818CF8" stroke-width="2"/>
                  <text x="227" y="31" text-anchor="middle" fill="#818CF8" font-size="12">jX₁</text>
                  <line x1="255" y1="50" x2="310" y2="50" stroke="#9CA3AF" stroke-width="2"/>

                  <!-- Nudo de la rama shunt -->
                  <circle cx="310" cy="50" r="4" fill="#9CA3AF"/>
                  <line x1="310" y1="50" x2="310" y2="88" stroke="#9CA3AF" stroke-width="2"/>

                  <!-- RFe -->
                  <rect x="288" y="88" width="45" height="20" rx="3" fill="none" stroke="#EF4444" stroke-width="2"/>
                  <text x="290" y="82" fill="#EF4444" font-size="11">Rfe</text>
                  <line x1="310" y1="108" x2="310" y2="128" stroke="#9CA3AF" stroke-width="1.5"/>

                  <!-- jXm -->
                  <rect x="288" y="128" width="45" height="20" rx="3" fill="none" stroke="#A78BFA" stroke-width="2"/>
                  <text x="290" y="122" fill="#A78BFA" font-size="11">jXm</text>
                  <line x1="310" y1="148" x2="310" y2="185" stroke="#9CA3AF" stroke-width="1.5"/>

                  <!-- Rama derecha: ABIERTA (s≈0 → R'2/s ≈ ∞) -->
                  <line x1="310" y1="50" x2="420" y2="50" stroke="#9CA3AF" stroke-width="2"/>
                  <rect x="420" y="39" width="55" height="22" rx="3" fill="none" stroke="#818CF8" stroke-width="2"/>
                  <text x="447" y="31" text-anchor="middle" fill="#818CF8" font-size="12">jX'₂</text>
                  <line x1="475" y1="50" x2="520" y2="50" stroke="#9CA3AF" stroke-width="2"/>
                  <!-- R'2/s ≈ ∞: circuito abierto -->
                  <line x1="520" y1="38" x2="520" y2="62" stroke="#4B5563" stroke-width="2.5"/>
                  <text x="535" y="45" fill="#4B5563" font-size="18">∞</text>
                  <text x="530" y="60" fill="#4B5563" font-size="9">R'₂/s→∞</text>
                  <!-- circuito abierto visual -->
                  <line x1="520" y1="50" x2="560" y2="50" stroke="#4B5563" stroke-width="1.5" stroke-dasharray="3,3"/>
                  <circle cx="565" cy="50" r="3" fill="none" stroke="#4B5563" stroke-width="1.5"/>

                  <!-- Etiquetas de corriente -->
                  <text x="68" y="43" fill="#9CA3AF" font-size="10">→ I₀≈I₁</text>
                  <text x="318" y="87" fill="#9CA3AF" font-size="10">↓ I₀</text>
                  <text x="330" y="103" fill="#EF4444" font-size="10">← IFe</text>
                  <text x="330" y="143" fill="#A78BFA" font-size="10">← Im</text>

                  <!-- Nota s≈0 -->
                  <rect x="580" y="90" width="85" height="35" rx="5" fill="#1a2030" stroke="#333" stroke-width="1"/>
                  <text x="622" y="107" text-anchor="middle" fill="#6EE7B7" font-size="10" font-weight="bold">s ≈ 0</text>
                  <text x="622" y="119" text-anchor="middle" fill="#6EE7B7" font-size="9">n ≈ nₛ</text>

                  <!-- Leyenda -->
                  <text x="340" y="210" text-anchor="middle" fill="#F9A826" font-size="10" font-weight="bold">ESTATOR</text>
                  <text x="480" y="210" text-anchor="middle" fill="#4B5563" font-size="10">ROTOR (abierto)</text>
                  <line x1="80" y1="205" x2="290" y2="205" stroke="#F9A826" stroke-width="1" stroke-dasharray="2,2"/>
                </svg>
                </div>
                """, unsafe_allow_html=True)

                st.markdown("##### Condición del Ensayo")
                st.write(r"Como $s \approx 0$, la impedancia $R'_2/s \rightarrow \infty$. La rama del rotor queda **en circuito abierto**: toda la corriente de línea es la corriente de magnetización $I_0$.")

            with col_v2:
                st.markdown("##### Medidas que se Toman")
                st.markdown(r"""
                Se miden con vatímetros, voltímetros y amperímetros en los terminales del estator:
                * **$U_0$** → Tensión de línea nominal (se aplica a su valor nominal).
                * **$I_0$** → Corriente de línea en vacío (pequeña, ~10-40% de $I_n$).
                * **$P_0$** → Potencia activa total absorbida en vacío.
                """)

                st.markdown("##### Extracción de Parámetros")
                st.info(r"Toda la potencia activa $P_0$ en vacío se consume en los **núcleos ferromagnéticos** (pérdidas en el hierro). Las pérdidas en el cobre del estator son despreciables porque $I_0$ es pequeña.")

                st.markdown("**1. Factor de potencia en vacío:**")
                st.latex(r"\cos\varphi_0 = \frac{P_0}{\sqrt{3} \cdot U_0 \cdot I_0}")

                st.markdown("**2. Resistencia de pérdidas en el hierro ($R_{Fe}$):**")
                st.latex(r"R_{Fe} = \frac{U_{fase}^2}{P_0 / 3} = \frac{3 \cdot U_{fase}^2}{P_0}")

                st.markdown("**3. Reactancia de magnetización ($X_m$):**")
                st.write(r"La corriente reactiva (magnetizante) es $I_m = I_0 \cdot \sin\varphi_0$:")
                st.latex(r"X_m = \frac{U_{fase}}{I_m} = \frac{U_{fase}}{I_0 \cdot \sin\varphi_0}")

        # ======================================================================
        # ENSAYO DE CORTOCIRCUITO (ROTOR FRENADO)
        # ======================================================================
        with tab_cc:
            st.markdown("#### Ensayo de Cortocircuito (Rotor Frenado)")
            st.write(r"""
            El rotor se **bloquea mecánicamente** para que no pueda girar ($n = 0$, por lo tanto $s = 1$).
            Se aplica una tensión reducida $U_{cc}$ (típicamente el 10-25% de la nominal) hasta que la corriente nominal $I_n$ circula por el motor.
            """)

            col_c1, col_c2 = st.columns([1.1, 1])

            with col_c1:
                st.markdown("##### Circuito Equivalente en Cortocircuito")
                st.markdown(r"""
                <div style="background:#0E1117; border:1px solid #2a2a3a; border-radius:10px; padding:18px 10px 14px 10px; margin-bottom:12px;">
                <svg viewBox="0 0 680 220" xmlns="http://www.w3.org/2000/svg" style="width:100%;font-family:'monospace',sans-serif;">

                  <!-- Rails -->
                  <line x1="30" y1="50" x2="650" y2="50" stroke="#2D3748" stroke-width="1.5" stroke-dasharray="4,3"/>
                  <line x1="30" y1="185" x2="650" y2="185" stroke="#2D3748" stroke-width="1.5" stroke-dasharray="4,3"/>

                  <!-- Fuente Ucc (reducida) -->
                  <circle cx="30" cy="117" r="22" fill="none" stroke="#F9A826" stroke-width="2.5"/>
                  <text x="30" y="114" text-anchor="middle" fill="#F9A826" font-size="10" font-weight="bold">Ucc</text>
                  <text x="30" y="126" text-anchor="middle" fill="#F9A826" font-size="8">reducida</text>
                  <line x1="30" y1="50" x2="30" y2="95" stroke="#F9A826" stroke-width="2.5"/>
                  <line x1="30" y1="139" x2="30" y2="185" stroke="#F9A826" stroke-width="2.5"/>

                  <!-- R1 -->
                  <line x1="52" y1="50" x2="95" y2="50" stroke="#9CA3AF" stroke-width="2"/>
                  <rect x="95" y="39" width="50" height="22" rx="3" fill="none" stroke="#F9A826" stroke-width="2"/>
                  <text x="120" y="31" text-anchor="middle" fill="#F9A826" font-size="12">R₁</text>
                  <line x1="145" y1="50" x2="195" y2="50" stroke="#9CA3AF" stroke-width="2"/>

                  <!-- jX1 -->
                  <rect x="195" y="39" width="50" height="22" rx="3" fill="none" stroke="#818CF8" stroke-width="2"/>
                  <text x="220" y="31" text-anchor="middle" fill="#818CF8" font-size="12">jX₁</text>
                  <line x1="245" y1="50" x2="285" y2="50" stroke="#9CA3AF" stroke-width="2"/>

                  <!-- Rama shunt CORTOCIRCUITADA (Xm ≈ ∞ → I0 ≈ 0) -->
                  <circle cx="285" cy="50" r="4" fill="#9CA3AF"/>
                  <line x1="285" y1="50" x2="285" y2="90" stroke="#4B5563" stroke-width="1.5" stroke-dasharray="3,3"/>
                  <rect x="263" y="90" width="45" height="20" rx="3" fill="#111" stroke="#4B5563" stroke-width="1.5"/>
                  <text x="285" y="104" text-anchor="middle" fill="#4B5563" font-size="9">Rfe ∥ jXm</text>
                  <text x="285" y="78" text-anchor="middle" fill="#4B5563" font-size="9">≈ abierto</text>
                  <line x1="285" y1="110" x2="285" y2="185" stroke="#4B5563" stroke-width="1.5" stroke-dasharray="3,3"/>

                  <!-- Tramo central hacia rotor -->
                  <line x1="285" y1="50" x2="345" y2="50" stroke="#9CA3AF" stroke-width="2"/>

                  <!-- jX'2 -->
                  <rect x="345" y="39" width="55" height="22" rx="3" fill="none" stroke="#818CF8" stroke-width="2"/>
                  <text x="372" y="31" text-anchor="middle" fill="#818CF8" font-size="12">jX'₂</text>
                  <line x1="400" y1="50" x2="455" y2="50" stroke="#9CA3AF" stroke-width="2"/>

                  <!-- R'2 (s=1 → R'2/s = R'2) -->
                  <rect x="455" y="39" width="65" height="22" rx="3" fill="none" stroke="#34D399" stroke-width="2"/>
                  <text x="487" y="31" text-anchor="middle" fill="#34D399" font-size="11">R'₂ (s=1)</text>
                  <line x1="520" y1="50" x2="565" y2="50" stroke="#9CA3AF" stroke-width="2"/>

                  <!-- Terminal derecho cortocircuitado abajo -->
                  <circle cx="565" cy="50" r="4" fill="#34D399"/>
                  <line x1="565" y1="50" x2="565" y2="185" stroke="#34D399" stroke-width="2"/>
                  <circle cx="565" cy="185" r="4" fill="#34D399"/>

                  <!-- Etiqueta de corriente -->
                  <text x="62" y="43" fill="#9CA3AF" font-size="10">→ Icc ≈ I'₂</text>

                  <!-- Nota s=1 -->
                  <rect x="590" y="100" width="75" height="35" rx="5" fill="#1a2030" stroke="#333" stroke-width="1"/>
                  <text x="627" y="117" text-anchor="middle" fill="#FF4B4B" font-size="10" font-weight="bold">s = 1</text>
                  <text x="627" y="129" text-anchor="middle" fill="#FF4B4B" font-size="9">n = 0</text>

                  <!-- Leyendas -->
                  <text x="165" y="210" text-anchor="middle" fill="#F9A826" font-size="10" font-weight="bold">ESTATOR</text>
                  <text x="285" y="210" text-anchor="middle" fill="#4B5563" font-size="10">SHUNT (ignorado)</text>
                  <text x="470" y="210" text-anchor="middle" fill="#34D399" font-size="10" font-weight="bold">ROTOR (frenado)</text>
                  <line x1="80" y1="205" x2="248" y2="205" stroke="#F9A826" stroke-width="1" stroke-dasharray="2,2"/>
                  <line x1="350" y1="205" x2="580" y2="205" stroke="#34D399" stroke-width="1" stroke-dasharray="2,2"/>
                </svg>
                </div>
                """, unsafe_allow_html=True)

                st.markdown("##### Condición del Ensayo")
                st.write(r"Con $s=1$ la rama shunt queda con una impedancia muy alta frente a la rama serie, por lo que $I_0 \approx 0$ y se desprecia. El circuito se reduce a la **impedancia de cortocircuito** en serie.")

            with col_c2:
                st.markdown("##### Medidas que se Toman")
                st.markdown(r"""
                Se miden al valor de tensión reducida $U_{cc}$ que produce $I_{cc} \approx I_n$:
                * **$U_{cc}$** → Tensión de línea reducida aplicada.
                * **$I_{cc}$** → Corriente de línea (= $I_n$ a efectos de cálculo).
                * **$P_{cc}$** → Potencia activa total absorbida en cc.
                """)

                st.markdown("##### Extracción de Parámetros")
                st.info(r"Toda la potencia $P_{cc}$ se consume en las **resistencias de los devanados** (pérdidas en el cobre del estator y rotor). La rama shunt se ignora.")

                st.markdown("**1. Impedancia de cortocircuito por fase:**")
                st.latex(r"Z_{cc} = \frac{U_{cc}/\sqrt{3}}{I_{cc}}")

                st.markdown("**2. Resistencia total de cortocircuito ($R_{cc}$):**")
                st.latex(r"R_{cc} = \frac{P_{cc}}{3 \cdot I_{cc}^2} = R_1 + R'_2")

                st.markdown("**3. Reactancia total de cortocircuito ($X_{cc}$):**")
                st.latex(r"X_{cc} = \sqrt{Z_{cc}^2 - R_{cc}^2} = X_1 + X'_2")

                st.markdown("**4. Reparto estator/rotor** (estimación clásica Fraile Mora):")
                st.write("Si no se dispone de ensayo separado para $R_1$, se asume reparto igualitario:")
                st.latex(r"R_1 \approx R'_2 \approx \frac{R_{cc}}{2} \qquad X_1 \approx X'_2 \approx \frac{X_{cc}}{2}")

            st.markdown("---")
            st.markdown("##### Calculadora de Parámetros a partir de los Ensayos")

            col_calc1, col_calc2, col_calc_out = st.columns([1, 1, 1.2])
            with col_calc1:
                st.markdown("**Datos del Ensayo de Vacío**")
                u0_c = st.number_input("$U_0$ Tensión de línea (V)", value=400.0, step=10.0, key="u0_ens")
                i0_c = st.number_input("$I_0$ Corriente vacío (A)", value=5.0, step=0.5, key="i0_ens")
                p0_c = st.number_input("$P_0$ Potencia vacío (W)", value=600.0, step=50.0, key="p0_ens")
            with col_calc2:
                st.markdown("**Datos del Ensayo de CC**")
                ucc_c = st.number_input("$U_{cc}$ Tensión cc (V)", value=50.0, step=5.0, key="ucc_ens")
                icc_c = st.number_input("$I_{cc}$ Corriente cc (A)", value=20.0, step=1.0, key="icc_ens")
                pcc_c = st.number_input("$P_{cc}$ Potencia cc (W)", value=800.0, step=50.0, key="pcc_ens")
            with col_calc_out:
                st.markdown("**Parámetros Obtenidos**")
                if i0_c > 0 and icc_c > 0:
                    u_fase0 = u0_c / math.sqrt(3)
                    cos_phi0 = min(p0_c / (math.sqrt(3) * u0_c * i0_c), 1.0)
                    sin_phi0 = math.sqrt(max(1 - cos_phi0**2, 0))
                    Rfe_calc  = (3 * u_fase0**2) / p0_c if p0_c > 0 else float('inf')
                    Im_calc   = i0_c * sin_phi0
                    Xm_calc   = u_fase0 / Im_calc if Im_calc > 0 else float('inf')

                    Zcc_calc  = (ucc_c / math.sqrt(3)) / icc_c
                    Rcc_calc  = pcc_c / (3 * icc_c**2)
                    Xcc_calc  = math.sqrt(max(Zcc_calc**2 - Rcc_calc**2, 0))

                    r1_calc   = Rcc_calc / 2
                    r2p_calc  = Rcc_calc / 2
                    x1_calc   = Xcc_calc / 2
                    x2p_calc  = Xcc_calc / 2

                    e1, e2 = st.columns(2)
                    e1.metric("$R_{Fe}$ (Ω)", f"{Rfe_calc:.2f}")
                    e2.metric("$X_m$ (Ω)", f"{Xm_calc:.2f}")
                    e1.metric("$R_1 \\approx R'_2$ (Ω)", f"{r1_calc:.4f}")
                    e2.metric("$X_1 \\approx X'_2$ (Ω)", f"{x1_calc:.4f}")
                    e1.metric("$Z_{cc}$ (Ω)", f"{Zcc_calc:.4f}")
                    e2.metric("$\\cos\\varphi_0$", f"{cos_phi0:.4f}")



    # --------------------------------------------------------------------------
    # PESTAÑA 2.5: ARRANQUE ESTRELLA-TRIÁNGULO
    # --------------------------------------------------------------------------
    with tab_arranque:
        st.markdown("### Arranque Estrella-Triángulo (Y-Δ)")
        st.write(r"""
        El arranque directo de un motor asíncrono somete a la red eléctrica a una **corriente de inserción** de 5 a 10 veces la corriente nominal.
        El método **Estrella-Triángulo** es la técnica más extendida para reducir este impacto, sin necesidad de equipos electrónicos.
        """)

        col_why, col_how = st.columns(2)
        with col_why:
            st.markdown("#### El Problema del Arranque Directo")
            st.write(r"""
            Al conectar el motor directamente a la red trifásica en configuración Triángulo (que es la conexión de régimen), se aplica la **tensión de línea completa ($U_L$)** a cada devanado de fase. Esto produce:
            """)
            st.latex(r"I_{arr,\Delta} = \frac{U_L}{Z_{cc}} \approx 5 \text{ a } 10 \cdot I_n")
            st.error(r"Esta corriente masiva provoca caídas de tensión en la red, perturbaciones en otros consumidores, estrés mecánico en el acoplamiento y calentamiento severo en los devanados.")

        with col_how:
            st.markdown("#### La Solución: Conexión Inicial en Estrella")
            st.write(r"""
            Al arrancar con los devanados en Estrella, cada bobina recibe únicamente la **tensión de fase** ($U_{fase} = U_L / \sqrt{3}$), que es $\sqrt{3}$ veces menor que en Triángulo.
            Al reducir la tensión por $\sqrt{3}$, la corriente por fase baja también por $\sqrt{3}$, pero la corriente de línea baja por **3 veces** (pues en estrella $I_L = I_{fase}$).
            """)
            st.latex(r"I_{arr,Y} = \frac{U_L / \sqrt{3}}{Z_{cc}} = \frac{1}{3} \cdot I_{arr,\Delta}")
            st.success(r"La corriente de arranque en la red se reduce a **1/3** del valor que tendría en conexión directa en Triángulo. El par de arranque también se reduce a 1/3.")

        st.markdown("---")
        st.markdown("#### Diagramas de Conexión: Estrella vs. Triángulo")

        col_svgY, col_svgD = st.columns(2)

        with col_svgY:
            st.markdown("**Fase 1: Arranque en Estrella (Y)** — Tensión reducida")
            st.markdown(r"""
            <div style="background:#0E1117; border:1px solid #2a2a3a; border-radius:10px; padding:16px 8px 10px 8px;">
            <svg viewBox="0 0 340 240" xmlns="http://www.w3.org/2000/svg" style="width:100%;font-family:'monospace',sans-serif;">
              <!-- Punto neutro central -->
              <circle cx="170" cy="150" r="6" fill="#6EE7B7" stroke="#34D399" stroke-width="1.5"/>
              <text x="182" y="154" fill="#34D399" font-size="10">Neutro (N)</text>

              <!-- Devanado U1-U2 (fase R) -->
              <line x1="170" y1="150" x2="80" y2="60" stroke="#EF4444" stroke-width="2.5"/>
              <rect x="100" y="85" width="40" height="15" rx="3" fill="none" stroke="#EF4444" stroke-width="2" transform="rotate(-45, 120, 92)"/>
              <text x="50" y="50" fill="#EF4444" font-size="12" font-weight="bold">R</text>
              <circle cx="80" cy="60" r="5" fill="#EF4444"/>
              <text x="88" y="58" fill="#EF4444" font-size="9">U₁</text>

              <!-- Devanado V1-V2 (fase S) -->
              <line x1="170" y1="150" x2="260" y2="60" stroke="#F9A826" stroke-width="2.5"/>
              <rect x="210" y="85" width="40" height="15" rx="3" fill="none" stroke="#F9A826" stroke-width="2" transform="rotate(45, 230, 92)"/>
              <text x="268" y="50" fill="#F9A826" font-size="12" font-weight="bold">S</text>
              <circle cx="260" cy="60" r="5" fill="#F9A826"/>
              <text x="243" y="58" fill="#F9A826" font-size="9">V₁</text>

              <!-- Devanado W1-W2 (fase T) -->
              <line x1="170" y1="150" x2="170" y2="220" stroke="#818CF8" stroke-width="2.5"/>
              <rect x="152" y="170" width="36" height="15" rx="3" fill="none" stroke="#818CF8" stroke-width="2"/>
              <text x="145" y="232" fill="#818CF8" font-size="12" font-weight="bold">T</text>
              <circle cx="170" cy="220" r="5" fill="#818CF8"/>
              <text x="178" y="222" fill="#818CF8" font-size="9">W₁</text>

              <!-- Etiqueta Ufase -->
              <text x="95" y="120" fill="#9CA3AF" font-size="10" transform="rotate(-45, 95, 120)">U_fase = UL/√3</text>
              
              <!-- Badge -->
              <rect x="5" y="5" width="115" height="28" rx="5" fill="#0d2a20" stroke="#34D399" stroke-width="1.5"/>
              <text x="62" y="16" text-anchor="middle" fill="#34D399" font-size="9" font-weight="bold">ARRANQUE</text>
              <text x="62" y="27" text-anchor="middle" fill="#34D399" font-size="9">I_línea = I_Δ/3</text>
            </svg>
            </div>
            """, unsafe_allow_html=True)

        with col_svgD:
            st.markdown("**Fase 2: Régimen en Triángulo (Δ)** — Tensión nominal")
            st.markdown(r"""
            <div style="background:#0E1117; border:1px solid #2a2a3a; border-radius:10px; padding:16px 8px 10px 8px;">
            <svg viewBox="0 0 340 260" xmlns="http://www.w3.org/2000/svg" style="width:100%;font-family:'monospace',sans-serif;">

              <!-- Vértices del triángulo: R(top-left), S(top-right), T(bottom-center) -->
              <!-- R = (80, 70), S = (260, 70), T = (170, 215) -->

              <!-- Vértice R -->
              <circle cx="80" cy="70" r="6" fill="#EF4444"/>
              <text x="60" y="67" fill="#EF4444" font-size="13" font-weight="bold">R</text>

              <!-- Vértice S -->
              <circle cx="260" cy="70" r="6" fill="#F9A826"/>
              <text x="270" y="67" fill="#F9A826" font-size="13" font-weight="bold">S</text>

              <!-- Vértice T -->
              <circle cx="170" cy="215" r="6" fill="#818CF8"/>
              <text x="160" y="238" fill="#818CF8" font-size="13" font-weight="bold">T</text>

              <!-- Lado superior RS: líneas + caja de devanado encima -->
              <line x1="86" y1="70" x2="130" y2="70" stroke="#9CA3AF" stroke-width="2"/>
              <rect x="130" y="58" width="80" height="24" rx="4" fill="#111827" stroke="#EF4444" stroke-width="2"/>
              <text x="170" y="74" text-anchor="middle" fill="#EF4444" font-size="11" font-weight="bold">U₁ — U₂</text>
              <line x1="210" y1="70" x2="254" y2="70" stroke="#9CA3AF" stroke-width="2"/>
              <!-- Etiqueta lateral del devanado RS -->
              <text x="170" y="50" text-anchor="middle" fill="#EF4444" font-size="9">Devanado R-S</text>

              <!-- Lado derecho ST: línea simple + etiqueta fuera (a la derecha) -->
              <line x1="257" y1="76" x2="173" y2="209" stroke="#9CA3AF" stroke-width="2"/>
              <!-- Caja del devanado ST a la derecha del lado -->
              <rect x="262" y="125" width="70" height="24" rx="4" fill="#111827" stroke="#F9A826" stroke-width="2"/>
              <text x="297" y="141" text-anchor="middle" fill="#F9A826" font-size="11" font-weight="bold">V₁—V₂</text>
              <text x="297" y="118" text-anchor="middle" fill="#F9A826" font-size="9">Devanado S-T</text>

              <!-- Lado izquierdo TR: línea simple + etiqueta fuera (a la izquierda) -->
              <line x1="167" y1="209" x2="83" y2="76" stroke="#9CA3AF" stroke-width="2"/>
              <!-- Caja del devanado TR a la izquierda del lado -->
              <rect x="8" y="125" width="70" height="24" rx="4" fill="#111827" stroke="#818CF8" stroke-width="2"/>
              <text x="43" y="141" text-anchor="middle" fill="#818CF8" font-size="11" font-weight="bold">W₁—W₂</text>
              <text x="43" y="118" text-anchor="middle" fill="#818CF8" font-size="9">Devanado T-R</text>

              <!-- Badge -->
              <rect x="5" y="5" width="140" height="30" rx="5" fill="#1a1205" stroke="#F9A826" stroke-width="1.5"/>
              <text x="75" y="17" text-anchor="middle" fill="#F9A826" font-size="9" font-weight="bold">RÉGIMEN NOMINAL</text>
              <text x="75" y="29" text-anchor="middle" fill="#F9A826" font-size="9">U_devanado = U_línea</text>
            </svg>
            </div>
            """, unsafe_allow_html=True)

        st.markdown("---")
        st.markdown("#### Relaciones Cuantitativas Fundamentales")

        col_eq1, col_eq2 = st.columns(2)
        with col_eq1:
            st.markdown("**Corriente de Arranque**")
            st.write(r"En arranque directo (Δ), la corriente de línea sería:")
            st.latex(r"I_{arr,\Delta} = \frac{U_L}{Z_{cc} / \sqrt{3}} \cdot \sqrt{3} = \frac{3 \cdot U_{fase}}{Z_{cc}}")
            st.write(r"Con conexión previa en Estrella:")
            st.latex(r"I_{arr,Y} = \frac{U_L / \sqrt{3}}{Z_{cc}} = \frac{1}{3} \cdot I_{arr,\Delta}")
            st.info(r"La corriente absorbida de la **red** se reduce a $\mathbf{1/3}$.")

        with col_eq2:
            st.markdown("**Par de Arranque**")
            st.write(r"El par es proporcional al cuadrado de la tensión aplicada al devanado:")
            st.latex(r"M_{arr,Y} = \left(\frac{U_Y}{U_\Delta}\right)^2 \cdot M_{arr,\Delta} = \frac{1}{3} \cdot M_{arr,\Delta}")
            st.warning(r"El par de arranque también se reduce a $\mathbf{1/3}$ del par de arranque directo. Esto limita el método a **cargas de arranque en vacío** o con par resistente nulo/bajo.")

        st.markdown("---")
        st.markdown("#### Tabla Comparativa: Arranque Directo vs. Estrella-Triángulo")
        st.markdown(r"""
        | Magnitud | Arranque Directo (Δ) | Arranque Y-Δ (fase Estrella) | Factor |
        |---|---|---|---|
        | Tensión en devanado | $U_L$ | $U_L / \sqrt{3}$ | ×0.577 |
        | Corriente de fase | $I_{fase,\Delta}$ | $I_{fase,\Delta}/\sqrt{3}$ | ×0.577 |
        | **Corriente de línea** | $I_{arr,\Delta}$ | $\mathbf{I_{arr,\Delta}/3}$ | **×1/3** |
        | **Par de arranque** | $M_{arr,\Delta}$ | $\mathbf{M_{arr,\Delta}/3}$ | **×1/3** |
        | Complejidad del cuadro | Simple | Contactor Y + Contactor Δ + Temporizado | Media |
        | Coste | Bajo | Medio | — |
        """)


    # --------------------------------------------------------------------------
    # PESTAÑA 2.6: BALANCE DE POTENCIAS
    # --------------------------------------------------------------------------
    with tab_balance:
        st.markdown("### Balance de Potencias en el Motor de Inducción")
        st.write(r"""
        El motor asíncrono no es una máquina perfecta: en cada etapa de la conversión de energía se producen pérdidas inevitables.
        El **Balance de Potencias** cuantifica exactamente dónde se pierde cada vatio desde que entra por los bornes hasta que sale por el eje.
        Este análisis es fundamental para calcular el **rendimiento ($\eta$)** real de la máquina.
        """)

        # ==========================================
        # DIAGRAMA SVG DE FLUJO DE POTENCIA
        # ==========================================
        st.markdown("#### Diagrama de Flujo de Potencia")
        st.markdown(r"""
        <div style="background:linear-gradient(135deg,#0a0f1e,#0d1117); border:1px solid #1e2a3a; border-radius:14px; padding:28px 20px 22px 20px; margin-bottom:16px;">
        <svg viewBox="0 0 900 220" xmlns="http://www.w3.org/2000/svg" style="width:100%;font-family:'Inter',sans-serif;">

          <!-- ================================================================ -->
          <!-- ETAPA 0: RED ELÉCTRICA — Rectángulo redondeado de entrada        -->
          <!-- ================================================================ -->
          <rect x="8" y="72" width="100" height="56" rx="10" fill="#0a1f2e" stroke="#00ADB5" stroke-width="2.5"/>
          <text x="58" y="97" text-anchor="middle" fill="#00ADB5" font-size="12" font-weight="bold">RED</text>
          <text x="58" y="111" text-anchor="middle" fill="#00ADB5" font-size="11" font-weight="bold">P₁</text>
          <text x="58" y="145" text-anchor="middle" fill="#4B7A8A" font-size="9">Potencia absorbida</text>
          <text x="58" y="156" text-anchor="middle" fill="#4B7A8A" font-size="9">de la red</text>

          <!-- Conector 0→1 -->
          <line x1="108" y1="100" x2="138" y2="100" stroke="#00ADB5" stroke-width="2.5"/>
          <polygon points="136,95 146,100 136,105" fill="#00ADB5"/>

          <!-- ================================================================ -->
          <!-- ETAPA 1: ESTATOR — Forma chevron (pentágono con punta derecha)   -->
          <!-- ================================================================ -->
          <!-- Chevron: x=145 base, ancho=130, alto=70 -->
          <polygon points="145,65 255,65 275,100 255,135 145,135 165,100" fill="#151a08" stroke="#F9A826" stroke-width="2.5"/>
          <text x="207" y="96" text-anchor="middle" fill="#F9A826" font-size="12" font-weight="bold">ESTATOR</text>
          <text x="207" y="112" text-anchor="middle" fill="#D4891A" font-size="10">Devanados</text>
          <text x="207" y="124" text-anchor="middle" fill="#D4891A" font-size="10">del estátor</text>

          <!-- Pérdidas estator: círculos hacia arriba -->
          <!-- Pérdida Cobre Cu1 -->
          <line x1="190" y1="65" x2="190" y2="30" stroke="#EF4444" stroke-width="1.5" stroke-dasharray="4,3"/>
          <circle cx="190" cy="20" r="17" fill="#1a0808" stroke="#EF4444" stroke-width="2"/>
          <text x="190" y="17" text-anchor="middle" fill="#EF4444" font-size="8" font-weight="bold">P_Cu1</text>
          <text x="190" y="27" text-anchor="middle" fill="#EF4444" font-size="7">Cobre</text>
          <!-- Pérdida Hierro Fe -->
          <line x1="225" y1="65" x2="225" y2="30" stroke="#F97316" stroke-width="1.5" stroke-dasharray="4,3"/>
          <circle cx="225" cy="20" r="17" fill="#1a0c04" stroke="#F97316" stroke-width="2"/>
          <text x="225" y="17" text-anchor="middle" fill="#F97316" font-size="8" font-weight="bold">P_Fe</text>
          <text x="225" y="27" text-anchor="middle" fill="#F97316" font-size="7">Hierro</text>

          <!-- Conector 1→2 -->
          <line x1="275" y1="100" x2="305" y2="100" stroke="#6EE7B7" stroke-width="2.5"/>
          <polygon points="303,95 313,100 303,105" fill="#6EE7B7"/>

          <!-- ================================================================ -->
          <!-- ETAPA 2: ENTREHIERRO — Hexágono                                  -->
          <!-- ================================================================ -->
          <!-- Hexágono centrado en (355, 100) ancho≈90 alto=70 -->
          <polygon points="315,100 335,68 375,68 395,100 375,132 335,132" fill="#081f1f" stroke="#6EE7B7" stroke-width="2.5"/>
          <text x="355" y="96" text-anchor="middle" fill="#6EE7B7" font-size="10" font-weight="bold">P_ag</text>
          <text x="355" y="109" text-anchor="middle" fill="#4AA88A" font-size="9">Entre-</text>
          <text x="355" y="120" text-anchor="middle" fill="#4AA88A" font-size="9">hierro</text>

          <!-- Conector 2→3 -->
          <line x1="395" y1="100" x2="425" y2="100" stroke="#6EE7B7" stroke-width="2.5"/>
          <polygon points="423,95 433,100 423,105" fill="#6EE7B7"/>

          <!-- ================================================================ -->
          <!-- ETAPA 3: ROTOR — Chevron inverso (entrada con muesca izq)        -->
          <!-- ================================================================ -->
          <polygon points="432,65 542,65 562,100 542,135 432,135 452,100" fill="#0a1f0a" stroke="#34D399" stroke-width="2.5"/>
          <text x="494" y="96" text-anchor="middle" fill="#34D399" font-size="12" font-weight="bold">ROTOR</text>
          <text x="494" y="112" text-anchor="middle" fill="#1E8A5E" font-size="10">Jaula de</text>
          <text x="494" y="124" text-anchor="middle" fill="#1E8A5E" font-size="10">ardilla</text>

          <!-- Pérdida rotor: círculo hacia arriba -->
          <line x1="494" y1="65" x2="494" y2="30" stroke="#EF4444" stroke-width="1.5" stroke-dasharray="4,3"/>
          <circle cx="494" cy="20" r="17" fill="#1a0808" stroke="#EF4444" stroke-width="2"/>
          <text x="494" y="17" text-anchor="middle" fill="#EF4444" font-size="8" font-weight="bold">P_Cu2</text>
          <text x="494" y="27" text-anchor="middle" fill="#EF4444" font-size="7">Cobre</text>

          <!-- Conector 3→4 -->
          <line x1="562" y1="100" x2="592" y2="100" stroke="#34D399" stroke-width="2.5"/>
          <polygon points="590,95 600,100 590,105" fill="#34D399"/>

          <!-- ================================================================ -->
          <!-- ETAPA 4: PÉRD. MECÁNICAS — Octágono / polígono 8 lados           -->
          <!-- ================================================================ -->
          <polygon points="615,72 635,60 655,60 675,72 675,128 655,140 635,140 615,128" fill="#110d20" stroke="#818CF8" stroke-width="2.5"/>
          <text x="645" y="94" text-anchor="middle" fill="#818CF8" font-size="9" font-weight="bold">P_mec</text>
          <text x="645" y="106" text-anchor="middle" fill="#6B5FA0" font-size="8">Rozam.</text>
          <text x="645" y="117" text-anchor="middle" fill="#6B5FA0" font-size="8">Ventil.</text>

          <!-- Pérdida mecánica hacia abajo -->
          <line x1="645" y1="140" x2="645" y2="175" stroke="#818CF8" stroke-width="1.5" stroke-dasharray="4,3"/>
          <circle cx="645" cy="188" r="12" fill="#110d20" stroke="#818CF8" stroke-width="1.5"/>
          <text x="645" y="192" text-anchor="middle" fill="#818CF8" font-size="7">Calor</text>

          <!-- Conector 4→5 -->
          <line x1="675" y1="100" x2="705" y2="100" stroke="#A78BFA" stroke-width="2.5"/>
          <polygon points="703,95 713,100 703,105" fill="#A78BFA"/>

          <!-- ================================================================ -->
          <!-- ETAPA 5: POTENCIA ÚTIL EN EJE — Rombo/diamante                  -->
          <!-- ================================================================ -->
          <polygon points="750,65 800,100 750,135 700,100" fill="#130a2a" stroke="#A78BFA" stroke-width="2.5"/>
          <text x="750" y="96" text-anchor="middle" fill="#A78BFA" font-size="10" font-weight="bold">P_u</text>
          <text x="750" y="108" text-anchor="middle" fill="#7C5FBA" font-size="9">Útil</text>
          <text x="750" y="120" text-anchor="middle" fill="#7C5FBA" font-size="9">en eje</text>

          <!-- Flecha salida eje -->
          <line x1="800" y1="100" x2="855" y2="100" stroke="#A78BFA" stroke-width="3"/>
          <polygon points="853,94 868,100 853,106" fill="#A78BFA"/>
          <text x="862" y="92" fill="#A78BFA" font-size="10" font-weight="bold">M</text>
          <text x="862" y="105" fill="#7C5FBA" font-size="8">Carga</text>

          <!-- Etiqueta de flujo principal en la parte de abajo -->
          <text x="58" y="170" text-anchor="middle" fill="#2D4A5A" font-size="8">① Entrada</text>
          <text x="207" y="155" text-anchor="middle" fill="#5A4010" font-size="8">② Pérd. Cu₁ + Fe</text>
          <text x="355" y="150" text-anchor="middle" fill="#1A5A4A" font-size="8">③ Entrehierro</text>
          <text x="494" y="155" text-anchor="middle" fill="#0A4A2A" font-size="8">④ Pérd. Cu₂</text>
          <text x="645" y="155" text-anchor="middle" fill="#2A1A50" font-size="8">⑤ Pérd. mec.</text>
          <text x="750" y="155" text-anchor="middle" fill="#4A2A8A" font-size="8">⑥ Salida</text>

        </svg>
        </div>
        """, unsafe_allow_html=True)

        st.markdown("---")

        col_b1, col_b2 = st.columns([1, 1.1])

        with col_b1:
            st.markdown("#### Ecuaciones del Flujo de Potencia")

            st.markdown("**1. Potencia Eléctrica Absorbida $P_1$:**")
            st.write("Energía que el motor extrae de la red trifásica. Es el punto de partida de todo el balance.")
            st.latex(r"P_1 = \sqrt{3} \cdot U_L \cdot I_L \cdot \cos\varphi")

            st.markdown("**2. Pérdidas en el Estator:**")
            st.write(r"Antes de cruzar el entrehierro, la energía sufre dos tipos de pérdidas en el núcleo y los devanados del estator:")
            st.latex(r"P_{Cu1} = 3 \cdot R_1 \cdot I_1^2 \quad \text{(Cobre estator)}")
            st.latex(r"P_{Fe} \quad \text{(Hierro: histéresis + corrientes de Foucault)}")

            st.markdown("**3. Potencia del Entrehierro $P_{ag}$** (Air Gap):")
            st.write(r"Potencia que cruza el entrehierro magnético hacia el rotor. Es la potencia síncrona total:")
            st.latex(r"P_{ag} = P_1 - P_{Cu1} - P_{Fe} = 3 \cdot \frac{R'_2}{s} \cdot I'^2_2")

            st.markdown("**4. Pérdidas en el Rotor $P_{Cu2}$:**")
            st.write(r"La fracción que disipa el rotor por efecto Joule. Crece linealmente con el deslizamiento — motor más lento = más calor en el rotor:")
            st.latex(r"P_{Cu2} = s \cdot P_{ag} = 3 \cdot R'_2 \cdot I'^2_2")

            st.markdown("**5. Potencia Mecánica Interna $P_{mi}$:**")
            st.latex(r"P_{mi} = P_{ag} - P_{Cu2} = (1 - s) \cdot P_{ag}")

            st.markdown("**6. Potencia Útil $P_u$ y Rendimiento $\eta$:**")
            st.write("Se descuentan las pérdidas mecánicas (rozamiento en rodamientos, ventilador):")
            st.latex(r"P_u = P_{mi} - P_{mec} \qquad \eta = \frac{P_u}{P_1} \cdot 100\%")

            with st.expander("Relaciones de par a partir del balance"):
                st.write(r"La potencia del entrehierro y el par están ligados por la velocidad síncrona:")
                st.latex(r"M_{em} = \frac{P_{ag}}{\omega_s} = \frac{P_{ag}}{2\pi n_s / 60}")
                st.write(r"Mientras que el par en el eje usa la velocidad real del rotor:")
                st.latex(r"M_u = \frac{P_u}{\omega_r} = \frac{P_u}{2\pi n / 60}")
                st.info(r"La diferencia $M_{em} - M_u$ es el par de rozamiento y ventilación ($M_{mec}$).")

        with col_b2:
            st.markdown("#### Simulador de Flujo (Diagrama Waterfall)")
            st.write("Introduce los datos de funcionamiento para ver cómo la potencia se va consumiendo en cada etapa:")

            p1_in = st.number_input("Potencia Absorbida $P_1$ (W)", value=10000, step=500, key="p1_bal")
            s_in = st.slider("Deslizamiento $s$", 0.01, 0.15, 0.03, step=0.005, format="%.3f", key="s_bal")
            p_cu1_in = st.number_input("Pérdidas Cobre Estator $P_{Cu1}$ (W)", value=400, step=50, key="pcu1_bal")
            p_fe_in = st.number_input("Pérdidas Hierro $P_{Fe}$ (W)", value=300, step=50, key="pfe_bal")
            p_mec_in = st.number_input("Pérdidas Mecánicas $P_{mec}$ (W)", value=200, step=50, key="pmec_bal")

            p_ag_calc = p1_in - p_cu1_in - p_fe_in
            p_cu2_calc = s_in * p_ag_calc
            p_mi_calc = p_ag_calc - p_cu2_calc
            p_util_calc = p_mi_calc - p_mec_in
            rendimiento = (p_util_calc / p1_in) * 100 if p1_in > 0 else 0

            # Métricas rápidas
            bm1, bm2, bm3 = st.columns(3)
            bm1.metric("$P_{ag}$", f"{p_ag_calc:.0f} W")
            bm2.metric("$P_{mi}$", f"{p_mi_calc:.0f} W")
            bm3.metric("$\\eta$", f"{rendimiento:.1f}%", delta=f"P_u = {p_util_calc:.0f} W", delta_color="off")

            fig_waterfall = go.Figure(go.Waterfall(
                name="Balance", orientation="v",
                measure=["absolute", "relative", "relative", "total", "relative", "total", "relative", "total"],
                x=["P₁ (Red)", "P_Cu1", "P_Fe", "P_ag", "P_Cu2", "P_mi", "P_mec", "P_útil"],
                textposition="outside",
                text=[
                    f"<b>{p1_in:,.0f} W</b>",
                    f"<b>-{p_cu1_in:,.0f} W</b>",
                    f"<b>-{p_fe_in:,.0f} W</b>",
                    f"<b>{p_ag_calc:,.0f} W</b>",
                    f"<b>-{p_cu2_calc:,.0f} W</b>",
                    f"<b>{p_mi_calc:,.0f} W</b>",
                    f"<b>-{p_mec_in:,.0f} W</b>",
                    f"<b>{p_util_calc:,.0f} W</b>"
                ],
                y=[p1_in, -p_cu1_in, -p_fe_in, 0, -p_cu2_calc, 0, -p_mec_in, 0],
                connector={"line": {"color": "rgba(255,255,255,0.15)", "width": 2, "dash": "solid"}},
                decreasing={"marker": {"color": "rgba(239, 68, 68, 0.8)", "line": {"color": "#ef4444", "width": 2}}},
                increasing={"marker": {"color": "rgba(0, 173, 181, 0.8)", "line": {"color": "#00ADB5", "width": 2}}},
                totals={"marker": {"color": "rgba(129, 140, 248, 0.8)", "line": {"color": "#818CF8", "width": 2}}}
            ))
            
            fig_waterfall.update_layout(
                title=dict(
                    text=f"Flujo de Potencia &nbsp;|&nbsp; Rendimiento: <span style='color:#10b981'><b>{rendimiento:.1f}%</b></span>", 
                    font=dict(size=16, family="Inter, sans-serif"),
                    x=0.5,
                    y=0.92
                ),
                showlegend=False,
                height=450,
                margin=dict(l=40, r=40, t=70, b=40),
                paper_bgcolor="rgba(0,0,0,0)",
                plot_bgcolor="rgba(0,0,0,0)",
                yaxis=dict(
                    showgrid=True, 
                    gridcolor="rgba(255,255,255,0.05)", 
                    zeroline=True, 
                    zerolinecolor="rgba(255,255,255,0.1)",
                    tickformat=",d",
                    ticksuffix=" W",
                    title_font=dict(size=12, color="rgba(255,255,255,0.5)")
                ),
                xaxis=dict(
                    showgrid=False,
                    tickfont=dict(size=12, family="Inter, sans-serif", color="#d1d5db"),
                ),
                font=dict(family="Inter, sans-serif", color="#e5e7eb", size=12)
            )
            st.plotly_chart(fig_waterfall, use_container_width=True)


    # --------------------------------------------------------------------------
    # PESTAÑA 2.7: PLACA DE CARACTERÍSTICAS
    # --------------------------------------------------------------------------
    with tab_placa:
        st.markdown("### Interpretación de la Placa de Características")
        st.write(r"""
        La placa de características (*nameplate*) es el **pasaporte técnico** del motor. 
        Todos los datos de instalación, protección y operación quedan grabados permanentemente en ella.
        Ignorar cualquiera de estos valores puede provocar desde un rendimiento deficiente hasta la destrucción del aislamiento por sobrecalentamiento.
        """)

        # ================================================================
        # PLACA SVG REALISTA
        # ================================================================
        st.markdown(r"""<div style="background: linear-gradient(135deg, #1c1e26, #12141a); border: 2px solid #3b4252; border-radius: 8px; padding: 25px; color: #eceff4; font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif; box-shadow: 0 10px 30px rgba(0,0,0,0.6); max-width: 800px; margin: 20px auto; position: relative;">
<div style="position: absolute; top: 10px; left: 10px; width: 10px; height: 10px; border-radius: 50%; background: radial-gradient(circle, #4c566a 30%, #2e3440 90%); border: 1px solid #1c1e26;"></div>
<div style="position: absolute; top: 10px; right: 10px; width: 10px; height: 10px; border-radius: 50%; background: radial-gradient(circle, #4c566a 30%, #2e3440 90%); border: 1px solid #1c1e26;"></div>
<div style="position: absolute; bottom: 10px; left: 10px; width: 10px; height: 10px; border-radius: 50%; background: radial-gradient(circle, #4c566a 30%, #2e3440 90%); border: 1px solid #1c1e26;"></div>
<div style="position: absolute; bottom: 10px; right: 10px; width: 10px; height: 10px; border-radius: 50%; background: radial-gradient(circle, #4c566a 30%, #2e3440 90%); border: 1px solid #1c1e26;"></div>
<div style="display: flex; justify-content: space-between; align-items: flex-end; border-bottom: 2px solid #4c566a; padding-bottom: 12px; margin-bottom: 15px; padding-left: 15px; padding-right: 15px;">
<div>
<h2 style="margin: 0; color: #88c0d0; font-size: 26px; letter-spacing: 3px; font-weight: 900;">SIMOTOR</h2>
<span style="font-size: 11px; color: #d8dee9; letter-spacing: 1px;">INDUSTRIAS ELÉCTRICAS S.A.</span>
</div>
<div style="text-align: right;">
<div style="font-weight: 800; font-size: 15px; letter-spacing: 1.5px;">MOTOR ASÍNCRONO TRIFÁSICO</div>
<div style="font-size: 11px; color: #81a1c1;">IEC 60034-1 &nbsp;|&nbsp; THREE-PHASE INDUCTION MOTOR</div>
</div>
</div>
<div style="text-align: center; margin-bottom: 20px; font-size: 16px; font-weight: bold; color: #a3be8c; letter-spacing: 2px; background: rgba(46, 52, 64, 0.5); padding: 5px; border-radius: 4px;">
TIPO: MS 100L-4 &nbsp;&nbsp;&nbsp;|&nbsp;&nbsp;&nbsp; S/N: 2024-0318
</div>
<div style="display: grid; grid-template-columns: repeat(4, 1fr); gap: 12px; text-align: center; margin-bottom: 15px; padding: 0 10px;">
<div style="background: #2e3440; padding: 12px; border-radius: 6px; border: 1px solid #434c5e; box-shadow: inset 0 2px 4px rgba(0,0,0,0.2);">
<div style="font-size: 11px; color: #81a1c1; margin-bottom: 6px; letter-spacing: 1px;">POTENCIA</div>
<div style="font-size: 22px; font-weight: 900; color: #ebcb8b;">3.0 kW</div>
</div>
<div style="background: #2e3440; padding: 12px; border-radius: 6px; border: 1px solid #434c5e; box-shadow: inset 0 2px 4px rgba(0,0,0,0.2);">
<div style="font-size: 11px; color: #81a1c1; margin-bottom: 6px; letter-spacing: 1px;">TENSIÓN</div>
<div style="font-size: 15px; font-weight: 800;">230 V Δ</div>
<div style="font-size: 14px; font-weight: 600; color: #d8dee9;">400 V Y</div>
</div>
<div style="background: #2e3440; padding: 12px; border-radius: 6px; border: 1px solid #434c5e; box-shadow: inset 0 2px 4px rgba(0,0,0,0.2);">
<div style="font-size: 11px; color: #81a1c1; margin-bottom: 6px; letter-spacing: 1px;">CORRIENTE</div>
<div style="font-size: 15px; font-weight: 800;">11.2 A Δ</div>
<div style="font-size: 14px; font-weight: 600; color: #d8dee9;">6.5 A Y</div>
</div>
<div style="background: #2e3440; padding: 12px; border-radius: 6px; border: 1px solid #434c5e; box-shadow: inset 0 2px 4px rgba(0,0,0,0.2);">
<div style="font-size: 11px; color: #81a1c1; margin-bottom: 6px; letter-spacing: 1px;">VELOCIDAD</div>
<div style="font-size: 22px; font-weight: 900; color: #88c0d0;">1440<span style="font-size: 12px; margin-left:4px;">min⁻¹</span></div>
</div>
</div>
<div style="display: grid; grid-template-columns: repeat(6, 1fr); gap: 10px; text-align: center; margin-bottom: 20px; padding: 0 10px;">
<div style="background: #3b4252; padding: 10px; border-radius: 4px; border: 1px solid #4c566a;">
<div style="font-size: 10px; color: #e5e9f0; margin-bottom: 4px;">Hz</div>
<div style="font-size: 16px; font-weight: bold;">50</div>
</div>
<div style="background: #3b4252; padding: 10px; border-radius: 4px; border: 1px solid #4c566a;">
<div style="font-size: 10px; color: #e5e9f0; margin-bottom: 4px;">cos φ</div>
<div style="font-size: 16px; font-weight: bold;">0.82</div>
</div>
<div style="background: #3b4252; padding: 10px; border-radius: 4px; border: 1px solid #4c566a;">
<div style="font-size: 10px; color: #e5e9f0; margin-bottom: 4px;">POLOS</div>
<div style="font-size: 16px; font-weight: bold;">4</div>
</div>
<div style="background: #3b4252; padding: 10px; border-radius: 4px; border: 1px solid #4c566a;">
<div style="font-size: 10px; color: #e5e9f0; margin-bottom: 4px;">SERVICIO</div>
<div style="font-size: 16px; font-weight: bold;">S1</div>
</div>
<div style="background: #3b4252; padding: 10px; border-radius: 4px; border: 1px solid #4c566a;">
<div style="font-size: 10px; color: #e5e9f0; margin-bottom: 4px;">AISL.</div>
<div style="font-size: 16px; font-weight: bold;">Cl. F</div>
</div>
<div style="background: #3b4252; padding: 10px; border-radius: 4px; border: 1px solid #4c566a;">
<div style="font-size: 10px; color: #e5e9f0; margin-bottom: 4px;">IP</div>
<div style="font-size: 16px; font-weight: bold;">55</div>
</div>
</div>
<div style="display: flex; justify-content: space-between; align-items: center; background: #242933; padding: 12px 20px; border-radius: 6px; border-left: 5px solid #a3be8c; margin: 0 10px;">
<div style="display: flex; align-items: center; gap: 20px;">
<div>
<div style="font-size: 11px; color: #81a1c1; letter-spacing: 1px;">EFICIENCIA</div>
<div style="font-size: 20px; font-weight: 900; color: #a3be8c;">87.7 % <span style="background: #a3be8c; color: #2e3440; padding: 2px 8px; border-radius: 4px; font-size: 13px; margin-left: 8px; vertical-align: middle;">IE3</span></div>
</div>
</div>
<div style="text-align: right; border-left: 1px solid #4c566a; padding-left: 20px;">
<div style="font-size: 11px; color: #81a1c1; letter-spacing: 1px;">PESO</div>
<div style="font-size: 16px; font-weight: 800;">28 kg</div>
</div>
</div>
<div style="text-align: center; font-size: 10px; color: #4c566a; margin-top: 20px; padding-top: 10px; border-top: 1px dotted #3b4252;">
MADE IN SPAIN · 2024 &nbsp;|&nbsp; www.simotor.es &nbsp;|&nbsp; +34 964 000 000
</div>
</div>""", unsafe_allow_html=True)

        st.caption("Placa de características normalizada con formato industrial limpio y estructurado (datos orientativos para un motor de 3 kW).")

        # Desglose didáctico
        st.markdown("#### Análisis de los parámetros principales")

        col_p1, col_p2 = st.columns(2)

        with col_p1:
            with st.expander("Tensión y Conexión (V)", expanded=True):
                st.write("**¿Qué significa?**")
                st.write("Indica las tensiones que soportan los devanados. El valor más bajo (230V) es lo máximo que admite cada fase del motor.")
                st.warning("**Regla de Oro:** Si tu red es de 400V entre fases, DEBES conectar en **Estrella (Y)**. Si conectas en Triángulo (Δ), aplicarás 400V a una bobina de 230V y el motor se quemará en segundos.")
            
            with st.expander("Potencia Nominal (kW / CV)"):
                st.write("**¿Qué significa?**")
                st.write("Es la **Potencia Útil ($P_u$)** que el motor entrega en el eje. No es la potencia que consume de la red (que siempre es mayor debido a las pérdidas).")
                st.latex(r"1 \text{ CV} \approx 0.736 \text{ kW} \quad | \quad 1 \text{ HP} \approx 0.746 \text{ kW}")

            with st.expander("Velocidad Nominal (min⁻¹ o rpm)"):
                st.write("**¿Qué significa?**")
                st.write("Es la velocidad real de giro a plena carga. Como es un motor asíncrono, siempre será menor a la de sincronismo.")
                st.info("💡 **Dato Didáctico:** Si ves 1440 rpm en la placa, sabes automáticamente que el motor es de 4 polos (sincronismo = 1500 rpm) y que su deslizamiento nominal es del 4%.")

        with col_p2:
            with st.expander("Corriente Nominal (A)"):
                st.write("**¿Qué significa?**")
                st.write("Es la intensidad que circula por la línea cuando el motor trabaja a su potencia nominal. Se dan dos valores asociados a la tensión: el mayor para la conexión Δ y el menor para Y.")
                st.write("Sirve para calibrar el **relé térmico** de protección.")

            with st.expander("Factor de Potencia (cos φ)"):
                st.write("**¿Qué significa?**")
                st.write("Indica qué parte de la corriente absorbida se convierte en trabajo útil frente a la corriente reactiva necesaria para crear los campos magnéticos.")
                st.write("Un valor de 0.82 es típico. Cuanto más bajo, más 'penaliza' la compañía eléctrica por consumo de reactiva.")

            with st.expander("Clase de Aislamiento (IC)"):
                st.write("**¿Qué significa?**")
                st.write("Indica la temperatura máxima que soporta el barniz de las bobinas sin degradarse. Las más comunes son:")
                st.markdown("- **Clase B:** 130°C\n- **Clase F:** 155°C (Estándar industrial)\n- **Clase H:** 180°C")

        st.markdown("---")
        st.markdown("#### Datos de Protección y Servicio")
        
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
        st.markdown("### Los 'Factores K': Diseño Físico y Eficiencia")
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
        
        st.markdown("#### El Factor de Carga ($k$) y la Curva de Rendimiento")
        st.write("""
        Más allá del diseño físico, el rendimiento del motor operando en una fábrica depende del **Factor de Carga ($k$)**, también llamado índice de carga. Es la relación entre la potencia que se le está exigiendo en ese instante y su potencia nominal de placa: $k = P / P_{nominal}$.
        """)
        
        st.markdown("**Teorema del Rendimiento Máximo**")
        st.write("Las pérdidas de un motor se dividen en dos familias:")
        st.markdown("""
        * **Fijas ($P_{Fe}$ + $P_{mec}$):** Rozamiento y magnetización. No cambian aunque cambie la carga.
        * **Variables ($P_{Cu}$):** Efecto Joule. Evolucionan con el cuadrado de la carga ($k^2$).
        """)
        st.write("Matemáticamente, si derivamos la ecuación del rendimiento respecto a $k$ e igualamos a cero, demostramos que el **rendimiento máximo se alcanza cuando las pérdidas variables igualan a las fijas:**")
        st.latex(r"P_{fijas} = k_{opt}^2 \cdot P_{Cu_{nominal}} \implies k_{opt} = \sqrt{\frac{P_{fijas}}{P_{Cu_{nominal}}}}")
    # --------------------------------------------------------------------------
    # PESTAÑA 2.9: TEOREMA DE FERRARIS (CAMPO GIRATORIO)
    # --------------------------------------------------------------------------
    with tab_ferraris:
        st.markdown("### El Corazón del Motor AC: El Teorema de Ferraris")
        st.write("""
        El físico italiano Galileo Ferraris descubrió en 1885 el principio que hace posible todos los motores de corriente alterna modernos: **cómo crear movimiento rotativo a partir de piezas completamente estáticas**.
        """)
        
        

        col_teo1, col_teo2 = st.columns([1, 1])

        with col_teo1:
            st.markdown("#### Las Premisas del Sistema")
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
            st.markdown("#### Campos Magnéticos Pulsantes")
            st.write("Cada bobina genera un campo magnético ($B$) en su propio eje estático. Su magnitud sube y baja al ritmo de su corriente (campo pulsante):")
            st.latex(r"\vec{B}_U(t) = B_{max} \cos(\omega t) \angle 0^\circ")
            st.latex(r"\vec{B}_V(t) = B_{max} \cos(\omega t - 120^\circ) \angle 120^\circ")
            st.latex(r"\vec{B}_W(t) = B_{max} \cos(\omega t - 240^\circ) \angle 240^\circ")
            
            st.info("⚠️ **Nota:** Fíjate que en cada ecuación, el ángulo aparece dos veces: restando dentro del coseno (retraso en el tiempo) y como el ángulo del vector (posición física de la bobina).")

        st.markdown("---")
        st.markdown("#### Demostración Matemática (Suma Vectorial)")
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
        
        # ==================================================================
        # SIMULADOR INTERACTIVO PROFESIONAL — TEOREMA DE FERRARIS
        # Canvas HTML5 animado con controles integrados
        # ==================================================================
        FERRARIS_SIM_HTML = """
        <link href="https://fonts.googleapis.com/css2?family=Inter:wght@400;600;700;800&display=swap" rel="stylesheet">
        <style>
          *{margin:0;padding:0;box-sizing:border-box;}
          body{background:transparent;overflow:hidden;font-family:'Inter',sans-serif;}
          #ferraris-wrap{
            background:linear-gradient(145deg,#080c14,#0d1220,#0a0f1a);
            border:1px solid rgba(255,255,255,0.08);
            border-radius:14px;
            padding:0;
            position:relative;
            overflow:hidden;
          }
          #ferraris-wrap::before{
            content:'';position:absolute;top:0;left:0;right:0;height:1px;
            background:linear-gradient(90deg,transparent,rgba(129,140,248,0.3),transparent);
          }
          .ctrl-bar{
            display:flex;align-items:center;justify-content:space-between;
            padding:14px 22px;
            background:rgba(255,255,255,0.02);
            border-bottom:1px solid rgba(255,255,255,0.06);
          }
          .ctrl-bar .title{
            font-size:14px;font-weight:700;color:#e5e7eb;letter-spacing:0.5px;
          }
          .ctrl-bar .title span{color:#818CF8;font-weight:800;}
          .ctrl-grp{display:flex;gap:12px;align-items:center;}
          .btn{
            background:rgba(129,140,248,0.12);border:1px solid rgba(129,140,248,0.25);
            color:#a5b4fc;border-radius:8px;padding:6px 16px;cursor:pointer;
            font-family:'Inter',sans-serif;font-size:12px;font-weight:600;
            transition:all 0.2s;
          }
          .btn:hover{background:rgba(129,140,248,0.25);color:#c7d2fe;}
          .btn.active{background:rgba(129,140,248,0.3);border-color:#818CF8;color:#fff;}
          .spd-label{font-size:11px;color:#6b7280;font-weight:600;letter-spacing:0.5px;}
          .info-strip{
            display:flex;gap:0;border-top:1px solid rgba(255,255,255,0.06);
          }
          .info-cell{
            flex:1;text-align:center;padding:10px 6px;
            border-right:1px solid rgba(255,255,255,0.04);
          }
          .info-cell:last-child{border-right:none;}
          .info-cell .lbl{font-size:9px;color:#6b7280;text-transform:uppercase;letter-spacing:1px;margin-bottom:2px;}
          .info-cell .val{font-size:16px;font-weight:800;color:#e5e7eb;}
          .info-cell .val.cyan{color:#22d3ee;}
          .info-cell .val.purple{color:#a78bfa;}
          .info-cell .val.green{color:#34d399;}
          .info-cell .val.amber{color:#f59e0b;}
        </style>
        <div id="ferraris-wrap">
          <div class="ctrl-bar">
            <div class="title"><span>▶</span> Simulador del Teorema de Ferraris — Campo Magnético Giratorio</div>
            <div class="ctrl-grp">
              <span class="spd-label">VELOCIDAD</span>
              <button class="btn" onclick="setSpd(0.3)" id="s1">0.3×</button>
              <button class="btn active" onclick="setSpd(1)" id="s2">1×</button>
              <button class="btn" onclick="setSpd(2)" id="s3">2×</button>
              <button class="btn" onclick="togglePlay()" id="ppBtn">⏸ Pausa</button>
            </div>
          </div>
          <canvas id="fc" style="display:block;width:100%;"></canvas>
          <div class="info-strip">
            <div class="info-cell"><div class="lbl">ωt</div><div class="val cyan" id="d_wt">0°</div></div>
            <div class="info-cell"><div class="lbl">|B_res|</div><div class="val green" id="d_mag">1.50</div></div>
            <div class="info-cell"><div class="lbl">B_U</div><div class="val" style="color:#22d3ee" id="d_bu">1.00</div></div>
            <div class="info-cell"><div class="lbl">B_V</div><div class="val" style="color:#f59e0b" id="d_bv">-0.50</div></div>
            <div class="info-cell"><div class="lbl">B_W</div><div class="val" style="color:#a78bfa" id="d_bw">-0.50</div></div>
            <div class="info-cell"><div class="lbl">Ángulo Res.</div><div class="val amber" id="d_ang">0°</div></div>
          </div>
        </div>
        <script>
        (function(){
        var cv=document.getElementById('fc'),g=cv.getContext('2d');
        var W,H,playing=true,spd=1,t=0;
        var PI=Math.PI,TAU=2*PI;

        /* Responsive sizing */
        function resize(){
          var wrap=document.getElementById('ferraris-wrap');
          W=wrap.clientWidth;
          if(W<10){requestAnimationFrame(resize);return;}
          H=Math.min(520,W*0.6);
          cv.width=W*2; cv.height=H*2;
          cv.style.height=H+'px';
          g.setTransform(2,0,0,2,0,0);
        }
        requestAnimationFrame(resize);
        window.addEventListener('resize',resize);

        var phaseCol=['#22d3ee','#f59e0b','#a78bfa'];
        var phaseNm=['U','V','W'];
        var phaseAng=[0, TAU/3, 2*TAU/3];
        var trailLen=180, trail=[];

        function lerp(a,b,t){return a+(b-a)*t;}

        /* Arrow drawing */
        function arrow(x0,y0,x1,y1,col,w,headSz){
          var dx=x1-x0,dy=y1-y0,len=Math.sqrt(dx*dx+dy*dy);
          if(len<1)return;
          var ux=dx/len,uy=dy/len;
          // shaft
          g.beginPath();g.moveTo(x0,y0);g.lineTo(x1-ux*headSz*0.6,y1-uy*headSz*0.6);
          g.strokeStyle=col;g.lineWidth=w;g.lineCap='round';g.stroke();
          // head
          var px=-uy,py=ux;
          g.beginPath();
          g.moveTo(x1,y1);
          g.lineTo(x1-ux*headSz+px*headSz*0.4, y1-uy*headSz+py*headSz*0.4);
          g.lineTo(x1-ux*headSz*0.65, y1-uy*headSz*0.65);
          g.lineTo(x1-ux*headSz-px*headSz*0.4, y1-uy*headSz-py*headSz*0.4);
          g.closePath();g.fillStyle=col;g.fill();
        }

        /* Main draw */
        function draw(){
          g.clearRect(0,0,W,H);

          /* ── Layout ── */
          var vecCx=W*0.38, vecCy=H*0.5;
          var R=Math.min(W*0.24, H*0.38);
          var wavX=W*0.7, wavW=W*0.25, wavH=H*0.32, wavCy=H*0.5;

          /* ──────────── VECTOR DIAGRAM (left) ──────────── */

          /* Stator ring */
          g.beginPath();g.arc(vecCx,vecCy,R+18,0,TAU);g.arc(vecCx,vecCy,R+8,0,TAU,true);g.closePath();
          var sg=g.createRadialGradient(vecCx,vecCy,R+8,vecCx,vecCy,R+18);
          sg.addColorStop(0,'rgba(255,255,255,0.04)');sg.addColorStop(1,'rgba(255,255,255,0.01)');
          g.fillStyle=sg;g.fill();
          g.strokeStyle='rgba(255,255,255,0.08)';g.lineWidth=1;g.stroke();

          /* Concentric grid circles */
          for(var rr=0.25;rr<=1.5;rr+=0.25){
            g.beginPath();g.arc(vecCx,vecCy,R*rr/1.5,0,TAU);
            g.strokeStyle=rr===1.5?'rgba(255,255,255,0.08)':'rgba(255,255,255,0.03)';
            g.lineWidth=rr===0.75||rr===1.5?1:0.5;g.stroke();
          }
          /* Axis lines */
          for(var ai=0;ai<6;ai++){
            var aa=ai*PI/3;
            g.beginPath();g.moveTo(vecCx,vecCy);
            g.lineTo(vecCx+Math.cos(aa)*(R+5),vecCy-Math.sin(aa)*(R+5));
            g.strokeStyle='rgba(255,255,255,0.04)';g.lineWidth=1;g.stroke();
          }

          /* Trajectory circle (radius = 1.5 Bmax) */
          g.beginPath();g.arc(vecCx,vecCy,R,0,TAU);
          g.strokeStyle='rgba(239,68,68,0.2)';g.lineWidth=2;g.setLineDash([6,4]);g.stroke();g.setLineDash([]);

          /* Trail */
          var Bu=Math.cos(t), Bv=Math.cos(t-TAU/3), Bw=Math.cos(t-2*TAU/3);
          var Brx=Bu+Bv*Math.cos(TAU/3)+Bw*Math.cos(2*TAU/3);
          var Bry=   Bv*Math.sin(TAU/3)+Bw*Math.sin(2*TAU/3);
          var Bmag=Math.sqrt(Brx*Brx+Bry*Bry);
          var Bang=Math.atan2(Bry,Brx);

          var scl=R/1.5;
          var rxP=vecCx+Brx*scl, ryP=vecCy-Bry*scl;
          trail.push({x:rxP,y:ryP});
          if(trail.length>trailLen)trail.shift();

          if(trail.length>2){
            g.beginPath();g.moveTo(trail[0].x,trail[0].y);
            for(var ti=1;ti<trail.length;ti++){
              g.lineTo(trail[ti].x,trail[ti].y);
            }
            g.strokeStyle='rgba(239,68,68,0.35)';g.lineWidth=2.5;g.lineCap='round';g.stroke();
            /* Glow */
            g.strokeStyle='rgba(239,68,68,0.1)';g.lineWidth=8;g.stroke();
          }

          /* Phase vectors */
          var phMags=[Bu,Bv,Bw];
          for(var i=0;i<3;i++){
            var a=phaseAng[i];
            var vx=phMags[i]*Math.cos(a)*scl;
            var vy=phMags[i]*Math.sin(a)*scl;
            var endX=vecCx+vx, endY=vecCy-vy;

            /* Phase axis label */
            var lbR=R+28;
            var lx=vecCx+Math.cos(a)*lbR, ly=vecCy-Math.sin(a)*lbR;
            g.font='bold 12px Inter,sans-serif';g.fillStyle=phaseCol[i];g.textAlign='center';g.textBaseline='middle';
            g.fillText(phaseNm[i]+'+',lx,ly);

            /* Glow under arrow */
            g.save();g.globalAlpha=0.15;g.shadowColor=phaseCol[i];g.shadowBlur=12;
            arrow(vecCx,vecCy,endX,endY,phaseCol[i],3,10);
            g.restore();
            /* Solid arrow */
            arrow(vecCx,vecCy,endX,endY,phaseCol[i],3,10);
          }

          /* Resultant vector */
          g.save();g.shadowColor='#ef4444';g.shadowBlur=20;g.globalAlpha=0.4;
          arrow(vecCx,vecCy,rxP,ryP,'#ef4444',5,14);
          g.restore();
          arrow(vecCx,vecCy,rxP,ryP,'#ef4444',5,14);

          /* Dot at tip */
          g.beginPath();g.arc(rxP,ryP,5,0,TAU);g.fillStyle='#ef4444';g.fill();
          g.beginPath();g.arc(rxP,ryP,8,0,TAU);g.strokeStyle='rgba(239,68,68,0.3)';g.lineWidth=2;g.stroke();

          /* Resultant label */
          g.font='bold 13px Inter,sans-serif';g.fillStyle='#fca5a5';g.textAlign='left';
          var lblOffX=rxP+14, lblOffY=ryP-8;
          g.fillText('B_res',lblOffX,lblOffY);
          g.font='600 10px Inter,sans-serif';g.fillStyle='rgba(252,165,165,0.6)';
          g.fillText('|'+Bmag.toFixed(2)+'| B_max',lblOffX,lblOffY+14);

          /* Center dot */
          g.beginPath();g.arc(vecCx,vecCy,3,0,TAU);g.fillStyle='rgba(255,255,255,0.3)';g.fill();

          /* Section title */
          g.font='600 11px Inter,sans-serif';g.fillStyle='rgba(255,255,255,0.25)';g.textAlign='center';
          g.fillText('DIAGRAMA VECTORIAL',vecCx,vecCy-R-38);

          /* ──────────── WAVEFORM PANEL (right) ──────────── */
          /* Background panel */
          var px0=wavX-wavW-10, py0=wavCy-wavH-30, pw=wavW*2+20, ph=wavH*2+55;
          g.fillStyle='rgba(255,255,255,0.015)';
          g.beginPath();
          var cr=10;
          g.moveTo(px0+cr,py0);g.arcTo(px0+pw,py0,px0+pw,py0+ph,cr);
          g.arcTo(px0+pw,py0+ph,px0,py0+ph,cr);g.arcTo(px0,py0+ph,px0,py0,cr);
          g.arcTo(px0,py0,px0+pw,py0,cr);g.closePath();g.fill();
          g.strokeStyle='rgba(255,255,255,0.05)';g.lineWidth=1;g.stroke();

          g.font='600 11px Inter,sans-serif';g.fillStyle='rgba(255,255,255,0.25)';g.textAlign='center';
          g.fillText('CORRIENTES TRIFÁSICAS',wavX,py0+14);

          /* Grid */
          g.strokeStyle='rgba(255,255,255,0.04)';g.lineWidth=0.5;
          for(var gy=-1;gy<=1;gy+=0.5){
            var yy=wavCy-gy*wavH;
            g.beginPath();g.moveTo(wavX-wavW,yy);g.lineTo(wavX+wavW,yy);g.stroke();
          }
          /* Zero axis */
          g.beginPath();g.moveTo(wavX-wavW,wavCy);g.lineTo(wavX+wavW,wavCy);
          g.strokeStyle='rgba(255,255,255,0.12)';g.lineWidth=1;g.stroke();

          /* Y axis labels */
          g.font='600 9px Inter,sans-serif';g.fillStyle='rgba(255,255,255,0.2)';g.textAlign='right';
          g.fillText('+I_max',wavX-wavW-4,wavCy-wavH+3);
          g.fillText('0',wavX-wavW-4,wavCy+3);
          g.fillText('−I_max',wavX-wavW-4,wavCy+wavH+3);

          /* Waveforms + vertical cursor */
          var tNorm=(t%(TAU))/TAU;
          var cursorX=wavX-wavW+tNorm*wavW*2;

          for(var p=0;p<3;p++){
            g.beginPath();
            for(var sx=0;sx<=wavW*2;sx++){
              var angle=(sx/(wavW*2))*TAU - phaseAng[p];
              var val=Math.cos(angle);
              var xx=wavX-wavW+sx;
              var yy=wavCy-val*wavH;
              if(sx===0)g.moveTo(xx,yy);else g.lineTo(xx,yy);
            }
            g.strokeStyle=phaseCol[p];g.lineWidth=2;g.globalAlpha=0.7;g.stroke();g.globalAlpha=1;

            /* Dot at current time */
            var cVal=Math.cos(t-phaseAng[p]);
            var dotY=wavCy-cVal*wavH;
            g.beginPath();g.arc(cursorX,dotY,4,0,TAU);g.fillStyle=phaseCol[p];g.fill();
          }

          /* Cursor line */
          g.beginPath();g.moveTo(cursorX,wavCy-wavH-15);g.lineTo(cursorX,wavCy+wavH+15);
          g.strokeStyle='rgba(255,255,255,0.25)';g.lineWidth=1;g.setLineDash([3,3]);g.stroke();g.setLineDash([]);

          /* Phase legend */
          var legY=wavCy+wavH+30;
          var legNames=['i_U (0°)','i_V (120°)','i_W (240°)'];
          for(var li=0;li<3;li++){
            var lx=wavX-wavW+li*(wavW*2/3)+20;
            g.beginPath();g.arc(lx,legY,4,0,TAU);g.fillStyle=phaseCol[li];g.fill();
            g.font='600 10px Inter,sans-serif';g.fillStyle=phaseCol[li];g.textAlign='left';
            g.fillText(legNames[li],lx+8,legY+3);
          }

          /* ──────────── Update HUD ──────────── */
          var wtDeg=((t*180/PI)%360+360)%360;
          document.getElementById('d_wt').textContent=wtDeg.toFixed(0)+'°';
          document.getElementById('d_mag').textContent=Bmag.toFixed(2);
          document.getElementById('d_bu').textContent=Bu.toFixed(2);
          document.getElementById('d_bv').textContent=Bv.toFixed(2);
          document.getElementById('d_bw').textContent=Bw.toFixed(2);
          var angDeg=((Bang*180/PI)%360+360)%360;
          document.getElementById('d_ang').textContent=angDeg.toFixed(0)+'°';
        }

        function loop(){
          if(playing)t+=0.02*spd;
          draw();
          requestAnimationFrame(loop);
        }
        loop();

        /* Controls */
        window.setSpd=function(v){
          spd=v;
          document.getElementById('s1').className='btn'+(v===0.3?' active':'');
          document.getElementById('s2').className='btn'+(v===1?' active':'');
          document.getElementById('s3').className='btn'+(v===2?' active':'');
        };
        window.togglePlay=function(){
          playing=!playing;
          document.getElementById('ppBtn').textContent=playing?'⏸ Pausa':'▶ Play';
          document.getElementById('ppBtn').className='btn'+(playing?'':' active');
        };
        })();
        </script>
        """

        components.html(FERRARIS_SIM_HTML, height=620, scrolling=False)
if __name__ == "__main__":
    app()