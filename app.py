import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from datetime import datetime
import io

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

                # Inversão dos itens positivos
                for col in df_dim.columns:
                    idx = int(col[1:])
                    if idx in [3,4,8,9,13,14,18,19,23,24,28,29,33,34,38,39]:
                        df_dim[col] = 6 - df_dim[col]

                score = df_dim.mean(axis=1).mean() * 20
                scores[dim] = round(score, 2)

            # Matriz de Risco
            matriz = pd.DataFrame([
                [dim, score, "Crítico" if score < 40 else "Alto" if score < 55 else "Moderado" if score < 70 else "Baixo"]
                for dim, score in scores.items()
            ], columns=["Dimensão", "Score (0-100)", "Nível de Risco"])

            # ==================== DASHBOARD ====================
            tab1, tab2, tab3 = st.tabs(["📊 Dashboard", "📋 Matriz", "📋 Plano de Ação"])

            with tab1:
                col1, col2 = st.columns(2)
                with col1:
                    fig, ax = plt.subplots(figsize=(10, 6))
                    sns.barplot(x=list(scores.values()), y=list(scores.keys()), palette="Blues_d", ax=ax)
                    ax.set_title("Scores por Dimensão")
                    st.pyplot(fig)
                with col2:
                    fig2, ax2 = plt.subplots(figsize=(10, 6))
                    colors = {"Crítico":"#d32f2f","Alto":"#f57c00","Moderado":"#fbc02d","Baixo":"#388e3c"}
                    sns.barplot(data=matriz, x="Score (0-100)", y="Dimensão",
                                palette=[colors[n] for n in matriz["Nível de Risco"]], ax=ax2)
                    ax2.set_title("Nível de Risco por Dimensão")
                    st.pyplot(fig2)

            with tab2:
                st.subheader("📋 Matriz de Risco")
                st.dataframe(matriz, use_container_width=True)

            with tab3:
                st.subheader("📋 Plano de Ação Automático")
                st.info("Plano de ação automático será gerado na próxima versão")

            st.success("✅ Diagnóstico gerado com sucesso!")
            st.balloons()

st.caption("PSICONR VISION © 2026 - Emanuelle Melo")
