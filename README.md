<!-- PROJECT TITLE -->
<h1 align="center">🍷 Wine Recommendation System</h1>

<p align="center">
    <strong>An AI-powered wine recommendation system using machine learning</strong>
    <br />
    <a href="https://www.kaggle.com/zynicide/wine-reviews">Dataset</a>
    ·
    <a href="#features">Features</a>
    ·
    <a href="#getting-started">Getting Started</a>
    ·
    <a href="#usage">Usage</a>
</p>

<p align="center">
  <img src="https://img.shields.io/badge/python-3.9+-blue.svg" alt="Python Version">
  <img src="https://img.shields.io/badge/license-MIT-green.svg" alt="License">
  <img src="https://img.shields.io/badge/code%20style-black-000000.svg" alt="Code Style">
</p>

---

## 📋 Table of Contents

- [About](#about)
- [Features](#features)
- [Project Structure](#project-structure)
- [Getting Started](#getting-started)
  - [Prerequisites](#prerequisites)
  - [Installation](#installation)
- [Usage](#usage)
  - [Data Processing](#data-processing)
  - [Jupyter Notebooks](#jupyter-notebooks)
  - [Web Application](#web-application)
  - [Python API](#python-api)
- [Recommendation Algorithms](#recommendation-algorithms)
- [Development](#development)
  - [Running Tests](#running-tests)
  - [Code Quality](#code-quality)
- [Docker](#docker)
- [Roadmap](#roadmap)
- [Contributing](#contributing)
- [License](#license)
- [Contact](#contact)
- [Acknowledgements](#acknowledgements)

---

## 🎯 About

This project implements a comprehensive wine recommendation system using machine learning techniques and the [Wine Reviews dataset from Kaggle](https://www.kaggle.com/zynicide/wine-reviews). The system provides multiple recommendation strategies including:

- **Point-based recommendations**: Find top-rated wines by score
- **Taster-based recommendations**: Discover wines reviewed by specific experts
- **Content-based filtering**: Get recommendations based on wine characteristics and descriptions
- **Budget-conscious recommendations**: Find the best value wines within your price range
- **Similar wine discovery**: Find wines similar to ones you already enjoy

The project has been modernized with:
- ✅ Modular, well-tested Python code
- ✅ Interactive web application using Streamlit
- ✅ Comprehensive test suite with pytest
- ✅ Professional project structure
- ✅ Docker support for easy deployment
- ✅ CI/CD pipeline with GitHub Actions

---

## ✨ Features

### 🔍 Multiple Recommendation Strategies

- **Rating-based**: Get top-rated wines filtered by country, variety, and minimum score
- **Expert-based**: Follow recommendations from your favorite wine tasters
- **Content similarity**: ML-powered similar wine discovery using TF-IDF and cosine similarity
- **Value optimization**: Find wines with the best quality-to-price ratio

### 📊 Data Analysis & Visualization

- Comprehensive data cleaning and preprocessing
- Statistical analysis of wine ratings, prices, and characteristics
- Geographic analysis with continent mapping
- Interactive visualizations with matplotlib, seaborn, and plotly

### 🌐 Web Interface

- Beautiful, responsive Streamlit web application
- Interactive filtering and exploration
- Real-time recommendations
- Data visualizations and analytics dashboard

### 🧪 Production-Ready Code

- Modular, object-oriented design
- Type hints for better code clarity
- Comprehensive test coverage with pytest
- Code formatting with Black
- Linting with flake8
- Docker containerization

---

## 📁 Project Structure

```
wine-recommendation/
├── data/
│   ├── raw/              # Original data files (gitignored)
│   └── processed/        # Cleaned data files (gitignored)
├── notebooks/            # Jupyter notebooks for analysis
│   ├── 01_data_cleaning.ipynb (legacy: Data Cleaning.ipynb)
│   ├── 02_geographic_analysis.ipynb (legacy: Analyzing geographic data.ipynb)
│   ├── 03_recommendation_by_points.ipynb (legacy: Wine recommendation by point.ipynb)
│   └── 04_recommendation_by_taster.ipynb (legacy: Wine recommendation by taster.ipynb)
├── src/
│   ├── __init__.py
│   ├── data_processing.py    # Data cleaning and preprocessing
│   ├── recommendation.py     # Recommendation algorithms
│   └── visualization.py      # Visualization functions
├── tests/
│   ├── __init__.py
│   ├── test_data_processing.py
│   └── test_recommendation.py
├── images/               # Screenshots and visualizations
├── app.py               # Streamlit web application
├── requirements.txt     # Python dependencies
├── environment.yml      # Conda environment specification
├── setup.py            # Package installation script
├── Dockerfile          # Docker container definition
├── .gitignore
├── LICENSE
└── README.md
```

---

## 🚀 Getting Started

### Prerequisites

- Python 3.9 or higher
- pip or conda for package management
- (Optional) Docker for containerized deployment

### Installation

#### Option 1: Using pip (recommended)

```bash
# Clone the repository
git clone https://github.com/felipeenne/wine-recommendation.git
cd wine-recommendation

# Create a virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Install the package in development mode
pip install -e .
```

#### Option 2: Using conda

```bash
# Clone the repository
git clone https://github.com/felipeenne/wine-recommendation.git
cd wine-recommendation

# Create conda environment
conda env create -f environment.yml
conda activate wine-recommendation
```

#### Option 3: Using Docker

```bash
# Build the Docker image
docker build -t wine-recommendation .

# Run the container
docker run -p 8501:8501 wine-recommendation
```

### Data Setup

1. Download the wine reviews dataset from [Kaggle](https://www.kaggle.com/zynicide/wine-reviews)
2. Extract the CSV file to `data/raw/`
3. Run the data cleaning process:

```bash
# Using Python script
python src/data_processing.py data/raw/winemag-data-130k-v2.csv data/processed/wines.csv

# Or using Jupyter notebook
jupyter notebook notebooks/01_data_cleaning.ipynb
```

---

## 💻 Usage

### Data Processing

```python
from src.data_processing import WineDataProcessor

# Initialize processor
processor = WineDataProcessor('data/raw/winemag-data-130k-v2.csv')

# Clean and process data
processor.handle_missing_values(strategy='drop')
processor.remove_duplicates()
processor.add_continent()

# Save processed data
processor.save_processed_data('data/processed/wines.csv')
```

### Jupyter Notebooks

Explore the analysis notebooks in order:

```bash
jupyter notebook
```

1. **Data Cleaning**: Clean and prepare the raw data
2. **Geographic Analysis**: Add continent information and analyze by region
3. **Recommendation by Points**: Build rating-based recommendation system
4. **Recommendation by Taster**: Build expert-based recommendation system

### Web Application

Launch the Streamlit web interface:

```bash
streamlit run app.py
```

The application will open in your browser at `http://localhost:8501`

### Python API

```python
from src.recommendation import WineRecommender

# Initialize recommender
recommender = WineRecommender('data/processed/wines.csv')

# Get top-rated wines from France
recommendations = recommender.recommend_by_points(
    country='France',
    min_points=95,
    top_n=10
)

# Find similar wines
similar = recommender.recommend_similar_wines('Chateau Margaux', top_n=5)

# Get best value wines under $50
value_wines = recommender.recommend_by_budget(
    max_price=50,
    min_points=90,
    top_n=10
)

# Get recommendations from a specific taster
taster_picks = recommender.recommend_by_taster('Roger Voss', top_n=10)
```

---

## 🤖 Recommendation Algorithms

### 1. Point-Based Recommendation

Uses wine ratings and applies filters (country, variety, price) to find top-rated wines.

**Algorithm**: Simple filtering and sorting with value score calculation.

### 2. Taster-Based Recommendation

Recommends wines based on ratings from specific wine experts.

**Algorithm**: Filter by taster and rank by points.

### 3. Content-Based Filtering

Uses TF-IDF (Term Frequency-Inverse Document Frequency) and cosine similarity to find wines with similar characteristics.

**Features used**: 
- Wine descriptions
- Variety
- Country
- Province

**Algorithm**:
1. Combine text features into single document per wine
2. Create TF-IDF matrix from documents
3. Compute cosine similarity between wines
4. Recommend wines with highest similarity scores

### 4. Budget-Based Recommendation

Finds wines with the best quality-to-price ratio within a budget.

**Algorithm**: Calculate value score (points/price) and rank accordingly.

---

## 🛠 Development

### Running Tests

```bash
# Run all tests
pytest

# Run with coverage
pytest --cov=src tests/

# Run specific test file
pytest tests/test_recommendation.py -v
```

### Code Quality

```bash
# Format code with Black
black src/ tests/ app.py

# Lint with flake8
flake8 src/ tests/ app.py

# Type checking (if using mypy)
mypy src/
```

### Pre-commit Hooks

Install pre-commit hooks to automatically format and lint code:

```bash
pip install pre-commit
pre-commit install
```

---

## 🐳 Docker

### Building the Image

```bash
docker build -t wine-recommendation:latest .
```

### Running the Container

```bash
# Run Streamlit app
docker run -p 8501:8501 wine-recommendation

# Run with volume mount for data
docker run -p 8501:8501 -v $(pwd)/data:/app/data wine-recommendation
```

### Docker Compose (optional)

Create a `docker-compose.yml` for easier management:

```yaml
version: '3.8'
services:
  app:
    build: .
    ports:
      - "8501:8501"
    volumes:
      - ./data:/app/data
```

Run with: `docker-compose up`

---

## 🗺 Roadmap

See [PROXIMOS_PASSOS.md](PROXIMOS_PASSOS.md) for a detailed roadmap of future improvements.

**Upcoming features:**

- [ ] Advanced ML models (collaborative filtering, neural networks)
- [ ] User profile and preference learning
- [ ] Wine pairing recommendations (food + wine)
- [ ] Price prediction model
- [ ] Multi-language support
- [ ] Mobile-responsive PWA
- [ ] REST API with FastAPI
- [ ] Database integration (PostgreSQL)
- [ ] User authentication and saved preferences
- [ ] Social features (share, rate, review)

---

## 🤝 Contributing

Contributions are welcome! Please see [CONTRIBUTING.md](CONTRIBUTING.md) for guidelines.

1. Fork the Project
2. Create your Feature Branch (`git checkout -b feature/AmazingFeature`)
3. Commit your Changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the Branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

---

## 📄 License

Distributed under the MIT License. See `LICENSE` for more information.

---

## 📞 Contact

**Felipe Enne Mendes Ribeiro**

- Email: felipeenne@gmail.com
- LinkedIn: [felipe-enne](https://www.linkedin.com/in/felipe-enne/)
- Portfolio: [felipeenne.com](https://felipeenne.com/)

**Project Link**: [https://github.com/felipeenne/wine-recommendation](https://github.com/felipeenne/wine-recommendation)

---

## 🙏 Acknowledgements

- [Wine Reviews Dataset](https://www.kaggle.com/zynicide/wine-reviews) from Kaggle
- Inspired by [wine-recommender](https://www.kaggle.com/sudhirnl7/wine-recommender/notebook)
- Data cleaning tutorial: [comprehensive-tutorial-data-cleaning](https://www.kaggle.com/milankalkenings/comprehensive-tutorial-data-cleaning)
- [Streamlit](https://streamlit.io/) for the amazing web framework
- [scikit-learn](https://scikit-learn.org/) for machine learning algorithms

---

<p align="center">Made with ❤️ and 🍷</p>
