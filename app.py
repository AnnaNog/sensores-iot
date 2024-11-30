import streamlit as st
import numpy as np
import pandas as pd
import plotly.express as px
from influxdb_client import InfluxDBClient, Point
from influxdb_client.client.write_api import SYNCHRONOUS
from datetime import datetime, timedelta
from sklearn.ensemble import IsolationForest
import time
import json
import os

# Configuração da página Streamlit
st.set_page_config(page_title="Detecção de Anomalias IoT", layout="wide")

# Estilo CSS personalizado
st.markdown("""
    <style>
    .main {
        padding: 2rem;
    }
    .stButton>button {
        width: 100%;
        margin-top: 1rem;
    }
    .metric-card {
        background-color: #f0f2f6;
        padding: 1rem;
        border-radius: 0.5rem;
        margin: 0.5rem 0;
    }
    </style>
""", unsafe_allow_html=True)

# Classe principal do aplicativo
class AnomalyDetectionApp:
    def __init__(self):
        self.load_config()
        self.initialize_influxdb()
        self.model = IsolationForest(contamination=0.1, random_state=42)
        
    def load_config(self):
        """Carrega ou solicita configurações do InfluxDB"""
        if 'influxdb_config' not in st.session_state:
            st.session_state.influxdb_config = {
                'url': '',
                'token': '',
                'org': '',
                'bucket': ''
            }
        
    def initialize_influxdb(self):
        """Inicializa conexão com InfluxDB"""
        try:
            self.client = InfluxDBClient(
                url=st.session_state.influxdb_config['url'],
                token=st.session_state.influxdb_config['token'],
                org=st.session_state.influxdb_config['org']
            )
            self.write_api = self.client.write_api(write_options=SYNCHRONOUS)
            self.query_api = self.client.query_api()
        except Exception as e:
            st.error(f"Erro ao conectar com InfluxDB: {str(e)}")
            
    def save_config(self, config):
        """Salva configurações do InfluxDB"""
        st.session_state.influxdb_config = config
        self.initialize_influxdb()
        
    def generate_sample_data(self, n_samples=100):
        """Gera dados de exemplo para temperatura e umidade"""
        now = datetime.utcnow()
        timestamps = [now - timedelta(minutes=i) for i in range(n_samples)]
        
        # Dados normais
        temp_base = 23.0
        humid_base = 60.0
        temperatures = [temp_base + np.random.normal(0, 1) for _ in range(n_samples)]
        humidity = [humid_base + np.random.normal(0, 2) for _ in range(n_samples)]
        
        # Inserindo algumas anomalias
        anomaly_indices = np.random.choice(n_samples, size=5, replace=False)
        for idx in anomaly_indices:
            temperatures[idx] = temp_base + np.random.normal(0, 5)
            humidity[idx] = humid_base + np.random.normal(0, 10)
            
        return timestamps, temperatures, humidity, anomaly_indices
        
    def write_data(self, timestamps, temperatures, humidity):
        """Escreve dados no InfluxDB"""
        try:
            for i in range(len(timestamps)):
                point = Point("sensores") \
                    .tag("local", "Fabrica") \
                    .field("temperatura", temperatures[i]) \
                    .field("umidade", humidity[i]) \
                    .time(timestamps[i])
                self.write_api.write(
                    bucket=st.session_state.influxdb_config['bucket'],
                    record=point
                )
            return True
        except Exception as e:
            st.error(f"Erro ao escrever dados: {str(e)}")
            return False
            
    def query_data(self, hours=1):
        """Consulta dados do InfluxDB"""
        query = f'''
        from(bucket: "{st.session_state.influxdb_config['bucket']}")
            |> range(start: -{hours}h)
            |> filter(fn: (r) => r["_measurement"] == "sensores")
            |> pivot(rowKey:["_time"], columnKey: ["_field"], valueColumn: "_value")
        '''
        
        try:
            result = self.query_api.query_data_frame(query=query)
            if isinstance(result, list):
                result = pd.concat(result)
            return result
        except Exception as e:
            st.error(f"Erro ao consultar dados: {str(e)}")
            return None
            
    def detect_anomalies(self, data):
        """Detecta anomalias nos dados usando Isolation Forest"""
        if data is None or len(data) == 0:
            return None
            
        # Preparar dados para detecção
        X = data[['temperatura', 'umidade']].values
        self.model.fit(X)
        
        # Predição (-1 para anomalias, 1 para normais)
        predictions = self.model.predict(X)
        return predictions == -1

    def render_config_page(self):
        """Renderiza página de configuração"""
        st.title("Configuração do InfluxDB Cloud")
        
        with st.form("config_form"):
            url = st.text_input("URL do InfluxDB", value=st.session_state.influxdb_config['url'])
            token = st.text_input("Token", value=st.session_state.influxdb_config['token'], type="password")
            org = st.text_input("Organização", value=st.session_state.influxdb_config['org'])
            bucket = st.text_input("Bucket", value=st.session_state.influxdb_config['bucket'])
            
            if st.form_submit_button("Salvar Configurações"):
                config = {
                    'url': url,
                    'token': token,
                    'org': org,
                    'bucket': bucket
                }
                self.save_config(config)
                st.success("Configurações salvas com sucesso!")
                
    def render_main_page(self):
        """Renderiza página principal"""
        st.title("Sistema de Detecção de Anomalias IoT")
        
        # Sidebar para controles
        with st.sidebar:
            st.header("Controles")
            if st.button("Gerar e Enviar Dados de Exemplo"):
                timestamps, temps, humids, anomaly_idx = self.generate_sample_data()
                if self.write_data(timestamps, temps, humids):
                    st.success("Dados de exemplo gerados e enviados com sucesso!")
            
            hours = st.slider("Horas de Dados para Análise", 1, 24, 1)
            
            if st.button("Atualizar Análise"):
                st.session_state.update_data = True
        
        # Layout principal com duas colunas
        col1, col2 = st.columns(2)
        
        with col1:
            st.subheader("Dados em Tempo Real")
            data = self.query_data(hours)
            if data is not None and len(data) > 0:
                # Gráfico de temperatura
                fig_temp = px.line(data, x='_time', y='temperatura', title='Temperatura ao Longo do Tempo')
                st.plotly_chart(fig_temp, use_container_width=True)
                
                # Gráfico de umidade
                fig_humid = px.line(data, x='_time', y='umidade', title='Umidade ao Longo do Tempo')
                st.plotly_chart(fig_humid, use_container_width=True)
        
        with col2:
            st.subheader("Detecção de Anomalias")
            if data is not None and len(data) > 0:
                anomalies = self.detect_anomalies(data)
                if anomalies is not None:
                    # Criar DataFrame com anomalias
                    anomaly_data = data.copy()
                    anomaly_data['anomalia'] = anomalies
                    
                    # Gráfico de dispersão com anomalias destacadas
                    fig_scatter = px.scatter(
                        anomaly_data,
                        x='temperatura',
                        y='umidade',
                        color='anomalia',
                        title='Detecção de Anomalias',
                        color_discrete_map={True: 'red', False: 'blue'}
                    )
                    st.plotly_chart(fig_scatter, use_container_width=True)
                    
                    # Métricas
                    n_anomalies = anomalies.sum()
                    st.metric("Total de Anomalias Detectadas", n_anomalies)
                    if n_anomalies > 0:
                        st.warning(f"Foram detectadas {n_anomalies} anomalias nos dados!")
                    
    def run(self):
        """Executa o aplicativo"""
        st.sidebar.title("Navegação")
        page = st.sidebar.radio("Ir para:", ["Principal", "Configurações"])
        
        if page == "Principal":
            if not all(st.session_state.influxdb_config.values()):
                st.warning("Configure as credenciais do InfluxDB primeiro!")
                st.sidebar.info("Vá para a página de Configurações")
            else:
                self.render_main_page()
        else:
            self.render_config_page()

if __name__ == "__main__":
    app = AnomalyDetectionApp()
    app.run()
