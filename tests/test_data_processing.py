"""
Tests for data processing module
"""

import pytest
import pandas as pd
import numpy as np
import tempfile
import os
from src.data_processing import WineDataProcessor, clean_wine_data


@pytest.fixture
def sample_wine_data():
    """Create sample wine data for testing."""
    data = {
        'country': ['US', 'France', 'Italy', 'US', None],
        'description': ['Great wine', 'Excellent', 'Amazing', 'Good', 'Ok'],
        'points': [95, 92, 88, 85, 90],
        'price': [50.0, 100.0, 30.0, None, 40.0],
        'province': ['California', 'Bordeaux', 'Tuscany', 'Oregon', 'Napa'],
        'title': ['Wine A', 'Wine B', 'Wine C', 'Wine D', 'Wine E'],
        'variety': ['Pinot Noir', 'Bordeaux-style Red', 'Sangiovese', 'Pinot Noir', 'Chardonnay'],
        'winery': ['Winery A', 'Winery B', 'Winery C', 'Winery D', 'Winery E']
    }
    return pd.DataFrame(data)


@pytest.fixture
def temp_csv_file(sample_wine_data):
    """Create a temporary CSV file with sample data."""
    with tempfile.NamedTemporaryFile(mode='w', delete=False, suffix='.csv') as f:
        sample_wine_data.to_csv(f.name, index=False)
        temp_path = f.name
    
    yield temp_path
    
    # Cleanup
    if os.path.exists(temp_path):
        os.remove(temp_path)


class TestWineDataProcessor:
    """Test cases for WineDataProcessor class."""
    
    def test_initialization(self, temp_csv_file):
        """Test processor initialization."""
        processor = WineDataProcessor(temp_csv_file)
        assert processor.df is not None
        assert len(processor.df) == 5
        assert processor.original_shape == (5, 8)
    
    def test_get_info(self, temp_csv_file):
        """Test get_info method."""
        processor = WineDataProcessor(temp_csv_file)
        info = processor.get_info()
        
        assert 'shape' in info
        assert 'columns' in info
        assert 'null_counts' in info
        assert info['shape'] == (5, 8)
    
    def test_handle_missing_values_drop(self, temp_csv_file):
        """Test dropping missing values."""
        processor = WineDataProcessor(temp_csv_file)
        original_len = len(processor.df)
        
        processor.handle_missing_values(strategy='drop')
        
        # Should have fewer rows after dropping nulls
        assert len(processor.df) < original_len
        assert processor.df.isnull().sum().sum() == 0
    
    def test_remove_duplicates(self, temp_csv_file):
        """Test duplicate removal."""
        processor = WineDataProcessor(temp_csv_file)
        
        # Add a duplicate row
        processor.df = pd.concat([processor.df, processor.df.iloc[[0]]], ignore_index=True)
        original_len = len(processor.df)
        
        processor.remove_duplicates()
        
        assert len(processor.df) < original_len
    
    def test_filter_by_points(self, temp_csv_file):
        """Test filtering by points."""
        processor = WineDataProcessor(temp_csv_file)
        
        processor.filter_by_points(min_points=90, max_points=100)
        
        assert all(processor.df['points'] >= 90)
        assert all(processor.df['points'] <= 100)
    
    def test_filter_by_price(self, temp_csv_file):
        """Test filtering by price."""
        processor = WineDataProcessor(temp_csv_file)
        
        processor.filter_by_price(min_price=40, max_price=100)
        
        assert all(processor.df['price'] >= 40)
        assert all(processor.df['price'] <= 100)
    
    def test_get_statistics(self, temp_csv_file):
        """Test statistics generation."""
        processor = WineDataProcessor(temp_csv_file)
        stats = processor.get_statistics()
        
        assert stats is not None
        assert 'points' in stats.columns
        assert 'price' in stats.columns
    
    def test_save_processed_data(self, temp_csv_file):
        """Test saving processed data."""
        processor = WineDataProcessor(temp_csv_file)
        
        with tempfile.NamedTemporaryFile(mode='w', delete=False, suffix='.csv') as f:
            output_path = f.name
        
        try:
            processor.save_processed_data(output_path)
            assert os.path.exists(output_path)
            
            # Verify saved data can be read
            saved_df = pd.read_csv(output_path)
            assert len(saved_df) == len(processor.df)
        finally:
            if os.path.exists(output_path):
                os.remove(output_path)
    
    def test_method_chaining(self, temp_csv_file):
        """Test method chaining capability."""
        processor = WineDataProcessor(temp_csv_file)
        
        result = processor.filter_by_points(min_points=85).filter_by_price(min_price=20)
        
        assert result is processor
        assert all(processor.df['points'] >= 85)


if __name__ == '__main__':
    pytest.main([__file__, '-v'])
