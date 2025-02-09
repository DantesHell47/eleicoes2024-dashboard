import streamlit as st
import pandas as pd
import plotly.express as px

@st.cache_data
def carregar_dados():
    df = pd.read_csv("eleicoes2024.csv")
    df = df.groupby(["NM_MUNICIPIO","DS_CARGO","NM_URNA_CANDIDATO","SG_PARTIDO"])["QT_VOTOS_NOMINAIS"].sum().reset_index().sort_values(by="QT_VOTOS_NOMINAIS")
    return df

df = carregar_dados()

st.title("CONSULTA MERDA DE MÉTRICAS DAS ELEIÇOES 2024")
st.divider()
st.write("## CANDIDATOS MAIS VOTADOS POR PARTIDO")

def verificador_df_vazio(municipio, partido):
    lista_partido = []
    for i in partido:
        if not df[(df.NM_MUNICIPIO == municipio) & (df.SG_PARTIDO == i) ].empty:
            lista_partido.append(i)
    return lista_partido

col1, col2 = st.columns(2)
with col1:
    municipio = st.selectbox("Selecione o municipio", df.NM_MUNICIPIO.sort_values().unique())
with col2:
    sigla_partido = verificador_df_vazio(municipio, df.SG_PARTIDO.sort_values().unique())
    sigla_partido = st.selectbox("Selecione a sigla do partido", sigla_partido)

df_filtrado = df[(df.NM_MUNICIPIO == municipio) & (df.SG_PARTIDO == sigla_partido)].sort_values(by="QT_VOTOS_NOMINAIS",ascending=False)

def plot_grafico_candidato_mais_votado():
    fig = px.bar(
        df_filtrado,
        y = "NM_URNA_CANDIDATO",
        x= "QT_VOTOS_NOMINAIS",
        orientation="h",
        color="NM_URNA_CANDIDATO",
        color_continuous_scale="Viridis",
        labels={"NM_URNA_CANDIDATO": "CANDIDATO", "QT_VOTOS_NOMINAIS":"VOTOS"},
        hover_data={"NM_URNA_CANDIDATO":False}
        )
    fig.update_layout(
        width=900,
        height=600,
        showlegend=False
    )
    fig.update_traces(hovertemplate="CANDIDATOS(a): %{y}<br> GADOS: %{x}")
    st.plotly_chart(fig)

    st.dataframe(df_filtrado, hide_index=True)
plot_grafico_candidato_mais_votado()

df_partido_mais_votado = df.groupby("SG_PARTIDO")["QT_VOTOS_NOMINAIS"].sum().reset_index()
df_partido_mais_votado = df_partido_mais_votado.sort_values(by="QT_VOTOS_NOMINAIS", ascending=False)

st.divider()
st.subheader("PARTIDOS MAIS VOTADOS (RANKING GERAL)")

def plotar_grafico_partido_geral():  
    fig = px.bar(
        df_partido_mais_votado,
        y = "SG_PARTIDO",
        x= "QT_VOTOS_NOMINAIS",
        orientation="h",
        color="SG_PARTIDO",
        color_continuous_scale="Viridis",
        # text_auto=True, 
        labels={"SG_PARTIDO": "PARTIDOS", "QT_VOTOS_NOMINAIS":"VOTOS"}
    )
    fig.update_layout(
        width=900,
        height=600,
        showlegend=False
    )
    fig.update_traces(hovertemplate="PARTIDO: %{y}<br> VOTOS: %{x}")
    st.plotly_chart(fig, use_container_width=True)

plotar_grafico_partido_geral()

df_partido_mais_votado["PERCENTUAL"] = (df_partido_mais_votado.QT_VOTOS_NOMINAIS / df.QT_VOTOS_NOMINAIS.sum()) * 100

def plot_pie():
    fig = px.pie(
        df_partido_mais_votado,
        names = "SG_PARTIDO",
        values="PERCENTUAL",
        title="PARTICIPAÇÃO PERCENTUAL DOS PARTIDOS",
        color_discrete_sequence = px.colors.qualitative.Set3
    )
    st.plotly_chart(fig, use_container_width=True)

plot_pie()

st.divider()
st.subheader("PARTIDOS MAIS VOTADOS (RANKING POR MUNICIPIO)")

municipio = st.selectbox("SELECIONE O MUNCIPIO", df.NM_MUNICIPIO.sort_values().unique())

df1 = df[df.NM_MUNICIPIO == municipio].groupby(["SG_PARTIDO"])["QT_VOTOS_NOMINAIS"].sum().reset_index().sort_values(by="QT_VOTOS_NOMINAIS", ascending=False)

def plotar_grafico_partidos_municipio():  
    fig = px.bar(
        df1,
        y = "SG_PARTIDO",
        x= "QT_VOTOS_NOMINAIS",
        orientation="h",
        color="SG_PARTIDO",
        color_continuous_scale="Viridis",
        # text_auto=True, 
        labels={"SG_PARTIDO": "PARTIDOS", "QT_VOTOS_NOMINAIS":"VOTOS"}
    )
    fig.update_layout(
        width=900,
        height=600,
        showlegend=False
    )
    fig.update_traces(hovertemplate="PARTIDO: %{y}<br> VOTOS: %{x}")
    st.plotly_chart(fig, use_container_width=True)

plotar_grafico_partidos_municipio()