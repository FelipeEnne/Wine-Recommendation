"""
Visualization Module for Wine Recommendation System

This module contains functions for creating various visualizations
of wine data including distribution plots, geographic analysis, and more.
"""

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from typing import Optional, List, Tuple
import warnings

warnings.filterwarnings('ignore')

# Set default style
plt.style.use('fivethirtyeight')
sns.set_palette("husl")


class WineVisualizer:
    """
    A class for creating visualizations of wine data.
    
    Attributes:
        df (pd.DataFrame): The wine reviews dataframe
        figsize (Tuple[int, int]): Default figure size for plots
    """
    
    def __init__(self, data_path: str, figsize: Tuple[int, int] = (12, 6)):
        """
        Initialize the WineVisualizer.
        
        Args:
            data_path (str): Path to the CSV file containing wine reviews
            figsize (Tuple[int, int]): Default figure size (width, height)
        """
        self.df = pd.read_csv(data_path)
        self.figsize = figsize
        
    def plot_points_distribution(self, save_path: Optional[str] = None):
        """
        Plot distribution of wine points/ratings.
        
        Args:
            save_path (str, optional): Path to save the figure
        """
        fig, axes = plt.subplots(1, 2, figsize=self.figsize)
        
        # Histogram
        axes[0].hist(self.df['points'], bins=30, edgecolor='black', alpha=0.7)
        axes[0].set_xlabel('Points')
        axes[0].set_ylabel('Frequency')
        axes[0].set_title('Distribution of Wine Ratings')
        axes[0].axvline(self.df['points'].mean(), color='red', linestyle='--', label=f'Mean: {self.df["points"].mean():.1f}')
        axes[0].legend()
        
        # Box plot
        axes[1].boxplot(self.df['points'])
        axes[1].set_ylabel('Points')
        axes[1].set_title('Wine Ratings Box Plot')
        
        plt.tight_layout()
        
        if save_path:
            plt.savefig(save_path, dpi=300, bbox_inches='tight')
        
        plt.show()
    
    def plot_price_distribution(self, max_price: Optional[float] = None, save_path: Optional[str] = None):
        """
        Plot distribution of wine prices.
        
        Args:
            max_price (float, optional): Maximum price to display (for better visualization)
            save_path (str, optional): Path to save the figure
        """
        df_plot = self.df[self.df['price'].notna()].copy()
        
        if max_price:
            df_plot = df_plot[df_plot['price'] <= max_price]
        
        fig, axes = plt.subplots(1, 2, figsize=self.figsize)
        
        # Histogram
        axes[0].hist(df_plot['price'], bins=50, edgecolor='black', alpha=0.7)
        axes[0].set_xlabel('Price ($)')
        axes[0].set_ylabel('Frequency')
        axes[0].set_title('Distribution of Wine Prices')
        axes[0].axvline(df_plot['price'].median(), color='red', linestyle='--', label=f'Median: ${df_plot["price"].median():.2f}')
        axes[0].legend()
        
        # Log scale histogram
        axes[1].hist(df_plot['price'], bins=50, edgecolor='black', alpha=0.7, log=True)
        axes[1].set_xlabel('Price ($)')
        axes[1].set_ylabel('Frequency (log scale)')
        axes[1].set_title('Distribution of Wine Prices (Log Scale)')
        
        plt.tight_layout()
        
        if save_path:
            plt.savefig(save_path, dpi=300, bbox_inches='tight')
        
        plt.show()
    
    def plot_price_vs_points(self, save_path: Optional[str] = None):
        """
        Plot relationship between price and points.
        
        Args:
            save_path (str, optional): Path to save the figure
        """
        df_plot = self.df[self.df['price'].notna()].copy()
        
        plt.figure(figsize=self.figsize)
        plt.scatter(df_plot['price'], df_plot['points'], alpha=0.3, s=10)
        plt.xlabel('Price ($)')
        plt.ylabel('Points')
        plt.title('Wine Price vs Rating')
        
        # Add trend line
        z = np.polyfit(df_plot['price'], df_plot['points'], 1)
        p = np.poly1d(z)
        plt.plot(df_plot['price'], p(df_plot['price']), "r--", alpha=0.8, label=f'Trend: y={z[0]:.4f}x+{z[1]:.2f}')
        plt.legend()
        
        # Calculate correlation
        corr = df_plot['price'].corr(df_plot['points'])
        plt.text(0.05, 0.95, f'Correlation: {corr:.3f}', transform=plt.gca().transAxes, 
                verticalalignment='top', bbox=dict(boxstyle='round', facecolor='wheat', alpha=0.5))
        
        if save_path:
            plt.savefig(save_path, dpi=300, bbox_inches='tight')
        
        plt.show()
    
    def plot_top_countries(self, top_n: int = 15, save_path: Optional[str] = None):
        """
        Plot top countries by number of wines.
        
        Args:
            top_n (int): Number of top countries to display
            save_path (str, optional): Path to save the figure
        """
        if 'country' not in self.df.columns:
            print("Country column not found in dataset")
            return
        
        country_counts = self.df['country'].value_counts().head(top_n)
        
        plt.figure(figsize=self.figsize)
        country_counts.plot(kind='barh', color='steelblue')
        plt.xlabel('Number of Wines')
        plt.title(f'Top {top_n} Countries by Number of Wines')
        plt.gca().invert_yaxis()
        
        if save_path:
            plt.savefig(save_path, dpi=300, bbox_inches='tight')
        
        plt.show()
    
    def plot_top_varieties(self, top_n: int = 15, save_path: Optional[str] = None):
        """
        Plot top wine varieties by count.
        
        Args:
            top_n (int): Number of top varieties to display
            save_path (str, optional): Path to save the figure
        """
        if 'variety' not in self.df.columns:
            print("Variety column not found in dataset")
            return
        
        variety_counts = self.df['variety'].value_counts().head(top_n)
        
        plt.figure(figsize=self.figsize)
        variety_counts.plot(kind='barh', color='darkgreen')
        plt.xlabel('Number of Wines')
        plt.title(f'Top {top_n} Wine Varieties')
        plt.gca().invert_yaxis()
        
        if save_path:
            plt.savefig(save_path, dpi=300, bbox_inches='tight')
        
        plt.show()
    
    def plot_points_by_country(self, top_n: int = 15, save_path: Optional[str] = None):
        """
        Plot average points by country.
        
        Args:
            top_n (int): Number of countries to display
            save_path (str, optional): Path to save the figure
        """
        if 'country' not in self.df.columns:
            print("Country column not found in dataset")
            return
        
        # Get countries with enough samples
        country_counts = self.df['country'].value_counts()
        top_countries = country_counts.head(top_n).index
        
        df_filtered = self.df[self.df['country'].isin(top_countries)]
        
        plt.figure(figsize=self.figsize)
        df_filtered.boxplot(column='points', by='country', figsize=self.figsize)
        plt.xticks(rotation=45, ha='right')
        plt.xlabel('Country')
        plt.ylabel('Points')
        plt.title('Wine Ratings by Country')
        plt.suptitle('')  # Remove automatic title
        
        if save_path:
            plt.savefig(save_path, dpi=300, bbox_inches='tight')
        
        plt.show()
    
    def plot_value_analysis(self, top_n: int = 20, save_path: Optional[str] = None):
        """
        Plot wines with best value (points per dollar).
        
        Args:
            top_n (int): Number of wines to display
            save_path (str, optional): Path to save the figure
        """
        df_plot = self.df[self.df['price'].notna()].copy()
        df_plot['value_score'] = df_plot['points'] / df_plot['price']
        
        top_value = df_plot.nlargest(top_n, 'value_score')
        
        plt.figure(figsize=(self.figsize[0], self.figsize[1] + 2))
        plt.barh(range(top_n), top_value['value_score'])
        plt.yticks(range(top_n), [title[:50] + '...' if len(title) > 50 else title 
                                   for title in top_value['title']], fontsize=8)
        plt.xlabel('Points per Dollar')
        plt.title(f'Top {top_n} Wines by Value (Points/$)')
        plt.gca().invert_yaxis()
        
        if save_path:
            plt.savefig(save_path, dpi=300, bbox_inches='tight')
        
        plt.show()
    
    def create_summary_dashboard(self, save_path: Optional[str] = None):
        """
        Create a comprehensive dashboard with multiple visualizations.
        
        Args:
            save_path (str, optional): Path to save the figure
        """
        fig = plt.figure(figsize=(16, 12))
        gs = fig.add_gridspec(3, 3, hspace=0.3, wspace=0.3)
        
        # 1. Points distribution
        ax1 = fig.add_subplot(gs[0, 0])
        ax1.hist(self.df['points'], bins=30, edgecolor='black', alpha=0.7)
        ax1.set_xlabel('Points')
        ax1.set_ylabel('Frequency')
        ax1.set_title('Rating Distribution')
        
        # 2. Price distribution
        ax2 = fig.add_subplot(gs[0, 1])
        df_price = self.df[self.df['price'].notna()]
        ax2.hist(df_price['price'], bins=50, edgecolor='black', alpha=0.7)
        ax2.set_xlabel('Price ($)')
        ax2.set_ylabel('Frequency')
        ax2.set_title('Price Distribution')
        
        # 3. Price vs Points
        ax3 = fig.add_subplot(gs[0, 2])
        ax3.scatter(df_price['price'], df_price['points'], alpha=0.3, s=5)
        ax3.set_xlabel('Price ($)')
        ax3.set_ylabel('Points')
        ax3.set_title('Price vs Rating')
        
        # 4. Top countries
        ax4 = fig.add_subplot(gs[1, :])
        if 'country' in self.df.columns:
            country_counts = self.df['country'].value_counts().head(10)
            country_counts.plot(kind='bar', ax=ax4, color='steelblue')
            ax4.set_xlabel('Country')
            ax4.set_ylabel('Count')
            ax4.set_title('Top 10 Countries')
            plt.setp(ax4.xaxis.get_majorticklabels(), rotation=45, ha='right')
        
        # 5. Top varieties
        ax5 = fig.add_subplot(gs[2, :])
        if 'variety' in self.df.columns:
            variety_counts = self.df['variety'].value_counts().head(10)
            variety_counts.plot(kind='bar', ax=ax5, color='darkgreen')
            ax5.set_xlabel('Variety')
            ax5.set_ylabel('Count')
            ax5.set_title('Top 10 Wine Varieties')
            plt.setp(ax5.xaxis.get_majorticklabels(), rotation=45, ha='right')
        
        if save_path:
            plt.savefig(save_path, dpi=300, bbox_inches='tight')
        
        plt.show()


if __name__ == "__main__":
    # Example usage
    print("Wine Visualization Module")
    print("=" * 50)
    
    # This would be run with actual data
    # visualizer = WineVisualizer('data/processed/wines.csv')
    # visualizer.create_summary_dashboard()
