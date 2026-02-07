"""
Streamlit Web Application for Wine Recommendation System

This application provides an interactive interface for exploring wine data
and getting personalized wine recommendations.
"""

import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from pathlib import Path
import sys

# Add src to path
sys.path.insert(0, str(Path(__file__).parent))

from src.recommendation import WineRecommender
from src.visualization import WineVisualizer

# Page configuration
st.set_page_config(
    page_title="Wine Recommendation System",
    page_icon="🍷",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS
st.markdown("""
    <style>
    .main-header {
        font-size: 3rem;
        font-weight: bold;
        color: #8B0000;
        text-align: center;
        padding: 1rem;
    }
    .sub-header {
        font-size: 1.5rem;
        color: #4A4A4A;
        text-align: center;
        padding-bottom: 2rem;
    }
    .metric-card {
        background-color: #F8F9FA;
        padding: 1rem;
        border-radius: 0.5rem;
        border: 1px solid #DEE2E6;
    }
    </style>
""", unsafe_allow_html=True)


@st.cache_data
def load_data(data_path):
    """Load wine data with caching."""
    try:
        df = pd.read_csv(data_path)
        return df
    except Exception as e:
        st.error(f"Error loading data: {e}")
        return None


@st.cache_resource
def initialize_recommender(data_path):
    """Initialize recommender with caching."""
    return WineRecommender(data_path)


def main():
    """Main application function."""
    
    # Header
    st.markdown('<div class="main-header">🍷 Wine Recommendation System</div>', unsafe_allow_html=True)
    st.markdown('<div class="sub-header">Discover your perfect wine using AI-powered recommendations</div>', unsafe_allow_html=True)
    
    # Sidebar
    st.sidebar.title("Navigation")
    page = st.sidebar.radio(
        "Choose a page:",
        ["🏠 Home", "🔍 Explore Data", "⭐ Recommendations", "📊 Analytics"]
    )
    
    # Data path configuration
    data_path = st.sidebar.text_input(
        "Data Path",
        value="data/processed/wines.csv",
        help="Path to the processed wine data CSV file"
    )
    
    # Check if data file exists
    if not Path(data_path).exists():
        st.warning(f"""
        ⚠️ Data file not found at `{data_path}`
        
        Please follow these steps:
        1. Download wine data from [Kaggle Wine Reviews](https://www.kaggle.com/zynicide/wine-reviews)
        2. Place it in `data/raw/`
        3. Run the data cleaning notebook or script
        4. Update the data path in the sidebar
        """)
        return
    
    # Load data and initialize recommender
    df = load_data(data_path)
    if df is None:
        return
    
    recommender = initialize_recommender(data_path)
    
    # Page routing
    if page == "🏠 Home":
        show_home_page(recommender, df)
    elif page == "🔍 Explore Data":
        show_explore_page(df)
    elif page == "⭐ Recommendations":
        show_recommendations_page(recommender)
    elif page == "📊 Analytics":
        show_analytics_page(df)


def show_home_page(recommender, df):
    """Display home page with overview statistics."""
    st.header("Welcome to Wine Recommendation System")
    
    stats = recommender.get_statistics()
    
    # Display metrics
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.metric("Total Wines", f"{stats['total_wines']:,}")
    with col2:
        st.metric("Countries", stats['total_countries'])
    with col3:
        st.metric("Varieties", stats['total_varieties'])
    with col4:
        st.metric("Avg Rating", f"{stats['avg_points']:.1f}")
    
    st.markdown("---")
    
    # Quick recommendations
    st.subheader("🏆 Top Rated Wines")
    top_wines = recommender.recommend_by_points(min_points=95, top_n=5)
    st.dataframe(top_wines, use_container_width=True)
    
    st.markdown("---")
    
    # Best value wines
    st.subheader("💎 Best Value Wines")
    value_wines = recommender.recommend_by_budget(max_price=50, min_points=90, top_n=5)
    if len(value_wines) > 0:
        st.dataframe(value_wines, use_container_width=True)
    else:
        st.info("No wines found matching the criteria.")


def show_explore_page(df):
    """Display data exploration page."""
    st.header("🔍 Explore Wine Data")
    
    # Filters
    col1, col2 = st.columns(2)
    
    with col1:
        countries = ['All'] + sorted(df['country'].dropna().unique().tolist())
        selected_country = st.selectbox("Filter by Country", countries)
    
    with col2:
        varieties = ['All'] + sorted(df['variety'].dropna().unique().tolist())
        selected_variety = st.selectbox("Filter by Variety", varieties)
    
    # Apply filters
    filtered_df = df.copy()
    if selected_country != 'All':
        filtered_df = filtered_df[filtered_df['country'] == selected_country]
    if selected_variety != 'All':
        filtered_df = filtered_df[filtered_df['variety'] == selected_variety]
    
    # Display filtered data
    st.subheader(f"Showing {len(filtered_df):,} wines")
    st.dataframe(filtered_df.head(100), use_container_width=True)
    
    # Visualizations
    st.markdown("---")
    st.subheader("Distribution Charts")
    
    col1, col2 = st.columns(2)
    
    with col1:
        # Points distribution
        fig_points = px.histogram(
            filtered_df, 
            x='points', 
            nbins=30,
            title='Distribution of Ratings',
            labels={'points': 'Rating', 'count': 'Count'}
        )
        st.plotly_chart(fig_points, use_container_width=True)
    
    with col2:
        # Price distribution
        fig_price = px.histogram(
            filtered_df[filtered_df['price'].notna()], 
            x='price', 
            nbins=50,
            title='Distribution of Prices',
            labels={'price': 'Price ($)', 'count': 'Count'}
        )
        st.plotly_chart(fig_price, use_container_width=True)


def show_recommendations_page(recommender):
    """Display recommendations page."""
    st.header("⭐ Get Wine Recommendations")
    
    # Recommendation type selector
    rec_type = st.radio(
        "Choose recommendation type:",
        ["By Rating & Filters", "By Taster", "Similar Wines", "By Budget"]
    )
    
    st.markdown("---")
    
    if rec_type == "By Rating & Filters":
        show_rating_recommendations(recommender)
    elif rec_type == "By Taster":
        show_taster_recommendations(recommender)
    elif rec_type == "Similar Wines":
        show_similar_recommendations(recommender)
    elif rec_type == "By Budget":
        show_budget_recommendations(recommender)


def show_rating_recommendations(recommender):
    """Show rating-based recommendations."""
    st.subheader("Find wines by rating and preferences")
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        countries = ['All'] + recommender.get_available_countries()
        country = st.selectbox("Country", countries)
        country = None if country == 'All' else country
    
    with col2:
        varieties = ['All'] + recommender.get_available_varieties(country)
        variety = st.selectbox("Variety", varieties)
        variety = None if variety == 'All' else variety
    
    with col3:
        min_points = st.slider("Minimum Rating", 80, 100, 90)
    
    top_n = st.slider("Number of recommendations", 5, 50, 10)
    
    if st.button("Get Recommendations", type="primary"):
        with st.spinner("Finding the best wines..."):
            recommendations = recommender.recommend_by_points(
                country=country,
                variety=variety,
                min_points=min_points,
                top_n=top_n
            )
            
            if len(recommendations) > 0:
                st.success(f"Found {len(recommendations)} wines!")
                st.dataframe(recommendations, use_container_width=True)
            else:
                st.warning("No wines found matching your criteria. Try adjusting the filters.")


def show_taster_recommendations(recommender):
    """Show taster-based recommendations."""
    st.subheader("Find wines recommended by your favorite taster")
    
    tasters = recommender.get_available_tasters()
    
    if not tasters:
        st.warning("No taster information available in the dataset.")
        return
    
    col1, col2 = st.columns(2)
    
    with col1:
        taster = st.selectbox("Select Taster", tasters)
    
    with col2:
        top_n = st.slider("Number of recommendations", 5, 50, 10)
    
    if st.button("Get Recommendations", type="primary"):
        with st.spinner("Finding recommendations..."):
            try:
                recommendations = recommender.recommend_by_taster(taster, top_n=top_n)
                st.success(f"Top {len(recommendations)} wines by {taster}!")
                st.dataframe(recommendations, use_container_width=True)
            except Exception as e:
                st.error(f"Error: {e}")


def show_similar_recommendations(recommender):
    """Show similar wine recommendations."""
    st.subheader("Find wines similar to one you like")
    
    wine_title = st.text_input("Enter wine name (or part of it)")
    top_n = st.slider("Number of recommendations", 5, 20, 10)
    
    if st.button("Find Similar Wines", type="primary"):
        if wine_title:
            with st.spinner("Building recommendation model..."):
                try:
                    recommendations = recommender.recommend_similar_wines(wine_title, top_n=top_n)
                    st.success(f"Found {len(recommendations)} similar wines!")
                    st.dataframe(recommendations, use_container_width=True)
                except ValueError as e:
                    st.error(f"Error: {e}")
                except Exception as e:
                    st.error(f"Unexpected error: {e}")
        else:
            st.warning("Please enter a wine name.")


def show_budget_recommendations(recommender):
    """Show budget-based recommendations."""
    st.subheader("Find the best wines within your budget")
    
    col1, col2 = st.columns(2)
    
    with col1:
        max_price = st.number_input("Maximum Price ($)", min_value=1, max_value=1000, value=50)
    
    with col2:
        min_points = st.slider("Minimum Rating", 80, 100, 85)
    
    top_n = st.slider("Number of recommendations", 5, 50, 10)
    
    if st.button("Find Best Value", type="primary"):
        with st.spinner("Finding best value wines..."):
            try:
                recommendations = recommender.recommend_by_budget(
                    max_price=max_price,
                    min_points=min_points,
                    top_n=top_n
                )
                
                if len(recommendations) > 0:
                    st.success(f"Found {len(recommendations)} great value wines!")
                    st.dataframe(recommendations, use_container_width=True)
                else:
                    st.warning("No wines found matching your criteria. Try adjusting the budget or rating threshold.")
            except Exception as e:
                st.error(f"Error: {e}")


def show_analytics_page(df):
    """Display analytics and visualizations page."""
    st.header("📊 Wine Analytics")
    
    # Price vs Rating scatter plot
    st.subheader("Price vs Rating Analysis")
    df_plot = df[df['price'].notna()].copy()
    
    fig_scatter = px.scatter(
        df_plot,
        x='price',
        y='points',
        color='country' if 'country' in df.columns else None,
        hover_data=['title', 'variety'],
        title='Wine Price vs Rating',
        labels={'price': 'Price ($)', 'points': 'Rating'}
    )
    st.plotly_chart(fig_scatter, use_container_width=True)
    
    # Top countries and varieties
    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader("Top 10 Countries")
        if 'country' in df.columns:
            country_counts = df['country'].value_counts().head(10)
            fig_countries = px.bar(
                x=country_counts.values,
                y=country_counts.index,
                orientation='h',
                labels={'x': 'Number of Wines', 'y': 'Country'}
            )
            st.plotly_chart(fig_countries, use_container_width=True)
    
    with col2:
        st.subheader("Top 10 Varieties")
        if 'variety' in df.columns:
            variety_counts = df['variety'].value_counts().head(10)
            fig_varieties = px.bar(
                x=variety_counts.values,
                y=variety_counts.index,
                orientation='h',
                labels={'x': 'Number of Wines', 'y': 'Variety'}
            )
            st.plotly_chart(fig_varieties, use_container_width=True)


if __name__ == "__main__":
    main()
