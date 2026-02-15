import json
import os
import streamlit as st

from app.config.loader import load_config
from app.pipeline.run import process_text_in_chunks
from app.visualization.visualizer import visualize_knowledge_graph

st.set_page_config(
    page_title="LLM Knowledge Graph",
    page_icon="🧠",
    layout="wide",
    initial_sidebar_state="expanded"
)

st.title("🧠 LLM Knowledge Graph Generator")
st.caption("Upload un texte → extraction (LLM) → standardisation → inférence → visualisation interactive")

# ---------------- Sidebar ----------------
st.sidebar.header("⚙️ Paramètres")

config_path = st.sidebar.text_input("Chemin config.toml", "config.toml")
output_html = st.sidebar.text_input("Sortie HTML", "storage/outputs/knowledge_graph.html")

debug = st.sidebar.checkbox("Debug (LLM raw)", value=False)
disable_std = st.sidebar.checkbox("Désactiver standardisation", value=False)
disable_inf = st.sidebar.checkbox("Désactiver inférence", value=False)

st.sidebar.markdown("---")
st.sidebar.info("Astuce : mets tes fichiers .txt dans `storage/inputs/`")

config = load_config(config_path)
if not config:
    st.error("❌ Impossible de charger config.toml. Vérifie le chemin.")
    st.stop()

# override config depuis UI
if disable_std:
    config.setdefault("standardization", {})["enabled"] = False
if disable_inf:
    config.setdefault("inference", {})["enabled"] = False

# ---------------- Main input area ----------------
colA, colB = st.columns([1.1, 1])

with colA:
    st.subheader("📄 Entrée")
    uploaded = st.file_uploader("Fichier .txt", type=["txt"])
    text_area = st.text_area("Ou colle ton texte ici", height=220, placeholder="Colle ton texte…")

with colB:
    st.subheader("🚀 Lancer")
    st.write("Clique pour générer le graphe.")
    run = st.button("Générer le graphe", use_container_width=True)

# ---------------- Run pipeline ----------------
if run:
    if uploaded is not None:
        input_text = uploaded.read().decode("utf-8", errors="ignore")
    else:
        input_text = text_area.strip()

    if not input_text:
        st.warning("⚠️ Ajoute un texte ou upload un fichier.")
        st.stop()

    with st.spinner("Extraction et construction du graphe en cours…"):
        triples = process_text_in_chunks(config, input_text, debug=debug)

    if not triples:
        st.error("❌ Aucun triplet extrait. Vérifie ton texte ou ton endpoint LLM.")
        st.stop()

    # save JSON next to HTML
    os.makedirs(os.path.dirname(output_html), exist_ok=True)
    json_path = output_html.replace(".html", ".json")
    with open(json_path, "w", encoding="utf-8") as f:
        json.dump(triples, f, indent=2, ensure_ascii=False)

    stats = visualize_knowledge_graph(triples, output_html, config=config)

    # ---------------- Results ----------------
    st.success("✅ Graphe généré avec succès")

    s1, s2, s3, s4 = st.columns(4)
    s1.metric("Nœuds", stats.get("nodes", 0))
    s2.metric("Arêtes", stats.get("edges", 0))
    s3.metric("Inférées", stats.get("inferred_edges", 0))
    s4.metric("Communautés", stats.get("communities", 0))

    st.subheader("🕸️ Visualisation")
    html = open(output_html, "r", encoding="utf-8").read()
    st.components.v1.html(html, height=780, scrolling=True)

    with st.expander("📦 Voir les triplets (JSON)"):
        st.json(triples)

    st.download_button(
        "Télécharger le JSON",
        data=json.dumps(triples, ensure_ascii=False, indent=2).encode("utf-8"),
        file_name=os.path.basename(json_path),
        mime="application/json",
        use_container_width=True
    )
