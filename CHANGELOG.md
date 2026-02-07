# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [2.0.0] - 2026-02-07

### Added

#### Project Structure & Organization
- ✨ Complete project restructure with modern Python package layout
- 📁 New `src/` directory with modular code organization
- 📁 New `tests/` directory with comprehensive test suite
- 📁 Organized `notebooks/` directory with numbered workflow
- 📁 Structured `data/` directory with raw/processed separation

#### Core Modules
- 🎯 `data_processing.py` - WineDataProcessor class for data cleaning and preprocessing
- 🎯 `recommendation.py` - WineRecommender class with multiple recommendation strategies
- 🎯 `visualization.py` - WineVisualizer class for data visualization

#### Features
- ⭐ Content-based filtering using TF-IDF and cosine similarity
- ⭐ Budget-based recommendations (best value wines)
- ⭐ Enhanced recommendation algorithms with value scoring
- ⭐ Similar wine discovery using ML
- 📊 Comprehensive data statistics and analytics

#### Web Application
- 🌐 Beautiful Streamlit web interface
- 🎨 Multiple pages: Home, Explore, Recommendations, Analytics
- 📈 Interactive Plotly visualizations
- 🔍 Advanced filtering and search capabilities

#### Development & DevOps
- ✅ Comprehensive test suite using pytest
- ✅ Test fixtures and sample data generators
- 🐳 Docker support with Dockerfile and .dockerignore
- 🔄 GitHub Actions CI/CD pipeline
- 🎨 Code formatting with Black
- 🔍 Linting with flake8 and pylint
- 📝 Pre-commit hooks configuration

#### Documentation
- 📚 Completely rewritten README with badges and comprehensive guide
- 📚 CONTRIBUTING.md with detailed contribution guidelines
- 📚 PROXIMOS_PASSOS.md with project roadmap (in Portuguese)
- 📚 Detailed docstrings in Google style
- 📚 Type hints throughout codebase

#### Dependencies & Configuration
- 📦 `requirements.txt` with pinned versions
- 📦 `environment.yml` for Conda users
- 📦 `setup.py` for package installation
- ⚙️ `pytest.ini` for test configuration
- ⚙️ `.pre-commit-config.yaml` for git hooks
- 🙈 Enhanced `.gitignore` for Python projects

### Changed
- 🔄 Notebooks renamed and reorganized with numbered prefix
- 🔄 Improved data cleaning pipeline with method chaining
- 🔄 Enhanced visualization functions with customization options
- 🔄 Better error handling and validation throughout

### Improved
- 🚀 Performance optimization for data processing
- 🚀 Better caching in Streamlit app
- 📈 More comprehensive data analysis
- 🎯 More accurate recommendations with multiple algorithms

### Technical Improvements
- 💪 Type hints added to all functions
- 💪 Comprehensive error handling
- 💪 Modular, reusable code
- 💪 Test coverage for critical functionality
- 💪 CI/CD integration for quality assurance

---

## [1.0.0] - Original Version

### Features
- Basic data cleaning notebook
- Geographic data analysis
- Point-based wine recommendations
- Taster-based wine recommendations
- Basic visualizations with matplotlib and seaborn

### Components
- Jupyter notebooks for analysis
- Basic README
- MIT License
- Simple .gitignore

---

## Future Releases

See [PROXIMOS_PASSOS.md](PROXIMOS_PASSOS.md) for planned features and improvements.

---

[2.0.0]: https://github.com/felipeenne/wine-recommendation/compare/v1.0.0...v2.0.0
[1.0.0]: https://github.com/felipeenne/wine-recommendation/releases/tag/v1.0.0
