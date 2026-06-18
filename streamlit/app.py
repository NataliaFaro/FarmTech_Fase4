import os
import pandas as pd
import streamlit as st
import joblib
import matplotlib.pyplot as plt
import seaborn as sns

st.set_page_config(
    page_title="FarmTech Solutions",
    layout="wide"
)

# Caminhos do projeto
pasta_projeto = os.path.dirname(os.path.dirname(__file__))

csv_path = os.path.join(
    pasta_projeto,
    "data",
    "dados_agricolas_fase4.csv"
)

modelo_path = os.path.join(
    pasta_projeto,
    "models",
    "modelo_produtividade.pkl"
)

# Carregar dados e modelo
df = pd.read_csv(csv_path)
modelo = joblib.load(modelo_path)

# Título
st.title("🌱 FarmTech Solutions")
st.subheader("Assistente Agrícola Inteligente")

# Indicadores principais
col1, col2, col3, col4 = st.columns(4)

col1.metric("Registros", len(df))
col2.metric("Umidade Média", round(df["umidade_solo"].mean(), 2))
col3.metric("pH Médio", round(df["ph_solo"].mean(), 2))
col4.metric("Produtividade Média", round(df["produtividade_kg_ha"].mean(), 2))

st.divider()

# Métricas do modelo
st.subheader("📊 Métricas do Modelo de Regressão")

m1, m2, m3, m4 = st.columns(4)

m1.metric("MAE", "446.13")
m2.metric("MSE", "283434.81")
m3.metric("RMSE", "532.39")
m4.metric("R²", "0.6907")

st.write(
    "O modelo de regressão linear foi treinado para prever a produtividade agrícola "
    "com base em umidade do solo, pH, temperatura, irrigação e fertilização."
)

st.divider()

# Visualização dos dados
st.subheader("📋 Visualização dos Dados")

st.dataframe(df.head(20), use_container_width=True)

st.divider()

# Correlação
st.subheader("📈 Correlação entre Variáveis")

corr = df.select_dtypes(include="number").corr()

st.dataframe(corr, use_container_width=True)

fig, ax = plt.subplots(figsize=(10, 6))
sns.heatmap(
    corr,
    annot=True,
    cmap="Blues",
    ax=ax
)

st.pyplot(fig)

st.divider()

# Gráfico de produtividade por cultura
st.subheader("🌾 Produtividade Média por Cultura")

prod_cultura = df.groupby("cultura")["produtividade_kg_ha"].mean().sort_values(ascending=False)

st.bar_chart(prod_cultura)

st.divider()

# Previsão
st.subheader("🤖 Previsão de Produtividade")

st.write(
    "Informe os parâmetros agrícolas abaixo para gerar uma previsão de produtividade "
    "e receber recomendações automáticas de manejo."
)

col_a, col_b = st.columns(2)

with col_a:
    umidade = st.slider("Umidade do Solo (%)", 40, 100, 65)
    ph = st.slider("pH do Solo", 4.0, 8.0, 6.5)
    temperatura = st.slider("Temperatura (°C)", 15, 40, 28)

with col_b:
    irrigacao = st.slider("Irrigação (mm)", 0, 30, 15)
    fertilizante = st.slider("Fertilizante (kg)", 0, 80, 40)

if st.button("Gerar Previsão"):

    dados = pd.DataFrame(
        [[umidade, ph, temperatura, irrigacao, fertilizante]],
        columns=[
            "umidade_solo",
            "ph_solo",
            "temperatura_c",
            "irrigacao_mm",
            "fertilizante_kg"
        ]
    )

    previsao = modelo.predict(dados)[0]

    st.success(f"Produtividade prevista: {previsao:.2f} kg/ha")

    st.subheader("💧 Recomendações de Manejo")

    if umidade < 60:
        st.warning("A umidade está baixa. Recomenda-se aumentar a irrigação.")
    elif umidade > 80:
        st.info("A umidade está elevada. Recomenda-se reduzir a irrigação.")
    else:
        st.success("A umidade está em faixa adequada.")

    if ph < 5.5:
        st.warning("O pH está baixo. Recomenda-se correção do solo.")
    elif ph > 7.2:
        st.warning("O pH está alto. Avaliar necessidade de ajuste no manejo.")
    else:
        st.success("O pH está em faixa adequada.")

    if fertilizante < 30:
        st.warning("O nível de fertilização está baixo. Avaliar reforço nutricional.")
    else:
        st.success("A fertilização está adequada.")

    if previsao >= 4500:
        st.success("Alto potencial produtivo.")
    elif previsao >= 3500:
        st.info("Potencial produtivo moderado.")
    else:
        st.warning("Potencial produtivo baixo. Recomenda-se revisar irrigação, pH e fertilização.")
