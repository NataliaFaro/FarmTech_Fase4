import os
import pandas as pd
import numpy as np
import joblib

from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression
from sklearn.metrics import mean_absolute_error, mean_squared_error, r2_score


# Caminho correto do CSV
pasta_projeto = os.path.dirname(os.path.dirname(__file__))

arquivo_csv = os.path.join(
    pasta_projeto,
    "data",
    "dados_agricolas_fase4.csv"
)

# Carregar CSV com tratamento da data
df = pd.read_csv(arquivo_csv)

df["data_coleta"] = pd.to_datetime(
    df["data_coleta"],
    format="%Y-%m-%d"
)

print("Base carregada com sucesso!")
print(df.head())
print("\nInformações da base:")
print(df.info())

# Variáveis de entrada
X = df[
    [
        "umidade_solo",
        "ph_solo",
        "temperatura_c",
        "irrigacao_mm",
        "fertilizante_kg"
    ]
]

# Variável que queremos prever
y = df["produtividade_kg_ha"]

# Separar dados em treino e teste
X_train, X_test, y_train, y_test = train_test_split(
    X,
    y,
    test_size=0.2,
    random_state=42
)

# Criar e treinar o modelo
modelo = LinearRegression()
modelo.fit(X_train, y_train)

# Fazer previsões
y_pred = modelo.predict(X_test)

# Calcular métricas
mae = mean_absolute_error(y_test, y_pred)
mse = mean_squared_error(y_test, y_pred)
rmse = np.sqrt(mse)
r2 = r2_score(y_test, y_pred)

print("\n===== MÉTRICAS DO MODELO =====")
print(f"MAE: {mae:.2f}")
print(f"MSE: {mse:.2f}")
print(f"RMSE: {rmse:.2f}")
print(f"R²: {r2:.4f}")

# Salvar modelo treinado
arquivo_modelo = os.path.join(
    pasta_projeto,
    "models",
    "modelo_produtividade.pkl"
)

joblib.dump(modelo, arquivo_modelo)

print("\nModelo salvo com sucesso!")
print(f"Local: {arquivo_modelo}")
