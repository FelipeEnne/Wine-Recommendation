"""
Recommendation Module for Wine Recommendation System

This module contains classes and functions for generating wine recommendations
using various algorithms including content-based filtering and collaborative filtering.
"""

import pandas as pd
import numpy as np
from typing import Optional, List, Dict, Tuple
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
from sklearn.preprocessing import StandardScaler


class WineRecommender:
    """
    A comprehensive wine recommendation system.
    
    This class implements multiple recommendation strategies including:
    - Point-based recommendations
    - Taster-based recommendations
    - Content-based filtering (using wine descriptions)
    - Collaborative filtering
    
    Attributes:
        df (pd.DataFrame): The wine reviews dataframe
        tfidf_matrix (np.ndarray): TF-IDF matrix for content-based filtering
        similarity_matrix (np.ndarray): Similarity matrix for recommendations
    """
    
    def __init__(self, data_path: str):
        """
        Initialize the WineRecommender.
        
        Args:
            data_path (str): Path to the processed CSV file containing wine reviews
        """
        self.df = pd.read_csv(data_path)
        self.tfidf_matrix = None
        self.similarity_matrix = None
        
    def recommend_by_points(self, 
                           country: Optional[str] = None, 
                           variety: Optional[str] = None,
                           min_points: int = 90,
                           top_n: int = 10) -> pd.DataFrame:
        """
        Recommend wines based on points/ratings.
        
        Args:
            country (str, optional): Filter by country. If None, all countries.
            variety (str, optional): Filter by wine variety. If None, all varieties.
            min_points (int): Minimum points threshold (default: 90)
            top_n (int): Number of recommendations to return (default: 10)
            
        Returns:
            pd.DataFrame: Top N recommended wines
        """
        filtered_df = self.df[self.df['points'] >= min_points].copy()
        
        if country and country.lower() != 'all':
            filtered_df = filtered_df[filtered_df['country'].str.lower() == country.lower()]
        
        if variety and variety.lower() != 'all':
            filtered_df = filtered_df[filtered_df['variety'].str.lower() == variety.lower()]
        
        # Sort by points (descending) and then by price (ascending) for value
        filtered_df['value_score'] = filtered_df['points'] / (filtered_df['price'].fillna(filtered_df['price'].median()) + 1)
        
        result = filtered_df.nlargest(top_n, ['points', 'value_score'])
        
        return result[['title', 'country', 'variety', 'points', 'price', 'description', 'winery']].reset_index(drop=True)
    
    def recommend_by_taster(self, 
                           taster_name: str, 
                           top_n: int = 10) -> pd.DataFrame:
        """
        Recommend wines based on a specific taster's highest ratings.
        
        Args:
            taster_name (str): Name of the wine taster
            top_n (int): Number of recommendations to return (default: 10)
            
        Returns:
            pd.DataFrame: Top N wines reviewed by the specified taster
        """
        if 'taster_name' not in self.df.columns:
            raise ValueError("Dataset does not contain 'taster_name' column")
        
        taster_df = self.df[self.df['taster_name'].str.lower() == taster_name.lower()].copy()
        
        if taster_df.empty:
            raise ValueError(f"No reviews found for taster: {taster_name}")
        
        result = taster_df.nlargest(top_n, 'points')
        
        return result[['title', 'country', 'variety', 'points', 'price', 'description', 'taster_name']].reset_index(drop=True)
    
    def get_available_tasters(self) -> List[str]:
        """
        Get list of all available tasters.
        
        Returns:
            List[str]: List of taster names
        """
        if 'taster_name' in self.df.columns:
            return sorted(self.df['taster_name'].dropna().unique().tolist())
        return []
    
    def get_available_countries(self) -> List[str]:
        """
        Get list of all available countries.
        
        Returns:
            List[str]: List of country names
        """
        if 'country' in self.df.columns:
            return sorted(self.df['country'].dropna().unique().tolist())
        return []
    
    def get_available_varieties(self, country: Optional[str] = None) -> List[str]:
        """
        Get list of all available wine varieties.
        
        Args:
            country (str, optional): Filter varieties by country
            
        Returns:
            List[str]: List of wine varieties
        """
        if 'variety' not in self.df.columns:
            return []
        
        df_filtered = self.df
        if country:
            df_filtered = df_filtered[df_filtered['country'].str.lower() == country.lower()]
        
        return sorted(df_filtered['variety'].dropna().unique().tolist())
    
    def build_content_based_model(self, features: List[str] = ['description', 'variety', 'country']):
        """
        Build content-based recommendation model using TF-IDF.
        
        Args:
            features (List[str]): List of feature columns to use for content-based filtering
        """
        # Combine text features
        self.df['combined_features'] = ''
        
        for feature in features:
            if feature in self.df.columns:
                self.df['combined_features'] += ' ' + self.df[feature].fillna('')
        
        # Create TF-IDF matrix
        tfidf = TfidfVectorizer(
            max_features=5000,
            stop_words='english',
            ngram_range=(1, 2),
            min_df=2
        )
        
        self.tfidf_matrix = tfidf.fit_transform(self.df['combined_features'])
        
        # Compute similarity matrix
        self.similarity_matrix = cosine_similarity(self.tfidf_matrix, self.tfidf_matrix)
        
        print(f"Content-based model built successfully. Matrix shape: {self.similarity_matrix.shape}")
    
    def recommend_similar_wines(self, 
                                wine_title: str, 
                                top_n: int = 10) -> pd.DataFrame:
        """
        Recommend wines similar to a given wine using content-based filtering.
        
        Args:
            wine_title (str): Title of the wine to find similar wines for
            top_n (int): Number of recommendations to return
            
        Returns:
            pd.DataFrame: Top N similar wines
        """
        if self.similarity_matrix is None:
            self.build_content_based_model()
        
        # Find the wine index
        matches = self.df[self.df['title'].str.contains(wine_title, case=False, na=False)]
        
        if matches.empty:
            raise ValueError(f"Wine '{wine_title}' not found in dataset")
        
        wine_idx = matches.index[0]
        
        # Get similarity scores
        similarity_scores = list(enumerate(self.similarity_matrix[wine_idx]))
        
        # Sort by similarity (excluding the wine itself)
        similarity_scores = sorted(similarity_scores, key=lambda x: x[1], reverse=True)[1:top_n+1]
        
        # Get wine indices
        wine_indices = [i[0] for i in similarity_scores]
        similarity_values = [i[1] for i in similarity_scores]
        
        result = self.df.iloc[wine_indices][['title', 'country', 'variety', 'points', 'price', 'description']].copy()
        result['similarity_score'] = similarity_values
        
        return result.reset_index(drop=True)
    
    def get_statistics(self) -> Dict[str, any]:
        """
        Get statistics about the wine dataset.
        
        Returns:
            Dict: Dictionary containing various statistics
        """
        stats = {
            'total_wines': len(self.df),
            'total_countries': self.df['country'].nunique() if 'country' in self.df.columns else 0,
            'total_varieties': self.df['variety'].nunique() if 'variety' in self.df.columns else 0,
            'total_tasters': self.df['taster_name'].nunique() if 'taster_name' in self.df.columns else 0,
            'avg_points': self.df['points'].mean() if 'points' in self.df.columns else 0,
            'avg_price': self.df['price'].mean() if 'price' in self.df.columns else 0,
            'point_range': (self.df['points'].min(), self.df['points'].max()) if 'points' in self.df.columns else (0, 0),
            'price_range': (self.df['price'].min(), self.df['price'].max()) if 'price' in self.df.columns else (0, 0),
        }
        
        return stats
    
    def recommend_by_budget(self, 
                           max_price: float, 
                           min_points: int = 85,
                           top_n: int = 10) -> pd.DataFrame:
        """
        Recommend best wines within a budget.
        
        Args:
            max_price (float): Maximum price willing to pay
            min_points (int): Minimum quality threshold (default: 85)
            top_n (int): Number of recommendations to return
            
        Returns:
            pd.DataFrame: Top N wines within budget sorted by value
        """
        if 'price' not in self.df.columns:
            raise ValueError("Dataset does not contain 'price' column")
        
        filtered_df = self.df[
            (self.df['price'] <= max_price) & 
            (self.df['points'] >= min_points) &
            (self.df['price'].notna())
        ].copy()
        
        # Calculate value score (points per dollar)
        filtered_df['value_score'] = filtered_df['points'] / filtered_df['price']
        
        result = filtered_df.nlargest(top_n, 'value_score')
        
        return result[['title', 'country', 'variety', 'points', 'price', 'value_score', 'description']].reset_index(drop=True)


if __name__ == "__main__":
    # Example usage
    print("Wine Recommender System")
    print("=" * 50)
    
    # This would be run with actual data
    # recommender = WineRecommender('data/processed/wines.csv')
    # print(recommender.get_statistics())
