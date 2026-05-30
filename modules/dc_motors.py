import streamlit as st
import numpy as np
import plotly.graph_objects as go
import math
import streamlit.components.v1 as components

# ==============================================================================
# ANIMACIÓN 2D PROFESIONAL - MOTOR DC (SECCIÓN TRANSVERSAL)
# ==============================================================================
DC_MOTOR_ANIMATION_HTML = """
<link href="https://fonts.googleapis.com/css2?family=Inter:wght@400;600;700&display=swap" rel="stylesheet">
<style>*{margin:0;padding:0;}body{background:transparent;overflow:hidden;}</style>
<canvas id="dcm" width="700" height="500" style="display:block;margin:0 auto;border-radius:10px;"></canvas>
<script>
(function(){
var c=document.getElementById('dcm'),g=c.getContext('2d');
var W=700,H=500,cx=290,cy=210,t=0;
var SR=158,PO=144,PIR=100,RR=92,SH=16,CL=73,NC=12;
var PA=48*Math.PI/180,CY=cy+RR+55,CMR=28;

function na(a){a%=2*Math.PI;return a<0?a+2*Math.PI:a;}
function arw(x,y,ang,col,sz){g.save();g.translate(x,y);g.rotate(ang);g.beginPath();g.moveTo(0,0);g.lineTo(-sz,-sz*0.45);g.lineTo(-sz,sz*0.45);g.closePath();g.fillStyle=col;g.fill();g.restore();}
function rr(x,y,w,h,r){g.beginPath();g.moveTo(x+r,y);g.arcTo(x+w,y,x+w,y+h,r);g.arcTo(x+w,y+h,x,y+h,r);g.arcTo(x,y+h,x,y,r);g.arcTo(x,y,x+w,y,r);g.closePath();}
function pole(ba,c1,c2,lb){g.beginPath();g.arc(cx,cy,PO,ba-PA,ba+PA);g.arc(cx,cy,PIR,ba+PA,ba-PA,true);g.closePath();var p=g.createRadialGradient(cx,cy,PIR,cx,cy,PO);p.addColorStop(0,c2);p.addColorStop(1,c1);g.fillStyle=p;g.fill();g.strokeStyle=c2;g.lineWidth=1;g.stroke();var lr=(PIR+PO)/2;g.font='bold 22px Inter,system-ui,sans-serif';g.fillStyle='#FFF';g.textAlign='center';g.textBaseline='middle';g.fillText(lb,cx+lr*Math.cos(ba),cy+lr*Math.sin(ba));}

function draw(){
g.clearRect(0,0,W,H);
g.fillStyle='#0D1117';g.fillRect(0,0,W,H);
rr(0,0,W,H,10);g.strokeStyle='#21262D';g.lineWidth=1;g.stroke();

// Title
g.font='600 13px Inter,system-ui,sans-serif';g.fillStyle='#8B949E';g.textAlign='center';
g.fillText('MOTOR DC \u2014 SECCI\u00d3N TRANSVERSAL ANIMADA',cx,22);

// Stator yoke
g.beginPath();g.arc(cx,cy,SR,0,2*Math.PI);g.arc(cx,cy,PO,0,2*Math.PI,true);
var sg=g.createRadialGradient(cx,cy,PO,cx,cy,SR);sg.addColorStop(0,'#2D333B');sg.addColorStop(1,'#21262D');
g.fillStyle=sg;g.fill();
g.beginPath();g.arc(cx,cy,SR,0,2*Math.PI);g.strokeStyle='#444C56';g.lineWidth=2;g.stroke();

// Poles
pole(0,'#9B2C2C','#DC5656','N');
pole(Math.PI,'#1D4ED8','#60A5FA','S');

// Field lines N to S
g.save();g.globalAlpha=0.3;g.strokeStyle='#F9A826';g.lineWidth=1.2;g.setLineDash([5,4]);
for(var i=-2;i<=2;i++){var yo=i*20;g.beginPath();g.moveTo(cx+PIR-5,cy+yo);g.bezierCurveTo(cx+35,cy+yo*0.5,cx-35,cy+yo*0.5,cx-PIR+5,cy+yo);g.stroke();g.setLineDash([]);arw(cx-3,cy+yo*0.45,Math.PI,'#F9A826',5);g.setLineDash([5,4]);}
g.setLineDash([]);g.globalAlpha=1;g.restore();

// Rotor (rotating)
g.save();g.translate(cx,cy);g.rotate(t);
var rg=g.createRadialGradient(0,0,SH,0,0,RR);rg.addColorStop(0,'#1C2128');rg.addColorStop(0.8,'#161B22');rg.addColorStop(1,'#21262D');
g.beginPath();g.arc(0,0,RR,0,2*Math.PI);g.fillStyle=rg;g.fill();g.strokeStyle='#373E47';g.lineWidth=1.5;g.stroke();

// Lamination lines
g.strokeStyle='rgba(255,255,255,0.03)';g.lineWidth=0.5;
for(var i=0;i<36;i++){var la=(i/36)*2*Math.PI;g.beginPath();g.moveTo(SH*Math.cos(la),SH*Math.sin(la));g.lineTo((RR-2)*Math.cos(la),(RR-2)*Math.sin(la));g.stroke();}

// Conductor slots
for(var i=0;i<NC;i++){
var sa=(i/NC)*2*Math.PI,sx=CL*Math.cos(sa),sy=CL*Math.sin(sa);
var ab=na(sa+t),isOut=ab<Math.PI/2||ab>3*Math.PI/2;
g.beginPath();g.arc(sx,sy,8.5,0,2*Math.PI);g.fillStyle='#0D1117';g.fill();
g.beginPath();g.arc(sx,sy,6.5,0,2*Math.PI);g.fillStyle=isOut?'#F97316':'#3B82F6';g.fill();
g.strokeStyle='rgba(255,255,255,0.2)';g.lineWidth=0.8;g.stroke();
if(isOut){g.beginPath();g.arc(sx,sy,2,0,2*Math.PI);g.fillStyle='#FFF';g.fill();}
else{g.strokeStyle='#FFF';g.lineWidth=1.3;g.beginPath();g.moveTo(sx-3.5,sy-3.5);g.lineTo(sx+3.5,sy+3.5);g.moveTo(sx+3.5,sy-3.5);g.lineTo(sx-3.5,sy+3.5);g.stroke();}}

// Shaft
var shg=g.createRadialGradient(0,0,0,0,0,SH);shg.addColorStop(0,'#4D555E');shg.addColorStop(1,'#3D444D');
g.beginPath();g.arc(0,0,SH,0,2*Math.PI);g.fillStyle=shg;g.fill();g.strokeStyle='#555D66';g.lineWidth=1;g.stroke();
g.fillStyle='#2D333B';g.fillRect(-2,-SH,4,SH*2);
g.restore();

// EM glow
var ga=0.08+0.04*Math.sin(t*3);
g.beginPath();g.arc(cx,cy,RR+3,0,2*Math.PI);g.strokeStyle='rgba(6,182,212,'+ga.toFixed(3)+')';g.lineWidth=5;g.stroke();

// Force arrows
for(var i=0;i<NC;i++){
var sa=(i/NC)*2*Math.PI+t,ab=na(sa);
var nN=ab<PA||ab>2*Math.PI-PA,nS=Math.abs(ab-Math.PI)<PA;
if(nN||nS){var px=cx+CL*Math.cos(sa),py=cy+CL*Math.sin(sa),fa=sa+Math.PI/2,fl=22,fx=px+fl*Math.cos(fa),fy=py+fl*Math.sin(fa);
g.strokeStyle='#06B6D4';g.lineWidth=2;g.beginPath();g.moveTo(px,py);g.lineTo(fx,fy);g.stroke();arw(fx,fy,fa,'#06B6D4',6);}}

// Torque arrow
g.beginPath();g.arc(cx,cy,SH+10,-2.5,1.3);g.strokeStyle='#06B6D4';g.lineWidth=2.5;g.stroke();
arw(cx+(SH+10)*Math.cos(1.3),cy+(SH+10)*Math.sin(1.3),1.3+Math.PI/2,'#06B6D4',7);
g.font='italic bold 14px Georgia,serif';g.fillStyle='#06B6D4';g.textAlign='center';g.textBaseline='middle';
g.fillText('\u03c9',cx,cy);

// Commutator
g.beginPath();g.arc(cx,CY,CMR,0,2*Math.PI);g.fillStyle='#161B22';g.fill();
for(var i=0;i<NC;i++){var a1=(i/NC)*2*Math.PI+t+0.04,a2=((i+1)/NC)*2*Math.PI+t-0.04;g.beginPath();g.arc(cx,CY,CMR,a1,a2);g.arc(cx,CY,CMR-7,a2,a1,true);g.closePath();g.fillStyle=i%2?'#D4A017':'#B8960B';g.fill();g.strokeStyle='rgba(0,0,0,0.3)';g.lineWidth=0.5;g.stroke();}

// Connection line
g.strokeStyle='#30363D';g.lineWidth=1;g.setLineDash([3,3]);g.beginPath();g.moveTo(cx,cy+RR+2);g.lineTo(cx,CY-CMR-2);g.stroke();g.setLineDash([]);

// Brushes with sparks
var bw=8,bh=20;
g.fillStyle='#6E7681';g.fillRect(cx-CMR-bw-3,CY-bh/2,bw,bh);g.strokeStyle='#8B949E';g.lineWidth=1;g.strokeRect(cx-CMR-bw-3,CY-bh/2,bw,bh);
var sp1=Math.max(0,Math.sin(t*30)*Math.sin(t*47));g.fillStyle='rgba(255,200,50,'+sp1.toFixed(2)+')';g.beginPath();g.arc(cx-CMR-1,CY,2.5,0,2*Math.PI);g.fill();
g.fillStyle='#6E7681';g.fillRect(cx+CMR+3,CY-bh/2,bw,bh);g.strokeStyle='#8B949E';g.lineWidth=1;g.strokeRect(cx+CMR+3,CY-bh/2,bw,bh);
var sp2=Math.max(0,Math.sin(t*33)*Math.sin(t*51));g.fillStyle='rgba(255,200,50,'+sp2.toFixed(2)+')';g.beginPath();g.arc(cx+CMR+1,CY,2.5,0,2*Math.PI);g.fill();

// Terminal wires
g.strokeStyle='#F97316';g.lineWidth=2;g.beginPath();g.moveTo(cx+CMR+bw+3,CY);g.lineTo(cx+CMR+50,CY);g.lineTo(cx+CMR+50,CY-28);g.stroke();
g.font='bold 14px Inter,sans-serif';g.fillStyle='#F97316';g.textAlign='center';g.fillText('+',cx+CMR+50,CY-34);
g.strokeStyle='#3B82F6';g.lineWidth=2;g.beginPath();g.moveTo(cx-CMR-bw-3,CY);g.lineTo(cx-CMR-50,CY);g.lineTo(cx-CMR-50,CY-28);g.stroke();
g.fillStyle='#3B82F6';g.fillText('\u2212',cx-CMR-50,CY-34);

// Labels
g.font='600 11px Inter,system-ui,sans-serif';g.fillStyle='#8B949E';g.textAlign='center';
g.fillText('EST\u00c1TOR (Inductor)',cx,cy-SR-12);
g.fillText('ROTOR (Inducido)',cx,cy+RR+16);
g.fillText('COLECTOR DE DELGAS',cx,CY+CMR+14);
g.font='10px Inter,sans-serif';g.fillStyle='#6E7681';
g.textAlign='right';g.fillText('Escobilla (\u2212)',cx-CMR-bw-8,CY+4);
g.textAlign='left';g.fillText('Escobilla (+)',cx+CMR+bw+8,CY+4);

// Air gap
var gx=cx+(PIR+RR)/2*Math.cos(-0.4),gy=cy+(PIR+RR)/2*Math.sin(-0.4);
g.font='9px Inter,sans-serif';g.fillStyle='#555D66';g.textAlign='left';
g.fillText('\u03b4 (entrehierro)',gx+5,gy-2);
g.strokeStyle='#555D66';g.lineWidth=0.8;g.beginPath();g.moveTo(cx+PIR*Math.cos(-0.4),cy+PIR*Math.sin(-0.4));g.lineTo(cx+RR*Math.cos(-0.4),cy+RR*Math.sin(-0.4));g.stroke();

// Legend
var lx=W-185,ly=32,lw=168,lh=135;
rr(lx,ly,lw,lh,6);g.fillStyle='rgba(13,17,23,0.92)';g.fill();g.strokeStyle='#30363D';g.lineWidth=1;g.stroke();
g.font='600 10px Inter,system-ui,sans-serif';g.fillStyle='#E6EDF3';g.textAlign='left';g.fillText('LEYENDA',lx+10,ly+16);
g.font='10px Inter,system-ui,sans-serif';var yl=ly+34;
g.beginPath();g.arc(lx+16,yl,5,0,2*Math.PI);g.fillStyle='#F97316';g.fill();
g.beginPath();g.arc(lx+16,yl,1.5,0,2*Math.PI);g.fillStyle='#FFF';g.fill();
g.fillStyle='#8B949E';g.fillText('Corriente saliente \u2299',lx+27,yl+4);
yl+=19;
g.beginPath();g.arc(lx+16,yl,5,0,2*Math.PI);g.fillStyle='#3B82F6';g.fill();
g.strokeStyle='#FFF';g.lineWidth=1;g.beginPath();g.moveTo(lx+13,yl-3);g.lineTo(lx+19,yl+3);g.moveTo(lx+19,yl-3);g.lineTo(lx+13,yl+3);g.stroke();
g.fillStyle='#8B949E';g.fillText('Corriente entrante \u2297',lx+27,yl+4);
yl+=19;
g.strokeStyle='#F9A826';g.lineWidth=1.2;g.setLineDash([4,3]);g.beginPath();g.moveTo(lx+10,yl);g.lineTo(lx+22,yl);g.stroke();g.setLineDash([]);
g.fillStyle='#8B949E';g.fillText('Campo B (N \u2192 S)',lx+27,yl+4);
yl+=19;
g.strokeStyle='#06B6D4';g.lineWidth=2;g.beginPath();g.moveTo(lx+10,yl);g.lineTo(lx+22,yl);g.stroke();arw(lx+22,yl,0,'#06B6D4',5);
g.fillStyle='#8B949E';g.fillText('Fuerza F = I \u00d7 B',lx+27,yl+4);
yl+=19;
g.beginPath();g.arc(lx+16,yl,5,-2,0.8);g.strokeStyle='#06B6D4';g.lineWidth=1.5;g.stroke();
g.fillStyle='#8B949E';g.fillText('Par motor (\u03c9)',lx+27,yl+4);

// Equations panel
var ex=W-185,ey=ly+lh+12,ew=168,eh=85;
rr(ex,ey,ew,eh,6);g.fillStyle='rgba(13,17,23,0.92)';g.fill();g.strokeStyle='#30363D';g.lineWidth=1;g.stroke();
g.font='600 10px Inter,system-ui,sans-serif';g.fillStyle='#E6EDF3';g.textAlign='left';g.fillText('ECUACIONES CLAVE',ex+10,ey+16);
g.font='italic 12px Georgia,serif';g.fillStyle='#C9D1D9';
g.fillText('F = I \u00b7 L \u00d7 B',ex+14,ey+36);
g.fillText('E = K \u00b7 \u03a6 \u00b7 \u03c9',ex+14,ey+54);
g.fillText('M = K \u00b7 \u03a6 \u00b7 I\u2090',ex+14,ey+72);

t+=0.01;requestAnimationFrame(draw);}
draw();
})();
</script>
"""

