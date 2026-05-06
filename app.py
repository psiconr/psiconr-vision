import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from datetime import datetime
import sqlite3
import bcrypt
import io
from reportlab.lib.pagesizes import A4
from reportlab.pdfgen import canvas

st.set_page_config(page_title="PSICONR VISION ULTRA", page_icon="🧠", layout="wide")

st.title("🧠 PSICONR VISION ULTRA")
st.caption("Gestão de Riscos Psicossociais - NR-01")

# Banco de dados simples
def init_db():
    conn = sqlite3.connect("psiconr_vision.db")
    c = conn.cursor()
    c.execute('''CREATE TABLE IF NOT EXISTS users (
                    id INTEGER PRIMARY KEY, 
                    email TEXT UNIQUE, 
                    password TEXT,
                    nome_empresa TEXT)''')
    c.execute('''CREATE TABLE IF NOT EXISTS diagnosticos (
                    id INTEGER PRIMARY KEY, 
                    user_id INTEGER, 
                    data TEXT,
                    scores TEXT)''')
    conn.commit()
    conn.close()

init_db()

st.success("✅ Sistema carregado com sucesso!")
st.info("Próximo passo: upload do questionário (q1 a q40)")

st.caption("PSICONR VISION © 2026 - Emanuelle Melo")
