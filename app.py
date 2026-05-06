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
                    if idx in [3,4,8,9,13,14,18,19,23,24,28,29,33,34,38,39]:
                        df_dim[col] = 6 - df_dim[col]

                score = df_dim.mean(axis=1).mean() * 20
                scores[dim] = round(score, 2)

            # Matriz de Risco
            matriz = pd.DataFrame([
                [dim, score, "Crítico" if score < 40 else "Alto" if score < 55 else "Moderado" if score < 70 else "Baixo"]
                for dim, score in scores.items()
            ], columns=["Dimensão", "Score (0-100)", "Nível de Risco"])

            # Plano de Ação Automático
            acoes = []
            for _, row in matriz.iterrows():
                if row["Nível de Risco"] in ["Crítico", "Alto"]:
                    acoes.append({
                        "Risco": row["Dimensão"],
                        "Ação Sugerida": f"Implementar plano imediato de redução de {row['Dimensão'].lower()}",
                        "Responsável": "RH + Liderança",
                        "Prazo": "30 dias",
                        "Prioridade": "Alta"
                    })
                elif row["Nível de Risco"] == "Moderado":
                    acoes.append({
                        "Risco": row["Dimensão"],
                        "Ação Sugerida": f"Monitorar e realizar ações preventivas em {row['Dimensão'].lower()}",
                        "Responsável": "RH",
                        "Prazo": "60 dias",
                        "Prioridade": "Média"
                    })
            plano = pd.DataFrame(acoes)

            # ==================== TABS ====================
            tab1, tab2, tab3, tab4 = st.tabs(["📊 Dashboard", "🕸️ Radar Chart", "📋 Matriz", "📋 Plano de Ação"])

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
                st.subheader("🕸️ Radar Chart de Riscos Psicossociais")
                fig3 = plt.figure(figsize=(10, 10))
                values = list(scores.values()) + [list(scores.values())[0]]
                angles = np.linspace(0, 2*np.pi, len(dimensoes), endpoint=False).tolist() + [0]
                ax = plt.subplot(111, polar=True)
                ax.plot(angles, values, 'o-', linewidth=2, color='#1f77b4')
                ax.fill(angles, values, alpha=0.25, color='#1f77b4')
                ax.set_thetagrids(np.degrees(angles[:-1]), dimensoes)
                st.pyplot(fig3)

            with tab3:
                st.subheader("📋 Matriz de Risco")
                st.dataframe(matriz, use_container_width=True)

            with tab4:
                st.subheader("📋 Plano de Ação Automático")
                st.dataframe(plano, use_container_width=True)
                csv = plano.to_csv(index=False).encode()
                st.download_button("Baixar Plano de Ação (CSV)", csv, "plano_acao.csv", "text/csv")

            st.success("✅ Diagnóstico completo gerado com sucesso!")
            st.balloons()

st.caption("PSICONR VISION © 2026 - Emanuelle Melo")
