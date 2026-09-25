"""
☁️ WordCloud Studio — Nube de Palabras
Aplicación Streamlit con diseño cálido y colorido

Instalación:
    pip install streamlit wordcloud matplotlib pandas Pillow numpy

Ejecución:
    streamlit run wordcloud_app.py
"""

import streamlit as st
import matplotlib.pyplot as plt
import pandas as pd
import numpy as np
import re
import io
from collections import Counter
from wordcloud import WordCloud, STOPWORDS

# ─────────────────────────────────────────────
# CONFIGURACIÓN
# ─────────────────────────────────────────────
st.set_page_config(
    page_title="WordCloud Studio",
    page_icon="☁️",
    layout="wide",
    initial_sidebar_state="expanded",
)

# ─────────────────────────────────────────────
# ESTILOS — diseño cálido y colorido
# ─────────────────────────────────────────────
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&family=IBM+Plex+Mono:wght@400;500&display=swap');

    html, body, [class*="css"] {
        font-family: 'Inter', sans-serif;
    }

    /* Fondo general cálido, degradado suave */
    .stApp {
        background: linear-gradient(160deg, #fff8f0 0%, #ffedd9 45%, #ffe3d1 100%);
    }

    /* Sidebar cálida con acento coral */
    [data-testid="stSidebar"] {
        background-color: #fffaf3 !important;
        border-right: 1px solid #ffd8ad;
    }
    [data-testid="stSidebar"] h2,
    [data-testid="stSidebar"] h3 {
        color: #c2410c !important;
        font-weight: 700 !important;
        font-size: 0.95rem !important;
        text-transform: uppercase !important;
        letter-spacing: 0.8px !important;
    }
    [data-testid="stSidebar"] label {
        color: #7c4a2d !important;
        font-size: 0.85rem !important;
        font-weight: 500 !important;
    }
    [data-testid="stSidebar"] p {
        color: #92603f !important;
        font-size: 0.88rem !important;
    }
    [data-testid="stSidebar"] hr {
        border-color: #ffd8ad !important;
        margin: 16px 0 !important;
    }

    /* Inputs */
    textarea, input[type="text"] {
        background-color: #ffffff !important;
        border: 1px solid #ffcf9f !important;
        border-radius: 10px !important;
        color: #4a2b12 !important;
        font-family: 'Inter', sans-serif !important;
        font-size: 0.9rem !important;
    }
    textarea:focus, input[type="text"]:focus {
        border-color: #f2542d !important;
        box-shadow: 0 0 0 2px rgba(242,84,45,0.15) !important;
    }

    /* Selectbox */
    [data-baseweb="select"] > div {
        background: #ffffff !important;
        border: 1px solid #ffcf9f !important;
        border-radius: 10px !important;
        color: #4a2b12 !important;
        font-size: 0.9rem !important;
    }

    /* Títulos */
    h1 {
        font-family: 'Inter', sans-serif !important;
        color: #c2410c !important;
        font-weight: 800 !important;
        letter-spacing: -0.5px !important;
    }
    h2, h3, h4, h5, h6 {
        font-family: 'Inter', sans-serif !important;
        color: #9a3412 !important;
        font-weight: 700 !important;
    }
    p, li {
        color: #5b3a24 !important;
        font-size: 0.95rem !important;
        line-height: 1.65 !important;
    }

    /* Botón principal — degradado coral/naranja */
    .stButton > button {
        background: linear-gradient(135deg, #fb7f3f 0%, #f2542d 100%) !important;
        color: #ffffff !important;
        border: none !important;
        border-radius: 10px !important;
        font-family: 'Inter', sans-serif !important;
        font-weight: 700 !important;
        font-size: 0.92rem !important;
        letter-spacing: 0.3px !important;
        padding: 0.65rem 1.4rem !important;
        width: 100% !important;
        transition: transform 0.15s ease, box-shadow 0.2s ease !important;
    }
    .stButton > button:hover {
        transform: translateY(-1px) !important;
        box-shadow: 0 6px 16px rgba(242,84,45,0.35) !important;
    }

    /* Botón descarga — teal cálido */
    [data-testid="stDownloadButton"] button {
        background: linear-gradient(135deg, #17a398 0%, #0f9b8e 100%) !important;
        color: #ffffff !important;
        border: none !important;
        border-radius: 10px !important;
        font-weight: 700 !important;
        font-size: 0.88rem !important;
        transition: transform 0.15s ease !important;
    }
    [data-testid="stDownloadButton"] button:hover {
        transform: translateY(-1px) !important;
    }

    /* Métricas */
    [data-testid="metric-container"] {
        background: #fffaf3;
        border: 1px solid #ffdcb3;
        border-top: 4px solid #f2542d;
        border-radius: 12px;
        padding: 18px 22px;
        box-shadow: 0 2px 10px rgba(242,84,45,0.08);
    }
    [data-testid="metric-container"] label {
        color: #c2703f !important;
        font-size: 0.78rem !important;
        font-weight: 700 !important;
        text-transform: uppercase !important;
        letter-spacing: 0.6px !important;
    }
    [data-testid="metric-container"] [data-testid="stMetricValue"] {
        color: #9a3412 !important;
        font-weight: 800 !important;
        font-size: 1.55rem !important;
    }

    /* Header */
    .header-card {
        background: #fffaf3;
        border: 1px solid #ffdcb3;
        border-left: 6px solid #f2542d;
        border-radius: 14px;
        padding: 28px 36px;
        margin-bottom: 24px;
        box-shadow: 0 3px 14px rgba(242,84,45,0.1);
    }

    /* Sección card */
    .section-card {
        background: #fffaf3;
        border: 1px solid #ffdcb3;
        border-radius: 14px;
        padding: 24px 28px;
        margin-bottom: 16px;
        box-shadow: 0 2px 10px rgba(242,84,45,0.06);
    }

    /* Barras de frecuencia */
    .freq-row {
        display: flex;
        align-items: center;
        gap: 14px;
        padding: 7px 14px;
        margin: 4px 0;
        background: #fff3e6;
        border: 1px solid #ffe4c4;
        border-radius: 10px;
        transition: background 0.15s;
    }
    .freq-row:hover { background: #ffe9d3; }

    .freq-bar {
        height: 8px;
        background: linear-gradient(90deg, #fb7f3f, #f2542d);
        border-radius: 4px;
        display: inline-block;
        vertical-align: middle;
    }

    /* Tag de ranking */
    .rank-tag {
        background: #ffe4c4;
        border: 1px solid #ffcf9f;
        border-radius: 6px;
        padding: 1px 8px;
        font-size: 0.75rem;
        font-weight: 700;
        color: #c2410c;
        font-family: 'IBM Plex Mono', monospace;
        min-width: 36px;
        text-align: center;
    }

    /* Welcome items */
    .info-item {
        display: flex;
        align-items: flex-start;
        gap: 12px;
        padding: 12px 16px;
        background: #fff3e6;
        border: 1px solid #ffe4c4;
        border-radius: 10px;
        margin-bottom: 8px;
    }

    /* Uso cards */
    .uso-tag {
        display: inline-block;
        background: #ffe9d3;
        border: 1px solid #ffcf9f;
        border-radius: 20px;
        padding: 5px 14px;
        font-size: 0.85rem;
        font-weight: 600;
        color: #9a3412;
        margin: 4px 3px;
    }

    /* Expander */
    div[data-testid="stExpander"] {
        border: 1px solid #ffdcb3 !important;
        border-radius: 12px !important;
        background: #fffaf3 !important;
    }

    hr { border-color: #ffdcb3 !important; }

    /* Nube container */
    .wc-container {
        background: #fffaf3;
        border: 1px solid #ffdcb3;
        border-radius: 14px;
        padding: 20px;
        box-shadow: 0 3px 14px rgba(242,84,45,0.08);
        margin-bottom: 16px;
    }
</style>
""", unsafe_allow_html=True)


# ─────────────────────────────────────────────
# STOPWORDS
# ─────────────────────────────────────────────
STOPWORDS_ES = {
    "de","la","el","en","y","a","los","del","se","las","un","por","con","no","una","su",
    "para","es","al","lo","como","mas","pero","sus","le","ya","o","este","si","porque",
    "esta","entre","cuando","muy","sin","sobre","tambien","me","hasta","hay","donde",
    "quien","desde","nos","durante","ni","contra","ese","eso","ante","bajo","tras",
    "que","fue","son","han","ha","ser","era","estan","siendo","sido","he","has","hemos",
    "habian","tiene","tienen","hacer","puede","pueden","asi","tan","parte","todo","todos",
    "todas","cada","otro","otra","otros","otras","mismo","misma","nuestro","nuestra",
    "ellos","ellas","nosotros","les","esa","esos","esas","aquel","aquella","aquellos",
}

def obtener_stopwords(idioma):
    sw = set(STOPWORDS)
    if idioma in ("Español", "Ambos"):
        sw |= STOPWORDS_ES
    return sw


# ─────────────────────────────────────────────
# PALETAS PROFESIONALES
# ─────────────────────────────────────────────
PALETAS = {
    "Escala de grises":     ["#111827","#1f2937","#374151","#4b5563","#6b7280","#9ca3af","#d1d5db"],
    "Azul corporativo":     ["#1e3a5f","#1d4ed8","#2563eb","#3b82f6","#60a5fa","#93c5fd","#0f2942"],
    "Verde institucional":  ["#064e3b","#065f46","#047857","#059669","#10b981","#34d399","#6ee7b7"],
    "Gris azulado":         ["#0f172a","#1e293b","#334155","#475569","#64748b","#94a3b8","#cbd5e1"],
    "Terracota":            ["#7c2d12","#9a3412","#c2410c","#ea580c","#f97316","#fb923c","#fdba74"],
    "Índigo profundo":      ["#1e1b4b","#312e81","#3730a3","#4338ca","#4f46e5","#6366f1","#818cf8"],
    "Monocromático negro":  ["#000000","#111111","#222222","#444444","#666666","#888888","#aaaaaa"],
}

FORMAS = {
    "Rectángulo": None,
    "Círculo":    "circle",
}

def crear_mascara(forma, size=500):
    if forma == "circle":
        y, x = np.ogrid[:size, :size]
        cx, cy = size // 2, size // 2
        mascara = np.ones((size, size), dtype=np.uint8) * 255
        mascara[(x - cx)**2 + (y - cy)**2 <= (size // 2 - 12)**2] = 0
        return mascara
    return None


# ─────────────────────────────────────────────
# FUNCIONES CORE
# ─────────────────────────────────────────────
def limpiar_texto(texto, stopwords, min_longitud):
    texto = texto.lower()
    texto = re.sub(r"http\S+|www\S+", "", texto)
    texto = re.sub(r"[^a-záéíóúüñàâèêîôùûäëïöü\s]", " ", texto, flags=re.UNICODE)
    palabras = [p for p in texto.split() if p not in stopwords and len(p) >= min_longitud]
    return " ".join(palabras)


def contar_palabras(texto_limpio):
    return pd.DataFrame(Counter(texto_limpio.split()).most_common(50),
                        columns=["Palabra", "Frecuencia"])


def generar_wordcloud(texto_limpio, paleta_nombre, max_words, fondo, forma, ancho=1000, alto=520):
    import random
    colores = PALETAS[paleta_nombre]

    def color_func(word, font_size, position, orientation, random_state=None, **kwargs):
        rng = random_state or random.Random()
        return colores[rng.randint(0, len(colores) - 1)]

    mascara = crear_mascara(forma, size=min(ancho, alto))
    wc = WordCloud(
        width=ancho, height=alto, max_words=max_words,
        background_color=fondo, color_func=color_func,
        mask=mascara, collocations=False,
        min_font_size=11, max_font_size=120,
        prefer_horizontal=0.75, relative_scaling=0.5, margin=5,
    ).generate(texto_limpio)

    fig, ax = plt.subplots(figsize=(ancho / 100, alto / 100))
    ax.imshow(wc, interpolation="bilinear")
    ax.axis("off")
    fig.patch.set_facecolor(fondo)
    plt.tight_layout(pad=0)
    return fig


def fig_a_bytes(fig):
    buf = io.BytesIO()
    fig.savefig(buf, format="png", dpi=150, bbox_inches="tight",
                facecolor=fig.get_facecolor())
    buf.seek(0)
    return buf.read()


# ─────────────────────────────────────────────
# SIDEBAR
# ─────────────────────────────────────────────
with st.sidebar:
    st.markdown("## ☁️ WordCloud Studio")
    st.divider()

    # ── Fuente ──
    st.markdown("### ¿De dónde sacamos el texto?")
    fuente = st.radio("fuente", ["✍️ Escribir / Pegar", "📂 Subir archivo"],
                      label_visibility="collapsed")
    texto_input = ""

    if fuente == "✍️ Escribir / Pegar":
        texto_input = st.text_area(
            "Texto:", height=190,
            placeholder="Pega aquí lo que quieras: un artículo, una reseña, un discurso, respuestas de una encuesta...")

        with st.expander("¿No tienes texto a mano? Prueba con uno de estos"):
            ejemplos = {
                "Inteligencia Artificial": """
                La inteligencia artificial es una disciplina de la informática orientada a desarrollar
                sistemas capaces de ejecutar tareas que requieren capacidades cognitivas humanas.
                El aprendizaje automático, las redes neuronales profundas y el procesamiento del
                lenguaje natural constituyen los pilares técnicos de los sistemas modernos de
                inteligencia artificial. Los modelos de lenguaje de gran escala, la visión
                computacional y la robótica autónoma representan aplicaciones de vanguardia.
                La inteligencia artificial transforma sectores como la salud, la educación,
                la manufactura, las finanzas y el transporte, generando eficiencias significativas.
                """,
                "Colombia": """
                Colombia es una nación situada en el extremo noroccidental de América del Sur,
                reconocida por su excepcional biodiversidad, riqueza cultural y diversidad de paisajes.
                Bogotá es la capital y principal centro económico, seguida de Medellín, Cali y
                Barranquilla como ciudades de relevancia nacional. El café colombiano goza de
                reconocimiento internacional por su calidad y perfil aromático. La floricultura
                colombiana abastece mercados globales con alta competitividad. El país alberga
                ecosistemas del Amazonas, los Andes, el Caribe y el Pacífico, constituyéndose
                como uno de los territorios con mayor biodiversidad del planeta.
                """,
                "Tecnología 4.0": """
                La cuarta revolución industrial redefine los modelos productivos mediante la
                convergencia de tecnologías digitales avanzadas. El Internet de las cosas,
                la inteligencia artificial, el análisis de grandes datos, la robótica colaborativa
                y la automatización inteligente son pilares estratégicos de la industria moderna.
                Las fábricas inteligentes integran sensores, conectividad y analítica para
                optimizar procesos en tiempo real. La manufactura aditiva, los gemelos digitales
                y la realidad aumentada transforman la ingeniería de producción. La computación
                en la nube y la ciberseguridad son habilitadores fundamentales de la
                transformación digital empresarial.
                """,
            }
            ejemplo_sel = st.selectbox("Ejemplo:", list(ejemplos.keys()),
                                       label_visibility="collapsed")
            if st.button("Usar este texto"):
                st.session_state["texto_ejemplo"] = ejemplos[ejemplo_sel]
                st.rerun()

        if "texto_ejemplo" in st.session_state and not texto_input:
            texto_input = st.session_state["texto_ejemplo"]

    else:
        archivo = st.file_uploader("Archivo:", type=["txt", "csv"],
                                   label_visibility="collapsed")
        if archivo:
            if archivo.name.endswith(".txt"):
                texto_input = archivo.read().decode("utf-8", errors="ignore")
            elif archivo.name.endswith(".csv"):
                df_csv = pd.read_csv(archivo)
                col_txt = st.selectbox("Columna de texto:", df_csv.columns.tolist())
                texto_input = " ".join(df_csv[col_txt].dropna().astype(str).tolist())
            st.success(f"¡Listo! Cargamos {len(texto_input):,} caracteres")

    st.divider()

    # ── Procesamiento ──
    st.markdown("### Ajustes de limpieza")
    idioma         = st.selectbox("Ignorar palabras vacías (stopwords):", ["Español", "Inglés", "Ambos", "Ninguno"])
    min_longitud   = st.slider("Largo mínimo de cada palabra", 2, 8, 3)
    palabras_extra = st.text_input("¿Alguna palabra más que quieras excluir?",
                                   placeholder="ej: también, así, aquí")

    st.divider()

    # ── Apariencia ──
    st.markdown("### Cómo se va a ver")
    paleta_sel  = st.selectbox("Paleta de colores:", list(PALETAS.keys()))
    fondo_sel   = st.radio("Fondo:", ["Blanco", "Negro"], horizontal=True)
    fondo_color = "white" if fondo_sel == "Blanco" else "black"
    forma_sel   = st.selectbox("Forma:", list(FORMAS.keys()))
    max_words   = st.slider("¿Cuántas palabras como máximo?", 20, 200, 80)

    st.divider()
    generar = st.button("GENERAR NUBE  ↗", use_container_width=True)


# ─────────────────────────────────────────────
# CONTENIDO PRINCIPAL
# ─────────────────────────────────────────────

# Header
st.markdown("""
<div class="header-card">
    <h1 style="margin:0; font-size:1.9rem;">☁️ WordCloud Studio</h1>
    <p style="margin:6px 0 0 0; color:#9a5a34 !important; font-size:0.97rem;">
        Pega un texto y descubre en segundos qué palabras lo dominan
    </p>
</div>
""", unsafe_allow_html=True)

# ── Pantalla de bienvenida ──
if not generar or not texto_input.strip():
    col_izq, col_der = st.columns([3, 2], gap="large")

    with col_izq:
        st.markdown('<div class="section-card">', unsafe_allow_html=True)
        st.markdown("### ¿Qué es esto?")
        st.markdown("""
        Una **nube de palabras** es una forma rápida y visual de ver de qué habla un texto:
        las palabras que más se repiten aparecen más grandes, así que de un solo vistazo
        te haces una idea de los temas principales, sin tener que leerlo todo.
        """)

        for icono, titulo, desc in [
            ("📊", "Frecuencia de palabras", "Te mostramos qué términos se repiten más en tu texto."),
            ("🔍", "Filtrado inteligente", "Quitamos automáticamente las palabras que no aportan (como \"de\", \"el\", \"y\"...)."),
            ("🎨", "Tú eliges el estilo", "Elige la paleta de colores, la forma y cuántas palabras quieres ver."),
            ("⬇️", "Te lo llevas contigo", "Descarga la imagen en buena calidad o la tabla de frecuencias en CSV."),
        ]:
            st.markdown(
                f'<div class="info-item">'
                f'<span style="font-size:1.3rem; flex-shrink:0;">{icono}</span>'
                f'<div><strong style="color:#9a3412;">{titulo}</strong>'
                f'<p style="margin:2px 0 0 0; color:#92603f !important; font-size:0.88rem;">{desc}</p></div>'
                f'</div>',
                unsafe_allow_html=True,
            )

        st.markdown("#### ¿Cómo lo uso?")
        for i, paso in enumerate([
            "Escribe o pega tu texto en el panel de la izquierda (o sube un archivo).",
            "Ajusta el idioma de las palabras vacías, la paleta y cuántas palabras quieres ver.",
            "Dale clic a **GENERAR NUBE ↗**.",
            "Descarga tu nube en PNG o la tabla de frecuencias en CSV.",
        ], 1):
            st.markdown(f"**{i}.** {paso}")

        st.markdown('</div>', unsafe_allow_html=True)

    with col_der:
        st.markdown('<div class="section-card">', unsafe_allow_html=True)
        st.markdown("### ¿Para qué la puedes usar?")
        for caso in [
            "📰 Análisis de prensa y noticias",
            "📋 Resultados de encuestas abiertas",
            "💬 Reseñas y comentarios de clientes",
            "🎓 Trabajos y textos académicos",
            "🗳️ Discursos y documentos",
            "📚 Estudios literarios",
            "📊 Informes de negocio",
        ]:
            st.markdown(
                f'<span class="uso-tag">{caso}</span>',
                unsafe_allow_html=True,
            )
        st.markdown('</div>', unsafe_allow_html=True)

        st.markdown('<div class="section-card" style="margin-top:16px;">', unsafe_allow_html=True)
        st.markdown("### Paletas disponibles")
        for nombre in PALETAS.keys():
            st.markdown(
                f'<div style="padding:5px 0; border-bottom:1px solid #ffe4c4;">'
                f'<span style="color:#9a3412; font-size:0.88rem; font-weight:600;">{nombre}</span>'
                f'</div>',
                unsafe_allow_html=True,
            )
        st.markdown('</div>', unsafe_allow_html=True)

    if not texto_input.strip() and generar:
        st.warning("Antes de generar la nube, pega o sube un texto en el panel de la izquierda 👈")
    st.stop()


# ─────────────────────────────────────────────
# PROCESAMIENTO
# ─────────────────────────────────────────────
stopwords_set = obtener_stopwords(idioma) if idioma != "Ninguno" else set()
if palabras_extra.strip():
    stopwords_set |= {p.strip().lower() for p in palabras_extra.split(",") if p.strip()}

texto_limpio = limpiar_texto(texto_input, stopwords_set, min_longitud)

if not texto_limpio.strip():
    st.error("Con esta configuración no quedó ninguna palabra. Baja el largo mínimo o cambia las stopwords e inténtalo de nuevo.")
    st.stop()

df_freq        = contar_palabras(texto_limpio)
total_palabras = len(texto_limpio.split())
vocabulario    = len(df_freq)

# ── Métricas ──
m1, m2, m3, m4 = st.columns(4)
m1.metric("Palabras procesadas",     f"{total_palabras:,}")
m2.metric("Vocabulario único",       f"{vocabulario:,}")
m3.metric("Palabra más repetida",    df_freq.iloc[0]["Palabra"] if not df_freq.empty else "—")
m4.metric("Veces que aparece",       int(df_freq.iloc[0]["Frecuencia"]) if not df_freq.empty else 0)

st.markdown("<br>", unsafe_allow_html=True)

# ── Nube ──
with st.spinner("Armando tu nube de palabras..."):
    fig_wc = generar_wordcloud(
        texto_limpio, paleta_sel, max_words, fondo_color,
        FORMAS[forma_sel], ancho=1000, alto=520,
    )

st.markdown('<div class="wc-container">', unsafe_allow_html=True)
st.markdown(f"**Tu nube de palabras** &nbsp;·&nbsp; Paleta: *{paleta_sel}* &nbsp;·&nbsp; Fondo: *{fondo_sel}* &nbsp;·&nbsp; hasta {max_words} palabras")
st.pyplot(fig_wc, use_container_width=True)
st.markdown('</div>', unsafe_allow_html=True)

img_bytes = fig_a_bytes(fig_wc)
st.download_button(
    "⬇️ Descargar imagen PNG",
    data=img_bytes, file_name="wordcloud.png", mime="image/png",
    use_container_width=True,
)

st.divider()

# ── Análisis ──
col_freq, col_tabla = st.columns([3, 2], gap="large")

with col_freq:
    st.markdown("### Las 20 palabras que más se repiten")
    top20    = df_freq.head(20)
    max_freq = top20["Frecuencia"].max()

    for rank, (_, row) in enumerate(top20.iterrows(), 1):
        p = row["Palabra"]
        f = int(row["Frecuencia"])
        barra_w = max(12, int((f / max_freq) * 210))
        st.markdown(
            f'<div class="freq-row">'
            f'<span class="rank-tag">#{rank:02d}</span>'
            f'<span style="font-weight:600; color:#7c2d12; min-width:130px; font-size:0.93rem;">{p}</span>'
            f'<div class="freq-bar" style="width:{barra_w}px; opacity:{0.5 + 0.5*(f/max_freq):.2f};"></div>'
            f'<span style="font-family:\'IBM Plex Mono\',monospace; font-size:0.88rem; '
            f'color:#9a3412; min-width:28px; text-align:right; font-weight:600;">{f}</span>'
            f'</div>',
            unsafe_allow_html=True,
        )

with col_tabla:
    st.markdown("### Tabla completa")
    st.dataframe(
        df_freq.head(30).style
               .background_gradient(subset=["Frecuencia"], cmap="Oranges")
               .format({"Frecuencia": "{:,}"}),
        use_container_width=True, height=500,
    )
    csv_bytes = df_freq.to_csv(index=False).encode("utf-8")
    st.download_button(
        "⬇️ Exportar tabla (.csv)",
        data=csv_bytes, file_name="frecuencias.csv", mime="text/csv",
        use_container_width=True,
    )

st.divider()

with st.expander("Ver el texto ya limpio (sin las palabras vacías)"):
    preview = texto_limpio[:2500] + ("..." if len(texto_limpio) > 2500 else "")
    st.markdown(
        f'<p style="font-family:IBM Plex Mono,monospace; font-size:0.85rem; '
        f'color:#5b3a24; background:#fff3e6; padding:16px; border-radius:10px; '
        f'border:1px solid #ffe4c4; line-height:1.8;">{preview}</p>',
        unsafe_allow_html=True,
    )

plt.close("all")
