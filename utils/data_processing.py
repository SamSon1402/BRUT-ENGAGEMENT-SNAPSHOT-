"""
Data processing utilities for the Brut Engagement Dashboard.
Contains functions for filtering, aggregating, and calculating metrics.
"""

import pandas as pd
import numpy as np
from datetime import datetime

def calculate_kpis(df):
    """
    Calculate key performance indicators from the data.
    
    Parameters:
    -----------
    df : pandas.DataFrame
        Input data frame with engagement metrics
    
    Returns:
    --------
    dict
        Dictionary containing calculated KPIs
    """
    # Calculate engagement rate for each row
    if 'engagement_rate' not in df.columns:
        df['engagement_rate'] = ((df['likes'] + df['comments'] + df['shares']) / df['views'] * 100).round(2)
    
    # Calculate KPIs
    total_views = df['views'].sum()
    avg_likes = int(df['likes'].mean())
    avg_engagement = df['engagement_rate'].mean()
    total_posts = len(df)
    
    return {
        'total_views': total_views,
        'avg_likes': avg_likes,
        'avg_engagement': avg_engagement,
        'total_posts': total_posts
    }

def filter_dataframe(df, start_date=None, end_date=None, platforms=None, regions=None, themes=None):
    """
    Filter the dataframe based on selected criteria.
    
    Parameters:
    -----------
    df : pandas.DataFrame
        Input data frame to filter
    start_date : datetime.date, optional
        Start date for filtering
    end_date : datetime.date, optional
        End date for filtering
    platforms : list, optional
        List of platforms to include
    regions : list, optional
        List of regions to include
    themes : list, optional
        List of content themes to include
    
    Returns:
    --------
    pandas.DataFrame
        Filtered dataframe
    """
    filtered_df = df.copy()
    
    # Date filtering
    if start_date is not None:
        filtered_df = filtered_df[filtered_df['timestamp'].dt.date >= start_date]
    if end_date is not None:
        filtered_df = filtered_df[filtered_df['timestamp'].dt.date <= end_date]
    
    # Platform filtering
    if platforms is not None and len(platforms) > 0:
        filtered_df = filtered_df[filtered_df['platform'].isin(platforms)]
    
    # Region filtering
    if regions is not None and len(regions) > 0:
        filtered_df = filtered_df[filtered_df['region'].isin(regions)]
    
    # Theme filtering
    if themes is not None and len(themes) > 0:
        filtered_df = filtered_df[filtered_df['content_theme'].isin(themes)]
    
    return filtered_df

def get_platform_data(df):
    """
    Aggregate data by platform for visualization.
    
    Parameters:
    -----------
    df : pandas.DataFrame
        Input data frame with engagement metrics
    
    Returns:
    --------
    pandas.DataFrame
        Aggregated data by platform
    """
    return df.groupby('platform').agg({
        'views': 'sum',
        'likes': 'sum',
        'comments': 'sum',
        'shares': 'sum',
        'engagement_rate': 'mean'
    }).reset_index()

def get_theme_data(df, top_n=5):
    """
    Aggregate data by content theme for visualization.
    
    Parameters:
    -----------
    df : pandas.DataFrame
        Input data frame with engagement metrics
    top_n : int, optional
        Number of top themes to return
    
    Returns:
    --------
    pandas.DataFrame
        Aggregated data by theme, sorted by engagement rate
    """
    theme_data = df.groupby('content_theme').agg({
        'views': 'sum',
        'engagement_rate': 'mean'
    }).reset_index()
    
    # Sort by engagement rate and get top N
    return theme_data.sort_values('engagement_rate', ascending=False).head(top_n)

def get_time_series_data(df):
    """
    Aggregate data by date for time series visualization.
    
    Parameters:
    -----------
    df : pandas.DataFrame
        Input data frame with engagement metrics
    
    Returns:
    --------
    pandas.DataFrame
        Aggregated data by date
    """
    # Create a copy with date column
    time_data = df.copy()
    time_data['date'] = time_data['timestamp'].dt.date
    
    # Group by date
    time_series = time_data.groupby('date').agg({
        'views': 'sum',
        'likes': 'sum',
        'comments': 'sum',
        'shares': 'sum'
    }).reset_index()
    
    # Calculate engagement rate
    time_series['engagement_rate'] = ((time_series['likes'] + time_series['comments'] + time_series['shares']) / time_series['views'] * 100).round(2)
    
    return time_series

def prepare_display_data(df, n_rows=10):
    """
    Prepare data for display in the table.
    
    Parameters:
    -----------
    df : pandas.DataFrame
        Input data frame with engagement metrics
    n_rows : int, optional
        Number of rows to return
    
    Returns:
    --------
    pandas.DataFrame
        Processed data for display
    """
    display_df = df.copy()
    display_df['timestamp'] = display_df['timestamp'].dt.strftime('%Y-%m-%d %H:%M')
    display_df = display_df.sort_values('timestamp', ascending=False)
    
    return display_df.head(n_rows)