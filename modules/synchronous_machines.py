import streamlit as st
import streamlit.components.v1 as components
import numpy as np
import plotly.graph_objects as go
import math

def app():
    st.header("Máquinas Síncronas (Alternadores y Motores)")
    st.caption("Análisis de la máquina síncrona: principios de doble excitación, funcionamiento como generador y como motor de velocidad constante.")

    tab_fundamentos, tab_circuito, tab_fasores, tab_control, tab_comparativa, tab_behn, tab_potier = st.tabs([
        "1 - Fundamentos",
        "2 - Circuito Equivalente",
        "3 - Diagramas Fasoriales",
        "4 - Control y Estabilidad",
        "5 - Síncrona vs Asíncrona",
        "6 - Behn-Eschenburg (Régimen Lineal)",
        "7 - Método de Potier"
    ])

    # --------------------------------------------------------------------------
    # PESTAÑA 1: FUNDAMENTOS
    # --------------------------------------------------------------------------
    with tab_fundamentos:
        st.markdown("### Principio de Funcionamiento: La Doble Excitación")
        st.write(
            "La máquina síncrona se distingue de todas las demás por requerir **dos alimentaciones independientes** "
            "para operar: una alterna trifásica en el estator y una de corriente continua en el rotor. "
            "Esta característica le otorga una capacidad única: controlar activamente tanto la potencia activa "
            "como la reactiva intercambiada con la red eléctrica."
        )

        st.info(
            "**Distribución de alimentación según el tamaño de la máquina:**\n\n"
            "- **Máquinas de gran potencia (construcción estándar):** Se inyecta corriente continua (CC) en el rotor "
            "(bobinas inductoras móviles) y corriente alterna (CA) en el estator (bobinas inducidas fijas). "
            "Esto facilita el aislamiento de las altas tensiones generadas o consumidas en la parte estática y "
            "evita el desgaste de escobillas al transferir grandes potencias.\n"
            "- **Máquinas de pequeña potencia:** En ocasiones se emplea la configuración inversa (bobinas inductoras de CC "
            "en el estator y devanado inducido de CA en el rotor), o bien se emplean imanes permanentes en el rotor, "
            "simplificando mecánicamente la máquina al eliminar la necesidad de contactos deslizantes."
        )

        SYNC_ANIMATION_HTML = """
        <!DOCTYPE html>
        <html>
        <head>
        <style>
          *{margin:0;padding:0;box-sizing:border-box}
          body{background:#0d1117;display:flex;justify-content:center;align-items:flex-start;font-family:'Segoe UI',-apple-system,sans-serif;color:#c9d1d9}
          .wrap{display:flex;flex-wrap:wrap;justify-content:center;align-items:center;gap:36px;padding:18px 10px}
          canvas{border-radius:10px;border:1px solid #21262d;box-shadow:0 8px 32px rgba(0,0,0,.6)}
          .leg{max-width:300px;font-size:12.5px;line-height:1.65}
          .leg h3{color:#f0f6fc;font-size:16px;font-weight:600;margin-bottom:14px;padding-bottom:10px;border-bottom:1px solid #21262d;letter-spacing:.3px}
          .leg .row{display:flex;align-items:baseline;gap:10px;margin-bottom:11px}
          .leg .d{width:10px;height:10px;border-radius:50%;flex-shrink:0;margin-top:3px}
          .leg .lb{font-weight:600}
          .leg hr{border:0;border-top:1px solid #21262d;margin:13px 0}
          .leg .note{background:#161b22;border:1px solid #21262d;border-radius:6px;padding:9px 12px;font-size:11.5px;color:#8b949e;text-align:center;margin-top:10px;font-family:'Consolas','Courier New',monospace}
        </style>
        </head>
        <body>
        <div class="wrap">
        <canvas id="cv" width="480" height="480"></canvas>
        <div class="leg">
          <h3>Principio de la Máquina Síncrona</h3>
          <div class="row"><div class="d" style="background:#f47067"></div><div><span class="lb" style="color:#f47067">Fase R / R'</span> — Corriente alterna trifásica.</div></div>
          <div class="row"><div class="d" style="background:#b392f0"></div><div><span class="lb" style="color:#b392f0">Fase S / S'</span> — Desfase 120°.</div></div>
          <div class="row"><div class="d" style="background:#58a6ff"></div><div><span class="lb" style="color:#58a6ff">Fase T / T'</span> — Desfase 240°.</div></div>
          <hr>
          <div class="row"><div class="d" style="background:#79c0ff"></div><div><span class="lb" style="color:#79c0ff">B<sub>estator</sub></span> — Campo magnético giratorio (Ferraris). Líneas de flujo azules en el entrehierro.</div></div>
          <div class="row"><div class="d" style="background:#f47067"></div><div><span class="lb" style="color:#f47067">B<sub>rotor</sub></span> — Campo del electroimán CC. Líneas de flujo rojas ancladas a los polos N-S.</div></div>
          <hr>
          <div class="row"><div class="d" style="background:#e3b341"></div><div><span class="lb" style="color:#e3b341">Bobinas CC</span> — Excitación del rotor con corriente continua I<sub>exc</sub>.</div></div>
          <div class="note">&delta; &asymp; 25&deg; &middot; Régimen motor &middot; n = n<sub>s</sub></div>
        </div>
        </div>
        <script>
        const cv=document.getElementById('cv'),c=cv.getContext('2d');
        const W=cv.width,H=cv.height,cx=W/2,cy=H/2;
        const Ro=200,Ri=168,Rr=118,Rs=15;
        const DELTA=25*Math.PI/180,SPD=0.9;

        const PH=[
          {n:'R', a:-Math.PI/2,              rgb:[244,112,103]},
          {n:"R'",a: Math.PI/2,              rgb:[244,112,103]},
          {n:'S', a:-Math.PI/2+2.094,        rgb:[179,146,240]},
          {n:"S'",a: Math.PI/2+2.094,        rgb:[179,146,240]},
          {n:'T', a:-Math.PI/2+4.189,        rgb:[88,166,255]},
          {n:"T'",a: Math.PI/2+4.189,        rgb:[88,166,255]},
        ];
        const PO={R:0,S:2.094,T:4.189};

        /* ---- helpers ---- */
        function arrow(x1,y1,x2,y2,col,w,h){
          const dx=x2-x1,dy=y2-y1,l=Math.hypot(dx,dy),ux=dx/l,uy=dy/l;
          c.save();c.strokeStyle=col;c.lineWidth=w;c.lineCap='round';
          c.beginPath();c.moveTo(x1,y1);c.lineTo(x2-ux*h*.6,y2-uy*h*.6);c.stroke();
          c.fillStyle=col;c.beginPath();c.moveTo(x2,y2);
          c.lineTo(x2-ux*h-uy*h*.38,y2-uy*h+ux*h*.38);
          c.lineTo(x2-ux*h+uy*h*.38,y2-uy*h-ux*h*.38);
          c.closePath();c.fill();c.restore();
        }

        /* Magnetic flux arc in the air gap: draws a curved line from
           angle a1 (near rotor) to a2 (near stator inner wall).
           The curve bows outward for a realistic field-line shape. */
        function fluxArc(a1,a2,r1,r2,col,alpha,dashOff){
          const x1=Math.cos(a1)*r1,y1=Math.sin(a1)*r1;
          const x2=Math.cos(a2)*r2,y2=Math.sin(a2)*r2;
          const mx=(x1+x2)/2,my=(y1+y2)/2;
          const len=Math.hypot(x2-x1,y2-y1);
          // perpendicular bulge
          const nx=-(y2-y1)/len,ny=(x2-x1)/len;
          const bulge=len*0.35;
          const cpx=mx+nx*bulge,cpy=my+ny*bulge;
          c.save();c.translate(cx,cy);
          c.globalAlpha=alpha;c.strokeStyle=col;c.lineWidth=1.4;
          c.setLineDash([6,5]);c.lineDashOffset=dashOff;
          c.beginPath();c.moveTo(x1,y1);c.quadraticCurveTo(cpx,cpy,x2,y2);c.stroke();
          c.setLineDash([]);c.globalAlpha=1;c.restore();
        }

        /* ---- main loop ---- */
        let t=0;
        function draw(){
          t+=0.016;
          const sA=SPD*t, rA=sA-DELTA;
          c.clearRect(0,0,W,H);

          // bg with subtle radial vignette
          const bg=c.createRadialGradient(cx,cy,80,cx,cy,cx+40);
          bg.addColorStop(0,'#0d1117');bg.addColorStop(1,'#080b10');
          c.fillStyle=bg;c.fillRect(0,0,W,H);

          /* === STATOR IRON === */
          // outer ring with gradient
          const sg=c.createRadialGradient(cx,cy,Ri,cx,cy,Ro);
          sg.addColorStop(0,'#1c2128');sg.addColorStop(1,'#161b22');
          c.beginPath();c.arc(cx,cy,Ro,0,6.283);c.fillStyle=sg;c.fill();
          c.strokeStyle='#30363d';c.lineWidth=1.5;c.stroke();
          // inner bore
          c.beginPath();c.arc(cx,cy,Ri,0,6.283);c.fillStyle='#0d1117';c.fill();
          c.strokeStyle='#30363d';c.lineWidth=1.5;c.stroke();

          // teeth marks
          for(let i=0;i<36;i++){
            const a=i*0.1745;
            c.strokeStyle='#30363d';c.lineWidth=1;
            c.beginPath();
            c.moveTo(cx+Math.cos(a)*Ri,cy+Math.sin(a)*Ri);
            c.lineTo(cx+Math.cos(a)*(Ri+7),cy+Math.sin(a)*(Ri+7));
            c.stroke();
          }

          /* === PHASE COILS (pulsating) === */
          for(const p of PH){
            const base=p.n.replace("'",""),off=PO[base];
            const prime=p.n.includes("'");
            const cur=Math.sin(sA*2-off);
            const I=prime?-cur:cur;
            const bri=0.15+0.85*Math.max(0,I);
            const [r,g,b]=p.rgb;
            const px=cx+Math.cos(p.a)*((Ri+Ro)/2);
            const py=cy+Math.sin(p.a)*((Ri+Ro)/2);
            // glow halo
            if(bri>0.25){
              const gl=c.createRadialGradient(px,py,0,px,py,16);
              gl.addColorStop(0,`rgba(${r},${g},${b},${bri*0.5})`);
              gl.addColorStop(1,`rgba(${r},${g},${b},0)`);
              c.fillStyle=gl;c.beginPath();c.arc(px,py,16,0,6.283);c.fill();
            }
            // coil body
            c.beginPath();c.arc(px,py,10,0,6.283);
            c.fillStyle=`rgba(${r},${g},${b},${bri})`;c.fill();
            c.strokeStyle=`rgba(${r},${g},${b},.9)`;c.lineWidth=1.5;c.stroke();
            // dot / cross
            if(I>0.12){c.fillStyle='#0d1117';c.beginPath();c.arc(px,py,2.5,0,6.283);c.fill();}
            else if(I<-0.12){c.strokeStyle='#0d1117';c.lineWidth=2;c.lineCap='round';
              c.beginPath();c.moveTo(px-3.5,py-3.5);c.lineTo(px+3.5,py+3.5);c.stroke();
              c.beginPath();c.moveTo(px+3.5,py-3.5);c.lineTo(px-3.5,py+3.5);c.stroke();}
            // label
            c.fillStyle='#484f58';c.font='500 11px sans-serif';c.textAlign='center';c.textBaseline='middle';
            c.fillText(p.n,cx+Math.cos(p.a)*(Ro+15),cy+Math.sin(p.a)*(Ro+15));
          }

          /* === AIR-GAP FLUX LINES (animated) === */
          // Rotor flux: radial lines from N-pole to stator, and stator to S-pole
          const nLines=8;
          const dashSpeed=-t*50;
          for(let i=0;i<nLines;i++){
            // N-pole hemisphere: lines fan out from N-pole cap
            const spread=0.55; // angular spread in radians from pole axis
            const frac=(i/(nLines-1)-0.5)*2; // -1..1
            const aRot=rA-Math.PI/2+frac*spread; // angle near N pole on rotor
            const aSta=rA-Math.PI/2+frac*spread*1.4; // slightly wider at stator
            fluxArc(aRot,aSta,Rr+4,Ri-4,'#f47067',0.35+0.15*Math.sin(t*3+i),dashSpeed);
            // S-pole hemisphere: lines come back
            const aRotS=rA+Math.PI/2+frac*spread;
            const aStaS=rA+Math.PI/2+frac*spread*1.4;
            fluxArc(aStaS,aRotS,Ri-4,Rr+4,'#f47067',0.35+0.15*Math.sin(t*3+i+1),-dashSpeed);
          }
          // Stator resultant field flux: lines aligned with stator field angle
          for(let i=0;i<nLines;i++){
            const spread=0.5;
            const frac=(i/(nLines-1)-0.5)*2;
            const aInner=sA-Math.PI/2+frac*spread;
            const aOuter=sA-Math.PI/2+frac*spread*1.3;
            fluxArc(aInner,aOuter,Ri-4,Ri+18,'#79c0ff',0.2+0.1*Math.sin(t*2.5+i),dashSpeed*0.7);
            const aInner2=sA+Math.PI/2+frac*spread;
            const aOuter2=sA+Math.PI/2+frac*spread*1.3;
            fluxArc(aOuter2,aInner2,Ri+18,Ri-4,'#79c0ff',0.2+0.1*Math.sin(t*2.5+i+1),-dashSpeed*0.7);
          }

          /* === ROTOR === */
          c.save();c.translate(cx,cy);c.rotate(rA);
          // core
          c.beginPath();c.arc(0,0,Rr-28,0,6.283);
          const rc=c.createRadialGradient(0,0,0,0,0,Rr-28);
          rc.addColorStop(0,'#1c2128');rc.addColorStop(1,'#161b22');
          c.fillStyle=rc;c.fill();c.strokeStyle='#30363d';c.lineWidth=1.5;c.stroke();
          // N pole
          c.beginPath();c.moveTo(-30,-32);c.lineTo(-24,-Rr);c.lineTo(24,-Rr);c.lineTo(30,-32);c.closePath();
          c.fillStyle='#21262d';c.fill();c.strokeStyle='#30363d';c.lineWidth=1.5;c.stroke();
          // S pole
          c.beginPath();c.moveTo(-30,32);c.lineTo(-24,Rr);c.lineTo(24,Rr);c.lineTo(30,32);c.closePath();
          c.fillStyle='#21262d';c.fill();c.strokeStyle='#30363d';c.lineWidth=1.5;c.stroke();
          // CC coils
          c.strokeStyle='#e3b341';c.lineWidth=3;c.lineCap='round';
          for(let i=0;i<5;i++){
            let y=-40-i*11;c.beginPath();c.moveTo(-22,y);c.lineTo(22,y);c.stroke();
            y=40+i*11;   c.beginPath();c.moveTo(-22,y);c.lineTo(22,y);c.stroke();
          }
          // I_exc arrows
          c.globalAlpha=0.7;
          arrow(-26,-38,-26,-86,'#e3b341',1.5,7);arrow(26,-86,26,-38,'#e3b341',1.5,7);
          c.globalAlpha=1;
          c.fillStyle='#e3b341';c.font='600 10px sans-serif';c.textAlign='center';c.textBaseline='middle';
          c.fillText('Iexc',0,-Rr-11);
          // N / S
          c.fillStyle='#e6edf3';c.font='bold 20px sans-serif';
          c.fillText('N',0,-Rr+16);c.fillText('S',0,Rr-16);
          // shaft
          c.beginPath();c.arc(0,0,Rs,0,6.283);
          const sh=c.createRadialGradient(0,0,0,0,0,Rs);
          sh.addColorStop(0,'#8b949e');sh.addColorStop(1,'#484f58');
          c.fillStyle=sh;c.fill();c.strokeStyle='#21262d';c.lineWidth=2;c.stroke();
          c.beginPath();c.arc(0,0,4,0,6.283);c.fillStyle='#0d1117';c.fill();
          c.restore();

          /* === FIELD VECTORS === */
          const bsL=140,brL=110;
          const bsX=cx+Math.cos(sA-Math.PI/2)*bsL,bsY=cy+Math.sin(sA-Math.PI/2)*bsL;
          const brX=cx+Math.cos(rA-Math.PI/2)*brL,brY=cy+Math.sin(rA-Math.PI/2)*brL;
          // vector trails (subtle glow)
          c.save();
          const tg1=c.createLinearGradient(cx,cy,bsX,bsY);
          tg1.addColorStop(0,'rgba(121,192,255,0)');tg1.addColorStop(1,'rgba(121,192,255,.25)');
          c.strokeStyle=tg1;c.lineWidth=8;c.lineCap='round';
          c.beginPath();c.moveTo(cx,cy);c.lineTo(bsX,bsY);c.stroke();
          const tg2=c.createLinearGradient(cx,cy,brX,brY);
          tg2.addColorStop(0,'rgba(244,112,103,0)');tg2.addColorStop(1,'rgba(244,112,103,.25)');
          c.strokeStyle=tg2;c.lineWidth=8;
          c.beginPath();c.moveTo(cx,cy);c.lineTo(brX,brY);c.stroke();
          c.restore();
          // arrows
          arrow(cx,cy,bsX,bsY,'#79c0ff',3,12);
          arrow(cx,cy,brX,brY,'#f47067',3,12);

          // delta arc
          c.beginPath();c.arc(cx,cy,52,sA-Math.PI/2,rA-Math.PI/2,true);
          c.strokeStyle='#e3b341';c.lineWidth=1.5;c.setLineDash([3,3]);c.stroke();c.setLineDash([]);
          const mA=(sA+rA)/2-Math.PI/2;
          c.fillStyle='#e3b341';c.font='italic 14px serif';c.textAlign='center';c.textBaseline='middle';
          c.fillText('δ',cx+Math.cos(mA)*66,cy+Math.sin(mA)*66);

          // vector labels
          c.font='600 12px sans-serif';
          c.fillStyle='#79c0ff';c.fillText('Best',cx+Math.cos(sA-Math.PI/2)*(bsL+16),cy+Math.sin(sA-Math.PI/2)*(bsL+16));
          c.fillStyle='#f47067';c.fillText('Brot',cx+Math.cos(rA-Math.PI/2)*(brL+16),cy+Math.sin(rA-Math.PI/2)*(brL+16));

          requestAnimationFrame(draw);
        }
        draw();
        </script>
        </body>
        </html>
        """
        components.html(SYNC_ANIMATION_HTML, height=520)

        with st.expander("Paso a Paso: Desde la Excitación del Rotor hasta el Giro o la Generación", expanded=True):
            st.markdown(r"""
            Comprender la máquina síncrona requiere seguir meticulosamente la cadena de fenómenos físicos
            que la gobiernan, desde la inyección de energía hasta la rotación o la generación de electricidad.
            
            **1. Excitación del Rotor con Corriente Continua**
            
            El proceso comienza en el **rotor** (también llamado inductor o polo). A través de anillos rozantes
            y escobillas, se inyecta una corriente continua $I_{exc}$ en el devanado de campo enrollado sobre él.
            Esta corriente genera un **campo magnético de intensidad controlable**, cuyas líneas de fuerza salen
            por el polo Norte del rotor y entran por el polo Sur, cruzando el entrehierro.
            
            $$\Phi_{rotor} \propto I_{exc}$$
            
            A diferencia de la máquina asíncrona (cuyo rotor recibe energía por inducción),
            aquí el flujo rotórico es **externo, regulable y de corriente continua**: el eje del electroimán
            está fijo respecto al rotor físico.
            
            ---
            
            **2. El Estator Crea un Campo Magnético Giratorio**
            
            Simultáneamente, los devanados trifásicos del estator (también denominado armadura o inducido)
            se alimentan con un sistema equilibrado de corrientes alternas a frecuencia $f$ de la red.
            Por el **Teorema de Ferraris**, la superposición vectorial de los tres campos pulsantes creados
            por las bobinas desfasadas 120° genera un **único campo magnético de módulo constante que gira**
            a la velocidad de sincronismo:
            
            $$n_s = \frac{60 \cdot f}{p} \quad \text{[rpm]}$$
            
            donde $p$ es el número de pares de polos del estator. Este campo giratorio invisible actúa como
            un imán que rota con exacta regularidad dentro de la máquina.
            
            ---
            
            **3. Acoplamiento Magnético y Arrastre al Sincronismo**
            
            El campo giratorio del estator atrae magnéticamente al rotor (electroimán de CC).
            La interacción entre ambos campos —el del rotor fijo respecto al eje y el del estator en
            rotación— crea un **par de enganche o par síncrono** que arrastra al rotor intentando
            alinearlo con el campo de estator.
            
            Si se aplica una carga mecánica moderada en el eje, el rotor no llega a alinearse perfectamente:
            queda rezagado un **ángulo de carga $\delta$** (llamado también ángulo de par o ángulo de potencia)
            respecto a la posición del campo giratorio. Mientras exista este desfase, el par electromagnético
            compensa el par resistente de la carga y el rotor gira **exactamente a $n_s$**.
            
            > **Clave del sincronismo:** En régimen permanente el rotor gira solidario con el campo del
            > estator — ni más lento, ni más rápido. No existe deslizamiento ($s = 0$). Cualquier variación
            > de carga se absorbe variando $\delta$, **nunca la velocidad**.
            
            ---
            
            **4. Funcionamiento como Motor Síncrono**
            
            Cuando la máquina está conectada a una red de tensión fija $U_1$ y se le acopla una **carga mecánica**
            en el eje (bomba, compresor, ventilador, etc.), actúa como motor:
            
            - La red impone $U_1$ y la frecuencia $f$ → el campo del estator gira a $n_s$.
            - El rotor, enganchado magnéticamente, gira también a $n_s$ con un ángulo de retraso $\delta > 0$.
            - Cuanto mayor sea la carga mecánica exigida, mayor será $\delta$, pero la velocidad permanece constante.
            - La potencia activa absorbida de la red aumenta con $\delta$:
            
            $$P_{motor} = \frac{3 \cdot U_1 \cdot E_0}{X_s} \cdot \sin(\delta)$$
            
            El motor síncrono es ideal cuando se necesita **velocidad absolutamente constante** independientemente
            de la carga (relojes industriales, máquinas de papel, laminadores de precisión).
            
            ---
            
            **5. Funcionamiento como Generador Síncrono (Alternador)**
            
            Si en lugar de carga mecánica resistente se **inyecta par motor en el eje** (mediante una turbina
            de vapor, hidráulica, de gas, o un motor Diesel), la máquina opera como **generador**:
            
            - La turbina arrastra el rotor a $n_s$ (impuesto mecánicamente).
            - El flujo del rotor excitado, al girar, corta los conductores del estator y por la **Ley de Faraday**
              induce una fuerza electromotriz (f.e.m.) trifásica alterna de valor:
            
            $$E_0 = K \cdot \Phi_{exc} \cdot n_s$$
            
            - Si $E_0$ es mayor que la tensión de red $U_1$ (sobreexcitación), la máquina inyecta
              potencia activa **y** reactiva capacitiva a la red.
            - Regulando $I_{exc}$ (y por tanto $E_0$) y el par de la turbina (ángulo $\delta$), el operador
              controla independientemente la potencia activa y reactiva entregada a la red.
            
            > En los grandes alternadores de central eléctrica, la frecuencia de la red eléctrica nacional
            > está determinada colectivamente por la velocidad de sincronismo de **todos** los generadores
            > conectados en paralelo.
            
            ---
            
            **6. Resultado Final: La Gran Ventaja de la Máquina Síncrona**
            
            La regulación independiente de $I_{exc}$ permite controlar el **factor de potencia** de la instalación:
            sobreexcitando, la máquina genera reactiva (actúa como condensador); subexcitando, la consume
            (actúa como bobina). Esto la convierte en el elemento de control de tensión por excelencia en
            los sistemas eléctricos de potencia.
            """)
            st.success(
                "**Resultado Final:** Una misma máquina puede, según cómo se excite y se acople mecánicamente, "
                "transformar energía eléctrica en mecánica (motor) o mecánica en eléctrica (generador), "
                "siempre girando a la velocidad de sincronismo exacta impuesta por la frecuencia de la red."
            )

        st.markdown("---")
        st.markdown("### Estados del Motor: Régimen en Vacío vs Régimen de Carga")
        st.markdown(
            "Para comprender profundamente cómo un motor síncrono intercambia energía mecánico-eléctrica, es necesario "
            "estudiar sus dos estados fundamentales y entender dos conceptos magnéticos clave:\n\n"
            "- **f.m.m. (Fuerza Magnetomotriz - $\\mathcal{F}$):** Es la \"fuerza\" o impulso magnético creado por las corrientes "
            "circulando por los devanados, análoga a la tensión eléctrica pero en el circuito magnético. En la máquina interactúan "
            "la f.m.m. del estator (debida a la CA) y la f.m.m. del rotor (debida a la CC).\n"
            "- **f.e.m. (Fuerza Electromotriz - $E_0$):** Es el voltaje interno generado (inducido) en las bobinas del estator "
            "por el barrido del campo magnético del rotor rotando a $n_s$. Esta f.e.m. se opone vectorial y casi directamente "
            "a la tensión de alimentación de la red ($V$)."
        )
        
        col_vac, col_car = st.columns(2)
        
        with col_vac:
            st.markdown("#### 1. Régimen en Vacío (Sin Carga)")
            st.markdown(
                "El motor gira a la velocidad de sincronismo ($n_s$) sin tener que arrastrar ninguna carga mecánica (par resistente nulo). "
                "Los ejes magnéticos (f.m.m.) del rotor y del estator están prácticamente alineados.\n\n"
                "- El **ángulo de carga ($\delta$)** es cero (o infinitesimal, solo para vencer fricciones mecánicas internas).\n"
                "- La f.e.m. interna ($E_0$) inducida por el rotor se encuentra casi exactamente superpuesta al vector de tensión de red ($V$).\n"
                "- Al no existir apenas diferencia fasorial vectorial, la corriente absorbida es ínfima."
            )
            
            fig_vac = go.Figure()
            fig_vac.add_annotation(x=0, y=1, ax=0, ay=0, xref='x', yref='y', axref='x', ayref='y', showarrow=True, arrowhead=3, arrowsize=1, arrowwidth=3, arrowcolor="#58a6ff")
            fig_vac.add_annotation(x=0, y=1.1, text="<b>V</b> (Tensión Red)", showarrow=False, font=dict(color="#58a6ff", size=13))
            
            fig_vac.add_annotation(x=0.03, y=0.90, ax=0, ay=0, xref='x', yref='y', axref='x', ayref='y', showarrow=True, arrowhead=3, arrowsize=1, arrowwidth=3, arrowcolor="#f47067")
            fig_vac.add_annotation(x=0.18, y=0.90, text="<b>E<sub>0</sub></b> (f.e.m.)", showarrow=False, font=dict(color="#f47067", size=13))
            
            fig_vac.update_layout(
                xaxis=dict(range=[-0.5, 0.5], showgrid=False, zeroline=True, zerolinecolor="#30363d", showticklabels=False),
                yaxis=dict(range=[-0.1, 1.25], showgrid=False, zeroline=True, zerolinecolor="#30363d", showticklabels=False),
                plot_bgcolor="rgba(0,0,0,0)", paper_bgcolor="rgba(0,0,0,0)",
                height=260, margin=dict(l=10, r=10, t=10, b=10)
            )
            st.plotly_chart(fig_vac, use_container_width=True)

        with col_car:
            st.markdown("#### 2. Régimen de Carga")
            st.markdown(
                "Al acoplar una carga mecánica en el eje, el rotor físico sufre una resistencia. Para seguir girando a $n_s$, "
                "los polos del rotor \"ceden\" y se retrasan geométricamente respecto al campo giratorio del estator.\n\n"
                "- Se genera un **ángulo de carga ($\delta$) > 0**.\n"
                "- Este retraso mecánico provoca que el vector de la f.e.m. ($E_0$) se atrase $\delta$ grados eléctricos respecto a $V$.\n"
                "- Esta desalineación geométrica produce una caída de tensión fasorial, obligando al estator a absorber "
                "la corriente activa necesaria para generar el par electromagnético."
            )
            
            fig_car = go.Figure()
            fig_car.add_annotation(x=0, y=1, ax=0, ay=0, xref='x', yref='y', axref='x', ayref='y', showarrow=True, arrowhead=3, arrowsize=1, arrowwidth=3, arrowcolor="#58a6ff")
            fig_car.add_annotation(x=0, y=1.1, text="<b>V</b> (Tensión Red)", showarrow=False, font=dict(color="#58a6ff", size=13))
            
            delta_rad = math.radians(35)
            e0_x = 0.90 * math.sin(delta_rad)
            e0_y = 0.90 * math.cos(delta_rad)
            fig_car.add_annotation(x=e0_x, y=e0_y, ax=0, ay=0, xref='x', yref='y', axref='x', ayref='y', showarrow=True, arrowhead=3, arrowsize=1, arrowwidth=3, arrowcolor="#f47067")
            fig_car.add_annotation(x=e0_x*1.2, y=e0_y*1.05, text="<b>E<sub>0</sub></b>", showarrow=False, font=dict(color="#f47067", size=13))
            
            # Arco del ángulo delta
            fig_car.add_shape(type="path", path=f"M 0 0.4 A 0.4 0.4 0 0 0 {0.4*math.sin(delta_rad)} {0.4*math.cos(delta_rad)}", line=dict(color="#8b949e", dash="dash", width=1.5))
            fig_car.add_annotation(x=0.15, y=0.45, text="<b>δ</b>", showarrow=False, font=dict(color="#8b949e", size=14))
            
            fig_car.update_layout(
                xaxis=dict(range=[-0.2, 0.8], showgrid=False, zeroline=True, zerolinecolor="#30363d", showticklabels=False),
                yaxis=dict(range=[-0.1, 1.25], showgrid=False, zeroline=True, zerolinecolor="#30363d", showticklabels=False),
                plot_bgcolor="rgba(0,0,0,0)", paper_bgcolor="rgba(0,0,0,0)",
                height=260, margin=dict(l=10, r=10, t=10, b=10)
            )
            st.plotly_chart(fig_car, use_container_width=True)

        st.markdown("---")
        st.markdown("### El Problema del Arranque del Motor Síncrono")
        with st.expander("Método de Arranque como Motor Asíncrono (Jaula de Amortiguamiento)", expanded=True):
            st.markdown(r"""
            El mayor defecto mecánico del motor síncrono es que **no tiene par de arranque propio** si se conecta directamente a la frecuencia nominal de la red (50 o 60 Hz). 
            
            Si conectamos el estator directamente a la red, el campo magnético giratorio arrancará casi instantáneamente a $n_s$ (p.ej., 3000 rpm). El rotor físico, que pesa toneladas y tiene muchísima inercia, no tiene tiempo material de engancharse a los polos de ese "tren bala" magnético. Sufrirá tirones brutales alternos hacia adelante y hacia atrás, vibrará violentamente, pero su velocidad neta será cero.
            
            #### La Solución Brillante: El Arranque Asíncrono
            Para solucionar esto sin acoplar un motor auxiliar externo, los ingenieros insertan barras gruesas de cobre o latón en las caras de los polos del rotor, y las cortocircuitan en sus extremos con anillos metálicos. Físicamente, le incrustan una **jaula de ardilla** (idéntica a la de los motores asíncronos), conocida como *jaula de amortiguamiento* o *devanado amortiguador*.
            
            El procedimiento de arranque se realiza en 3 fases exactas:
            
            1. **Arranque Asíncrono (El Empuje Inicial):**
               - El circuito de excitación de CC del rotor se mantiene **apagado** (desconectado o en cortocircuito a través de una resistencia de descarga para evitar altos voltajes inducidos).
               - Se conecta la alimentación trifásica de CA al estator.
               - El campo giratorio del estator barre las barras de la jaula de amortiguamiento, induciendo potentes corrientes en ellas (Ley de Faraday).
               - Estas corrientes generan un campo magnético que interactúa con el estator, creando un **par de arranque asíncrono**.
               - El rotor, pesadamente, empieza a acelerar exactamente como si fuera un motor asíncrono industrial de jaula de ardilla.
               
            2. **Aproximación al Sincronismo:**
               - Sabemos que un motor asíncrono jamás puede alcanzar físicamente $n_s$, porque necesita deslizamiento ($s > 0$) para inducir corriente. El motor acelera hasta quedarse "rozando" la velocidad síncrona (por ejemplo, alcanza el 95% o 97% de $n_s$).
               
            3. **El Enganche Final (Sincronización):**
               - En este preciso instante, cuando el rotor ya persigue muy de cerca al campo del estator, **se enciende la excitación de corriente continua** ($I_{exc}$).
               - Los polos de hierro del rotor se convierten de golpe en potentes electroimanes fijos.
               - Dado que el diferencial de velocidad (deslizamiento) ya es muy pequeño, la atracción de los polos opuestos es suficiente para dar un último tirón mecánico. El rotor **se engancha magnéticamente** al campo del estator.
               - Ahora gira exactamente a $n_s$. Al no haber deslizamiento ($s=0$), la jaula de amortiguamiento deja de "ver" variaciones de flujo magnético y no se induce más corriente en ella. El motor pasa a comportarse de manera 100% síncrona.
            
            *El Doble Propósito:* Esta jaula de amortiguamiento se deja instalada de por vida. Además del arranque, actúa como "amortiguador mecánico" (Damper) durante la marcha normal: si un bache en la red hace oscilar bruscamente el ángulo $\delta$, la oscilación de velocidad hace que el campo barra ligeramente la jaula, induciendo un par que frena y amortigua la oscilación, estabilizando el rotor de inmediato.
            """)

        st.markdown("---")
        st.markdown("### Cinemática: Velocidad Síncrona")
        col_v1, col_v2 = st.columns(2)
        with col_v1:
            st.markdown("#### Velocidad de Sincronismo")
            st.latex(r"n_s = \frac{60 \cdot f}{p} \quad \text{[rpm]}")
            st.write(
                "El rotor está magnéticamente 'enganchado' al campo giratorio del estator. "
                "En régimen permanente, ambos giran exactamente a la misma velocidad: no existe deslizamiento."
            )
            st.info(
                "**Ejemplo:** Para $f = 50$ Hz y $p = 1$ par de polos → $n_s = 3000$ rpm. "
                "Con $p = 2$ pares → $n_s = 1500$ rpm."
            )
        with col_v2:
            st.markdown("#### Doble Excitación")
            st.markdown("""
            * **Estator (Armadura):** Alimentado por corriente alterna trifásica de la red. Crea el campo magnético giratorio.
            * **Rotor (Inductor):** Alimentado por **corriente continua** regulable. Crea un campo magnético fijo respecto al eje del rotor.
            * La interacción entre ambos campos genera el **par electromagnético**.
            * Regulando $I_{exc}$ se controla $E_0$ y con ello el flujo de potencia reactiva con la red.
            """)

    # --------------------------------------------------------------------------
    # PESTAÑA 2: CIRCUITO EQUIVALENTE
    # --------------------------------------------------------------------------
    with tab_circuito:
        st.markdown("### Modelo de la Reactancia Síncrona (Polos Lisos)")
        st.write(
            "Para una máquina de polos lisos (entrehierro uniforme), el circuito equivalente por fase "
            "se reduce a una fuente de f.e.m. interna $E_0$ en serie con la impedancia síncrona "
            "$(R_a + jX_s)$. Habitualmente $R_a \\ll X_s$ y se desprecia:"
        )
        st.latex(r"\vec{U}_1 = \vec{E}_0 - \vec{I}_a \cdot (R_a + jX_s)")

        st.markdown("""
        <div style="background:#0E1117; border:1px solid #2a2a3a; border-radius:10px; padding:10px; display:flex; justify-content:center; margin-bottom: 20px; margin-top: 20px;">
        <svg width="100%" height="200" viewBox="0 0 500 200" xmlns="http://www.w3.org/2000/svg" style="font-family:'monospace',sans-serif;">
          <!-- Fuente E0 -->
          <circle cx="100" cy="100" r="25" fill="none" stroke="#F9A826" stroke-width="2"/>
          <path d="M 85 100 Q 92.5 85, 100 100 T 115 100" fill="none" stroke="#F9A826" stroke-width="2"/>
          <text x="85" y="145" fill="#F9A826" font-size="16" font-weight="bold">E₀</text>
          
          <!-- Cables base -->
          <line x1="100" y1="75" x2="100" y2="50" stroke="#E5E7EB" stroke-width="2"/>
          <line x1="100" y1="50" x2="180" y2="50" stroke="#E5E7EB" stroke-width="2"/>
          <line x1="100" y1="125" x2="100" y2="150" stroke="#E5E7EB" stroke-width="2"/>
          <line x1="100" y1="150" x2="400" y2="150" stroke="#E5E7EB" stroke-width="2"/>
          
          <!-- Resistencia Ra -->
          <path d="M 180 50 L 190 40 L 210 60 L 230 40 L 250 60 L 260 50" fill="none" stroke="#00ADB5" stroke-width="2"/>
          <text x="210" y="30" fill="#00ADB5" font-size="16" font-weight="bold">Rₐ</text>
          
          <line x1="260" y1="50" x2="280" y2="50" stroke="#E5E7EB" stroke-width="2"/>

          <!-- Inductancia Xs -->
          <path d="M 280 50 Q 290 25, 300 50 Q 310 25, 320 50 Q 330 25, 340 50 Q 350 25, 360 50" fill="none" stroke="#FF4B4B" stroke-width="2"/>
          <text x="310" y="30" fill="#FF4B4B" font-size="16" font-weight="bold">jXₛ</text>

          <line x1="360" y1="50" x2="400" y2="50" stroke="#E5E7EB" stroke-width="2"/>

          <!-- Bornes -->
          <circle cx="400" cy="50" r="5" fill="#E5E7EB"/>
          <circle cx="400" cy="150" r="5" fill="#E5E7EB"/>
          <text x="420" y="105" fill="#E5E7EB" font-size="18" font-weight="bold">U₁</text>
          
          <!-- Flecha U1 -->
          <line x1="400" y1="65" x2="400" y2="135" stroke="#E5E7EB" stroke-width="1.5" stroke-dasharray="4"/>
          <polygon points="400,60 396,68 404,68" fill="#E5E7EB"/>
          <polygon points="400,140 396,132 404,132" fill="#E5E7EB"/>

          <!-- Flecha de Corriente Ia -->
          <line x1="120" y1="35" x2="160" y2="35" stroke="#00ADB5" stroke-width="2"/>
          <polygon points="160,35 152,31 152,39" fill="#00ADB5"/>
          <text x="135" y="25" fill="#00ADB5" font-size="16" font-weight="bold">Iₐ</text>
          
          <!-- Caja de Impedancia Sincrona -->
          <rect x="170" y="15" width="200" height="60" fill="none" stroke="#9CA3AF" stroke-width="1" stroke-dasharray="5,5" rx="5"/>
          <text x="270" y="95" fill="#9CA3AF" font-size="12" text-anchor="middle">Impedancia Síncrona Zₛ</text>
        </svg>
        </div>
        """, unsafe_allow_html=True)

        col_c1, col_c2 = st.columns(2)
        with col_c1:
            st.markdown("""
            * **$E_0$** — F.e.m. interna o tensión de vacío inducida por el flujo del rotor. Depende directamente de $I_{exc}$.
            * **$U_1$** — Tensión en bornes de la red (impuesta externamente).
            * **$I_a$** — Corriente de armadura (circula por el estator).
            * **$R_a$** — Resistencia del devanado estatórico (despreciable en máquinas grandes).
            * **$X_s$** — Reactancia síncrona: suma de la reactancia de dispersión del estator y la reactancia de reacción de inducido.
            """)
        with col_c2:
            st.info(
                "La $E_0$ depende directamente de la corriente de excitación ($I_{exc}$). "
                "Aumentar $I_{exc}$ aumenta $E_0$, lo que permite **inyectar o absorber reactiva de la red** "
                "sin cambiar la potencia activa transferida."
            )
            st.markdown("#### Potencia activa transferida (por fase)")
            st.latex(r"P = \frac{U_1 \cdot E_0}{X_s} \cdot \sin(\delta)")
            st.markdown("#### Potencia reactiva generada (por fase)")
            st.latex(r"Q = \frac{U_1 \cdot E_0 \cdot \cos(\delta) - U_1^2}{X_s}")

        st.markdown("---")
        st.markdown("### Operación en Circuito Abierto (Ensayo de Vacío)")
        st.write("¿Qué sucede si hacemos girar la máquina síncrona a su velocidad nominal ($n_s$), excitamos el rotor con corriente continua, pero **no conectamos ninguna carga** a los bornes del estator? Esta disposición se conoce como **funcionamiento en vacío o circuito abierto**.")

        st.markdown("""
        <div style="background:#0E1117; border:1px solid #2a2a3a; border-radius:10px; padding:10px; display:flex; justify-content:center; margin-bottom: 20px; margin-top: 20px;">
        <svg width="100%" height="200" viewBox="0 0 500 200" xmlns="http://www.w3.org/2000/svg" style="font-family:'monospace',sans-serif;">
          <!-- Fuente E0 -->
          <circle cx="100" cy="100" r="25" fill="none" stroke="#F9A826" stroke-width="2"/>
          <path d="M 85 100 Q 92.5 85, 100 100 T 115 100" fill="none" stroke="#F9A826" stroke-width="2"/>
          <text x="85" y="145" fill="#F9A826" font-size="16" font-weight="bold">E₀</text>
          
          <!-- Cables -->
          <line x1="100" y1="75" x2="100" y2="50" stroke="#E5E7EB" stroke-width="2"/>
          <line x1="100" y1="50" x2="180" y2="50" stroke="#E5E7EB" stroke-width="2"/>
          <line x1="100" y1="125" x2="100" y2="150" stroke="#E5E7EB" stroke-width="2"/>
          <line x1="100" y1="150" x2="400" y2="150" stroke="#E5E7EB" stroke-width="2"/>
          
          <!-- Impedancia (Block simple) -->
          <rect x="180" y="40" width="180" height="20" fill="none" stroke="#9CA3AF" stroke-width="2"/>
          <text x="270" y="55" fill="#9CA3AF" font-size="14" text-anchor="middle">Zₛ = Rₐ + jXₛ</text>
          
          <line x1="360" y1="50" x2="400" y2="50" stroke="#E5E7EB" stroke-width="2"/>

          <!-- Bornes Abiertos -->
          <circle cx="400" cy="50" r="5" fill="#E5E7EB"/>
          <circle cx="400" cy="150" r="5" fill="#E5E7EB"/>
          
          <!-- I = 0 -->
          <text x="270" y="30" fill="#FF4B4B" font-size="16" font-weight="bold" text-anchor="middle">Iₐ = 0 A</text>

          <!-- Voltimetro -->
          <line x1="400" y1="50" x2="460" y2="50" stroke="#E5E7EB" stroke-width="1.5" stroke-dasharray="4"/>
          <line x1="400" y1="150" x2="460" y2="150" stroke="#E5E7EB" stroke-width="1.5" stroke-dasharray="4"/>
          <line x1="460" y1="50" x2="460" y2="80" stroke="#E5E7EB" stroke-width="1.5" stroke-dasharray="4"/>
          <line x1="460" y1="150" x2="460" y2="120" stroke="#E5E7EB" stroke-width="1.5" stroke-dasharray="4"/>
          
          <circle cx="460" cy="100" r="20" fill="none" stroke="#00ADB5" stroke-width="2"/>
          <text x="460" y="105" fill="#00ADB5" font-size="16" font-weight="bold" text-anchor="middle">V</text>
          <text x="415" y="105" fill="#F9A826" font-size="16" font-weight="bold">U₁ = E₀</text>
        </svg>
        </div>
        """, unsafe_allow_html=True)

        col_vacio1, col_vacio2 = st.columns(2)
        with col_vacio1:
            st.markdown("#### Análisis del Circuito")
            st.markdown(r"""
            Al estar los bornes del estator desconectados, el circuito eléctrico está físicamente abierto. Por tanto, es imposible que circule corriente por la armadura:
            $$I_a = 0 \text{ A}$$
            
            Si aplicamos la ecuación fundamental del circuito equivalente:
            $$\vec{U}_1 = \vec{E}_0 - \vec{I}_a (R_a + jX_s)$$
            
            Al sustituir $I_a = 0$, el término de caída de tensión desaparece completamente, y llegamos a la conclusión clave del circuito abierto:
            $$\vec{U}_1 = \vec{E}_0$$
            """)
            st.info("**Conclusión Física:** En circuito abierto, la tensión que medimos en los bornes del generador ($U_1$) es **exactamente igual** a la fuerza electromotriz (F.E.M.) interna inducida por el rotor ($E_0$).")

        with col_vacio2:
            st.markdown("#### ¿Para qué sirve esta disposición?")
            st.markdown(r"""
            El ensayo de circuito abierto (o ensayo de vacío) es **fundamental** para conocer la "huella dactilar" magnética de la máquina. Su propósito principal es obtener la **Curva de Vacío o Característica de Magnetización**.
            
            1. **Determinar la Saturación Magnética:** A medida que aumentamos la corriente de excitación del rotor ($I_{exc}$), el flujo ($\Phi$) aumenta proporcionalmente. Sin embargo, el núcleo de hierro de la máquina tiene un límite. Llegará un momento en que el hierro se "satura" y, aunque inyectemos mucha más $I_{exc}$, la tensión $E_0$ apenas subirá.
            2. **Calcular la Reactancia Síncrona ($X_s$):** Junto con el "Ensayo de Cortocircuito", el ensayo de vacío es imprescindible para calcular matemáticamente el valor de $X_s$ de la máquina.
            3. **Sincronización:** Es el estado previo y necesario antes de acoplar un generador a la red nacional. Se acelera la turbina hasta $n_s$ y se ajusta la $I_{exc}$ en circuito abierto hasta que $E_0$ iguale exactamente la tensión de la red.
            """)

        with st.expander("Base Matemática: La Curva de Magnetización", expanded=True):
            st.write("La relación entre la f.e.m. generada y el flujo magnético obedece a la Ley de Faraday. Para una máquina síncrona, el valor eficaz de la tensión de fase generada es:")
            st.latex(r"E_0 = 4.44 \cdot f \cdot N_{fase} \cdot k_w \cdot \Phi_{rotor}")
            st.markdown(r"""
            Donde:
            * **$f$**: Frecuencia eléctrica (proporcional a la velocidad de giro).
            * **$N_{fase}$**: Número de espiras en serie por fase del estator.
            * **$k_w$**: Factor de devanado (corrige el hecho de que las bobinas están distribuidas y acortadas).
            * **$\Phi_{rotor}$**: Flujo magnético por polo.
            
            Dado que la máquina gira a velocidad constante ($f$ es constante), todos los términos son fijos excepto el flujo. Por tanto:
            $$E_0 = K \cdot \Phi_{rotor}$$
            
            Como el flujo $\Phi_{rotor}$ es creado por la fuerza magnetomotriz del rotor ($F_e = N_{exc} \cdot I_{exc}$), la curva $E_0$ vs $I_{exc}$ nos dibuja exactamente la curva de magnetización del hierro, mostrando la zona lineal inicial y el codo de saturación.
            """)

        st.markdown("---")
        st.markdown("### Ensayo de Cortocircuito y Obtención de la Impedancia Síncrona ($Z_s$)")
        st.write("Ya sabemos qué pasa si dejamos los bornes abiertos. ¿Pero qué ocurre si los unimos entre sí con un cable de resistencia casi nula mientras la máquina gira a $n_s$? Esto es el **ensayo de cortocircuito**.")
        
        st.markdown("""
        <div style="background:#0E1117; border:1px solid #2a2a3a; border-radius:10px; padding:10px; display:flex; justify-content:center; margin-bottom: 20px; margin-top: 20px;">
        <svg width="100%" height="200" viewBox="0 0 500 200" xmlns="http://www.w3.org/2000/svg" style="font-family:'monospace',sans-serif;">
          <!-- Fuente E0 -->
          <circle cx="100" cy="100" r="25" fill="none" stroke="#F9A826" stroke-width="2"/>
          <path d="M 85 100 Q 92.5 85, 100 100 T 115 100" fill="none" stroke="#F9A826" stroke-width="2"/>
          <text x="85" y="145" fill="#F9A826" font-size="16" font-weight="bold">E₀</text>
          
          <!-- Cables -->
          <line x1="100" y1="75" x2="100" y2="50" stroke="#E5E7EB" stroke-width="2"/>
          <line x1="100" y1="50" x2="180" y2="50" stroke="#E5E7EB" stroke-width="2"/>
          <line x1="100" y1="125" x2="100" y2="150" stroke="#E5E7EB" stroke-width="2"/>
          <line x1="100" y1="150" x2="400" y2="150" stroke="#E5E7EB" stroke-width="2"/>
          
          <!-- Impedancia -->
          <rect x="180" y="40" width="180" height="20" fill="none" stroke="#9CA3AF" stroke-width="2"/>
          <text x="270" y="55" fill="#9CA3AF" font-size="14" text-anchor="middle">Zₛ = Rₐ + jXₛ</text>
          
          <line x1="360" y1="50" x2="400" y2="50" stroke="#E5E7EB" stroke-width="2"/>

          <!-- Bornes -->
          <circle cx="400" cy="50" r="5" fill="#E5E7EB"/>
          <circle cx="400" cy="150" r="5" fill="#E5E7EB"/>
          
          <!-- Cortocircuito (Amperímetro) -->
          <line x1="400" y1="50" x2="400" y2="80" stroke="#FF4B4B" stroke-width="3"/>
          <line x1="400" y1="150" x2="400" y2="120" stroke="#FF4B4B" stroke-width="3"/>
          
          <circle cx="400" cy="100" r="20" fill="none" stroke="#FF4B4B" stroke-width="2"/>
          <text x="400" y="105" fill="#FF4B4B" font-size="16" font-weight="bold" text-anchor="middle">A</text>
          
          <!-- Flecha Icc -->
          <line x1="420" y1="65" x2="420" y2="135" stroke="#FF4B4B" stroke-width="2"/>
          <polygon points="420,135 416,127 424,127" fill="#FF4B4B"/>
          <text x="430" y="105" fill="#FF4B4B" font-size="16" font-weight="bold">I_cc</text>

          <!-- U = 0 -->
          <text x="345" y="105" fill="#E5E7EB" font-size="16" font-weight="bold">U₁ = 0 V</text>
        </svg>
        </div>
        """, unsafe_allow_html=True)

        col_cc1, col_cc2 = st.columns(2)
        with col_cc1:
            st.markdown("#### Análisis del Cortocircuito")
            st.markdown(r"""
            Al cortocircuitar los bornes, la tensión a la salida se vuelve cero por definición física:
            $$\vec{U}_1 = 0 \text{ V}$$
            
            Si volvemos a aplicar la ecuación fundamental del circuito equivalente ($\vec{U}_1 = \vec{E}_0 - \vec{I}_{cc} \cdot Z_s$):
            $$0 = \vec{E}_0 - \vec{I}_{cc} \cdot (R_a + jX_s)$$
            
            Despejando la corriente de cortocircuito ($\vec{I}_{cc}$), obtenemos:
            $$\vec{I}_{cc} = \frac{\vec{E}_0}{R_a + jX_s} = \frac{\vec{E}_0}{\vec{Z}_s}$$
            """)
            st.info("**Seguridad Experimental:** En un cortocircuito a máxima excitación, $\vec{I}_{cc}$ derretiría la máquina. Por eso, el ensayo se hace partiendo de una excitación del rotor ($I_{exc}$) nula, subiéndola muy poco a poco hasta que el amperímetro del estator marque la corriente nominal de seguridad ($I_N$).")

        with col_cc2:
            st.markdown("#### La Impedancia Síncrona ($Z_s$)")
            st.markdown(r"""
            La Impedancia Síncrona ($\vec{Z}_s$) es la resistencia total al paso de corriente alterna que presenta el interior del generador. Combina la resistencia pura del cobre de las bobinas ($R_a$) y la reactancia magnética global ($X_s$).
            
            **Obtención experimental conjunta:**
            Gracias a la combinación de los dos ensayos (vacío y cortocircuito), calcular el módulo de la impedancia síncrona es matemáticamente directo. Para un mismo valor de corriente de excitación ($I_{exc}$):
            1. Anotamos la tensión generada en vacío ($E_0$).
            2. Anotamos la corriente que circula en cortocircuito ($I_{cc}$).
            3. Aplicamos la Ley de Ohm generalizada:
            
            $$Z_s = \frac{E_0 \text{ (f.e.m. de vacío)}}{I_{cc} \text{ (corriente de cortocircuito)}}$$
            """)

        with st.expander("Base Matemática: Separación de R_a y X_s", expanded=True):
            st.markdown(r"""
            Una vez obtenido el valor del módulo total de la impedancia síncrona ($Z_s$), necesitamos separar sus dos componentes ortogonales para construir el circuito equivalente exacto:
            $$Z_s = \sqrt{R_a^2 + X_s^2}$$
            
            1. **Medida de $R_a$:** La resistencia del devanado inducido se mide en corriente continua (inyectando CC entre bornes con el motor parado). Este valor se multiplica por un factor empírico para contemplar el "efecto pelicular" (efecto Kelvin) en corriente alterna, obteniendo su valor real en operación (usualmente de 1.2 a 1.5 veces mayor).
            2. **Cálculo final de $X_s$:** Teniendo $Z_s$ de los ensayos combinados y $R_a$ de la medición óhmica, la reactancia síncrona se despeja aplicando el Teorema de Pitágoras:
            $$X_s = \sqrt{Z_s^2 - R_a^2}$$
            
            💡 *Nota de Ingeniería:* En alternadores comerciales de gran potencia (centrales eléctricas), el cableado es tan grueso (poca $R_a$) y los campos magnéticos tan inmensos (mucha $X_s$), que $X_s$ suele ser entre 10 y 100 veces más grande que $R_a$. Por eso, en cálculos rápidos de ingeniería, es muy común asumir que $R_a \approx 0$ y, por tanto, **$Z_s \approx X_s$**.
            """)

        st.markdown("---")
        st.markdown("### Reactancia Síncrona ($X_s$): Componentes")
        with st.expander("Desglose físico de la Reactancia Síncrona", expanded=True):
            st.markdown(r"""
            La reactancia síncrona $X_s$ engloba dos fenómenos físicos distintos que en la práctica
            resulta muy difícil separar experimentalmente:
            
            **1. Reactancia de Dispersión del Estator ($X_\sigma$)**
            
            Una fracción del flujo generado por la corriente del estator no cruza el entrehierro
            para enlazar con el rotor, sino que se "dispersa" por los propios dientes y cabezas de bobina
            del estator. Este flujo de dispersión genera una tensión adicional proporcional a la derivada
            de la corriente, que se modela como una reactancia en serie.
            
            **2. Reactancia de Reacción de Inducido ($X_a$)**
            
            Cuando la corriente $I_a$ circula por el devanado estatórico, crea su propio campo magnético
            en el entrehierro (la "reacción de inducido"). Este campo se superpone al campo del rotor,
            modificando el flujo resultante en el entrehierro y, por tanto, la f.e.m. inducida. Esta
            interacción se modela como una reactancia adicional en serie.
            
            $$X_s = X_\sigma + X_a$$
            
            En máquinas de polos salientes, la reacción de inducido es anisótropa y requiere descomponerse
            en los ejes d y q (modelo de Park), resultando en dos reactancias distintas: $X_d$ (eje directo)
            y $X_q$ (eje en cuadratura), siendo siempre $X_d > X_q$.
            """)

        st.markdown("---")
        st.markdown("### El Efecto de la Reacción del Inducido y su Compensación")
        with st.expander("Profundizando en la Reacción de Inducido y el Regulador AVR", expanded=True):
            st.markdown(r"""
            La **Reacción del Inducido** es el fenómeno electromagnético más crítico que afecta a la tensión de salida de un generador síncrono.
            
            #### ¿Qué es físicamente?
            En vacío, el único campo magnético que existe es el del rotor ($F_e$). Sin embargo, en cuanto conectas una carga (una fábrica, una ciudad), empieza a circular la corriente trifásica $I_a$ por las bobinas del estator (inducido). 
            Por la Ley de Ampère, esta corriente crea **su propio campo magnético giratorio** ($F_i$). 
            
            La máquina pasa a tener dos campos interactuando en el mismo espacio. El campo del estator ($F_i$) "choca" o interactúa con el campo del rotor ($F_e$), deformándolo, debilitándolo o fortaleciéndolo. A esta alteración del flujo original se le llama **Reacción del Inducido**.
            
            #### El efecto según el tipo de carga
            Dependiendo del factor de potencia ($\cos\varphi$) de la carga, el efecto es diametralmente distinto:
            1. **Carga Inductiva ($\varphi > 0$, retraso):** El campo del estator se opone casi directamente al campo del rotor. Ejerce una fuerza **desmagnetizante**. Hunde drásticamente el voltaje del generador.
            2. **Carga Capacitiva ($\varphi < 0$, adelanto):** El campo del estator se suma al campo del rotor. Ejerce una fuerza **magnetizante**. Dispara peligrosamente el voltaje del generador.
            3. **Carga Puramente Resistiva ($\varphi = 0°$):** El campo del estator está desfasado 90° espaciales respecto al rotor. Ejerce una fuerza **transversal**, que deforma el flujo empujándolo hacia un lado (esto es lo que genera el par electromagnético resistente en el eje).
            
            #### ¿Cómo contrarrestar este caos? (Regulación de Tensión / AVR)
            Si un operador de central eléctrica no interviniese, cada vez que aumentara el consumo eléctrico (carga inductiva típica de motores), la tensión de toda la red caería en picado por culpa de la reacción de inducido desmagnetizante y las caídas en las bobinas.
            
            Para contrarrestarlo de forma automática, todos los alternadores incorporan un **AVR (Automatic Voltage Regulator)** o Regulador Automático de Tensión. Este sistema electrónico mide continuamente la tensión de salida $U_1$:
            
            * Si **$U_1$ baja** (entrada de carga inductiva), el AVR inyecta instantáneamente más corriente continua ($I_{exc}$) al rotor. Esto hace crecer la fuerza electromotriz interna ($E_0$) lo suficiente para "ganar el pulso" a la reacción de inducido y restaurar $U_1$ a su valor nominal (p.ej., 20 kV).
            * Si **$U_1$ sube** (desconexión brusca de carga), el AVR reduce rápidamente la excitación.
            
            **Conclusión:** La regulación de tensión en un generador no es más que una batalla constante del sistema de excitación ($I_{exc}$) para compensar y anular los efectos nocivos de la reacción del inducido.
            """)

        st.markdown("---")
        st.markdown("### Variación de la Tensión con la Carga (Regulación de Tensión)")
        with st.expander("¿Qué le pasa al voltaje cuando conecto aparatos? (Fórmulas y Concepto)", expanded=True):
            st.markdown(r"""
            Imagina que nuestro generador de la central eléctrica está girando a velocidad constante y tiene la corriente de excitación fija ($E_0$ generada constante). 
            ¿Qué ocurre con el voltaje que le llega a los consumidores ($U_1$) a medida que conectan más fábricas o aparatos (aumenta la corriente $I_a$)?
            
            #### La Ecuación Exacta
            Partiendo del circuito equivalente, la tensión en los bornes de salida se calcula matemáticamente así:
            $$\vec{U}_1 = \vec{E}_0 - \vec{I}_a(R_a + jX_s)$$
            
            Esto significa que **el voltaje que recibe la red ($U_1$) no es constante ni fijo por arte de magia**. Sufre una variación o "caída" respecto al voltaje generado puro en vacío ($E_0$). A esta variación porcentual se le llama **Regulación de Tensión**:
            
            $$\text{Regulación (\%)} = \frac{E_0 - U_1}{U_1} \times 100$$
            
            #### El Factor de Potencia lo cambia todo
            La forma en que cae la tensión no depende solo de la *cantidad* de corriente ($I_a$), sino vitalmente de su *ángulo de desfase* (factor de potencia $\cos\varphi$). Físicamente ocurre lo siguiente:
            
            1. **Cargas Puramente Resistivas ($\cos\varphi = 1$):** (Ej. Estufas, hornos). 
               - La caída de tensión es **moderada**. Al pedir más y más corriente, $U_1$ baja lentamente.
            2. **Cargas Inductivas ($\cos\varphi < 1$ en retraso):** (Ej. Motores industriales, transformadores). 
               - La caída de tensión es **brutal**. Como vimos en el apartado anterior, el campo del estator destruye el flujo del rotor por estar opuesto (reacción del inducido desmagnetizante), y además los cables del estator "roban" tensión ($jX_s$). Resultado: el voltaje $U_1$ se desploma muy rápidamente. La Regulación de Tensión será grande y fuertemente positiva (ej. 30%).
            3. **Cargas Capacitivas ($\cos\varphi < 1$ en adelanto):** (Ej. Largas líneas de transmisión en vacío). 
               - Ocurre algo fascinante y peligroso: la reacción de inducido refuerza el flujo del rotor. **¡El voltaje $U_1$ aumenta!** a medida que sacamos más corriente. La máquina auto-excita su magnetismo. El generador entregará más voltaje a la ciudad estando cargado que estando en vacío ($U_1 > E_0$). La Regulación de Tensión dará un valor **negativo**.
               
            💡 *Reflexión didáctica final:* Un generador ideal sería aquel que no tuviera reactancia interna ($X_s = 0$), ya que $U_1$ sería siempre idéntico a $E_0$ conectes lo que conectes. Pero en el mundo real, $X_s$ es gigantesca, haciendo que los generadores sean eléctricamente muy "blandos" o sensibles a la carga inductiva. ¡Esa es la razón exacta por la que necesitamos tener siempre encendido el cerebro automático (AVR) para corregirlo al instante!
            """)

    # --------------------------------------------------------------------------
    # PESTAÑA 3: DIAGRAMAS FASORIALES
    # --------------------------------------------------------------------------
    with tab_fasores:
        st.markdown("### Diagrama Fasorial Completo de la máquina Síncrona")
        st.write("Para entender realmente cómo interactúan los flujos magnéticos y las tensiones en el interior de la máquina síncrona (funcionando como generador), analizamos el diagrama fasorial completo a partir de sus fuerzas magnetomotrices.")

        col_diag, col_text = st.columns([1.3, 1])
        with col_diag:
            st.markdown("""
            <div style="background:#0E1117; border:1px solid #2a2a3a; border-radius:10px; padding:10px; display:flex; justify-content:center;">
            <svg width="100%" height="350" viewBox="100 50 500 300" xmlns="http://www.w3.org/2000/svg" style="font-family:'monospace',sans-serif;">
              <defs>
                <marker id="arr_g" markerWidth="10" markerHeight="10" refX="8" refY="5" orient="auto">
                  <path d="M0,0 L0,10 L10,5 z" fill="#00ADB5"/>
                </marker>
                <marker id="arr_r" markerWidth="10" markerHeight="10" refX="8" refY="5" orient="auto">
                  <path d="M0,0 L0,10 L10,5 z" fill="#FF4B4B"/>
                </marker>
                <marker id="arr_y" markerWidth="10" markerHeight="10" refX="8" refY="5" orient="auto">
                  <path d="M0,0 L0,10 L10,5 z" fill="#F9A826"/>
                </marker>
                <marker id="arr_w" markerWidth="10" markerHeight="10" refX="8" refY="5" orient="auto">
                  <path d="M0,0 L0,10 L10,5 z" fill="#E5E7EB"/>
                </marker>
              </defs>

              <!-- Ángulos rectos -->
              <polygon points="250,250 264.8,247.4 262.2,232.6 247.4,235.2" fill="none" stroke="#4B5563" stroke-width="1.5"/>
              <polygon points="250,250 263.5,243.4 256.9,229.9 243.4,236.5" fill="none" stroke="#4B5563" stroke-width="1.5"/>
              <polygon points="460.3,267.5 451.6,262.5 456.6,253.8 465.3,258.8" fill="none" stroke="#4B5563" stroke-width="1.5"/>

              <!-- Arcos de ángulos -->
              <path d="M 310 250 A 60 60 0 0 1 302 280" fill="none" stroke="#9CA3AF" stroke-width="1.5"/>
              <text x="315" y="270" fill="#9CA3AF" font-size="14">φ</text>

              <path d="M 370 250 A 120 120 0 0 0 357.7 197.1" fill="none" stroke="#9CA3AF" stroke-width="1.5"/>
              <text x="375" y="235" fill="#9CA3AF" font-size="14">δ</text>

              <path d="M 348.5 232.7 A 100 100 0 0 0 339.8 205.9" fill="none" stroke="#9CA3AF" stroke-width="1.5"/>
              <text x="352" y="215" fill="#9CA3AF" font-size="14">α</text>

              <path d="M 239.6 190.9 A 60 60 0 0 0 223.6 196.1" fill="none" stroke="#9CA3AF" stroke-width="1.5"/>
              <text x="215" y="190" fill="#9CA3AF" font-size="14">α</text>

              <!-- Vectores de tensión (Amarillos/Blancos) -->
              <line x1="250" y1="250" x2="430" y2="250" stroke="#F9A826" stroke-width="2.5" marker-end="url(#arr_y)"/>
              <text x="330" y="240" fill="#F9A826" font-size="16" font-weight="bold">V</text>

              <line x1="430" y1="250" x2="460.3" y2="267.5" stroke="#E5E7EB" stroke-width="2" marker-end="url(#arr_w)"/>
              <text x="445" y="280" fill="#E5E7EB" font-size="13">RI</text>

              <line x1="460.3" y1="267.5" x2="495.3" y2="206.9" stroke="#E5E7EB" stroke-width="2" marker-end="url(#arr_w)"/>
              <text x="480" y="255" fill="#E5E7EB" font-size="13">jXσI</text>

              <line x1="250" y1="250" x2="495.3" y2="206.9" stroke="#F9A826" stroke-width="2.5" marker-end="url(#arr_y)"/>
              <text x="375" y="220" fill="#F9A826" font-size="16" font-weight="bold">Er</text>

              <line x1="250" y1="250" x2="557.6" y2="99.1" stroke="#F9A826" stroke-width="2.5" marker-end="url(#arr_y)"/>
              <text x="420" y="165" fill="#F9A826" font-size="16" font-weight="bold">E₀</text>

              <!-- Vectores de Corriente (Cyan) -->
              <line x1="250" y1="250" x2="336.6" y2="300" stroke="#00ADB5" stroke-width="2.5" marker-end="url(#arr_g)"/>
              <text x="345" y="305" fill="#00ADB5" font-size="16" font-weight="bold">I</text>

              <!-- Vectores de MMF/Flujo (Rojo) -->
              <line x1="250" y1="250" x2="310.6" y2="285" stroke="#FF4B4B" stroke-width="2.5" marker-end="url(#arr_r)"/>
              <text x="260" y="295" fill="#FF4B4B" font-size="14" font-weight="bold">Fi</text>

              <line x1="250" y1="250" x2="225.8" y2="112.1" stroke="#FF4B4B" stroke-width="2.5" marker-end="url(#arr_r)"/>
              <text x="235" y="150" fill="#FF4B4B" font-size="14" font-weight="bold">Fr (Φr)</text>

              <line x1="250" y1="250" x2="165.2" y2="77.1" stroke="#FF4B4B" stroke-width="2.5" marker-end="url(#arr_r)"/>
              <text x="140" y="85" fill="#FF4B4B" font-size="14" font-weight="bold">Fe</text>

              <!-- -Fi -->
              <line x1="225.8" y1="112.1" x2="165.2" y2="77.1" stroke="#FF4B4B" stroke-width="2" stroke-dasharray="4,4" marker-end="url(#arr_r)"/>
              <text x="180" y="110" fill="#FF4B4B" font-size="13">-Fi</text>
              
              <!-- Ejes de referencia sutiles -->
              <circle cx="250" cy="250" r="3" fill="#E5E7EB"/>
            </svg>
            </div>
            """, unsafe_allow_html=True)
            
        with col_text:
            st.markdown("#### Resumen Visual Rápido:")
            st.markdown(r"""
            1. **El Rotor empuja ($F_e$):** La corriente continua inyectada en el rotor crea la fuerza magnetomotriz principal.
            2. **La Corriente 'molesta' ($F_i$):** Al conectar una carga, circula la corriente $I$ por el estator, creando su propio campo magnético ($F_i$), lo que se conoce como *reacción de inducido*.
            3. **Lo que queda es el Flujo Resultante ($F_r$ o $\Phi_r$):** El flujo que realmente actúa en el entrehierro de la máquina es la suma vectorial del empuje del rotor más la reacción del estator ($F_r = F_e + F_i$).
            4. **Ese flujo fabrica el Voltaje Interno ($E_r$):** Según la Ley de Faraday, el flujo resultante $\Phi_r$ induce la fuerza electromotriz $E_r$, la cual se encuentra retrasada exactamente 90° respecto a él.
            5. **Pérdidas en los cables ($RI$ y $jX_\sigma I$):** Antes de salir a la red eléctrica, la energía sufre ligeras caídas de tensión por culpa de la resistencia y la dispersión magnética en los propios devanados del estator.
            6. **Voltaje Útil ($V$):** Es lo que finalmente sobrevive y llega a los bornes de la red para alimentar las fábricas o ciudades.
            """)
            st.info("💡 **¿Por qué la reacción de inducido ($F_i$) es tan pesada para el generador?** Si observas el diagrama (carga inductiva), el campo $F_i$ 'tira' en dirección casi opuesta al campo del rotor $F_e$, debilitando drásticamente el flujo resultante $F_r$. Esto obliga al operador a inyectar continuamente mucha más corriente de excitación para que el voltaje útil $V$ no se hunda.")

        st.markdown("---")
        st.markdown("### Efecto del Nivel de Excitación")
        st.write("El diagrama fasorial anterior muestra un estado de subexcitación. A continuación veremos cómo cambia el comportamiento global de la máquina al variar el nivel de excitación ($I_{exc}$).")

        col_f1, col_f2, col_f3 = st.columns(3)
        with col_f1:
            st.markdown("#### Subexcitación")
            st.write("$E_0 \\cos(\\delta) < U_1$")
            st.write(
                "La corriente de armadura $I_a$ está **retrasada** respecto a $U_1$ (factor de potencia inductivo). "
                "La máquina **consume** potencia reactiva de la red. Actúa como una bobina."
            )
            st.error("**Q < 0** — La máquina absorbe reactiva inductiva")
        with col_f2:
            st.markdown("#### Excitación Normal")
            st.write("$E_0 \\cos(\\delta) = U_1$")
            st.write(
                "La corriente de armadura está **en fase** con $U_1$. "
                "Factor de potencia unitario ($\\cos\\varphi = 1$). "
                "La máquina ni genera ni consume reactiva."
            )
            st.success("**Q = 0** — Factor de potencia unidad")
        with col_f3:
            st.markdown("#### Sobreexcitación")
            st.write("$E_0 \\cos(\\delta) > U_1$")
            st.write(
                "La corriente de armadura $I_a$ está **adelantada** respecto a $U_1$ (factor de potencia capacitivo). "
                "La máquina **genera** potencia reactiva hacia la red. Actúa como un condensador."
            )
            st.info("**Q > 0** — La máquina inyecta reactiva capacitiva")

        st.markdown("---")
        with st.expander("El Compensador Síncrono: Máquina Síncrona en Vacío", expanded=True):
            st.markdown(r"""
            Si la máquina síncrona funciona **en vacío** (sin carga mecánica acoplada, $\delta \approx 0$),
            toda su capacidad queda disponible para el control de reactiva. En este modo se denomina
            **compensador síncrono** (o condensador síncrono).
            
            * **Sobreexcitado ($I_{exc}$ alto):** Inyecta reactiva capacitiva a la red → eleva la tensión
              en el punto de conexión. Equivale a conectar un banco de condensadores controlable.
            * **Subexcitado ($I_{exc}$ bajo):** Absorbe reactiva inductiva de la red → reduce la tensión.
              Equivale a conectar reactancias.
            
            Esta capacidad de regulación continua y rápida lo convierte en una herramienta fundamental
            para la gestión de la tensión en los nodos de la red de transporte eléctrica.
            """)


    # --------------------------------------------------------------------------
    # PESTAÑA 4: CONTROL Y ESTABILIDAD
    # --------------------------------------------------------------------------
    with tab_control:
        st.markdown("### Estabilidad y Física del Ángulo de Carga ($\delta$)")
        
        with st.expander("¿Qué es exactamente el ángulo Delta (δ)? (Base Física y Didáctica)", expanded=True):
            st.markdown(r"""
            El ángulo $\delta$, conocido como **ángulo de carga**, **ángulo de par** o **ángulo de potencia**, es el concepto más importante para entender el funcionamiento electromecánico de la máquina síncrona.
            
            #### 1. Definición Física y "La Goma Elástica"
            Físicamente, el estator genera un campo magnético giratorio a la velocidad de sincronismo $n_s$. El rotor (que es un imán excitado con CC) se engancha magnéticamente a este campo y gira exactamente con él. 
            
            * **En vacío ($P = 0$):** Los polos del rotor están perfectamente alineados con los polos del campo giratorio del estator. El ángulo mecánico entre ellos es cero. En este estado, $\delta = 0°$.
            * **Con carga ($P > 0$):** Si empezamos a aplicar fuerza motriz a la turbina (generador) o le metemos carga mecánica al eje (motor), el rotor se desalineará ligeramente respecto al campo del estator, **pero sin dejar de girar a la misma velocidad $n_s$**. 
            
            💡 **Analogía:** Imagina el acoplamiento magnético como una **goma elástica invisible** que une el tren magnético del estator con el rotor. Si haces fuerza extra en el eje, la goma se estira (se desalinea) y "tira" con más fuerza. Este grado de "estiramiento magnético" se traduce eléctricamente en el ángulo $\delta$.
            
            #### 2. Definición Eléctrica y Fasorial
            Eléctricamente, este desplazamiento mecánico del rotor provoca un desfase temporal entre las ondas de tensión. El ángulo $\delta$ es el ángulo que forma la fuerza electromotriz $\vec{E}_0$ respecto a la tensión de la red $\vec{U}_1$.
            * **Generador:** El rotor se adelanta mecánicamente para empujar. Por tanto, $\vec{E}_0$ va *adelantado* respecto a $\vec{U}_1$ ($\delta > 0$).
            * **Motor:** El rotor se retrasa porque la carga lo frena. Por tanto, $\vec{E}_0$ va *retrasado* respecto a $\vec{U}_1$ ($\delta < 0$).
            
            #### 3. Deducción Matemática de la Potencia Activa
            Partiendo de la potencia activa por fase ($P_{1\phi} = U_1 \cdot I_a \cdot \cos\varphi$).
            Si analizamos la geometría del diagrama fasorial (asumiendo que la resistencia del cobre es muy pequeña $R_a \approx 0$), la caída de tensión en la inductancia es puramente vertical ($jX_s\vec{I}_a$). Aplicando proyecciones trigonométricas obtenemos la relación:
            $$I_a \cdot X_s \cdot \cos(\varphi) = E_0 \cdot \sin(\delta)$$
            
            Si despejamos la corriente activa ($I_a \cos\varphi$) y multiplicamos por 3 (para obtener la potencia trifásica total), llegamos a la **ecuación fundamental de transmisión de potencia síncrona**:
            $$P = 3 \cdot \frac{U_1 \cdot E_0}{X_s} \cdot \sin(\delta)$$
            
            **Conclusión:** La potencia activa real ($P$) intercambiada no depende de la frecuencia ni de cambios de velocidad (porque $n$ es constante), sino exclusivamente del "estiramiento" $\delta$.
            """)

        st.markdown("---")

        col_p1, col_p2 = st.columns([1, 1.2])
        with col_p1:
            st.markdown("#### Ecuación de la Potencia (Polos Lisos)")
            st.latex(r"P = \frac{3 \cdot U_1 \cdot E_0}{X_s} \cdot \sin(\delta)")
            st.write(
                "Esta función sinusoidal tiene un máximo en $\\delta = 90°$. "
                "Se define la **potencia máxima o par máximo estático**:"
            )
            st.latex(r"P_{max} = \frac{3 \cdot U_1 \cdot E_0}{X_s}")

        with col_p2:
            st.markdown("#### El Par Electromagnético ($M$)")
            st.markdown(r"""
            La potencia activa es exactamente escalable al par mecánico en el eje, puesto que la velocidad del motor es constante ($\omega_s$).
            
            $$M = \frac{P}{\omega_s} = \frac{3 \cdot U_1 \cdot E_0}{\omega_s \cdot X_s} \cdot \sin(\delta)$$
            
            La máquina reacciona a los cambios de carga estirando o encogiendo el ángulo $\delta$. Si $\delta > 0$, empuja como generador. Si $\delta < 0$, absorbe como motor.
            """)



    # --------------------------------------------------------------------------
    # PESTAÑA 5: SÍNCRONA VS ASÍNCRONA
    # --------------------------------------------------------------------------
    with tab_comparativa:
        st.markdown("### Motor Síncrono vs Motor Asíncrono")
        st.write(
            "Aunque ambas son máquinas de corriente alterna y su estator es prácticamente idéntico "
            "(generando un campo magnético giratorio), la forma en la que sus rotores interactúan con "
            "este campo define dos mundos mecánicos y eléctricos completamente distintos."
        )

        col_sync, col_async = st.columns(2)
        with col_sync:
            st.markdown("#### Motor Síncrono: 'El Preciso'")
            st.markdown(r"""
            **1. Excitación y Campo:**
            Tiene **doble excitación**. El rotor es un electroimán alimentado por corriente continua externa.
            
            **2. Ecuación de Velocidad:**
            Gira exactamente a la velocidad de sincronismo. **No hay deslizamiento** ($s=0$).
            $$n = n_s = \frac{60 \cdot f}{p}$$
            
            **3. Generación de Par:**
            El par electromagnético depende del **ángulo de carga** $\delta$ (ángulo mecánico de retraso del rotor respecto al campo del estator).
            $$P = \frac{3 \cdot U_1 \cdot E_0}{X_s} \cdot \sin(\delta)$$
            
            **4. Potencia Reactiva:**
            Regulando la $I_{exc}$ puede generar o consumir reactiva ($Q > 0$ o $Q < 0$).
            
            **5. Arranque:**
            **No tiene par de arranque propio** a la frecuencia de red. Necesita ayuda (motor auxiliar, variador de frecuencia o jaula de amortiguamiento).
            """)
        
        with col_async:
            st.markdown("#### Motor Asíncrono: 'El Caballo de Batalla'")
            st.markdown(r"""
            **1. Excitación y Campo:**
            **Excitación única**. El rotor recibe corriente sólo por inducción electromagnética (Ley de Faraday).
            
            **2. Ecuación de Velocidad:**
            Gira más lento que el sincronismo. **Existe deslizamiento** ($s > 0$).
            $$n = n_s \cdot (1 - s) \quad \text{con} \quad s = \frac{n_s - n}{n_s}$$
            
            **3. Generación de Par:**
            El par depende de la corriente inducida en el rotor, la cual depende del deslizamiento $s$.
            $$M \approx \frac{3 \cdot U_1^2 \cdot \frac{R'_2}{s}}{\omega_s \left[ (R_1 + \frac{R'_2}{s})^2 + X_{cc}^2 \right]}$$
            
            **4. Potencia Reactiva:**
            **Siempre consume reactiva** inductiva ($Q < 0$) para magnetizar el núcleo. No puede generarla.
            
            **5. Arranque:**
            **Arranque directo y robusto**. Genera un fuerte par desde velocidad cero.
            """)

        st.markdown("---")
        st.markdown("#### Resumen Fisico Didactico")
        st.info(
            "**Imagina a dos corredores (el rotor) intentando atrapar a un tren magnetico que no se detiene (el campo del estator a $n_s$):**\n\n"
            "**El Motor Asincrono:** Para poder agarrar la energia del tren (induccion), el corredor **necesita correr un poco mas despacio** que el tren (deslizamiento). Si llegara a correr a la misma velocidad que el tren, no sentiria el 'viento' de energia (no hay variacion de flujo), perderia fuerza y se frenaria. Corre persiguiendo siempre, pero nunca lo alcanza.\n\n"
            "**El Motor Sincrono:** Este corredor trae **su propio iman** (excitacion CC). Se 'engancha' magneticamente al tren desde el principio. Corre **exactamente a la misma velocidad** que el tren. Si la carga mecanica se vuelve mas pesada, simplemente se estira un poco el enganche (angulo $\\delta$), pero no pierde velocidad. Si el enganche se rompe (supera 90 grados), se cae estrepitosamente (pierde sincronismo)."
        )

    # --------------------------------------------------------------------------
    # PESTAÑA 6: MÉTODO DE BEHN-ESCHENBURG (RÉGIMEN LINEAL)
    # --------------------------------------------------------------------------
    with tab_behn:
        st.markdown("### Método de Behn-Eschenburg (Impedancia Síncrona en Régimen Lineal)")
        st.markdown(
            "El **método de Behn-Eschenburg** es el procedimiento experimental clásico para determinar la **impedancia síncrona** "
            "($Z_s$) de la máquina síncrona, válido exclusivamente en la **zona lineal** de la curva de magnetización "
            "(antes del codo de saturación). Se basa en la combinación de dos ensayos independientes realizados "
            "sobre la máquina girando a velocidad de sincronismo ($n_s$)."
        )

        st.warning(
            "**Limitación fundamental:** Este método asume que el circuito magnético opera en zona lineal "
            "(proporcionalidad directa entre $I_{exc}$ y $\\Phi$). En máquinas reales trabajando a tensión nominal, "
            "el hierro está parcialmente saturado, lo que provoca que este método **sobreestime** el valor de $Z_s$ "
            "y, por tanto, subestime la corriente de cortocircuito real. Para el régimen saturado se emplea "
            "el **Método de Potier** (pestaña siguiente)."
        )

        # ====================================================================
        #  PASO A PASO: LOS DOS ENSAYOS
        # ====================================================================
        st.markdown("---")
        st.markdown("#### Ensayos Experimentales Necesarios")

        col_ens1, col_ens2 = st.columns(2)
        with col_ens1:
            st.markdown(
                "**1. Ensayo de Vacío (OCC — Open Circuit Characteristic)**\n\n"
                "La máquina gira a $n_s$ con los bornes del estator **abiertos** (sin carga conectada). "
                "Se varía progresivamente la corriente de excitación del rotor ($I_{exc}$) desde cero "
                "y se mide la tensión en bornes $U_0$. Como $I_a = 0$, no hay caída de tensión interna, "
                "por lo que:\n\n"
                "$$U_0 = E_0$$\n\n"
                "**Resultado:** Curva $E_0$ vs $I_{exc}$ — inicialmente recta (zona lineal), luego se "
                "curva al saturarse el hierro."
            )
        with col_ens2:
            st.markdown(
                "**2. Ensayo de Cortocircuito (SCC — Short Circuit Characteristic)**\n\n"
                "La máquina gira a $n_s$ con los bornes del estator **cortocircuitados** a través de amperímetros. "
                "Se varía $I_{exc}$ desde cero y se mide la corriente de armadura $I_{cc}$.\n\n"
                "Como $U_1 = 0$ V, toda la f.e.m. se consume en la impedancia interna:\n\n"
                "$$E_0 = I_{cc} \\cdot Z_s$$\n\n"
                "**Resultado:** Curva $I_{cc}$ vs $I_{exc}$ — **siempre lineal** (recta que pasa por el origen), "
                "porque en cortocircuito el flujo resultante en el entrehierro es muy pequeño (el campo del estator "
                "casi anula al del rotor) y el hierro permanece en zona no saturada."
            )

        # ====================================================================
        #  SIMULADOR INTERACTIVO PROFESIONAL — BEHN-ESCHENBURG
        #  HTML5 Canvas con controles integrados, sin re-run de Streamlit
        # ====================================================================
        st.markdown("---")
        st.markdown("#### Construcción Gráfica Interactiva: Obtención de $Z_s$")
        st.markdown(
            "El siguiente simulador muestra las dos curvas experimentales superpuestas (OCC y SCC). "
            "Ajuste los parámetros y deslice el cursor de excitación para visualizar cómo se obtienen "
            "$E_0$, $I_{cc}$ y la impedancia síncrona $Z_s$ gráficamente."
        )

        BEHN_SIM_HTML = """
        <link href="https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800&display=swap" rel="stylesheet">
        <style>
          *{margin:0;padding:0;box-sizing:border-box;}
          body{background:transparent;overflow:hidden;}
          #bw{
            font-family:'Inter',sans-serif;
            background:linear-gradient(145deg,#080c14,#0d1220,#0a0f1a);
            border:1px solid rgba(255,255,255,0.08);
            border-radius:14px;position:relative;overflow:hidden;
          }
          #bw::before{content:'';position:absolute;top:0;left:0;right:0;height:1px;
            background:linear-gradient(90deg,transparent,rgba(249,168,38,0.4),transparent);}
          .bh{display:flex;align-items:center;justify-content:space-between;padding:14px 22px;
            background:rgba(255,255,255,0.02);border-bottom:1px solid rgba(255,255,255,0.06);}
          .bh .tt{font-size:14px;font-weight:700;color:#e5e7eb;letter-spacing:0.5px;}
          .bh .tt span{color:#F9A826;font-weight:800;}
          .bp{display:flex;gap:0;padding:0;border-bottom:1px solid rgba(255,255,255,0.06);}
          .bp .pc{flex:1;padding:14px 16px;border-right:1px solid rgba(255,255,255,0.04);}
          .bp .pc:last-child{border-right:none;}
          .bp .pc label{display:block;font-size:9px;color:#6b7280;text-transform:uppercase;
            letter-spacing:1px;margin-bottom:6px;font-weight:600;}
          .bp .pc input[type=range]{width:100%;accent-color:#F9A826;height:6px;margin:0;}
          .bp .pc .sv{font-size:16px;font-weight:800;color:#e5e7eb;margin-top:4px;}
          .bp .pc .sv.gold{color:#F9A826;}
          .bp .pc .sv.blue{color:#58a6ff;}
          .bp .pc .sv.gray{color:#9ca3af;}
          canvas#bc{display:block;width:100%;}
          .br{display:flex;gap:0;border-top:1px solid rgba(255,255,255,0.06);}
          .br .rc{flex:1;text-align:center;padding:12px 6px;
            border-right:1px solid rgba(255,255,255,0.04);}
          .br .rc:last-child{border-right:none;}
          .br .rc .rl{font-size:9px;color:#6b7280;text-transform:uppercase;letter-spacing:1px;margin-bottom:3px;}
          .br .rc .rv{font-size:20px;font-weight:800;}
          .br .rc .rv.gold{color:#F9A826;}
          .br .rc .rv.blue{color:#58a6ff;}
          .br .rc .rv.green{color:#34d399;}
          .br .rc .rv.cyan{color:#22d3ee;}
          .br .rc .rv.purple{color:#a78bfa;}
          .br .rc .ru{font-size:10px;color:#4b5563;margin-top:1px;}
        </style>
        <div id="bw">
          <div class="bh">
            <div class="tt"><span>⚡</span> Método de Behn-Eschenburg — Obtención Gráfica de Z<sub>s</sub></div>
          </div>
          <div class="bp">
            <div class="pc">
              <label>Pendiente OCC (V/A)</label>
              <input type="range" id="sl_kocc" min="20" max="300" value="100" step="5">
              <div class="sv gold" id="v_kocc">100</div>
            </div>
            <div class="pc">
              <label>Pendiente SCC (A/A)</label>
              <input type="range" id="sl_kscc" min="1" max="20" value="5" step="0.5">
              <div class="sv blue" id="v_kscc">5.0</div>
            </div>
            <div class="pc">
              <label>Resistencia Ra (Ω)</label>
              <input type="range" id="sl_ra" min="0" max="20" value="1" step="0.5">
              <div class="sv gray" id="v_ra">1.0</div>
            </div>
            <div class="pc" style="flex:1.5">
              <label>Corriente de Excitación I<sub>exc</sub> (A)</label>
              <input type="range" id="sl_iexc" min="0.5" max="20" value="10" step="0.5">
              <div class="sv gold" id="v_iexc">10.0</div>
            </div>
          </div>
          <canvas id="bc"></canvas>
          <div class="br">
            <div class="rc"><div class="rl">E₀ (Vacío)</div><div class="rv gold" id="r_e0">1000</div><div class="ru">V</div></div>
            <div class="rc"><div class="rl">I<sub>cc</sub> (Cortocirc.)</div><div class="rv blue" id="r_icc">50.0</div><div class="ru">A</div></div>
            <div class="rc"><div class="rl">Z<sub>s</sub></div><div class="rv green" id="r_zs">20.00</div><div class="ru">Ω</div></div>
            <div class="rc"><div class="rl">X<sub>s</sub></div><div class="rv cyan" id="r_xs">19.97</div><div class="ru">Ω</div></div>
            <div class="rc"><div class="rl">X<sub>s</sub> / R<sub>a</sub></div><div class="rv purple" id="r_ratio">19.97</div><div class="ru">—</div></div>
          </div>
        </div>
        <script>
        (function(){
        var cv=document.getElementById('bc'),g=cv.getContext('2d');
        var W,H;
        var sl_k=document.getElementById('sl_kocc'),sl_s=document.getElementById('sl_kscc');
        var sl_r=document.getElementById('sl_ra'),sl_i=document.getElementById('sl_iexc');

        function resize(){
          var wrap=document.getElementById('bw');
          W=wrap.clientWidth;
          if(W<10){requestAnimationFrame(resize);return;}
          H=Math.min(440,W*0.5);
          cv.width=W*2;cv.height=H*2;cv.style.height=H+'px';
          g.setTransform(2,0,0,2,0,0);
          draw();
        }
        requestAnimationFrame(resize);window.addEventListener('resize',resize);

        /* Margins for chart area */
        var ML=70,MR=70,MT=30,MB=50;

        function draw(){
          var kOCC=parseFloat(sl_k.value), kSCC=parseFloat(sl_s.value);
          var Ra=parseFloat(sl_r.value), Iexc=parseFloat(sl_i.value);

          /* Update value displays */
          document.getElementById('v_kocc').textContent=kOCC;
          document.getElementById('v_kscc').textContent=kSCC.toFixed(1);
          document.getElementById('v_ra').textContent=Ra.toFixed(1);
          document.getElementById('v_iexc').textContent=Iexc.toFixed(1);

          /* Calculated values */
          var E0=kOCC*Iexc, Icc=kSCC*Iexc;
          var Zs=Icc>0?E0/Icc:0;
          var Xs=Math.sqrt(Math.max(Zs*Zs-Ra*Ra,0));
          var ratio=Ra>0?Xs/Ra:Infinity;

          /* Update results HUD */
          document.getElementById('r_e0').textContent=E0.toFixed(0);
          document.getElementById('r_icc').textContent=Icc.toFixed(1);
          document.getElementById('r_zs').textContent=Zs.toFixed(2);
          document.getElementById('r_xs').textContent=Xs.toFixed(2);
          document.getElementById('r_ratio').textContent=isFinite(ratio)?ratio.toFixed(1):'∞';

          g.clearRect(0,0,W,H);

          /* Chart area */
          var cW=W-ML-MR, cH=H-MT-MB;
          var maxIexc=25, maxE0=kOCC*maxIexc*1.1, maxIcc=kSCC*maxIexc*1.1;

          function xPx(v){return ML+v/maxIexc*cW;}
          function yPxL(v){return MT+cH-v/maxE0*cH;}
          function yPxR(v){return MT+cH-v/maxIcc*cH;}

          /* Grid */
          g.strokeStyle='rgba(255,255,255,0.04)';g.lineWidth=0.5;
          for(var gx=0;gx<=maxIexc;gx+=5){
            var xx=xPx(gx);
            g.beginPath();g.moveTo(xx,MT);g.lineTo(xx,MT+cH);g.stroke();
          }
          for(var i=0;i<=5;i++){
            var yy=MT+cH*i/5;
            g.beginPath();g.moveTo(ML,yy);g.lineTo(ML+cW,yy);g.stroke();
          }

          /* Axes */
          g.strokeStyle='rgba(255,255,255,0.15)';g.lineWidth=1.5;
          g.beginPath();g.moveTo(ML,MT);g.lineTo(ML,MT+cH);g.lineTo(ML+cW,MT+cH);g.stroke();
          /* Right axis */
          g.beginPath();g.moveTo(ML+cW,MT);g.lineTo(ML+cW,MT+cH);g.stroke();

          /* X axis labels */
          g.font='600 10px Inter,sans-serif';g.fillStyle='rgba(255,255,255,0.35)';g.textAlign='center';
          for(var gx=0;gx<=maxIexc;gx+=5){
            g.fillText(gx+'',xPx(gx),MT+cH+16);
          }
          g.fillText('I_exc (A)',ML+cW/2,MT+cH+38);

          /* Left Y axis labels (E0) */
          g.textAlign='right';g.fillStyle='rgba(249,168,38,0.5)';
          for(var i=0;i<=5;i++){
            var val=maxE0*i/5;
            g.fillText(val.toFixed(0),ML-8,MT+cH-cH*i/5+4);
          }
          g.save();g.translate(16,MT+cH/2);g.rotate(-Math.PI/2);
          g.textAlign='center';g.font='600 11px Inter,sans-serif';g.fillStyle='rgba(249,168,38,0.7)';
          g.fillText('E₀ (V)',0,0);g.restore();

          /* Right Y axis labels (Icc) */
          g.textAlign='left';g.fillStyle='rgba(88,166,255,0.5)';g.font='600 10px Inter,sans-serif';
          for(var i=0;i<=5;i++){
            var val=maxIcc*i/5;
            g.fillText(val.toFixed(0),ML+cW+8,MT+cH-cH*i/5+4);
          }
          g.save();g.translate(W-14,MT+cH/2);g.rotate(Math.PI/2);
          g.textAlign='center';g.font='600 11px Inter,sans-serif';g.fillStyle='rgba(88,166,255,0.7)';
          g.fillText('I_cc (A)',0,0);g.restore();

          /* OCC curve */
          g.beginPath();
          for(var ix=0;ix<=maxIexc;ix+=0.2){
            var xx=xPx(ix),yy=yPxL(kOCC*ix);
            if(ix===0)g.moveTo(xx,yy);else g.lineTo(xx,yy);
          }
          g.strokeStyle='#F9A826';g.lineWidth=3;g.lineCap='round';g.stroke();
          /* OCC glow */
          g.strokeStyle='rgba(249,168,38,0.15)';g.lineWidth=10;g.stroke();

          /* SCC curve */
          g.beginPath();
          for(var ix=0;ix<=maxIexc;ix+=0.2){
            var xx=xPx(ix),yy=yPxR(kSCC*ix);
            if(ix===0)g.moveTo(xx,yy);else g.lineTo(xx,yy);
          }
          g.strokeStyle='#58a6ff';g.lineWidth=3;g.lineCap='round';g.stroke();
          /* SCC glow */
          g.strokeStyle='rgba(88,166,255,0.15)';g.lineWidth=10;g.stroke();

          /* Curve labels */
          g.font='bold 12px Inter,sans-serif';g.textAlign='left';
          var lblIx=maxIexc*0.75;
          g.fillStyle='#F9A826';g.fillText('OCC (Vacío)',xPx(lblIx)+6,yPxL(kOCC*lblIx)-10);
          g.fillStyle='#58a6ff';g.fillText('SCC (Cortocircuito)',xPx(lblIx)+6,yPxR(kSCC*lblIx)-10);

          /* === Vertical cursor line at Iexc === */
          var cx=xPx(Iexc);
          g.beginPath();g.moveTo(cx,MT);g.lineTo(cx,MT+cH);
          g.strokeStyle='rgba(255,255,255,0.2)';g.lineWidth=1;g.setLineDash([5,5]);g.stroke();g.setLineDash([]);

          /* === Horizontal projection lines === */
          var yE0=yPxL(E0), yIcc=yPxR(Icc);

          /* E0 horizontal to left axis */
          g.beginPath();g.moveTo(ML,yE0);g.lineTo(cx,yE0);
          g.strokeStyle='rgba(249,168,38,0.4)';g.lineWidth=1.5;g.setLineDash([4,4]);g.stroke();g.setLineDash([]);

          /* Icc horizontal to right axis */
          g.beginPath();g.moveTo(cx,yIcc);g.lineTo(ML+cW,yIcc);
          g.strokeStyle='rgba(88,166,255,0.4)';g.lineWidth=1.5;g.setLineDash([4,4]);g.stroke();g.setLineDash([]);

          /* === E0 intersection dot === */
          g.beginPath();g.arc(cx,yE0,8,0,Math.PI*2);
          g.fillStyle='rgba(249,168,38,0.2)';g.fill();
          g.beginPath();g.arc(cx,yE0,5,0,Math.PI*2);
          g.fillStyle='#F9A826';g.fill();
          g.strokeStyle='rgba(255,255,255,0.5)';g.lineWidth=2;g.stroke();

          /* E0 label */
          g.font='bold 12px Inter,sans-serif';g.fillStyle='#F9A826';g.textAlign='left';
          g.fillText('E₀ = '+E0.toFixed(0)+' V',cx+12,yE0-6);

          /* === Icc intersection dot === */
          g.beginPath();g.arc(cx,yIcc,8,0,Math.PI*2);
          g.fillStyle='rgba(88,166,255,0.2)';g.fill();
          g.beginPath();g.arc(cx,yIcc,5,0,Math.PI*2);
          g.fillStyle='#58a6ff';g.fill();
          g.strokeStyle='rgba(255,255,255,0.5)';g.lineWidth=2;g.stroke();

          /* Icc label */
          g.font='bold 12px Inter,sans-serif';g.fillStyle='#58a6ff';g.textAlign='left';
          g.fillText('I_cc = '+Icc.toFixed(1)+' A',cx+12,yIcc+16);

          /* Iexc label at bottom */
          g.font='bold 11px Inter,sans-serif';g.fillStyle='rgba(255,255,255,0.5)';g.textAlign='center';
          g.fillText('I_exc = '+Iexc.toFixed(1)+' A',cx,MT+cH+28);

          /* === Zs formula badge === */
          var bx=ML+cW*0.02, by=MT+10;
          g.fillStyle='rgba(0,0,0,0.5)';
          g.beginPath();
          var bw=195,bh=52,br=8;
          g.moveTo(bx+br,by);g.arcTo(bx+bw,by,bx+bw,by+bh,br);
          g.arcTo(bx+bw,by+bh,bx,by+bh,br);g.arcTo(bx,by+bh,bx,by,br);
          g.arcTo(bx,by,bx+bw,by,br);g.closePath();g.fill();
          g.strokeStyle='rgba(52,211,153,0.3)';g.lineWidth=1;g.stroke();
          g.font='600 11px Inter,sans-serif';g.fillStyle='rgba(52,211,153,0.7)';g.textAlign='left';
          g.fillText('Zs = E₀ / I_cc',bx+12,by+18);
          g.font='800 18px Inter,sans-serif';g.fillStyle='#34d399';
          g.fillText(Zs.toFixed(2)+' Ω',bx+12,by+42);
        }

        /* Event listeners */
        [sl_k,sl_s,sl_r,sl_i].forEach(function(el){el.addEventListener('input',draw);});

        draw();
        })();
        </script>
        """

        components.html(BEHN_SIM_HTML, height=600, scrolling=False)

        # ====================================================================
        #  PROCEDIMIENTO PASO A PASO
        # ====================================================================
        st.markdown("---")
        with st.expander("Procedimiento Paso a Paso: Cómo Obtener Zₛ Gráficamente", expanded=True):
            st.markdown(
                "El método de Behn-Eschenburg se ejecuta en **5 pasos** secuenciales:\n\n"
                "**Paso 1 — Realizar el Ensayo de Vacío (OCC)**\n\n"
                "Con la máquina girando a $n_s$ y bornes abiertos, se varía $I_{exc}$ desde 0 hasta un valor "
                "suficiente para superar el codo de saturación. Se registran los pares $(I_{exc}, E_0)$ y se "
                "dibuja la **Curva de Vacío** (curva dorada en el diagrama).\n\n"
                "---\n\n"
                "**Paso 2 — Realizar el Ensayo de Cortocircuito (SCC)**\n\n"
                "Con los bornes cortocircuitados a través de amperímetros, se repite el barrido de $I_{exc}$ "
                "(partiendo de cero por seguridad). Se registran los pares $(I_{exc}, I_{cc})$ y se dibuja la "
                "**Curva de Cortocircuito** (recta azul en el diagrama). Esta curva es siempre una recta "
                "que pasa por el origen.\n\n"
                "---\n\n"
                "**Paso 3 — Seleccionar un punto de excitación $I_{exc}$ en la zona lineal**\n\n"
                "Se elige un valor de $I_{exc}$ que esté **dentro de la zona lineal** de la curva de vacío "
                "(antes del codo de saturación). Se traza una línea vertical en ese punto del eje de abscisas.\n\n"
                "---\n\n"
                "**Paso 4 — Leer los valores de $E_0$ e $I_{cc}$**\n\n"
                "La intersección de la vertical con la curva OCC da el valor de $E_0$ (tensión de vacío). "
                "La intersección con la recta SCC da el valor de $I_{cc}$ (corriente de cortocircuito). "
                "Ambos valores corresponden **al mismo $I_{exc}$**.\n\n"
                "---\n\n"
                "**Paso 5 — Calcular la Impedancia Síncrona**\n\n"
                "Se aplica directamente la relación:\n\n"
                "$$Z_s = \\frac{E_0 \\text{ (de la curva OCC)}}{I_{cc} \\text{ (de la curva SCC)}}$$\n\n"
                "Y la reactancia síncrona se obtiene separando la componente resistiva:\n\n"
                "$$X_s = \\sqrt{Z_s^2 - R_a^2}$$\n\n"
                "donde $R_a$ se mide independientemente con un ensayo en corriente continua entre bornes "
                "del estator (máquina parada)."
            )

        # ====================================================================
        #  FÓRMULAS Y NOTAS DE INGENIERÍA
        # ====================================================================
        st.markdown("---")
        with st.expander("Base Matemática y Notas de Ingeniería", expanded=False):
            st.markdown(
                "#### Deducción Formal\n\n"
                "En el ensayo de vacío ($I_a = 0$), la ecuación del circuito equivalente se reduce a:\n\n"
                "$$\\vec{U}_0 = \\vec{E}_0 \\quad \\Rightarrow \\quad U_0 = E_0$$\n\n"
                "En el ensayo de cortocircuito ($U_1 = 0$), la ecuación se reduce a:\n\n"
                "$$0 = \\vec{E}_0 - \\vec{I}_{cc} \\cdot Z_s \\quad \\Rightarrow \\quad Z_s = \\frac{E_0}{I_{cc}}$$\n\n"
                "Combinando ambas medidas **para el mismo valor de $I_{exc}$**:\n\n"
                "$$\\boxed{Z_s = \\frac{E_0(I_{exc})}{I_{cc}(I_{exc})} = \\frac{k_{OCC}}{k_{SCC}}}$$\n\n"
                "donde $k_{OCC}$ y $k_{SCC}$ son las pendientes de las curvas en la zona lineal. "
                "Obsérvese que $Z_s$ en régimen lineal es **constante** e independiente de $I_{exc}$, "
                "ya que ambas curvas son rectas que pasan por el origen.\n\n"
                "---\n\n"
                "#### Notas de Ingeniería\n\n"
                "1. **Sobreestimación de $Z_s$:** Al utilizar la pendiente de la OCC en zona lineal "
                "(que es la pendiente más empinada posible), se obtiene un $E_0$ mayor que el real "
                "en condiciones de saturación. Esto produce un $Z_s$ calculado **mayor** que el verdadero, "
                "y por tanto una corriente de cortocircuito estimada **menor** que la real. Es un cálculo "
                "conservador para la regulación de tensión, pero **no conservador para la protección** "
                "(subestima las corrientes de falta).\n\n"
                "2. **Validez:** El método es riguroso únicamente si la máquina trabaja en la zona lineal "
                "(excitación baja o máquinas con gran entrehierro). Para máquinas que operan cerca de la "
                "saturación (la inmensa mayoría de las máquinas comerciales a tensión nominal), se debe "
                "recurrir al método de Potier.\n\n"
                "3. **Aproximación $Z_s \\approx X_s$:** En máquinas de potencia media y grande, la relación "
                "$X_s / R_a$ supera típicamente el valor de 10-100. Por ello, el error al despreciar $R_a$ "
                "es inferior al 1%, y se asume directamente $Z_s \\approx X_s$.\n\n"
                "4. **Valores típicos de $X_s$ en por unidad (p.u.):**\n"
                "   - Turbogeneradores (polos lisos): $X_s \\approx 1.0 - 2.0$ p.u.\n"
                "   - Hidrogeneradores (polos salientes): $X_d \\approx 0.6 - 1.2$ p.u., $X_q \\approx 0.4 - 0.8$ p.u."
            )

    # --------------------------------------------------------------------------
    # PESTAÑA 7: MÉTODO GRÁFICO DE POTIER
    # --------------------------------------------------------------------------
    with tab_potier:
        st.markdown("### Metodo Grafico de Potier (obtener impedancia síncrona en RÉGIMEN NO LINEAL o de SATURACIÓN)")
        st.markdown(
            "El **metodo de Potier** es la tecnica experimental clasica y mas rigurosa para separar los dos efectos "
            "que componen la impedancia sincrona aparente: la **reactancia de dispersion** ($X_\\sigma$ o $X_p$) "
            "y la **reaccion de inducido** ($F_a$). Es imprescindible cuando la maquina opera en la zona saturada "
            "de su curva magnetica, donde el metodo simplificado ($X_s = E_0 / I_{cc}$) introduce errores inaceptables."
        )

        # ====================================================================
        #  DEFINICIONES PREVIAS
        # ====================================================================
        st.markdown("---")
        st.markdown("#### Definiciones Previas Fundamentales")
        col_def1, col_def2 = st.columns(2)
        with col_def1:
            st.markdown(
                "**f.e.m. (Fuerza Electromotriz) — $E_0$**\n\n"
                "Es la tension interna inducida en el estator por el giro del campo magnetico del rotor. "
                "Se mide directamente en bornes cuando la maquina gira a $n_s$ **sin carga conectada** (ensayo de vacio). "
                "Su valor depende exclusivamente de la corriente de excitacion del rotor:\n\n"
                "$$E_0 = K \\cdot \\Phi_{exc} \\cdot n_s$$"
            )
        with col_def2:
            st.markdown(
                "**f.m.m. (Fuerza Magnetomotriz) — $\\mathcal{F}$**\n\n"
                "Es el impulso magnetico creado por una corriente circulando por un devanado. "
                "En la maquina sincrona coexisten dos f.m.m.:\n\n"
                "- $\\mathcal{F}_{exc}$: creada por la CC del rotor (corriente de excitacion $I_{exc}$).\n"
                "- $\\mathcal{F}_a$: creada por la CA del estator (corriente de armadura $I_a$). "
                "Esta **se opone** parcialmente al flujo del rotor — efecto conocido como *reaccion de inducido*."
            )

        # ====================================================================
        #  ENSAYOS NECESARIOS
        # ====================================================================
        st.markdown("---")
        st.markdown("#### Ensayos Experimentales Necesarios")
        st.markdown(
            "Para aplicar el metodo de Potier se necesitan **tres ensayos** realizados sobre la maquina "
            "girando a velocidad de sincronismo ($n_s$):"
        )
        col_e1, col_e2, col_e3 = st.columns(3)
        with col_e1:
            st.markdown(
                "**1. Ensayo de Vacio (OCC)**\n\n"
                "La maquina gira a $n_s$ con bornes abiertos (sin carga). "
                "Se varia $I_{exc}$ y se mide la tension en bornes $U_0 = E_0$.\n\n"
                "Resultado: curva $E_0$ vs $I_{exc}$ — la **Caracteristica de Vacio**."
            )
        with col_e2:
            st.markdown(
                "**2. Ensayo de Cortocircuito (SCC)**\n\n"
                "Se cortocircuitan los bornes del estator. Se eleva $I_{exc}$ hasta que la "
                "corriente de armadura alcance su valor **nominal** $I_{a,n}$.\n\n"
                "Resultado: se obtiene $I_{exc,cc}$ — la excitacion de cortocircuito para $I_{a,n}$."
            )
        with col_e3:
            st.markdown(
                "**3. Ensayo de Carga Reactiva Pura (ZPFC)**\n\n"
                "La maquina alimenta una carga puramente inductiva ($\\cos\\varphi = 0$ en retraso) "
                "manteniendo $I_a = I_{a,n}$. Se varia $I_{exc}$ y se mide la tension en bornes.\n\n"
                "Resultado: curva $U$ vs $I_{exc}$ a $\\cos\\varphi = 0$ — la **Caracteristica Reactiva**."
            )

        # ====================================================================
        #  DATOS DE ENTRADA DEL USUARIO
        # ====================================================================
        st.markdown("---")
        st.markdown("#### Datos de la Maquina y Ensayos")
        st.markdown(
            "Introduce los datos nominales y los puntos medidos en cada ensayo. "
            "Los valores por defecto corresponden a un alternador trifasico tipico de laboratorio."
        )

        col_params, col_occ, col_zpfc = st.columns([1, 1.5, 1.5])

        with col_params:
            st.markdown("**Parametros Nominales**")
            Un_fase = st.number_input("Tension nominal de fase Un (V)", value=2300.0, step=100.0, format="%.1f", key="potier_un")
            Ia_nom = st.number_input("Corriente nominal Ia,n (A)", value=100.0, step=10.0, format="%.1f", key="potier_ia")
            Iexc_cc = st.number_input("Iexc de cortocircuito para Ia,n (A)", value=3.0, step=0.5, format="%.2f", key="potier_icc")

        with col_occ:
            st.markdown("**Curva de Vacio (OCC) — puntos medidos**")
            st.caption("Introduce pares (Iexc, E0) separados por comas, un par por linea.")
            occ_default = "0.0, 0\n1.0, 800\n2.0, 1550\n3.0, 2100\n4.0, 2450\n5.0, 2650\n6.0, 2780\n7.0, 2870\n8.0, 2930\n9.0, 2970\n10.0, 3000"
            occ_text = st.text_area("Iexc (A), E0 (V)", value=occ_default, height=200, key="potier_occ")

        with col_zpfc:
            st.markdown("**Curva ZPFC (cosfi=0) — puntos medidos**")
            st.caption("Introduce pares (Iexc, U) a Ia = Ia,n y cosfi = 0.")
            zpfc_default = "3.0, 0\n4.0, 550\n5.0, 1100\n6.0, 1550\n7.0, 1850\n8.0, 2080\n9.0, 2250\n10.0, 2380\n11.0, 2480\n12.0, 2550"
            zpfc_text = st.text_area("Iexc (A), U (V)", value=zpfc_default, height=200, key="potier_zpfc")

        # ====================================================================
        #  PARSEO DE DATOS
        # ====================================================================
        def parse_curve(text):
            xs, ys = [], []
            for line in text.strip().split("\n"):
                line = line.strip()
                if not line:
                    continue
                parts = line.split(",")
                if len(parts) >= 2:
                    try:
                        xs.append(float(parts[0].strip()))
                        ys.append(float(parts[1].strip()))
                    except ValueError:
                        pass
            return np.array(xs), np.array(ys)

        occ_iexc, occ_e0 = parse_curve(occ_text)
        zpfc_iexc, zpfc_u = parse_curve(zpfc_text)

        if len(occ_iexc) < 3 or len(zpfc_iexc) < 3:
            st.error("Se necesitan al menos 3 puntos para cada curva (OCC y ZPFC).")
        else:
            # ==================================================================
            #  CALCULOS DEL METODO DE POTIER (Fig. 5.23)
            # ==================================================================
            # Nomenclatura segun la figura de referencia:
            #   A  = punto sobre la curva ZPFC a tension nominal V
            #   D  = punto de construccion (A desplazado a la izquierda por Ie_cc)
            #   C  = interseccion de la paralela desde D con la OCC (= Er)
            #   B  = proyeccion vertical de C sobre la linea horizontal V
            #   Triangulo de Potier = CBA (vertice C arriba, base BA horizontal)
            #   CB (vertical) = X_sigma * I = caida por reactancia de dispersion
            #   BA (horizontal) = F_i = reaccion de inducido

            # --- Pendiente de la recta de entrehierro (zona lineal de la OCC) ---
            idx_lin = occ_e0 > 0
            if np.sum(idx_lin) >= 2:
                i_lin = occ_iexc[idx_lin][:2]
                e_lin = occ_e0[idx_lin][:2]
                m_airgap = (e_lin[1] - e_lin[0]) / (i_lin[1] - i_lin[0])
            else:
                m_airgap = occ_e0[1] / occ_iexc[1] if occ_iexc[1] != 0 else 1.0

            # --- Punto A: sobre la ZPFC a tension nominal V ---
            if Un_fase <= np.max(zpfc_u) and Un_fase >= np.min(zpfc_u):
                Ie_A = float(np.interp(Un_fase, zpfc_u, zpfc_iexc))
            else:
                Ie_A = float(zpfc_iexc[-1])
                st.warning(f"La tension nominal ({Un_fase:.0f} V) esta fuera del rango de la curva ZPFC. "
                           f"Se usa el ultimo punto disponible: Ie = {Ie_A:.2f} A.")
            V_nom = Un_fase  # tension nominal = V en la figura

            # --- Punto D: desde A retroceder Ie_cc a la izquierda (horizontal) ---
            Ie_D = Ie_A - Iexc_cc
            V_D = V_nom  # misma altura

            # --- Desde D, trazar paralela a la recta de entrehierro hacia ARRIBA-DERECHA ---
            # hasta cortar la OCC → punto C
            iexc_fine = np.linspace(float(occ_iexc[0]), float(occ_iexc[-1]), 1000)
            occ_interp = np.interp(iexc_fine, occ_iexc, occ_e0)
            line_from_D = V_D + m_airgap * (iexc_fine - Ie_D)

            # Buscar interseccion (OCC cruza la linea paralela)
            diff = occ_interp - line_from_D
            sign_changes = np.where(np.diff(np.sign(diff)))[0]

            # Filtrar solo intersecciones a la DERECHA de D
            valid_crossings = [idx for idx in sign_changes if iexc_fine[idx] > Ie_D]

            if len(valid_crossings) > 0:
                idx_cross = valid_crossings[0]
                i1, i2 = iexc_fine[idx_cross], iexc_fine[idx_cross + 1]
                d1, d2 = diff[idx_cross], diff[idx_cross + 1]
                Ie_C = float(i1 - d1 * (i2 - i1) / (d2 - d1))
                Er = float(np.interp(Ie_C, occ_iexc, occ_e0))
            else:
                idx_closest = np.argmin(np.abs(diff[iexc_fine > Ie_D]))
                offset = np.sum(iexc_fine <= Ie_D)
                Ie_C = float(iexc_fine[offset + idx_closest])
                Er = float(occ_interp[offset + idx_closest])
                st.warning("No se encontro interseccion clara entre la paralela y la OCC. "
                           "Revisa los datos de entrada.")

            # --- Punto B: proyeccion vertical de C sobre la horizontal V ---
            Ie_B = Ie_C
            V_B = V_nom

            # --- Segmentos del Triangulo de Potier CBA ---
            CB_voltage = Er - V_nom        # Cateto vertical = X_sigma * I
            BA_excitation = Ie_A - Ie_B    # Cateto horizontal = F_i (reaccion de inducido)
            DA_excitation = Iexc_cc        # Hipotenusa base = Ie_cc (construccion)

            # --- Parametros calculados ---
            X_sigma = CB_voltage / Ia_nom if Ia_nom > 0 else 0.0
            Fi = BA_excitation  # Reaccion de inducido

            # --- Datos para el grafico ---
            iexc_ag = np.linspace(0, float(occ_iexc[-1]), 100)
            e_ag = m_airgap * iexc_ag

            # ==================================================================
            #  DIAGRAMA INTERACTIVO (Fig. 5.23b)
            # ==================================================================
            st.markdown("---")
            st.markdown("#### Diagrama de Potier — Construccion Grafica (Fig. 5.23)")

            fig = go.Figure()

            # --- Curva OCC (Curva de vacio) ---
            fig.add_trace(go.Scatter(
                x=occ_iexc, y=occ_e0, mode='lines+markers',
                name='Curva de vacio (OCC)',
                line=dict(color='#00ADB5', width=3),
                marker=dict(size=5, color='#00ADB5')
            ))

            # --- Curva ZPFC (Curva de reactiva) ---
            fig.add_trace(go.Scatter(
                x=zpfc_iexc, y=zpfc_u, mode='lines+markers',
                name='Curva de reactiva (ZPFC)',
                line=dict(color='#F9A826', width=3),
                marker=dict(size=5, color='#F9A826')
            ))

            # --- Recta de entrehierro ---
            fig.add_trace(go.Scatter(
                x=iexc_ag, y=e_ag, mode='lines',
                name='Recta Entrehierro',
                line=dict(color='#8b949e', width=1.5, dash='dash')
            ))

            # --- Linea horizontal V (tension nominal) ---
            fig.add_trace(go.Scatter(
                x=[0, Ie_A + 2], y=[V_nom, V_nom], mode='lines',
                name=f'V = {V_nom:.0f} V',
                line=dict(color='#484f58', width=1.5, dash='dot'),
                showlegend=True
            ))

            # --- Linea horizontal Er ---
            fig.add_trace(go.Scatter(
                x=[0, Ie_C + 0.5], y=[Er, Er], mode='lines',
                name=f'Er = {Er:.0f} V',
                line=dict(color='#484f58', width=1, dash='dot'),
                showlegend=True
            ))

            # --- Punto A (ZPFC a V) ---
            fig.add_trace(go.Scatter(
                x=[Ie_A], y=[V_nom], mode='markers+text',
                name=f'A (Ie={Ie_A:.2f} A, V={V_nom:.0f} V)',
                marker=dict(size=13, color='#F9A826', symbol='circle',
                            line=dict(width=2, color='white')),
                text=['A'], textposition='top right',
                textfont=dict(size=15, color='#F9A826', family='serif')
            ))

            # --- Punto D (construccion: A - Ie_cc) ---
            fig.add_trace(go.Scatter(
                x=[Ie_D], y=[V_D], mode='markers+text',
                name=f'D (Ie={Ie_D:.2f} A)',
                marker=dict(size=10, color='#c9d1d9', symbol='circle',
                            line=dict(width=2, color='white')),
                text=['D'], textposition='top left',
                textfont=dict(size=15, color='#c9d1d9', family='serif')
            ))

            # --- Segmento DA (horizontal, = Ie_cc) ---
            fig.add_trace(go.Scatter(
                x=[Ie_D, Ie_A], y=[V_D, V_nom], mode='lines',
                name=f'DA = Ie_cc = {Iexc_cc:.2f} A',
                line=dict(color='#EF4444', width=2),
                showlegend=True
            ))

            # --- Paralela desde D a la recta de entrehierro ---
            i_par_start = max(Ie_D - 0.3, 0)
            i_par_end = min(Ie_C + 0.5, float(occ_iexc[-1]))
            i_parallel = np.linspace(i_par_start, i_par_end, 80)
            e_parallel = V_D + m_airgap * (i_parallel - Ie_D)
            fig.add_trace(go.Scatter(
                x=i_parallel, y=e_parallel, mode='lines',
                name='Paralela desde D',
                line=dict(color='#3B82F6', width=2, dash='dash')
            ))

            # --- Punto C (interseccion con OCC) ---
            fig.add_trace(go.Scatter(
                x=[Ie_C], y=[Er], mode='markers+text',
                name=f'C (Ie={Ie_C:.2f} A, Er={Er:.0f} V)',
                marker=dict(size=13, color='#3B82F6', symbol='circle',
                            line=dict(width=2, color='white')),
                text=['C'], textposition='top left',
                textfont=dict(size=15, color='#3B82F6', family='serif')
            ))

            # --- Punto B (proyeccion de C sobre V-line) ---
            fig.add_trace(go.Scatter(
                x=[Ie_B], y=[V_B], mode='markers+text',
                name=f'B (Ie={Ie_B:.2f} A, V={V_B:.0f} V)',
                marker=dict(size=13, color='#c9d1d9', symbol='circle',
                            line=dict(width=2, color='white')),
                text=['B'], textposition='bottom left',
                textfont=dict(size=15, color='#c9d1d9', family='serif')
            ))

            # --- Triangulo de Potier CBA (relleno) ---
            fig.add_trace(go.Scatter(
                x=[Ie_C, Ie_B, Ie_A, Ie_C],
                y=[Er, V_B, V_nom, Er],
                fill='toself',
                fillcolor='rgba(59,130,246,0.10)',
                line=dict(color='#3B82F6', width=2.5),
                name='Triangulo de Potier (CBA)',
                showlegend=True
            ))

            # --- Punto M en eje X (debajo de A) ---
            fig.add_annotation(
                x=Ie_A, y=0, text="<b>M</b>",
                showarrow=True, arrowhead=0, arrowwidth=1, arrowcolor='#484f58',
                ay=-25, font=dict(color='#F9A826', size=12)
            )

            # --- Anotacion: segmento CB (vertical) = X_sigma * I ---
            fig.add_annotation(
                x=Ie_B - 0.6, y=(Er + V_nom) / 2,
                text=f"<b>CB = X<sub>σ</sub>·I</b><br>{CB_voltage:.0f} V",
                showarrow=False, font=dict(color='#3B82F6', size=12),
                align='right',
                bgcolor='rgba(13,17,23,0.8)', bordercolor='#3B82F6', borderwidth=1, borderpad=4
            )

            # --- Anotacion: segmento BA (horizontal) = F_i ---
            fig.add_annotation(
                x=(Ie_B + Ie_A) / 2, y=V_nom - 100,
                text=f"<b>BA = F<sub>i</sub></b><br>{BA_excitation:.2f} A",
                showarrow=False, font=dict(color='#F9A826', size=12),
                align='center',
                bgcolor='rgba(13,17,23,0.8)', bordercolor='#F9A826', borderwidth=1, borderpad=4
            )

            # --- Anotacion: Er y V en eje Y ---
            fig.add_annotation(
                x=-0.3, y=Er, text=f"<b>E<sub>r</sub></b>={Er:.0f}",
                showarrow=False, font=dict(color='#3B82F6', size=11), xanchor='right'
            )
            fig.add_annotation(
                x=-0.3, y=V_nom, text=f"<b>V</b>={V_nom:.0f}",
                showarrow=False, font=dict(color='#c9d1d9', size=11), xanchor='right'
            )

            # --- Bracket X_sigma*I entre V y Er ---
            fig.add_trace(go.Scatter(
                x=[0.3, 0.3], y=[V_nom, Er], mode='lines',
                line=dict(color='#EF4444', width=2),
                showlegend=False
            ))
            fig.add_annotation(
                x=0.8, y=(V_nom + Er) / 2,
                text=f"<b>X<sub>σ</sub>·I</b>",
                showarrow=False, font=dict(color='#EF4444', size=13)
            )

            # --- Segmento F_i en eje X (de M hacia la derecha) ---
            fig.add_annotation(
                x=Ie_A + Fi / 2, y=-80,
                text=f"← F<sub>i</sub> = {Fi:.2f} A →",
                showarrow=False, font=dict(color='#F9A826', size=11)
            )
            # Punto F en el eje
            fig.add_annotation(
                x=Ie_A + Fi, y=0, text="<b>F</b>",
                showarrow=True, arrowhead=0, arrowwidth=1, arrowcolor='#484f58',
                ay=-25, font=dict(color='#c9d1d9', size=12)
            )

            fig.update_layout(
                xaxis_title="Corriente de Excitacion  Ie  o  Fe  (A)",
                yaxis_title="E₀ , V  (V)",
                plot_bgcolor='#0d1117',
                paper_bgcolor='#0d1117',
                font=dict(color='#c9d1d9', family='Segoe UI, sans-serif'),
                legend=dict(
                    bgcolor='rgba(22,27,34,0.9)', bordercolor='#30363d', borderwidth=1,
                    font=dict(size=11), x=0.01, y=0.99, xanchor='left', yanchor='top'
                ),
                xaxis=dict(gridcolor='#21262d', zerolinecolor='#30363d',
                           range=[-0.5, float(max(occ_iexc[-1], zpfc_iexc[-1])) + 1]),
                yaxis=dict(gridcolor='#21262d', zerolinecolor='#30363d',
                           range=[-150, float(max(occ_e0[-1], Er)) * 1.08]),
                height=560,
                margin=dict(l=70, r=30, t=30, b=70)
            )

            st.plotly_chart(fig, use_container_width=True)

            # ==================================================================
            #  EXPLICACION DE LA CONSTRUCCION PASO A PASO
            # ==================================================================
            st.markdown("---")
            st.markdown("#### Construccion del Triangulo de Potier — Paso a Paso")

            st.markdown(
                f"**Paso 1 — Punto A (punto de operacion nominal sobre la curva ZPFC):**\n\n"
                f"Sobre la curva de carga reactiva pura (ZPFC), localizamos el punto correspondiente "
                f"a la tension nominal en bornes $V = {V_nom:.0f}$ V. Este es el punto **A**, cuya "
                f"coordenada horizontal es $I_e = {Ie_A:.2f}$ A (punto **M** en el eje de abscisas). "
                f"Este valor es la excitacion total que el rotor necesita para mantener $V$ en bornes "
                f"alimentando una carga puramente inductiva a corriente nominal."
            )
            st.markdown(
                f"**Paso 2 — Punto D (retroceso por la excitacion de cortocircuito):**\n\n"
                f"Desde **A**, nos desplazamos **horizontalmente hacia la izquierda** una distancia igual "
                f"a la corriente de excitacion de cortocircuito $I_{{e,cc}} = {Iexc_cc:.2f}$ A "
                f"(obtenida del ensayo de cortocircuito a corriente nominal). "
                f"Este nuevo punto es **D**, situado en $(I_e = {Ie_D:.2f}$ A$,\\; V = {V_nom:.0f}$ V$)$. "
                f"El segmento $DA = I_{{e,cc}}$ representa toda la excitacion que, en cortocircuito, "
                f"se destina integramente a vencer la impedancia interna."
            )
            st.markdown(
                f"**Paso 3 — Punto C (interseccion con la curva de vacio):**\n\n"
                f"Desde **D**, trazamos una recta **paralela a la recta de entrehierro** "
                f"(pendiente $m = {m_airgap:.0f}$ V/A) en direccion ascendente-derecha. "
                f"Esta linea corta la **curva de vacio (OCC)** en el punto **C**, "
                f"a una tension $E_r = {Er:.0f}$ V y una excitacion $I_e = {Ie_C:.2f}$ A. "
                f"La tension $E_r$ es la **f.e.m. resultante** que el rotor debe producir internamente "
                f"para sostener $V$ en bornes tras las caidas internas."
            )
            st.markdown(
                f"**Paso 4 — Punto B (proyeccion vertical):**\n\n"
                f"Desde **C**, bajamos una vertical hasta la linea horizontal $V = {V_nom:.0f}$ V. "
                f"El pie de esta vertical es el punto **B** $(I_e = {Ie_B:.2f}$ A$,\\; V = {V_nom:.0f}$ V$)$. "
                f"El triangulo rectangulo **CBA** (angulo recto en B) es el **Triangulo de Potier**."
            )

            # ==================================================================
            #  INTERPRETACION DE CADA SEGMENTO
            # ==================================================================
            st.markdown("---")
            st.markdown("#### Significado Fisico de Cada Segmento")

            col_seg1, col_seg2, col_seg3 = st.columns(3)

            with col_seg1:
                st.markdown(
                    f"**Cateto vertical CB**\n\n"
                    f"- **Valor:** {CB_voltage:.0f} V\n"
                    f"- **Significado:** Caida de tension $X_\\sigma \\cdot I_a$ producida por la "
                    f"**reactancia de dispersion** del estator.\n"
                    f"- La diferencia $E_r - V$ mide exactamente cuanto voltaje \"se pierde\" "
                    f"en el flujo de dispersion (flujo que no cruza el entrehierro)."
                )

            with col_seg2:
                st.markdown(
                    f"**Cateto horizontal BA**\n\n"
                    f"- **Valor:** {BA_excitation:.2f} A de excitacion\n"
                    f"- **Significado:** Es la f.m.m. de **reaccion de inducido** $F_i$. "
                    f"Representa cuanta excitacion adicional debe inyectar el rotor "
                    f"para compensar el campo desmagnetizante de la armadura.\n"
                    f"- El rotor necesita ${Ie_A:.2f}$ A en total, pero solo "
                    f"${Ie_B:.2f}$ A contribuyen al flujo util."
                )

            with col_seg3:
                st.markdown(
                    f"**Segmento DA (paso de construccion)**\n\n"
                    f"- **Valor:** {Iexc_cc:.2f} A de excitacion\n"
                    f"- **Significado:** Corriente de excitacion de cortocircuito $I_{{e,cc}}$ "
                    f"para $I_a = I_{{a,n}} = {Ia_nom:.0f}$ A.\n"
                    f"- Es el dato experimental del ensayo SCC que permite iniciar la "
                    f"construccion. En cortocircuito, toda esta f.m.m. se consume "
                    f"internamente ($V = 0$)."
                )

            # ==================================================================
            #  DIAGRAMA FASORIAL (Fig. 5.23a)
            # ==================================================================
            st.markdown("---")
            st.markdown("#### Diagrama Fasorial Asociado (Carga Inductiva Pura)")
            st.markdown(
                f"Para una carga puramente inductiva ($\\cos\\varphi = 0$), la corriente $I$ "
                f"esta retrasada 90 grados respecto a la tension $V$. En estas condiciones los fasores "
                f"se alinean verticalmente, lo que simplifica la relacion:\n\n"
                f"$$E_r = V + X_\\sigma \\cdot I_a = {V_nom:.0f} + {CB_voltage:.0f} = {Er:.0f} \\text{{ V}}$$\n\n"
                f"La f.m.m. resultante $F_r$ (leida en la OCC para $E_r$) debe sumarse a la reaccion "
                f"de inducido $F_i$ para obtener la excitacion total:\n\n"
                f"$$F_e = F_r + F_i$$\n\n"
                f"Para carga inductiva pura, $F_i$ se opone directamente a $F_r$ (mismo eje), "
                f"por lo que la suma es **aritmetica**. Para otros factores de potencia, la suma "
                f"es **vectorial** (fasorial)."
            )

            # ==================================================================
            #  CALCULO DE PARAMETROS
            # ==================================================================
            st.markdown("---")
            st.markdown("#### Calculo de los Parametros del Motor")

            st.markdown(
                f"**Paso 1 — Reactancia de dispersion de Potier ($X_\\sigma$):**\n\n"
                f"Del cateto vertical $CB$ del triangulo:\n\n"
                f"$$X_\\sigma \\cdot I_a = CB = E_r - V = {Er:.0f} - {V_nom:.0f} = {CB_voltage:.0f} \\text{{ V}}$$\n\n"
                f"$$X_\\sigma = \\frac{{CB}}{{I_{{a,n}}}} = \\frac{{{CB_voltage:.0f}}}{{{Ia_nom:.0f}}} = "
                f"\\boxed{{{X_sigma:.3f} \\; \\Omega}}$$"
            )

            st.markdown(
                f"**Paso 2 — Reaccion de inducido ($F_i$):**\n\n"
                f"Del cateto horizontal $BA$ del triangulo:\n\n"
                f"$$F_i = BA = I_{{e,A}} - I_{{e,B}} = {Ie_A:.2f} - {Ie_B:.2f} = "
                f"\\boxed{{{Fi:.2f} \\text{{ A de excitacion}}}}$$\n\n"
                f"Esto significa que, a corriente nominal, el efecto desmagnetizante "
                f"de la armadura equivale a ${Fi:.2f}$ A de excitacion."
            )

            # --- E_r y F_r ---
            # F_r = excitacion leida en la OCC para Er
            Fr = float(np.interp(Er, occ_e0, occ_iexc))

            st.markdown(
                f"**Paso 3 — f.e.m. resultante ($E_r$) y excitacion resultante ($F_r$):**\n\n"
                f"$$E_r = V + X_\\sigma \\cdot I_a = {V_nom:.0f} + {X_sigma:.3f} \\times {Ia_nom:.0f} = "
                f"\\boxed{{{V_nom + X_sigma * Ia_nom:.0f} \\text{{ V}}}}$$\n\n"
                f"Entrando con $E_r = {Er:.0f}$ V en la curva de vacio (OCC):\n\n"
                f"$$F_r = {Fr:.2f} \\text{{ A de excitacion}}$$"
            )

            st.markdown(
                f"**Paso 4 — Excitacion total necesaria ($F_e$):**\n\n"
                f"Para carga inductiva pura ($F_i$ se opone directamente a $F_r$):\n\n"
                f"$$F_e = F_r + F_i = {Fr:.2f} + {Fi:.2f} = "
                f"\\boxed{{{Fr + Fi:.2f} \\text{{ A}}}}$$\n\n"
                f"Este valor coincide (dentro de tolerancia) con la excitacion leida en el "
                f"punto **A** de la curva ZPFC: $I_{{e,A}} = {Ie_A:.2f}$ A, "
                f"confirmando la coherencia del metodo.\n\n"
                f"Para un factor de potencia generico $\\cos\\varphi$, la excitacion total "
                f"se obtiene mediante suma vectorial:\n\n"
                f"$$F_e = \\sqrt{{(F_r \\cos\\delta + F_i \\sin\\varphi)^2 + (F_r \\sin\\delta + F_i \\cos\\varphi)^2}}$$"
            )

            # ==================================================================
            #  RESUMEN DE RESULTADOS
            # ==================================================================
            st.markdown("---")
            st.markdown("#### Resumen de Resultados Obtenidos")
            col_r1, col_r2, col_r3, col_r4 = st.columns(4)
            with col_r1:
                st.metric(label="Reactancia de Potier (Xσ)", value=f"{X_sigma:.3f} Ω")
            with col_r2:
                st.metric(label="Caida X_σ·I (CB)", value=f"{CB_voltage:.0f} V")
            with col_r3:
                st.metric(label="Reaccion Inducido (Fi)", value=f"{Fi:.2f} A")
            with col_r4:
                st.metric(label="f.e.m. resultante (Er)", value=f"{Er:.0f} V")

            st.markdown(
                "**Propiedad fundamental del triangulo de Potier:** "
                "El triangulo $CBA$ es **invariante** en forma y tamano mientras la maquina "
                "gire a la misma velocidad y soporte la misma corriente de carga $I_a$. "
                "Si se desliza rigidamente manteniendo el vertice $C$ apoyado sobre la curva de vacio (OCC), "
                "el vertice $A$ traza exactamente la curva de reactiva (ZPFC)."
            )

if __name__ == "__main__":
    app()
