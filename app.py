import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from datetime import datetime
import io
import json

st.set_page_config(page_title="PSICONR VISION ULTRA", page_icon="🧠", layout="wide")

st.title("🧠 PSICONR VISION ULTRA")
st.caption("Gestão de Riscos Psicossociais conforme NR-01")

st.success("✅ Sistema carregado com sucesso!")

# ==================== DIMENSÕES ====================
dimensoes = [
    "Demandas Quantitativas", "Ritmo de Trabalho", "Autonomia",
    "Apoio Social", "Qualidade da Liderança", "Justiça Organizacional",
    "Comportamentos Ofensivos", "Conflito Trabalho-Vida"
]

# ==================== UPLOAD ====================
st.subheader("📤 Upload das Respostas do Questionário")
st.info("Arquivo Excel ou CSV com as colunas: colaborador, setor, q1 até q40")

arquivo = st.file_uploader("Escolha o arquivo", type=["xlsx", "csv"])

if arquivo is not None:
    if arquivo.name.endswith(".csv"):
        df = pd.read_csv(arquivo)
    else:
        df = pd.read_excel(arquivo)

    st.success(f"✅ {len(df)} respostas carregadas!")

    if st.button("🚀 Gerar Diagnóstico Completo", type="primary", use_container_width=True):
        with st.spinner("Processando diagnóstico..."):
            scores = {}
            for i, dim in enumerate(dimensoes):
                cols = [f"q{j+1}" for j in range(i*5, (i+1)*5)]
                df_dim = df[cols].copy()

                for col in df_dim.columns:
                    idx = int(col[1:])
                    if idx in [3,4,8,
