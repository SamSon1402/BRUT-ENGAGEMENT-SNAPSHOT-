"""
Synthetic data generator for Brut Content Engagement Dashboard.
Creates realistic social media engagement data across platforms, regions, and content themes.
"""

import pandas as pd
import numpy as np
from datetime import datetime, timedelta
import random
import os

def generate_synthetic_data(output_path="brut_social_media_data.csv", num_records=1000, seed=42):
    """
    Generate synthetic social media engagement data for Brut dashboard.
    
    Parameters:
    -----------
    output_path : str
        Path to save the CSV file
    num_records : int
        Number of records to generate
    seed : int
        Random seed for reproducibility
    
    Returns:
    --------
    pandas.DataFrame
        The generated data
    """
    # Set random seed for reproducibility
    np.random.seed(seed)
    
    # Constants
    platforms = ['Instagram', 'TikTok', 'Facebook', 'YouTube', 'Twitter']
    regions = ['France', 'US', 'India', 'UK', 'Germany', 'Brazil', 'Japan']
    themes = ['Environment', 'Social Justice', 'Politics', 'Entertainment', 
              'Technology', 'Health', 'Sports', 'Fashion', 'Food', 'Travel']

    # Generate dates for the last 6 months
    end_date = datetime.now()
    start_date = end_date - timedelta(days=180)
    dates = [start_date + timedelta(days=x) for x in range((end_date - start_date).days)]

    # Create empty dataframe
    data = []

    # Generate posts with realistic patterns
    for _ in range(num_records):
        date = random.choice(dates)
        platform = random.choice(platforms)
        region = random.choice(regions)
        theme = random.choice(themes)
        
        # Base metrics with some patterns
        # Different platforms have different engagement patterns
        if platform == 'TikTok':
            base_views = np.random.normal(50000, 15000)
            like_ratio = np.random.normal(0.15, 0.05)  # Higher like ratio on TikTok
            share_ratio = np.random.normal(0.04, 0.02)
            comment_ratio = np.random.normal(0.02, 0.01)
        elif platform == 'Instagram':
            base_views = np.random.normal(30000, 10000)
            like_ratio = np.random.normal(0.12, 0.04)
            share_ratio = np.random.normal(0.02, 0.01)
            comment_ratio = np.random.normal(0.03, 0.01)
        elif platform == 'YouTube':
            base_views = np.random.normal(25000, 8000)
            like_ratio = np.random.normal(0.08, 0.03)
            share_ratio = np.random.normal(0.01, 0.005)
            comment_ratio = np.random.normal(0.04, 0.02)  # Higher comment ratio on YouTube
        elif platform == 'Twitter':
            base_views = np.random.normal(15000, 5000)
            like_ratio = np.random.normal(0.07, 0.03)
            share_ratio = np.random.normal(0.05, 0.02)  # Higher share ratio on Twitter
            comment_ratio = np.random.normal(0.01, 0.005)
        else:  # Facebook
            base_views = np.random.normal(40000, 12000)
            like_ratio = np.random.normal(0.1, 0.04)
            share_ratio = np.random.normal(0.03, 0.01)
            comment_ratio = np.random.normal(0.02, 0.01)
        
        # Different themes have different popularity
        theme_multiplier = {
            'Environment': np.random.normal(1.2, 0.1),
            'Social Justice': np.random.normal(1.3, 0.1),
            'Politics': np.random.normal(1.1, 0.2),
            'Entertainment': np.random.normal(1.4, 0.1),
            'Technology': np.random.normal(0.9, 0.1),
            'Health': np.random.normal(1.0, 0.1),
            'Sports': np.random.normal(1.1, 0.1),
            'Fashion': np.random.normal(0.8, 0.1),
            'Food': np.random.normal(0.9, 0.1),
            'Travel': np.random.normal(1.0, 0.1)
        }
        
        # Different regions have different engagement levels
        region_multiplier = {
            'France': np.random.normal(1.1, 0.1),
            'US': np.random.normal(1.2, 0.1),
            'India': np.random.normal(1.3, 0.1),
            'UK': np.random.normal(1.0, 0.1),
            'Germany': np.random.normal(0.9, 0.1),
            'Brazil': np.random.normal(1.1, 0.1),
            'Japan': np.random.normal(0.8, 0.1)
        }
        
        # Calculate final metrics
        views = max(int(base_views * theme_multiplier[theme] * region_multiplier[region]), 100)
        likes = max(int(views * like_ratio), 0)
        shares = max(int(views * share_ratio), 0)
        comments = max(int(views * comment_ratio), 0)
        
        # Add time component - posts during weekends tend to get more engagement
        if date.weekday() >= 5:  # Weekend
            views = int(views * np.random.normal(1.2, 0.1))
            likes = int(likes * np.random.normal(1.2, 0.1))
            shares = int(shares * np.random.normal(1.2, 0.1))
            comments = int(comments * np.random.normal(1.2, 0.1))
        
        # Add randomized hour component to timestamp
        hour = np.random.randint(8, 23)
        minute = np.random.randint(0, 60)
        timestamp = datetime(date.year, date.month, date.day, hour, minute)
        
        data.append({
            'timestamp': timestamp,
            'platform': platform,
            'region': region,
            'content_theme': theme,
            'views': views,
            'likes': likes,
            'shares': shares,
            'comments': comments
        })

    # Create DataFrame and sort by timestamp
    df = pd.DataFrame(data)
    df = df.sort_values('timestamp')

    # Save to CSV if output path is provided
    if output_path:
        # Create directory if it doesn't exist
        output_dir = os.path.dirname(output_path)
        if output_dir and not os.path.exists(output_dir):
            os.makedirs(output_dir)
            
        df.to_csv(output_path, index=False)
        print(f"Generated {len(df)} records of synthetic social media data")
        print(f"Saved to {output_path}")

    return df

def load_or_generate_data(file_path="brut_social_media_data.csv"):
    """
    Load existing data or generate new data if file doesn't exist.
    
    Parameters:
    -----------
    file_path : str
        Path to the CSV file
    
    Returns:
    --------
    pandas.DataFrame
        The loaded or generated data
    """
    try:
        # Try to read the CSV file
        df = pd.read_csv(file_path)
        df['timestamp'] = pd.to_datetime(df['timestamp'])
        return df
    except FileNotFoundError:
        # If file doesn't exist, generate synthetic data
        print(f"Data file not found at {file_path}. Generating synthetic data...")
        return generate_synthetic_data(file_path)

if __name__ == "__main__":
    # When run directly, generate a new dataset
    generate_synthetic_data()