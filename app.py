# =====================================================
# DASHBOARD DE VENTAS DE TECNOLOGÍA
# Autor: Tu Nombre
# =====================================================

import streamlit as st
import pandas as pd
import plotly.express as px

# ---------- CONFIGURACIÓN DE LA PÁGINA ----------
st.set_page_config(
    page_title="Dashboard Ventas Tecnología",
    page_icon="💻",
    layout="wide"
)

# ---------- CARGAR Y LIMPIAR DATOS ----------
@st.cache_data
def cargar_datos():
    df = pd.read_csv('ventas_tecnologia.csv')
    df = df.drop_duplicates()
    df['fecha'] = pd.to_datetime(df['fecha'])
    df['cliente'] = df['cliente'].fillna('Desconocido')
    mediana_edad = df['edad_cliente'].median()
    df['edad_cliente'] = df['edad_cliente'].fillna(mediana_edad)
    df['cantidad'] = df['cantidad'].fillna(df['cantidad'].median())
    df.loc[(df['edad_cliente'] < 18) | (df['edad_cliente'] > 100), 'edad_cliente'] = mediana_edad
    df.loc[df['cantidad'] > 5, 'cantidad'] = 5
    df['total_venta'] = df['cantidad'] * df['precio_unitario']
    df['mes'] = df['fecha'].dt.strftime('%Y-%m')
    return df

df = cargar_datos()

# ---------- TÍTULO ----------
st.title("💻 Dashboard de Ventas - Tienda de Tecnología")
st.markdown("Análisis interactivo de ventas de laptops, celulares y accesorios.")

# ---------- FILTROS LATERALES ----------
st.sidebar.header("🔎 Filtros")

ciudades = st.sidebar.multiselect(
    "Ciudad:",
    options=df['ciudad'].unique(),
    default=df['ciudad'].unique()
)

categorias = st.sidebar.multiselect(
    "Categoría:",
    options=df['categoria'].unique(),
    default=df['categoria'].unique()
)

df_filtrado = df[
    (df['ciudad'].isin(ciudades)) &
    (df['categoria'].isin(categorias))
]

# ---------- MÉTRICAS PRINCIPALES ----------
st.markdown("### 📊 Métricas Principales")
col1, col2, col3, col4 = st.columns(4)

col1.metric("💰 Ventas Totales", f"${df_filtrado['total_venta'].sum():,.0f}")
col2.metric("🛒 N° Transacciones", f"{len(df_filtrado):,}")
col3.metric("📦 Unidades Vendidas", f"{df_filtrado['cantidad'].sum():,}")
col4.metric("⭐ Satisfacción Prom.", f"{df_filtrado['satisfaccion'].mean():.2f}")

st.markdown("---")

# ---------- GRÁFICOS ----------
col_a, col_b = st.columns(2)

with col_a:
    st.subheader("📈 Ventas por Categoría")
    ventas_cat = df_filtrado.groupby('categoria')['total_venta'].sum().reset_index()
    fig1 = px.bar(ventas_cat, x='categoria', y='total_venta',
                  color='categoria', text_auto='.2s')
    st.plotly_chart(fig1, use_container_width=True)

with col_b:
    st.subheader("🥧 Distribución por Método de Pago")
    fig2 = px.pie(df_filtrado, names='metodo_pago', values='total_venta', hole=0.4)
    st.plotly_chart(fig2, use_container_width=True)

col_c, col_d = st.columns(2)

with col_c:
    st.subheader("🏙️ Ventas por Ciudad")
    ventas_ciudad = df_filtrado.groupby('ciudad')['total_venta'].sum().reset_index()
    fig3 = px.bar(ventas_ciudad, x='total_venta', y='ciudad',
                  orientation='h', color='total_venta',
                  color_continuous_scale='Blues')
    st.plotly_chart(fig3, use_container_width=True)

with col_d:
    st.subheader("📅 Evolución Mensual de Ventas")
    ventas_mes = df_filtrado.groupby('mes')['total_venta'].sum().reset_index()
    fig4 = px.line(ventas_mes, x='mes', y='total_venta', markers=True)
    st.plotly_chart(fig4, use_container_width=True)

# ---------- TABLA DE DATOS ----------
st.markdown("---")
st.subheader("📋 Detalle de Datos")
st.dataframe(df_filtrado, use_container_width=True)

st.markdown("---")
st.caption("Dashboard creado con Streamlit | Datos simulados con fines educativos")