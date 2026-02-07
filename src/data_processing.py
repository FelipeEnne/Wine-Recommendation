"""
Data Processing Module for Wine Recommendation System

This module contains functions and classes for cleaning, processing,
and preparing wine review data for analysis and recommendation.
"""

import pandas as pd
import numpy as np
from typing import Optional, List, Tuple
import pycountry_convert as pc


class WineDataProcessor:
    """
    A class for processing wine review data.
    
    This class handles data cleaning, feature engineering, and preprocessing
    for the wine recommendation system.
    
    Attributes:
        df (pd.DataFrame): The wine reviews dataframe
        original_shape (Tuple[int, int]): Shape of the original dataframe
    """
    
    def __init__(self, data_path: str):
        """
        Initialize the WineDataProcessor.
        
        Args:
            data_path (str): Path to the CSV file containing wine reviews
        """
        self.df = pd.read_csv(data_path)
        self.original_shape = self.df.shape
        
    def get_info(self) -> dict:
        """
        Get basic information about the dataset.
        
        Returns:
            dict: Dictionary containing dataset statistics
        """
        return {
            'shape': self.df.shape,
            'columns': list(self.df.columns),
            'null_counts': self.df.isnull().sum().to_dict(),
            'dtypes': self.df.dtypes.to_dict(),
            'memory_usage': self.df.memory_usage(deep=True).sum() / 1024**2  # MB
        }
    
    def handle_missing_values(self, strategy: str = 'drop', columns: Optional[List[str]] = None) -> 'WineDataProcessor':
        """
        Handle missing values in the dataset.
        
        Args:
            strategy (str): Strategy to handle missing values ('drop', 'fill_mean', 'fill_median', 'fill_mode')
            columns (List[str], optional): Specific columns to process. If None, processes all columns.
            
        Returns:
            WineDataProcessor: Self for method chaining
        """
        if columns is None:
            columns = self.df.columns.tolist()
        
        if strategy == 'drop':
            self.df = self.df.dropna(subset=columns)
        elif strategy == 'fill_mean':
            for col in columns:
                if self.df[col].dtype in ['int64', 'float64']:
                    self.df[col].fillna(self.df[col].mean(), inplace=True)
        elif strategy == 'fill_median':
            for col in columns:
                if self.df[col].dtype in ['int64', 'float64']:
                    self.df[col].fillna(self.df[col].median(), inplace=True)
        elif strategy == 'fill_mode':
            for col in columns:
                self.df[col].fillna(self.df[col].mode()[0], inplace=True)
        
        return self
    
    def remove_duplicates(self) -> 'WineDataProcessor':
        """
        Remove duplicate rows from the dataset.
        
        Returns:
            WineDataProcessor: Self for method chaining
        """
        self.df = self.df.drop_duplicates()
        return self
    
    def add_continent(self) -> 'WineDataProcessor':
        """
        Add continent information based on country.
        
        Returns:
            WineDataProcessor: Self for method chaining
        """
        def get_continent(country_name: str) -> str:
            """Get continent from country name."""
            if pd.isna(country_name):
                return 'Unknown'
            
            try:
                country_code = pc.country_name_to_country_alpha2(country_name, cn_name_format="default")
                continent_code = pc.country_alpha2_to_continent_code(country_code)
                continent_name = pc.convert_continent_code_to_continent_name(continent_code)
                return continent_name
            except:
                # Handle special cases
                special_cases = {
                    'England': 'Europe',
                    'US': 'North America',
                    'United States': 'North America',
                }
                return special_cases.get(country_name, 'Unknown')
        
        if 'country' in self.df.columns:
            self.df['continent'] = self.df['country'].apply(get_continent)
        
        return self
    
    def filter_by_points(self, min_points: int = 80, max_points: int = 100) -> 'WineDataProcessor':
        """
        Filter wines by point range.
        
        Args:
            min_points (int): Minimum points threshold
            max_points (int): Maximum points threshold
            
        Returns:
            WineDataProcessor: Self for method chaining
        """
        self.df = self.df[(self.df['points'] >= min_points) & (self.df['points'] <= max_points)]
        return self
    
    def filter_by_price(self, min_price: float = 0, max_price: Optional[float] = None) -> 'WineDataProcessor':
        """
        Filter wines by price range.
        
        Args:
            min_price (float): Minimum price
            max_price (float, optional): Maximum price. If None, no upper limit.
            
        Returns:
            WineDataProcessor: Self for method chaining
        """
        if 'price' in self.df.columns:
            self.df = self.df[self.df['price'] >= min_price]
            if max_price is not None:
                self.df = self.df[self.df['price'] <= max_price]
        
        return self
    
    def save_processed_data(self, output_path: str) -> None:
        """
        Save processed data to CSV.
        
        Args:
            output_path (str): Path where to save the processed data
        """
        self.df.to_csv(output_path, index=False)
        print(f"Data saved to {output_path}")
        print(f"Original shape: {self.original_shape}, Final shape: {self.df.shape}")
        print(f"Rows removed: {self.original_shape[0] - self.df.shape[0]}")
    
    def get_statistics(self) -> pd.DataFrame:
        """
        Get statistical summary of numerical columns.
        
        Returns:
            pd.DataFrame: Statistical summary
        """
        return self.df.describe()
    
    def get_categorical_summary(self) -> dict:
        """
        Get summary of categorical columns.
        
        Returns:
            dict: Dictionary with value counts for each categorical column
        """
        categorical_cols = self.df.select_dtypes(include=['object']).columns
        return {col: self.df[col].value_counts().head(10).to_dict() for col in categorical_cols}


def clean_wine_data(input_path: str, output_path: str) -> pd.DataFrame:
    """
    Main function to clean wine review data.
    
    This is a convenience function that applies a standard cleaning pipeline.
    
    Args:
        input_path (str): Path to input CSV file
        output_path (str): Path to save cleaned CSV file
        
    Returns:
        pd.DataFrame: Cleaned dataframe
    """
    processor = WineDataProcessor(input_path)
    
    print("Initial data info:")
    print(processor.get_info())
    
    # Apply cleaning pipeline
    processor.handle_missing_values(strategy='drop')
    processor.remove_duplicates()
    processor.add_continent()
    
    # Save processed data
    processor.save_processed_data(output_path)
    
    return processor.df


if __name__ == "__main__":
    # Example usage
    import sys
    
    if len(sys.argv) > 2:
        input_file = sys.argv[1]
        output_file = sys.argv[2]
        clean_wine_data(input_file, output_file)
    else:
        print("Usage: python data_processing.py <input_csv> <output_csv>")
