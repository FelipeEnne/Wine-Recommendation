"""
Wine Recommendation System

A comprehensive wine recommendation system using machine learning techniques
including content-based filtering, collaborative filtering, and hybrid approaches.
"""

__version__ = "2.0.0"
__author__ = "Felipe Enne Mendes Ribeiro"
__email__ = "felipeenne@gmail.com"

from .data_processing import WineDataProcessor
from .recommendation import WineRecommender
from .visualization import WineVisualizer

__all__ = [
    "WineDataProcessor",
    "WineRecommender",
    "WineVisualizer",
]
