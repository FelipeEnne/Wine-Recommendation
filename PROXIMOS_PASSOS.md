# Próximos Passos do Projeto - Wine Recommendation

## Análise do Estado Atual

Este projeto de recomendação de vinhos está funcional, mas apresenta várias oportunidades de modernização e melhoria. Abaixo está um plano estruturado para atualizar e expandir o projeto.

---

## 📋 Melhorias Prioritárias

### 1. **Estrutura e Gestão de Dependências**

**Problema Atual:**
- Não há arquivo `requirements.txt` ou `environment.yml`
- Instruções vagas sobre instalação de bibliotecas
- Dificulta reprodutibilidade do ambiente

**Ações:**
- [ ] Criar `requirements.txt` com versões específicas de todas as dependências
- [ ] Criar `environment.yml` para usuários do Conda
- [ ] Documentar versão mínima do Python necessária
- [ ] Adicionar instruções claras de instalação no README

**Dependências a documentar:**
```
pandas
numpy
matplotlib
seaborn
pycountry-convert
jupyter
```

---

### 2. **Estrutura de Projeto Moderna**

**Problema Atual:**
- Notebooks soltos na raiz do projeto
- Sem organização modular
- Dificulta manutenção e expansão

**Ações:**
- [ ] Reorganizar em estrutura modular:
```
wine-recommendation/
├── data/
│   ├── raw/          (dados originais - gitignored)
│   ├── processed/    (dados limpos - gitignored)
│   └── .gitkeep
├── notebooks/
│   ├── 01_data_cleaning.ipynb
│   ├── 02_geographic_analysis.ipynb
│   ├── 03_recommendation_by_points.ipynb
│   └── 04_recommendation_by_taster.ipynb
├── src/
│   ├── __init__.py
│   ├── data_processing.py
│   ├── recommendation.py
│   └── visualization.py
├── tests/
│   ├── __init__.py
│   ├── test_data_processing.py
│   └── test_recommendation.py
├── images/
├── docs/
├── .gitignore
├── README.md
├── requirements.txt
├── setup.py
└── LICENSE
```

---

### 3. **Modularização do Código**

**Problema Atual:**
- Toda lógica está dentro dos notebooks
- Código duplicado entre notebooks
- Dificulta reutilização e testes

**Ações:**
- [ ] Extrair funções de limpeza de dados para `src/data_processing.py`
- [ ] Criar classes/funções para sistemas de recomendação em `src/recommendation.py`
- [ ] Separar funções de visualização em `src/visualization.py`
- [ ] Manter notebooks apenas para análise exploratória e demonstração

**Exemplo de refatoração:**
```python
# src/recommendation.py
class WineRecommender:
    def __init__(self, data_path):
        self.df = pd.read_csv(data_path)
    
    def recommend_by_points(self, country=None, variety=None, top_n=10):
        """Recomenda vinhos baseado em pontuação"""
        pass
    
    def recommend_by_taster(self, taster_name, top_n=10):
        """Recomenda vinhos baseado em degustador"""
        pass
```

---

### 4. **Implementar Testes**

**Problema Atual:**
- Sem testes automatizados
- Sem garantia de qualidade do código

**Ações:**
- [ ] Adicionar pytest como dependência
- [ ] Criar testes unitários para funções de processamento
- [ ] Criar testes para sistema de recomendação
- [ ] Configurar GitHub Actions para CI/CD

**Exemplo:**
```python
# tests/test_recommendation.py
import pytest
from src.recommendation import WineRecommender

def test_recommend_by_points():
    recommender = WineRecommender('data/processed/wines.csv')
    results = recommender.recommend_by_points(top_n=5)
    assert len(results) == 5
    assert all(results['points'] >= 90)
```

---

### 5. **Melhorar Sistema de Recomendação**

**Problema Atual:**
- Recomendações muito simples (apenas por pontuação)
- Não usa técnicas modernas de ML

**Ações:**
- [ ] Implementar filtragem colaborativa
- [ ] Adicionar sistema baseado em conteúdo usando TF-IDF nas descrições
- [ ] Implementar algoritmo híbrido combinando múltiplos métodos
- [ ] Adicionar análise de sentimento nas reviews
- [ ] Usar scikit-learn para clustering de vinhos similares

**Técnicas a implementar:**
- Content-Based Filtering (TF-IDF + Cosine Similarity)
- Collaborative Filtering (User-based ou Item-based)
- Matrix Factorization (SVD, NMF)
- Deep Learning (Neural Collaborative Filtering)

---

### 6. **Interface de Usuário**

**Problema Atual:**
- Apenas notebooks, sem interface interativa
- Dificulta uso por não-programadores

**Ações:**
- [ ] Criar aplicação web com Streamlit ou Flask
- [ ] Interface para buscar vinhos por critérios
- [ ] Visualizações interativas com Plotly
- [ ] Deploy em Heroku, Streamlit Cloud ou Railway

