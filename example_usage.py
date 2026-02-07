#!/usr/bin/env python
"""
Example usage of the Wine Recommendation System

This script demonstrates how to use the main components of the
wine recommendation system programmatically.
"""

from src.data_processing import WineDataProcessor
from src.recommendation import WineRecommender
from src.visualization import WineVisualizer


def example_data_processing():
    """Example: Data processing and cleaning."""
    print("=" * 60)
    print("EXAMPLE 1: Data Processing")
    print("=" * 60)
    
    # Initialize processor
    processor = WineDataProcessor('data/raw/winemag-data-130k-v2.csv')
    
    # Get initial info
    print("\nInitial data info:")
    info = processor.get_info()
    print(f"Shape: {info['shape']}")
    print(f"Columns: {len(info['columns'])}")
    
    # Clean data
    print("\nCleaning data...")
    processor.handle_missing_values(strategy='drop')
    processor.remove_duplicates()
    processor.add_continent()
    
    # Get statistics
    print("\nStatistical summary:")
    print(processor.get_statistics())
    
    # Save processed data
    processor.save_processed_data('data/processed/wines.csv')
    
    print("\n✓ Data processing complete!")


def example_recommendations():
    """Example: Getting wine recommendations."""
    print("\n" + "=" * 60)
    print("EXAMPLE 2: Wine Recommendations")
    print("=" * 60)
    
    # Initialize recommender
    recommender = WineRecommender('data/processed/wines.csv')
    
    # Get statistics
    print("\nDataset statistics:")
    stats = recommender.get_statistics()
    for key, value in stats.items():
        print(f"  {key}: {value}")
    
    # Example 1: Top-rated wines from France
    print("\n1. Top 5 French wines:")
    french_wines = recommender.recommend_by_points(
        country='France',
        min_points=95,
        top_n=5
    )
    print(french_wines[['title', 'points', 'price']])
    
    # Example 2: Best value wines under $30
    print("\n2. Best value wines under $30:")
    value_wines = recommender.recommend_by_budget(
        max_price=30,
        min_points=90,
        top_n=5
    )
    print(value_wines[['title', 'points', 'price', 'value_score']])
    
    # Example 3: Recommendations from a specific taster
    tasters = recommender.get_available_tasters()
    if tasters:
        print(f"\n3. Top picks from {tasters[0]}:")
        taster_recs = recommender.recommend_by_taster(tasters[0], top_n=5)
        print(taster_recs[['title', 'points', 'price']])
    
    # Example 4: Similar wines using content-based filtering
    print("\n4. Finding similar wines...")
    recommender.build_content_based_model()
    
    # Get a sample wine
    sample_wine = recommender.df.iloc[0]['title']
    print(f"   Finding wines similar to: {sample_wine}")
    
    similar = recommender.recommend_similar_wines(sample_wine, top_n=3)
    print(similar[['title', 'similarity_score', 'points']])
    
    print("\n✓ Recommendations complete!")


def example_visualization():
    """Example: Data visualization."""
    print("\n" + "=" * 60)
    print("EXAMPLE 3: Data Visualization")
    print("=" * 60)
    
    # Initialize visualizer
    visualizer = WineVisualizer('data/processed/wines.csv')
    
    print("\nCreating visualizations...")
    
    # Plot distributions
    print("  - Points distribution")
    visualizer.plot_points_distribution()
    
    print("  - Price distribution")
    visualizer.plot_price_distribution(max_price=200)
    
    print("  - Price vs Points relationship")
    visualizer.plot_price_vs_points()
    
    # Plot top countries and varieties
    print("  - Top countries")
    visualizer.plot_top_countries(top_n=10)
    
    print("  - Top varieties")
    visualizer.plot_top_varieties(top_n=10)
    
    # Create comprehensive dashboard
    print("  - Summary dashboard")
    visualizer.create_summary_dashboard(save_path='images/dashboard.png')
    
    print("\n✓ Visualizations complete!")


def example_complete_workflow():
    """Example: Complete workflow from data to recommendations."""
    print("\n" + "=" * 60)
    print("EXAMPLE 4: Complete Workflow")
    print("=" * 60)
    
    # Step 1: Process data
    print("\nStep 1: Processing data...")
    processor = WineDataProcessor('data/raw/winemag-data-130k-v2.csv')
    processor.handle_missing_values(strategy='drop')
    processor.remove_duplicates()
    processor.add_continent()
    processor.filter_by_points(min_points=85)  # Only wines rated 85+
    processor.save_processed_data('data/processed/wines_clean.csv')
    
    # Step 2: Get recommendations
    print("\nStep 2: Getting recommendations...")
    recommender = WineRecommender('data/processed/wines_clean.csv')
    
    # Find top Pinot Noir wines from US under $50
    recommendations = recommender.recommend_by_points(
        country='US',
        variety='Pinot Noir',
        min_points=90,
        top_n=10
    )
    
    print("\nTop 10 US Pinot Noir wines (90+ points):")
    print(recommendations[['title', 'points', 'price', 'winery']])
    
    # Step 3: Visualize
    print("\nStep 3: Creating visualizations...")
    visualizer = WineVisualizer('data/processed/wines_clean.csv')
    visualizer.plot_value_analysis(top_n=10)
    
    print("\n✓ Workflow complete!")


def main():
    """Run all examples."""
    print("\n" + "🍷" * 30)
    print("Wine Recommendation System - Example Usage")
    print("🍷" * 30)
    
    # Check if data exists
    import os
    
    if not os.path.exists('data/processed/wines.csv'):
        print("\n⚠️  Warning: Processed data not found.")
        print("Please run data processing first:")
        print("  python src/data_processing.py data/raw/winemag-data-130k-v2.csv data/processed/wines.csv")
        print("\nRunning data processing example only...\n")
        
        if os.path.exists('data/raw/winemag-data-130k-v2.csv'):
            example_data_processing()
        else:
            print("Error: Raw data not found. Please download from Kaggle:")
            print("https://www.kaggle.com/zynicide/wine-reviews")
        return
    
    # Run examples
    try:
        example_recommendations()
        
        # Uncomment to run visualization examples
        # example_visualization()
        
        # Uncomment to run complete workflow
        # example_complete_workflow()
        
    except Exception as e:
        print(f"\n❌ Error: {e}")
        print("Make sure you have the processed data available.")
    
    print("\n" + "🍷" * 30)
    print("Examples complete! Enjoy exploring wines!")
    print("🍷" * 30 + "\n")


if __name__ == "__main__":
    main()
