"""
Tests for recommendation module
"""

import pytest
import pandas as pd
import tempfile
import os
from src.recommendation import WineRecommender


@pytest.fixture
def sample_wine_data():
    """Create sample wine data for testing."""
    data = {
        'country': ['US', 'France', 'Italy', 'US', 'Spain', 'France', 'Italy', 'US'],
        'description': [
            'Rich and complex Pinot Noir',
            'Elegant Bordeaux blend',
            'Classic Italian red',
            'Fruity Oregon Pinot',
            'Bold Tempranillo',
            'Delicate white wine',
            'Tuscan red wine',
            'California Chardonnay'
        ],
        'points': [95, 92, 88, 85, 90, 87, 93, 89],
        'price': [50.0, 100.0, 30.0, 25.0, 40.0, 45.0, 70.0, 35.0],
        'title': ['Wine A', 'Wine B', 'Wine C', 'Wine D', 'Wine E', 'Wine F', 'Wine G', 'Wine H'],
        'variety': ['Pinot Noir', 'Bordeaux-style Red', 'Sangiovese', 'Pinot Noir', 
                   'Tempranillo', 'Chardonnay', 'Sangiovese', 'Chardonnay'],
        'winery': ['Winery A', 'Winery B', 'Winery C', 'Winery D', 'Winery E', 'Winery F', 'Winery G', 'Winery H'],
        'taster_name': ['John', 'Jane', 'John', 'Bob', 'Jane', 'John', 'Bob', 'Jane']
    }
    return pd.DataFrame(data)


@pytest.fixture
def temp_csv_file(sample_wine_data):
    """Create a temporary CSV file with sample data."""
    with tempfile.NamedTemporaryFile(mode='w', delete=False, suffix='.csv') as f:
        sample_wine_data.to_csv(f.name, index=False)
        temp_path = f.name
    
    yield temp_path
    
    if os.path.exists(temp_path):
        os.remove(temp_path)


class TestWineRecommender:
    """Test cases for WineRecommender class."""
    
    def test_initialization(self, temp_csv_file):
        """Test recommender initialization."""
        recommender = WineRecommender(temp_csv_file)
        assert recommender.df is not None
        assert len(recommender.df) == 8
    
    def test_recommend_by_points(self, temp_csv_file):
        """Test point-based recommendations."""
        recommender = WineRecommender(temp_csv_file)
        
        recommendations = recommender.recommend_by_points(min_points=90, top_n=3)
        
        assert len(recommendations) <= 3
        assert all(recommendations['points'] >= 90)
        assert recommendations['points'].is_monotonic_decreasing or len(recommendations) <= 1
    
    def test_recommend_by_points_with_filters(self, temp_csv_file):
        """Test point-based recommendations with country filter."""
        recommender = WineRecommender(temp_csv_file)
        
        recommendations = recommender.recommend_by_points(country='US', min_points=80, top_n=5)
        
        assert all(recommendations['country'] == 'US')
        assert all(recommendations['points'] >= 80)
    
    def test_recommend_by_variety(self, temp_csv_file):
        """Test recommendations filtered by variety."""
        recommender = WineRecommender(temp_csv_file)
        
        recommendations = recommender.recommend_by_points(variety='Pinot Noir', top_n=5)
        
        assert all(recommendations['variety'] == 'Pinot Noir')
    
    def test_recommend_by_taster(self, temp_csv_file):
        """Test taster-based recommendations."""
        recommender = WineRecommender(temp_csv_file)
        
        recommendations = recommender.recommend_by_taster('John', top_n=3)
        
        assert len(recommendations) <= 3
        assert all(recommendations['taster_name'] == 'John')
    
    def test_recommend_by_taster_invalid(self, temp_csv_file):
        """Test taster-based recommendations with invalid taster."""
        recommender = WineRecommender(temp_csv_file)
        
        with pytest.raises(ValueError):
            recommender.recommend_by_taster('NonExistentTaster', top_n=5)
    
    def test_get_available_tasters(self, temp_csv_file):
        """Test getting list of tasters."""
        recommender = WineRecommender(temp_csv_file)
        
        tasters = recommender.get_available_tasters()
        
        assert isinstance(tasters, list)
        assert len(tasters) > 0
        assert 'John' in tasters
        assert 'Jane' in tasters
    
    def test_get_available_countries(self, temp_csv_file):
        """Test getting list of countries."""
        recommender = WineRecommender(temp_csv_file)
        
        countries = recommender.get_available_countries()
        
        assert isinstance(countries, list)
        assert 'US' in countries
        assert 'France' in countries
        assert 'Italy' in countries
    
    def test_get_available_varieties(self, temp_csv_file):
        """Test getting list of varieties."""
        recommender = WineRecommender(temp_csv_file)
        
        varieties = recommender.get_available_varieties()
        
        assert isinstance(varieties, list)
        assert 'Pinot Noir' in varieties
        assert 'Chardonnay' in varieties
    
    def test_build_content_based_model(self, temp_csv_file):
        """Test building content-based model."""
        recommender = WineRecommender(temp_csv_file)
        
        recommender.build_content_based_model()
        
        assert recommender.tfidf_matrix is not None
        assert recommender.similarity_matrix is not None
        assert recommender.similarity_matrix.shape[0] == len(recommender.df)
    
    def test_recommend_similar_wines(self, temp_csv_file):
        """Test similar wine recommendations."""
        recommender = WineRecommender(temp_csv_file)
        
        recommendations = recommender.recommend_similar_wines('Wine A', top_n=3)
        
        assert len(recommendations) <= 3
        assert 'similarity_score' in recommendations.columns
        assert 'Wine A' not in recommendations['title'].values
    
    def test_get_statistics(self, temp_csv_file):
        """Test getting dataset statistics."""
        recommender = WineRecommender(temp_csv_file)
        
        stats = recommender.get_statistics()
        
        assert 'total_wines' in stats
        assert 'total_countries' in stats
        assert 'avg_points' in stats
        assert stats['total_wines'] == 8
    
    def test_recommend_by_budget(self, temp_csv_file):
        """Test budget-based recommendations."""
        recommender = WineRecommender(temp_csv_file)
        
        recommendations = recommender.recommend_by_budget(max_price=50, min_points=85, top_n=5)
        
        assert all(recommendations['price'] <= 50)
        assert all(recommendations['points'] >= 85)
        assert 'value_score' in recommendations.columns


if __name__ == '__main__':
    pytest.main([__file__, '-v'])
