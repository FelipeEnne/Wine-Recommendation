# Contributing to Wine Recommendation System

First off, thank you for considering contributing to Wine Recommendation System! It's people like you that make this project better for everyone.

## Table of Contents

- [Code of Conduct](#code-of-conduct)
- [How Can I Contribute?](#how-can-i-contribute)
  - [Reporting Bugs](#reporting-bugs)
  - [Suggesting Enhancements](#suggesting-enhancements)
  - [Pull Requests](#pull-requests)
- [Development Setup](#development-setup)
- [Style Guidelines](#style-guidelines)
  - [Git Commit Messages](#git-commit-messages)
  - [Python Style Guide](#python-style-guide)
  - [Documentation Style](#documentation-style)
- [Testing Guidelines](#testing-guidelines)

## Code of Conduct

This project and everyone participating in it is governed by our Code of Conduct. By participating, you are expected to uphold this code. Please report unacceptable behavior to felipeenne@gmail.com.

## How Can I Contribute?

### Reporting Bugs

Before creating bug reports, please check the existing issues as you might find out that you don't need to create one. When you are creating a bug report, please include as many details as possible:

**Bug Report Template:**

```markdown
**Describe the bug**
A clear and concise description of what the bug is.

**To Reproduce**
Steps to reproduce the behavior:
1. Go to '...'
2. Click on '....'
3. Scroll down to '....'
4. See error

**Expected behavior**
A clear and concise description of what you expected to happen.

**Screenshots**
If applicable, add screenshots to help explain your problem.

**Environment:**
 - OS: [e.g. Ubuntu 20.04, Windows 10]
 - Python Version: [e.g. 3.9.7]
 - Package Version: [e.g. 2.0.0]

**Additional context**
Add any other context about the problem here.
```

### Suggesting Enhancements

Enhancement suggestions are tracked as GitHub issues. When creating an enhancement suggestion, please include:

- A clear and descriptive title
- A detailed description of the proposed enhancement
- Explain why this enhancement would be useful
- List any alternative solutions or features you've considered

### Pull Requests

1. Fork the repository
2. Create a new branch from `main`:
   ```bash
   git checkout -b feature/your-feature-name
   ```
3. Make your changes
4. Add or update tests as necessary
5. Ensure all tests pass:
   ```bash
   pytest
   ```
6. Format your code:
   ```bash
   black src/ tests/
   flake8 src/ tests/
   ```
7. Commit your changes (see commit message guidelines below)
8. Push to your fork
9. Create a Pull Request

**Pull Request Guidelines:**

- Include a clear title and description
- Reference any related issues
- Include screenshots for UI changes
- Ensure all CI checks pass
- Update documentation if needed
- Add tests for new functionality

## Development Setup

1. Clone your fork:
   ```bash
   git clone https://github.com/YOUR-USERNAME/wine-recommendation.git
   cd wine-recommendation
   ```

2. Set up development environment:
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   pip install -r requirements.txt
   pip install -e .
   ```

3. Install development dependencies:
   ```bash
   pip install pytest pytest-cov black flake8 pylint mypy pre-commit
   ```

4. Set up pre-commit hooks:
   ```bash
   pre-commit install
   ```

5. Create a branch for your work:
   ```bash
   git checkout -b feature/my-new-feature
   ```

## Style Guidelines

### Git Commit Messages

- Use the present tense ("Add feature" not "Added feature")
- Use the imperative mood ("Move cursor to..." not "Moves cursor to...")
- Limit the first line to 72 characters or less
- Reference issues and pull requests liberally after the first line
- Consider starting the commit message with an applicable emoji:
  - 🎨 `:art:` - Improving structure/format of the code
  - ⚡ `:zap:` - Improving performance
  - 🔥 `:fire:` - Removing code or files
  - 🐛 `:bug:` - Fixing a bug
  - ✨ `:sparkles:` - Introducing new features
  - 📝 `:memo:` - Writing docs
  - 🚀 `:rocket:` - Deploying stuff
  - ✅ `:white_check_mark:` - Adding tests
  - 🔒 `:lock:` - Fixing security issues
  - ⬆️ `:arrow_up:` - Upgrading dependencies
  - ⬇️ `:arrow_down:` - Downgrading dependencies
  - 👷 `:construction_worker:` - Adding CI build system

**Example:**
```
✨ Add content-based recommendation using TF-IDF

- Implement TF-IDF vectorization for wine descriptions
- Add cosine similarity calculation
- Create recommend_similar_wines method
- Add tests for new functionality

Closes #123
```

### Python Style Guide

We follow PEP 8 with some modifications:

- **Line length**: 100 characters (not 79)
- **Imports**: Use absolute imports, group them (stdlib, third-party, local)
- **Formatting**: Use Black for automatic formatting
- **Type hints**: Use type hints for function arguments and return values
- **Docstrings**: Use Google-style docstrings

**Example:**

```python
from typing import List, Optional
import pandas as pd


def recommend_wines(
    data: pd.DataFrame,
    country: Optional[str] = None,
    min_points: int = 90,
    top_n: int = 10
) -> pd.DataFrame:
    """
    Recommend wines based on specified criteria.
    
    Args:
        data (pd.DataFrame): Wine reviews dataframe
        country (str, optional): Filter by country. Defaults to None.
        min_points (int): Minimum rating threshold. Defaults to 90.
        top_n (int): Number of recommendations. Defaults to 10.
    
    Returns:
        pd.DataFrame: Top N recommended wines
        
    Raises:
        ValueError: If min_points is not between 0 and 100
        
    Example:
        >>> df = pd.read_csv('wines.csv')
        >>> recommendations = recommend_wines(df, country='France', top_n=5)
    """
    if not 0 <= min_points <= 100:
        raise ValueError("min_points must be between 0 and 100")
    
    # Implementation here
    pass
```

### Documentation Style

- Use clear, concise language
- Include code examples where appropriate
- Keep documentation up-to-date with code changes
- Use Markdown for documentation files
- Include type hints in function signatures

## Testing Guidelines

- Write tests for all new functionality
- Maintain or improve code coverage
- Use descriptive test names that explain what is being tested
- Follow the AAA pattern: Arrange, Act, Assert
- Use fixtures for common test setup
- Mock external dependencies

**Test Example:**

```python
import pytest
from src.recommendation import WineRecommender


class TestWineRecommender:
    """Test suite for WineRecommender class."""
    
    @pytest.fixture
    def recommender(self, sample_data_path):
        """Fixture to create a recommender instance."""
        return WineRecommender(sample_data_path)
    
    def test_recommend_by_points_returns_correct_count(self, recommender):
        """Test that recommend_by_points returns the requested number of wines."""
        # Arrange
        top_n = 5
        
        # Act
        result = recommender.recommend_by_points(top_n=top_n)
        
        # Assert
        assert len(result) <= top_n
        assert all(result['points'] >= 90)
```

### Running Tests

```bash
# Run all tests
pytest

# Run with coverage report
pytest --cov=src --cov-report=html

# Run specific test file
pytest tests/test_recommendation.py

# Run specific test
pytest tests/test_recommendation.py::TestWineRecommender::test_recommend_by_points

# Run with verbose output
pytest -v
```

## Questions?

Feel free to open an issue with the label `question` or reach out to felipeenne@gmail.com.

Thank you for contributing! 🍷
