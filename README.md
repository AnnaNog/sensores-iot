# Sistema de Detecção de Anomalias IoT 🔍

Sistema de monitoramento em tempo real com detecção de anomalias utilizando InfluxDB Cloud, Python e Machine Learning.

## 🌟 Características

- Interface gráfica intuitiva com Streamlit
- Integração com InfluxDB Cloud para armazenamento de séries temporais
- Detecção de anomalias em tempo real usando Isolation Forest
- Visualização interativa de dados com Plotly
- Geração automática de dados de exemplo
- Dashboard em tempo real para monitoramento
- Sistema de alertas para anomalias detectadas

## 🔧 Requisitos do Sistema

- Python 3.8 ou superior
- Conta no InfluxDB Cloud (gratuita disponível)
- Pip (gerenciador de pacotes Python)
- Git (opcional, para clonar o repositório)

## 📦 Dependências Principais

- streamlit>=1.24.0
- influxdb-client>=1.36.0
- pandas>=1.5.3
- numpy>=1.24.3
- plotly>=5.13.1
- scikit-learn>=1.2.2

## 🚀 Instalação

1. Clone o repositório (ou baixe o código):
```bash
git clone https://github.com/freecorps/anomaly-detection-iot.git
cd anomaly-detection-iot
```

2. Crie e ative um ambiente virtual:

No Windows:
```bash
python -m venv venv
venv\Scripts\activate
```

No Linux/Mac:
```bash
python -m venv venv
source venv/bin/activate
```

3. Instale as dependências:
```bash
pip install -r requirements.txt
```

## ⚙️ Configuração

1. Acesse sua conta no InfluxDB Cloud e obtenha as seguintes informações:
   - URL do servidor
   - Token de API
   - Nome da organização
   - Nome do bucket

2. No aplicativo, vá para a página de "Configurações" e preencha estas informações

## 🎮 Como Usar

1. Inicie o aplicativo:
```bash
streamlit run app.py
```

2. Acesse o aplicativo no navegador (geralmente http://localhost:8501)

3. Na primeira execução:
   - Vá para a página "Configurações"
   - Insira suas credenciais do InfluxDB Cloud
   - Clique em "Salvar Configurações"

4. Na página principal:
   - Use o botão "Gerar e Enviar Dados de Exemplo" para criar dados de teste
   - Ajuste o período de análise usando o slider
   - Observe os gráficos de temperatura e umidade
   - Verifique o gráfico de detecção de anomalias
   - Use o botão "Atualizar Análise" para atualizar os dados

## 📊 Funcionalidades Detalhadas

### Página de Configuração
- Formulário para credenciais do InfluxDB
- Validação de conexão
- Armazenamento seguro das configurações

### Página Principal
- Dashboard em tempo real
- Gráficos de séries temporais
- Visualização de anomalias
- Controles interativos
- Sistema de alertas

### Geração de Dados
- Dados simulados realistas
- Anomalias inseridas aleatoriamente
- Timestamp automático
- Valores de temperatura e umidade

### Detecção de Anomalias
- Algoritmo Isolation Forest
- Detecção em tempo real
- Visualização de pontos anômalos
- Métricas de quantidade de anomalias

## 📈 Visualizações

O sistema oferece diferentes tipos de visualizações:

1. **Gráficos de Séries Temporais**
   - Temperatura ao longo do tempo
   - Umidade ao longo do tempo
   - Zoom e pan interativos
   - Tooltips informativos

2. **Gráfico de Dispersão de Anomalias**
   - Pontos normais vs. anômalos
   - Código de cores para fácil identificação
   - Interatividade completa

3. **Métricas e Alertas**
   - Contagem de anomalias
   - Alertas visuais
   - Estatísticas em tempo real

## 🔐 Segurança

- Credenciais armazenadas de forma segura
- Conexão segura com InfluxDB Cloud
- Validação de dados
- Tratamento de erros robusto

## 🛠️ Estrutura do Projeto

```
anomaly-detection-iot/
│
├── app.py                 # Aplicativo principal
├── requirements.txt       # Dependências do projeto
├── README.md             # Este arquivo
└── venv/                 # Ambiente virtual (gerado na instalação)
```

## 🤝 Contribuindo

1. Faça um Fork do projeto
2. Crie uma branch para sua feature (`git checkout -b feature/AmazingFeature`)
3. Commit suas mudanças (`git commit -m 'Add some AmazingFeature'`)
4. Push para a branch (`git push origin feature/AmazingFeature`)
5. Abra um Pull Request

## 📝 Licença

Este projeto está sob a licença MIT. Veja o arquivo [LICENSE](LICENSE) para mais detalhes.

## 📫 Contato

Link do Projeto: [https://github.com/freecorps/anomaly-detection-iot](https://github.com/freecorps/anomaly-detection-iot)

## 🙏 Agradecimentos

- [InfluxDB](https://www.influxdata.com/)
- [Streamlit](https://streamlit.io/)
- [Plotly](https://plotly.com/)
- [Scikit-learn](https://scikit-learn.org/)

## 📊 Demonstração

![Imagem da dashboard](https://i.imgur.com/vXWyxFE.png)

![Imagem da pagina de configs](https://i.imgur.com/SBZ9vPu.png)