**Exemplo Streamlit:**
```python
# app.py
import streamlit as st
from src.recommendation import WineRecommender

st.title('🍷 Wine Recommendation System')

country = st.selectbox('Select Country', options=['All', 'US', 'France', ...])
variety = st.selectbox('Select Variety', options=['All', 'Pinot Noir', ...])

if st.button('Get Recommendations'):
    recommender = WineRecommender('data/processed/wines.csv')
    recommendations = recommender.recommend_by_points(country, variety)
    st.dataframe(recommendations)
```

---

### 7. **Atualização de Dependências**

**Problema Atual:**
- Sem controle de versões
- Possíveis vulnerabilidades de segurança

**Ações:**
- [ ] Atualizar para versões mais recentes de pandas, numpy, matplotlib
- [ ] Considerar alternativas modernas (ex: Polars ao invés de Pandas para grandes datasets)
- [ ] Adicionar ferramentas de análise de segurança (Safety, Bandit)

---

### 8. **Documentação**

**Problema Atual:**
- README básico
- Sem documentação de API
- Sem exemplos de uso

**Ações:**
- [ ] Expandir README com:
  - Badges (build status, coverage, license)
  - GIFs/screenshots da aplicação
  - Exemplos de código
  - Seção de contribuição
- [ ] Adicionar docstrings em todas as funções (formato Google ou NumPy)
- [ ] Criar documentação com Sphinx ou MkDocs
- [ ] Adicionar CONTRIBUTING.md
- [ ] Criar CHANGELOG.md

---

### 9. **Análises Avançadas**

**Ações:**
- [ ] Análise de preço vs qualidade
- [ ] Mapa interativo de regiões vinícolas
- [ ] Tendências temporais (se houver dados de data)
- [ ] Análise de palavras mais comuns em reviews de vinhos top
- [ ] Network analysis de variedades e países
- [ ] Predição de preço baseado em características

---

### 10. **MLOps e Deployment**

**Ações:**
- [ ] Criar pipeline de treinamento automatizado
- [ ] Versionar modelos com MLflow ou DVC
- [ ] Containerizar aplicação com Docker
- [ ] Deploy automatizado (GitHub Actions)
- [ ] Monitoramento de performance do modelo

---

## 🚀 Plano de Implementação Sugerido

### Fase 1: Fundação (Semana 1-2)
1. Criar `requirements.txt` e `environment.yml`
2. Reorganizar estrutura de pastas
3. Atualizar `.gitignore`
4. Melhorar README

### Fase 2: Modularização (Semana 3-4)
5. Extrair código dos notebooks para módulos Python
6. Implementar testes básicos
7. Configurar CI/CD

### Fase 3: Melhorias de ML (Semana 5-7)
8. Implementar novos algoritmos de recomendação
9. Adicionar análises avançadas
10. Otimizar performance

### Fase 4: Interface e Deploy (Semana 8-10)
11. Criar aplicação web com Streamlit
12. Dockerizar aplicação
13. Deploy em plataforma cloud
14. Documentação final

---

## 📊 Tecnologias Recomendadas para Modernização

### Core ML/Data Science
- **pandas** → considerar **Polars** para datasets grandes
- **scikit-learn** → algoritmos de ML
- **surprise** → biblioteca especializada em sistemas de recomendação
- **implicit** → collaborative filtering otimizado

### Visualização
- **matplotlib/seaborn** → manter para análise estática
- **plotly** → adicionar para visualizações interativas
- **folium** → mapas interativos de regiões vinícolas

### Web Framework
- **Streamlit** → prototipagem rápida (recomendado)
- **Flask/FastAPI** → mais controle e escalabilidade

### DevOps/MLOps
- **pytest** → testes
- **black** → formatação de código
- **flake8/pylint** → linting
- **pre-commit** → hooks de git
- **Docker** → containerização
- **DVC** → versionamento de dados
- **MLflow** → tracking de experimentos

---

## 🎯 Métricas de Sucesso

- [ ] Cobertura de testes > 80%
- [ ] Documentação completa de todas as funções
- [ ] Aplicação web funcional e deployada
- [ ] Tempo de resposta < 2s para recomendações
- [ ] Sistema de recomendação com múltiplos algoritmos
- [ ] CI/CD pipeline funcional

---

## 📚 Recursos e Referências

### Sistemas de Recomendação
- [Surprise Library Documentation](http://surpriselib.com/)
- [Building Recommender Systems with Python](https://www.manning.com/books/practical-recommender-systems)
- [Microsoft Recommenders](https://github.com/microsoft/recommenders)

### Best Practices
- [Cookiecutter Data Science](https://drivendata.github.io/cookiecutter-data-science/)
- [Python Best Practices for Data Science](https://github.com/drivendata/cookiecutter-data-science)

### Deploy
- [Streamlit Deployment](https://docs.streamlit.io/streamlit-community-cloud/deploy-your-app)
- [Docker for Data Science](https://www.datacamp.com/tutorial/docker-for-data-science)

---

## 🤝 Próximos Passos Imediatos

1. **Criar requirements.txt** - estabelecer base reprodutível
2. **Reorganizar estrutura** - preparar para crescimento
3. **Extrair funções principais** - começar modularização
4. **Implementar novo algoritmo** - melhorar recomendações
5. **Criar app Streamlit básico** - democratizar acesso

---

*Documento criado em: Fevereiro 2026*
*Versão: 1.0*