def app():
    st.header("Motores de Corriente Continua (DC)")
    st.caption("Análisis fundamental de la máquina de corriente continua, principios de funcionamiento, tipos de excitación y curvas características.")

    tab_fundamentos, tab_partes, tab_ecuaciones, tab_tipos, tab_curvas, tab_arranque, tab_cuadrantes = st.tabs([
        "1 - Fundamentos",
        "2 - Partes Físicas",
        "3 - Ecuaciones",
        "4 - Excitación",
        "5 - Curvas y Control",
        "6 - Arranque",
        "7 - Cuadrantes"
    ])

    with tab_fundamentos:
        st.markdown("### Principio de Funcionamiento")
        st.write("El funcionamiento del motor de corriente continua se basa en la **Fuerza de Lorentz** y la inducción electromagnética descrita por la **Ley de Faraday**. Al interaccionar el campo magnético del estator con la corriente que circula por el rotor, se produce un par mecánico.")
        
        components.html(DC_MOTOR_ANIMATION_HTML, height=520)
        
        with st.expander("🛠️ Paso a Paso: Desde la Alimentación hasta el Movimiento", expanded=True):
            st.markdown(r"""
            Para entender cómo una máquina estática se convierte en un motor rotativo, debemos seguir el flujo de energía paso a paso:
            
            1.  **Excitación del Estator:** Se inyecta corriente continua en las bobinas del estator (o se usan imanes permanentes). Esta corriente genera un **campo magnético fijo** y constante (Flujo $\Phi$) que atraviesa el espacio del rotor.
            2.  **Alimentación del Inducido:** A través de las escobillas y el colector de delgas, introducimos corriente continua en los devanados del rotor (inducido).
            3.  **Aparición de la Fuerza de Lorentz:** Los conductores del rotor, ahora con corriente $I$, se encuentran inmersos en el campo magnético $B$ del estator. De acuerdo con la formulación diferencial de la ley de Lorentz ($d\vec{F} = I \cdot d\vec{l} \times \vec{B}$), cada elemento infinitesimal de corriente experimenta una fuerza elemental que, al integrarse a lo largo del conductor, produce la fuerza motriz.
            4.  **Generación de Par Motor:** Debido a la geometría cilíndrica del rotor, las fuerzas en los conductores opuestos crean un **momento o par de giro ($M$)**. Este par empuja al rotor a comenzar su rotación.
            5.  **Acción del Colector:** A medida que el rotor gira y los conductores cambian de posición respecto a los polos (Norte/Sur), el colector de delgas invierte automáticamente el sentido de la corriente en el momento preciso. Esto asegura que el par de giro mantenga siempre la misma dirección.
            6.  **Giro del Eje y FCEM:** El rotor acelera hasta que el par motor se equilibra con el par de la carga. Simultáneamente, por el hecho de girar en un campo magnético, se genera la **Fuerza Contraelectromotriz ($E$)**, que regula el consumo de corriente del motor.
            """)
            st.success("✨ **Resultado Final:** La energía eléctrica se ha transformado en energía mecánica disponible en el eje del motor.")
        
        with st.expander("🎯 Desacoplo de Corrientes y Ortogonalidad (90º)", expanded=True):
            st.markdown("""
            Una de las mayores ventajas de la máquina de corriente continua, y la razón por la que se usa como modelo ideal para el control de otras máquinas (como el Control Vectorial en AC), es el **desacoplo natural de sus corrientes**.
            """)
            
            col_d1, col_d2 = st.columns(2)
            with col_d1:
                st.markdown("**Desacoplo de Flujo y Par**")
                st.write("""
                En un motor de excitación independiente, podemos controlar dos variables de forma totalmente aislada:
                *   **Corriente de Excitación ($I_{exc}$):** Controla únicamente el **flujo magnético ($\Phi$)** en el estator (Eje Directo o Eje d).
                *   **Corriente de Inducido ($I_a$):** Controla únicamente el **par motor ($M$)** (Eje de Cuadratura o Eje q).
                """)
                st.info("Al ser circuitos independientes, variar el par no afecta al flujo, permitiendo una respuesta dinámica rapidísima.")
                
            with col_d2:
                st.markdown("**La Regla de los 90 Grados**")
                st.write(r"""
                Para que un motor sea eficiente, el par producido debe ser el máximo posible para una corriente dada. Físicamente, esto ocurre cuando el campo magnético del estator y el campo magnético del rotor son **perpendiculares (90º)** entre sí.
                """)
                st.latex(r"M = K \cdot \vec{\Phi} \times \vec{I_a} = K \cdot \Phi \cdot I_a \cdot \sin(\theta)")
                st.write(r"""
                Gracias a la posición de las escobillas, la máquina de DC asegura que $\theta = 90^\circ$ en todo momento. Como $\sin(90^\circ) = 1$, el aprovechamiento de la energía es máximo.
                """)

            st.success("💡 **Conclusión:** El diseño mecánico (escobillas y colector) garantiza que los ejes de flujo y par estén siempre 'desacoplados' y en cuadratura, emulando la estructura de un sistema de coordenadas cartesianas perfecto.")
        
        col1, col2 = st.columns(2)
        with col1:
            st.markdown("#### Fuerza Electromagnética (Fuerza de Lorentz)")
            st.markdown(r"""
            A nivel microscópico, la fuerza sobre una carga individual $q$ que se desplaza con velocidad $\vec{v}$ en un campo de inducción magnética $\vec{B}$ viene dada por la expresión $\vec{F} = q(\vec{v} \times \vec{B})$. En el análisis de máquinas eléctricas, donde trabajamos con conductores de geometría compleja o campos que pueden no ser perfectamente uniformes, la ley se formula en su **forma diferencial** haciendo uso del concepto clave de **elemento de corriente**.

            La fuerza infinitesimal $d\vec{F}$ que experimenta un segmento diferencial de conductor de longitud $dl$ recorrido por una corriente de intensidad $I$ e inmerso en un campo magnético con densidad de flujo $\vec{B}$ se expresa como:
            """)
            st.latex(r"d\vec{F} = I \cdot (d\vec{l} \times \vec{B})")
            st.markdown(r"""
            Donde:
            *   $I \cdot d\vec{l}$ es el **elemento diferencial de corriente**, un vector fundamental en electromagnetismo. Su módulo es el producto de la corriente $I$ por la longitud infinitesimal $dl$ del segmento, y su dirección y sentido vienen definidos por el vector desplazamiento $d\vec{l}$, que es tangente al conductor en la dirección del flujo de la corriente.
            *   $\vec{B}$ es el vector densidad de flujo magnético en la posición espacial que ocupa dicho elemento de corriente.
            *   $d\vec{F}$ es la fuerza diferencial resultante, la cual es siempre **ortogonal** al plano que contiene al elemento de corriente y al vector campo magnético (regla del producto vectorial).

            ##### De la Fuerza Diferencial al Par Motor
            Para determinar la fuerza total $\vec{F}$ ejercida sobre un conductor completo a lo largo de una trayectoria geométrica $C$, realizamos la integración de línea de todas las fuerzas diferenciales a lo largo del contorno:
            """)
            st.latex(r"\vec{F} = \int_{C} I \cdot (d\vec{l} \times \vec{B})")
            st.markdown(r"""
            En el caso simplificado de un **conductor rectilíneo** de longitud activa $L$ con corriente constante y sometido a un **campo magnético uniforme** $\vec{B}$, los términos constantes salen de la integral, recuperando la conocida expresión macroscópica:
            """)
            st.latex(r"\vec{F} = I \cdot (\vec{L} \times \vec{B})")
            st.info("La regla de la mano izquierda de Fleming ayuda a visualizar esta interacción ortogonal: el dedo índice representa la dirección de la densidad de flujo (N a S), el dedo corazón el sentido de la corriente, y el pulgar indica la dirección de la fuerza resultante.")
            
        with col2:
            st.markdown("#### Fuerza Contraelectromotriz (FCEM)")
            st.write("Al girar el rotor en el seno del campo magnético, los devanados cortan líneas de flujo. Esto induce una fuerza electromotriz interna que **se opone** a la tensión de alimentación aplicada:")
            st.latex(r"E = K \cdot \Phi \cdot \omega")
            st.caption(r"Donde $K$ es una constante constructiva de la máquina, $\Phi$ es el flujo magnético y $\omega$ la velocidad angular.")

    with tab_partes:
        st.markdown("### Constitución Físico-Mecánica")
        st.write("La máquina de DC requiere un diseño mecánico especial para asegurar que el par resultante sea siempre en la misma dirección, logrando un giro continuo.")
        
        col_st, col_rt = st.columns(2)
        with col_st:
            st.markdown("#### El Estator (Inductor)")
            st.markdown("""
            <div style="background-color: #080808; padding: 15px; border-radius: 12px; border: 1px solid #1A1A1A; margin-bottom: 15px; display: flex; justify-content: center;">
            <svg width="150" height="150" viewBox="0 0 150 150" xmlns="http://www.w3.org/2000/svg">
                <circle cx="75" cy="75" r="65" fill="none" stroke="#21262D" stroke-width="15"/>
                <path d="M 60 25 L 90 25 L 85 45 L 65 45 Z" fill="#DC5656" stroke="#9B2C2C"/>
                <text x="75" y="40" fill="white" font-family="sans-serif" font-weight="bold" font-size="12" text-anchor="middle">N</text>
                <path d="M 60 125 L 90 125 L 85 105 L 65 105 Z" fill="#60A5FA" stroke="#1D4ED8"/>
                <text x="75" y="120" fill="white" font-family="sans-serif" font-weight="bold" font-size="12" text-anchor="middle">S</text>
                <line x1="75" y1="50" x2="75" y2="100" stroke="#F9A826" stroke-width="2" stroke-dasharray="4,4"/>
                <line x1="60" y1="50" x2="60" y2="100" stroke="#F9A826" stroke-width="2" stroke-dasharray="4,4"/>
                <line x1="90" y1="50" x2="90" y2="100" stroke="#F9A826" stroke-width="2" stroke-dasharray="4,4"/>
            </svg>
            </div>
            """, unsafe_allow_html=True)
            st.write("Es la parte fija de la máquina encargada de crear el campo magnético principal. Puede estar formado por imanes permanentes (en motores pequeños) o por electroimanes con devanados alimentados por corriente continua.")
            
            st.markdown("#### El Rotor (Inducido)")
            st.markdown("""
            <div style="background-color: #080808; padding: 15px; border-radius: 12px; border: 1px solid #1A1A1A; margin-bottom: 15px; display: flex; justify-content: center;">
            <svg width="150" height="150" viewBox="0 0 150 150" xmlns="http://www.w3.org/2000/svg">
                <circle cx="75" cy="75" r="50" fill="#1C2128" stroke="#373E47" stroke-width="2"/>
                <circle cx="75" cy="75" r="12" fill="#4D555E" stroke="#21262D"/>
                <g fill="#F97316">
                    <circle cx="75" cy="32" r="5"/><circle cx="118" cy="75" r="5"/>
                    <circle cx="75" cy="118" r="5"/><circle cx="32" cy="75" r="5"/>
                    <circle cx="105" cy="45" r="5"/><circle cx="105" cy="105" r="5"/>
                    <circle cx="45" cy="105" r="5"/><circle cx="45" cy="45" r="5"/>
                </g>
            </svg>
            </div>
            """, unsafe_allow_html=True)
            st.write("Es la parte móvil y cilíndrica construida con chapas magnéticas. Alberga en sus ranuras los devanados donde se induce la FCEM y donde actúa la fuerza motriz.")
            
        with col_rt:
            st.markdown("#### Colector de Delgas y Escobillas")
            st.markdown("""
            <div style="background-color: #080808; padding: 15px; border-radius: 12px; border: 1px solid #1A1A1A; margin-bottom: 15px; display: flex; justify-content: center;">
            <svg width="150" height="150" viewBox="0 0 150 150" xmlns="http://www.w3.org/2000/svg">
                <circle cx="75" cy="75" r="40" fill="#161B22"/>
                <path d="M 75 35 A 40 40 0 0 1 115 75 L 105 75 A 30 30 0 0 0 75 45 Z" fill="#D4A017" stroke="#111" stroke-width="1"/>
                <path d="M 115 75 A 40 40 0 0 1 75 115 L 75 105 A 30 30 0 0 0 105 75 Z" fill="#B8960B" stroke="#111" stroke-width="1"/>
                <path d="M 75 115 A 40 40 0 0 1 35 75 L 45 75 A 30 30 0 0 0 75 105 Z" fill="#D4A017" stroke="#111" stroke-width="1"/>
                <path d="M 35 75 A 40 40 0 0 1 75 35 L 75 45 A 30 30 0 0 0 45 75 Z" fill="#B8960B" stroke="#111" stroke-width="1"/>
                <rect x="20" y="65" width="15" height="20" fill="#6E7681" stroke="#8B949E"/>
                <rect x="115" y="65" width="15" height="20" fill="#6E7681" stroke="#8B949E"/>
                <line x1="10" y1="75" x2="20" y2="75" stroke="#3B82F6" stroke-width="3"/>
                <line x1="130" y1="75" x2="140" y2="75" stroke="#F97316" stroke-width="3"/>
                <text x="10" y="65" fill="#3B82F6" font-family="sans-serif" font-weight="bold" font-size="14" text-anchor="middle">-</text>
                <text x="140" y="65" fill="#F97316" font-family="sans-serif" font-weight="bold" font-size="14" text-anchor="middle">+</text>
            </svg>
            </div>
            """, unsafe_allow_html=True)
            st.write("El **colector** es un anillo segmentado de láminas de cobre (delgas) conectadas a las bobinas del rotor. Actúa como un inversor/rectificador mecánico.")
            st.write("Las **escobillas** son piezas de grafito que frotan contra el colector giratorio, siendo el enlace eléctrico entre la fuente exterior y el rotor.")
            
            with st.expander("🔄 Proceso de Rectificación (Conmutación)", expanded=True):
                st.write("""
                La **conmutación** es el proceso mediante el cual se invierte el sentido de la corriente en una bobina del inducido en el momento en que esta pasa de la influencia de un polo magnético a la del siguiente.
                """)
                st.markdown("**¿Por qué es necesaria?**")
                st.write("""
                Si la corriente en una bobina mantuviera siempre el mismo sentido mientras el rotor gira, al pasar de un polo Norte a un polo Sur, la fuerza de Lorentz sobre ella invertiría su dirección, haciendo que el par fuera alterno y el motor vibrara sin llegar a girar.
                """)
                st.markdown("**Mecánica del proceso:**")
                st.markdown("""
                1.  **Giro del rotor:** A medida que el inducido gira, las delgas del colector se desplazan bajo las escobillas fijas.
                2.  **Cortocircuito momentáneo:** Cuando una escobilla toca dos delgas simultáneamente, la bobina conectada a ellas queda en cortocircuito. Este instante debe coincidir con la **Zona Neutra** (donde la inducción es mínima) para evitar chispas.
                3.  **Inversión de corriente:** Al seguir girando, la bobina se conecta a la fuente con la polaridad invertida respecto a antes del cortocircuito.
                """)
                st.info("💡 **Resultado:** Gracias a esta 'rectificación mecánica', la corriente en los conductores bajo un polo determinado siempre circula en el mismo sentido, garantizando un **par motor unidireccional y continuo**.")

    with tab_ecuaciones:
        st.markdown("### Ecuaciones Fundamentales en Régimen Permanente")
        st.write("El comportamiento de un motor DC puede modelarse con un circuito eléctrico equivalente sencillo que consta de una fuente de tensión, la resistencia de armadura y la FCEM.")
        
        col_eq_text, col_eq_img = st.columns([1.1, 1])
        with col_eq_text:
            st.latex(r"V = E + I_a \cdot R_a \quad \text{(1. Ecuacion de Tension)}")
            st.latex(r"E = K \cdot \Phi \cdot \omega \quad \text{(2. Fuerza Contraelectromotriz)}")
            st.latex(r"M = K \cdot \Phi \cdot I_a \quad \text{(3. Par Electromagnetico)}")
            
            st.markdown(r"""
            * **$V$**: Tensión en bornes de la red (V).
            * **$I_a$**: Corriente de armadura (A).
            * **$R_a$**: Resistencia rotórica ($\Omega$).
            * **$E$**: Fuerza Contraelectromotriz (V).
            * **$\Phi$**: Flujo magnético por polo (Wb).
            * **$\omega$**: Velocidad mecánica (rad/s).
            * **$M$**: Par interno (N·m).
            """)
            
        with col_eq_img:
            st.markdown("""
            <div style="background-color: #080808; padding: 20px; border-radius: 12px; border: 1px solid #1A1A1A; display: flex; justify-content: center; align-items: center; height: 100%;">
            <svg width="100%" height="220" viewBox="0 0 400 220" xmlns="http://www.w3.org/2000/svg">
              <style>
                .circ-line { fill: none; stroke: #00ADB5; stroke-width: 2.5; stroke-linecap: round; stroke-linejoin: round; }
                .circ-coil { fill: none; stroke: #00ADB5; stroke-width: 2.5; stroke-linecap: round; stroke-linejoin: round; }
                .circ-text { fill: #E5E7EB; font-family: 'Inter', sans-serif; font-size: 14px; }
                .circ-node { fill: #080808; stroke: #00ADB5; stroke-width: 2.5; }
                .circ-brush { fill: #00ADB5; }
              </style>

              <!-- CIRCUITO EXCITACIÓN -->
              <circle cx="80" cy="160" r="5" class="circ-node"/>
              <text x="80" y="185" class="circ-text" text-anchor="middle" font-weight="bold">+</text>
              
              <path d="M 80 155 L 80 60 L 110 60" class="circ-line"/>
              <text x="55" y="55" class="circ-text">E1</text>

              <path d="M 110 60 Q 117.5 30 125 60 T 140 60 T 155 60 T 170 60" class="circ-coil"/>

              <path d="M 170 60 L 200 60 L 200 155" class="circ-line"/>
              <text x="210" y="55" class="circ-text">E2</text>

              <circle cx="200" cy="160" r="5" class="circ-node"/>
              <text x="200" y="185" class="circ-text" text-anchor="middle" font-weight="bold">-</text>

              <!-- CIRCUITO INDUCIDO -->
              <circle cx="300" cy="110" r="22" class="circ-line"/>
              <rect x="294" y="84" width="12" height="4" class="circ-brush"/>
              <rect x="294" y="132" width="12" height="4" class="circ-brush"/>

              <path d="M 300 84 L 300 40 L 350 40" class="circ-line"/>
              <text x="315" y="55" class="circ-text">A1</text>

              <circle cx="355" cy="40" r="5" class="circ-node"/>
              <text x="375" y="45" class="circ-text" font-weight="bold">+</text>

              <path d="M 300 136 L 300 180 L 350 180" class="circ-line"/>
              <text x="315" y="170" class="circ-text">A2</text>

              <circle cx="355" cy="180" r="5" class="circ-node"/>
              <text x="375" y="185" class="circ-text" font-weight="bold">-</text>

              <text x="200" y="210" class="circ-text" text-anchor="middle" fill="#9CA3AF">a) Excitación independiente</text>
            </svg>
            </div>
            """, unsafe_allow_html=True)
        
        st.markdown("---")
        st.markdown("### Balance de Potencias")
        st.write("""
        El estudio del flujo de potencia en un motor de corriente continua permite entender cómo se degrada la energía eléctrica absorbida hasta convertirse en energía mecánica útil en el eje. A continuación, se ilustra el diagrama de flujo energético y las partes del motor donde se produce cada transformación o pérdida:
        """)
        
        st.markdown("""
        <div style="background-color: #080808; padding: 20px; border-radius: 12px; border: 1px solid #1A1A1A; margin-bottom: 20px; display: flex; justify-content: center; align-items: center; width: 100%;">
        <svg width="100%" height="200" viewBox="0 0 600 200" xmlns="http://www.w3.org/2000/svg">
            <style>
                .box { fill: #161B22; stroke: #30363D; stroke-width: 2; rx: 8; ry: 8; }
                .box-text { fill: #E6EDF3; font-family: 'Inter', sans-serif; font-size: 15px; font-weight: 600; text-anchor: middle; }
                .sub-text { fill: #8B949E; font-family: 'Inter', sans-serif; font-size: 11px; text-anchor: middle; }
                .arrow { stroke: #00ADB5; stroke-width: 3; fill: none; stroke-linecap: round; stroke-linejoin: round; }
                .arrow-head { fill: #00ADB5; }
                .loss-arrow { stroke: #EF4444; stroke-width: 3; fill: none; stroke-linecap: round; stroke-linejoin: round; stroke-dasharray: 4,4; }
                .loss-head { fill: #EF4444; }
                .loss-text { fill: #EF4444; font-family: 'Inter', sans-serif; font-size: 12px; font-weight: 600; text-anchor: middle; }
                .part-text { fill: #06B6D4; font-family: 'Inter', sans-serif; font-size: 11px; font-style: italic; text-anchor: middle; }
            </style>
            <!-- P_abs -->
            <rect x="20" y="40" width="120" height="70" class="box" />
            <text x="80" y="65" class="box-text">P_abs</text>
            <text x="80" y="82" class="sub-text">Pot. Eléctrica</text>
            <text x="80" y="100" class="part-text">(Bornes)</text>
            <!-- Arrow 1 -->
            <path d="M 140 75 L 220 75" class="arrow" />
            <polygon points="220,70 230,75 220,80" class="arrow-head" />
            <!-- Loss Cu -->
            <path d="M 180 75 L 180 145" class="loss-arrow" />
            <polygon points="175,145 180,155 185,145" class="loss-head" />
            <text x="180" y="170" class="loss-text">P_Cu (Joule)</text>
            <text x="180" y="185" class="loss-text" style="font-size:10px; fill:#9CA3AF;">(Devanados)</text>
            <!-- P_mi -->
            <rect x="240" y="40" width="120" height="70" class="box" />
            <text x="300" y="65" class="box-text">P_mi</text>
            <text x="300" y="82" class="sub-text">Pot. Interna</text>
            <text x="300" y="100" class="part-text">(Entrehierro)</text>
            <!-- Arrow 2 -->
            <path d="M 360 75 L 440 75" class="arrow" />
            <polygon points="440,70 450,75 440,80" class="arrow-head" />
            <!-- Loss Rot -->
            <path d="M 400 75 L 400 145" class="loss-arrow" />
            <polygon points="395,145 400,155 405,145" class="loss-head" />
            <text x="400" y="170" class="loss-text">P_rot (Mec/Fe)</text>
            <text x="400" y="185" class="loss-text" style="font-size:10px; fill:#9CA3AF;">(Núcleo/Cojinetes)</text>
            <!-- P_u -->
            <rect x="460" y="40" width="120" height="70" class="box" style="stroke: #10B981;" />
            <text x="520" y="65" class="box-text" style="fill: #10B981;">P_u</text>
            <text x="520" y="82" class="sub-text">Pot. Mecánica</text>
            <text x="520" y="100" class="part-text" style="fill: #10B981;">(Eje del Motor)</text>
        </svg>
        </div>
        """, unsafe_allow_html=True)
        
        with st.expander("📊 Ver Análisis de Flujo de Potencia", expanded=True):
            st.markdown("**1. Potencia Eléctrica Absorbida ($P_{abs}$)**")
            st.write("Es la potencia total que el motor demanda de la red eléctrica:")
            st.latex(r"P_{abs} = V \cdot I_{total}")
            st.caption("Donde $I_{total}$ es la suma de la corriente de inducido y de excitación (según el tipo de conexión).")
            
            st.markdown("**2. Pérdidas Eléctricas (Efecto Joule)**")
            st.write("Energía disipada en forma de calor en los devanados de cobre debido a su resistencia interna:")
            st.latex(r"P_{Cu,a} = R_a \cdot I_a^2 \quad \text{(Perdidas en el inducido)}")
            st.latex(r"P_{Cu,exc} = R_{exc} \cdot I_{exc}^2 \quad \text{(Perdidas en la excitacion)}")
            
            st.markdown("**3. Potencia Electromagnética o Interna ($P_{mi}$)**")
            st.write("Es la potencia que efectivamente se convierte de eléctrica a mecánica en el entrehierro de la máquina:")
            st.latex(r"P_{mi} = E \cdot I_a = M \cdot \omega")
            st.info("Esta potencia representa el 'puente' entre el dominio eléctrico ($E, I_a$) y el dominio mecánico ($M, \omega$).")
            
            st.markdown("**4. Pérdidas Rotacionales ($P_{rot}$)**")
            st.write("Engloban las pérdidas en el hierro ($P_{Fe}$) por histéresis y corrientes parásitas, y las pérdidas mecánicas ($P_{mec}$) por rozamiento en cojinetes, escobillas y resistencia del aire (ventilación):")
            st.latex(r"P_{rot} = P_{Fe} + P_{mec}")
            
            st.markdown("**5. Potencia Útil ($P_u$)**")
            st.write("Es la potencia mecánica final que entrega el eje a la carga conectada:")
            st.latex(r"P_u = P_{mi} - P_{rot}")
            
            st.markdown("**6. Rendimiento ($\eta$)**")
            st.write("Indica la eficiencia global de la conversión energética:")
            st.latex(r"\eta (\%) = \frac{P_u}{P_{abs}} \cdot 100")

            st.success(r"**Diagrama de Flujo Energético:** $P_{abs} \xrightarrow{-P_{Cu}} P_{mi} \xrightarrow{-P_{rot}} P_u$")

    with tab_tipos:
        st.markdown("### Tipos de Excitación")
        st.write(r"El comportamiento del motor DC cambia radicalmente dependiendo de cómo se interconectan el circuito del inductor (que crea $\Phi$) y el circuito del inducido (por donde circula $I_a$).")
        
        c1, c2 = st.columns(2)
        with c1:
            st.markdown("#### Excitación Independiente")
            st.write("""
            En este tipo de motor, el devanado de excitación (estator) y el devanado del inducido (rotor) se alimentan mediante fuentes de corriente continua **totalmente separadas e independientes**.
            """)
            
            with st.expander("🔍 Ver Análisis Detallado", expanded=True):
                st.markdown("**Configuración del Circuito:**")
                st.write("""
                Al no existir conexión eléctrica entre ambos circuitos, la corriente de excitación ($I_{exc}$) no se ve afectada por las variaciones de la corriente de carga en el inducido ($I_a$). Esto permite un control extremadamente preciso sobre el flujo magnético ($\Phi$).
                """)
                
                st.latex(r"V_{exc} = R_{exc} \cdot I_{exc}")
                st.latex(r"V_a = E + I_a \cdot R_a")
                
                st.markdown("**Características Principales:**")
                st.markdown("""
                *   **Linealidad Elevada:** Es el motor con el comportamiento más lineal. Si mantenemos el flujo constante, el par es directamente proporcional a la corriente de inducido y la caída de velocidad es mínima.
                *   **Control de Velocidad Flexible:** Podemos variar la velocidad desde cero hasta el valor nominal variando $V_a$, y subir por encima del valor nominal reduciendo $I_{exc}$ (debilitamiento de campo).
                *   **Estabilidad:** No hay riesgo de embalamiento ante variaciones de carga bruscas (siempre que se mantenga la excitación).
                """)
                
                st.info("⚠️ **Peligro Crítico:** Si el circuito de excitación se interrumpe accidentalmente mientras el inducido está alimentado, el flujo cae a valores residuales muy bajos. Para mantener la FCEM ($E$), el motor intentará acelerar a velocidades extremas para compensar la falta de flujo, pudiendo destruirse mecánicamente (embalamiento).")

            st.markdown("#### Excitación Derivación (Shunt)")
            st.write("El devanado inductor se conecta **en paralelo** con el inducido. La tensión aplicada es la misma para ambos.")
            st.write("Se caracteriza por tener una **velocidad casi constante** independiente de la carga. Ideal para cintas transportadoras y máquinas herramienta.")

        with c2:
            st.markdown("#### Excitación Serie")
            st.write("El devanado inductor se conecta **en serie** con el inducido, de modo que $I_{exc} = I_a$.")
            st.write("Proporciona un **par de arranque extraordinariamente alto** (el par crece con el cuadrado de la corriente). Es el clásico motor de **tracción** ferroviaria y tranvías. ¡Cuidado! Si pierde la carga mecánica, se 'embala' a velocidades destructivas.")
            
            st.markdown("#### Excitación Compuesta (Compound)")
            st.write("Combina devanados serie y derivación para intentar sumar las ventajas de ambos: buen par de arranque sin el peligro de embalamiento.")

    with tab_curvas:
        st.markdown("### Curva Par-Velocidad y Control")
        st.write(r"Si despejamos $\omega$ de las ecuaciones fundamentales e introducimos el par $M$, encontramos la relación directa entre la velocidad y el par mecánico:")
        
        st.latex(r"\omega = \frac{V}{K \cdot \Phi} - \frac{R_a}{(K \cdot \Phi)^2} \cdot M")
        
        st.write("En un motor Shunt o de excitación independiente con $\\Phi$ constante, esto define una línea recta con pendiente negativa. Para **controlar la velocidad**, el ingeniero puede actuar sobre tres variables:")
        st.markdown("- **Control por V**: Variar la tensión de entrada. Modifica la velocidad base. Es el método más eficiente (control de armadura).\n- **Control por Flujo ($\\Phi$)**: Debilitar el campo inductor permite alcanzar velocidades más altas (por encima de la nominal) a costa de perder par máximo.\n- **Control por $R_a$**: Añadir resistencias en serie. Método ineficiente usado antiguamente para arranques suaves.")

        st.markdown("---")
        st.markdown("#### Simulador Avanzado de Control de Velocidad")
        
        col_v, col_r, col_phi = st.columns(3)
        with col_v:
            v_in = st.slider("Tensión de Armadura V (V)", 50, 400, 220, step=10)
        with col_r:
            ra_in = st.slider("Resistencia Armadura Ra (Ω)", 0.1, 2.0, 0.5, step=0.1)
        with col_phi:
            flujo_relativo = st.slider("Flujo Inductor (%)", 50, 100, 100, step=5) / 100.0
            
        v_nom, ra_nom, kphi_nom = 220, 0.5, 1.8 
        kphi_actual = kphi_nom * flujo_relativo
        
        m_vec = np.linspace(0, 150, 100)
        
        # Curvas
        omega_nom_vec = (v_nom / kphi_nom) - (ra_nom / (kphi_nom**2)) * m_vec
        rpm_nom_vec = np.maximum(omega_nom_vec * (60 / (2 * math.pi)), 0)
        
        omega_vec = (v_in / kphi_actual) - (ra_in / (kphi_actual**2)) * m_vec
        rpm_vec = np.maximum(omega_vec * (60 / (2 * math.pi)), 0)
        rpm_vacio = (v_in / kphi_actual) * (60 / (2 * math.pi))
        
        # Gráfica minimalista
        fig = go.Figure()
        fig.add_trace(go.Scatter(x=m_vec, y=rpm_nom_vec, mode='lines', line=dict(color='gray', width=2, dash='dash'), name='Nominal (220V, 100%)', hoverinfo='none'))
        fig.add_trace(go.Scatter(x=m_vec, y=rpm_vec, mode='lines', line=dict(color='#00ADB5', width=4), name='Operación Actual'))
        fig.add_trace(go.Scatter(x=[0], y=[rpm_vacio], mode='markers+text', marker=dict(size=12, color='#F9A826'), text=[f'{rpm_vacio:.0f} RPM'], textposition='middle right', showlegend=False, textfont=dict(color='#F9A826', size=13)))
        
        fig.update_layout(
            plot_bgcolor='rgba(0,0,0,0)',
            paper_bgcolor='rgba(0,0,0,0)',
            xaxis=dict(title="Par Electromagnético (N·m)", showgrid=True, gridcolor='#222222', zeroline=True, zerolinecolor='#444'),
            yaxis=dict(title="Velocidad Mecánica (RPM)", showgrid=True, gridcolor='#222222', zeroline=True, zerolinecolor='#444'),
            height=400, margin=dict(l=10, r=10, t=10, b=10),
            legend=dict(yanchor="top", y=0.99, xanchor="right", x=0.99, bgcolor="rgba(0,0,0,0.5)")
        )
        st.plotly_chart(fig, use_container_width=True)
        
        with st.expander("📌 Análisis Físico de los Parámetros", expanded=True):
            st.markdown(r"""
            * **Control por Tensión ($V$):** Al modificar $V$, la curva se desplaza de forma paralela. Es el método ideal porque cambia la velocidad sin perder par máximo ni eficiencia térmica.
            * **Control por Flujo ($\Phi$):** Reducir el flujo ("debilitamiento de campo") eleva drásticamente la velocidad de vacío, pero la curva "cae" mucho más rápido al aplicar carga mecánica. Se usa sólo para superar la velocidad nominal a costa de perder par.
            * **Control por Resistencia ($R_a$):** Aumentar $R_a$ no cambia la velocidad de vacío, pero hace que la pendiente se desplome (la velocidad se hunde con la carga). Es un método muy ineficiente debido al calor disipado.
            """)

    with tab_arranque:
        st.markdown("### El Arranque en Motores de CC")
        st.write("""
        El arranque es un régimen transitorio crítico en los motores de corriente continua. Debido a la ausencia de fuerza contraelectromotriz inicial, el motor puede comportarse prácticamente como un cortocircuito si no se toman medidas.
        """)
        
        col_arr1, col_arr2 = st.columns(2)
        with col_arr1:
            st.markdown("#### El Problema: Corriente de Arranque Elevada")
            st.write("""
            En el instante del arranque ($t=0$), la velocidad es nula ($\omega = 0$), lo que implica que la FCEM también lo es ($E = 0$). La ecuación de tensión se reduce a:
            """)
            st.latex(r"I_{arr} = \frac{V}{R_a}")
            st.warning("Dado que la resistencia de armadura ($R_a$) es deliberadamente muy pequeña para maximizar la eficiencia, la corriente de arranque puede llegar a ser entre 10 y 50 veces la corriente nominal, dañando el colector, las escobillas y provocando caídas de tensión en la red.")
            
        with col_arr2:
            st.markdown("#### La Solución: Reóstato de Arranque")
            st.write("""
            Para limitar esta corriente a valores seguros (típicamente entre $1.5$ y $2.5$ veces la $I_{nom}$), se intercala una resistencia variable en serie con el inducido, denominada **reóstato de arranque** ($R_{arr}$).
            """)
            st.latex(r"I_a = \frac{V - E}{R_a + R_{arr}}")
            st.info("A medida que el motor gana velocidad y aumenta la $E$, el reóstato se va eliminando por escalones hasta que el motor queda conectado directamente a la red.")

        st.markdown("---")
        st.markdown("#### Proceso de Arranque por Pasos")
        st.markdown("""
        1.  **Excitación Máxima:** Siempre se debe asegurar que el campo inductor esté a su valor máximo antes de alimentar el inducido para generar el mayor par de arranque posible y que la FCEM crezca rápidamente.
        2.  **Inserción de $R_{arr}$:** El reóstato debe estar en su posición de máxima resistencia.
        3.  **Conexión al inducido:** Se aplica la tensión nominal al conjunto rotor + reóstato.
        4.  **Corte de escalones:** A medida que la velocidad sube, la corriente baja. En ese momento se retira un escalón de resistencia para mantener la corriente en niveles que permitan seguir acelerando con buen par.
        """)

    with tab_cuadrantes:
        st.markdown("### Los Cuatro Cuadrantes de Funcionamiento")
        st.write("""
        Un sistema de accionamiento eléctrico completo debe ser capaz de operar en cualquier combinación de velocidad y par. Estos estados se representan en un plano cartesiano (Par vs Velocidad) dividido en cuatro cuadrantes principales.
        """)
        
        # Representación visual de los cuadrantes
        st.markdown("#### Mapa de Operación")
        col_c1, col_c2 = st.columns(2)
        with col_c1:
            st.info("""
            **Cuadrante I: Motor Directo**
            *   **Velocidad:** (+) / **Par:** (+)
            *   **Estado:** La máquina consume energía para girar hacia adelante y mover la carga.
            *   **Ejemplo:** Un vehículo acelerando en llano.
            """)
            st.success("""
            **Cuadrante IV: Freno Inverso**
            *   **Velocidad:** (-) / **Par:** (+)
            *   **Estado:** La máquina gira hacia atrás pero el par se opone al giro, frenándola.
            *   **Ejemplo:** Frenado regenerativo al retroceder.
            """)
            
        with col_c2:
            st.error("""
            **Cuadrante II: Freno Directo**
            *   **Velocidad:** (+) / **Par:** (-)
            *   **Estado:** La máquina gira hacia adelante pero el par es opuesto (actúa como generador).
            *   **Ejemplo:** Un vehículo bajando una pendiente usando el motor como freno.
            """)
            st.warning("""
            **Cuadrante III: Motor Inverso**
            *   **Velocidad:** (-) / **Par:** (-)
            *   **Estado:** La máquina consume energía para girar hacia atrás y mover la carga.
            *   **Ejemplo:** Marcha atrás activa de un vehículo eléctrico.
            """)

        st.markdown("---")
        st.markdown("#### Flujo de Potencia y Control")
        st.write("""
        El signo de la potencia mecánica ($P = M \cdot \omega$) es la clave para distinguir los regímenes:
        *   **Motor (Cuadrantes I y III):** Potencia positiva ($P > 0$). El sistema extrae energía eléctrica de la red para realizar trabajo mecánico.
        *   **Freno/Generador (Cuadrantes II y IV):** Potencia negativa ($P < 0$). La carga entrega energía mecánica al motor, que la convierte en eléctrica (pudiendo devolverla a la red o disiparla en resistencias).
        """)
        
        with st.expander("🔌 Implementación Electrónica: Puente en H", expanded=True):
            st.write("""
            Para operar en los 4 cuadrantes, se requiere un convertidor capaz de invertir tanto la tensión media ($V$) como el sentido de la corriente de inducido ($I_a$). 
            
            El **Puente en H** es la topología estándar: mediante el control de 4 interruptores estáticos (MOSFETs/IGBTs), se puede aplicar tensión en ambos sentidos y permitir que la corriente fluya bidireccionalmente, logrando el control total sobre la velocidad y el par en cualquier situación de carga.
            """)
            
        st.markdown("#### Simulador: Punto de Operación 4 Cuadrantes")
        
        # Controles minimalistas arriba
        c_sim1, c_sim2 = st.columns(2)
        with c_sim1:
            sel_w = st.slider("Velocidad Angular $\omega$ (%)", -100, 100, 50, step=5)
        with c_sim2:
            sel_m = st.slider("Par Electromagnético $M$ (%)", -100, 100, 40, step=5)
            
        # Lógica de estados
        p_mec = sel_w * sel_m
        if sel_w >= 0 and sel_m >= 0: 
            quad_num = "I"
            quad_name = "Motor Directo"
            color_res = "#00ADB5"
            desc = "La máquina extrae energía para mover la carga en sentido de avance."
        elif sel_w >= 0 and sel_m < 0: 
            quad_num = "II"
            quad_name = "Freno Directo (Regenerativo)"
            color_res = "#FF4B4B"
            desc = "La máquina frena el avance de la carga, actuando como generador."
        elif sel_w < 0 and sel_m < 0: 
            quad_num = "III"
            quad_name = "Motor Inverso"
            color_res = "#00ADB5"
            desc = "La máquina extrae energía para mover la carga en sentido de retroceso."
        else: 
            quad_num = "IV"
            quad_name = "Freno Inverso (Regenerativo)"
            color_res = "#FF4B4B"
            desc = "La máquina frena el retroceso de la carga, actuando como generador."

        # Distribución inferior: Métricas y Gráfica
        col_res, col_plot = st.columns([1, 1.8])
        
        with col_res:
            st.markdown(f"<div style='margin-top: 25px; margin-bottom: 5px; font-size: 13px; color: #9CA3AF;'>Estado Actual</div>", unsafe_allow_html=True)
            st.markdown(f"<h2 style='color: {color_res}; margin-top: 0px;'>Cuadrante {quad_num}</h2>", unsafe_allow_html=True)
            st.markdown(f"**{quad_name}**")
            
            st.metric("Potencia Mecánica", f"{p_mec} W", delta="Generando (Freno)" if p_mec < 0 else "Consumiendo (Motor)", delta_color="inverse")
            st.info(desc)
            
        with col_plot:
            fig_q = go.Figure()
            
            # Colores de fondo sutiles para cuadrantes
            fig_q.add_shape(type="rect", x0=0, y0=0, x1=110, y1=110, fillcolor="rgba(0, 173, 181, 0.05)", line_width=0)
            fig_q.add_shape(type="rect", x0=0, y0=0, x1=110, y1=-110, fillcolor="rgba(255, 75, 75, 0.05)", line_width=0)
            fig_q.add_shape(type="rect", x0=0, y0=0, x1=-110, y1=-110, fillcolor="rgba(0, 173, 181, 0.05)", line_width=0)
            fig_q.add_shape(type="rect", x0=0, y0=0, x1=-110, y1=110, fillcolor="rgba(255, 75, 75, 0.05)", line_width=0)
            
            # Ejes
            fig_q.add_vline(x=0, line_width=2, line_color="#333")
            fig_q.add_hline(y=0, line_width=2, line_color="#333")
            
            # Anotaciones
            fig_q.add_annotation(x=55, y=90, text="Q1<br>MOTOR", showarrow=False, font=dict(color="#00ADB5", size=16), opacity=0.4)
            fig_q.add_annotation(x=55, y=-90, text="Q2<br>FRENO", showarrow=False, font=dict(color="#FF4B4B", size=16), opacity=0.4)
            fig_q.add_annotation(x=-55, y=-90, text="Q3<br>MOTOR", showarrow=False, font=dict(color="#00ADB5", size=16), opacity=0.4)
            fig_q.add_annotation(x=-55, y=90, text="Q4<br>FRENO", showarrow=False, font=dict(color="#FF4B4B", size=16), opacity=0.4)

            # Punto de operación
            fig_q.add_trace(go.Scatter(
                x=[sel_w], y=[sel_m], 
                mode='markers+text', 
                marker=dict(size=18, color=color_res, symbol="circle", line=dict(color='white', width=2)),
                text=["Operación"],
                textposition="top center",
                textfont=dict(color="white", size=13),
                name="Punto"
            ))
            
            # Líneas guía de rastreo
            fig_q.add_trace(go.Scatter(x=[sel_w, sel_w], y=[0, sel_m], mode='lines', line=dict(color=color_res, width=1.5, dash='dot'), hoverinfo='none', showlegend=False))
            fig_q.add_trace(go.Scatter(x=[0, sel_w], y=[sel_m, sel_m], mode='lines', line=dict(color=color_res, width=1.5, dash='dot'), hoverinfo='none', showlegend=False))

            fig_q.update_layout(
                plot_bgcolor='rgba(0,0,0,0)',
                paper_bgcolor='rgba(0,0,0,0)',
                xaxis_title="Velocidad Angular $\omega$ (%)",
                yaxis_title="Par Electromagnético $M$ (%)",
                xaxis=dict(range=[-110, 110], showgrid=True, gridcolor='#222', zeroline=False),
                yaxis=dict(range=[-110, 110], showgrid=True, gridcolor='#222', zeroline=False),
                height=400, margin=dict(l=10, r=10, t=10, b=10),
                showlegend=False
            )
            st.plotly_chart(fig_q, use_container_width=True)

if __name__ == "__main__":
    app()
