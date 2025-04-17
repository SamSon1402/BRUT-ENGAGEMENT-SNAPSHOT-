import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import plotly.express as px
import plotly.graph_objects as go
from datetime import datetime, timedelta
import altair as alt
import time

# Set page configuration
st.set_page_config(
    page_title="Brut Engagement Dashboard",
    page_icon="🎮",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS for retro gaming aesthetic
retro_css = """
<style>
@import url('https://fonts.googleapis.com/css2?family=VT323&family=Space+Mono&display=swap');

/* Main Page */
.main .block-container {
    padding-top: 2rem;
    padding-bottom: 2rem;
    background-color: #121212 !important;
}

/* Retro Gaming Title */
.retro-title {
    font-family: 'VT323', monospace;
    text-align: center;
    color: #39ff14;
    font-size: 3.5rem;
    text-shadow: 4px 4px 0px #ff00ff, 0 0 5px #39ff14;
    padding: 10px;
    margin-bottom: 20px;
    background-color: #0a0a0a;
    background-image: linear-gradient(90deg, #0a0a0a 25%, #1f1f1f 25%, #1f1f1f 50%, #0a0a0a 50%, #0a0a0a 75%, #1f1f1f 75%, #1f1f1f 100%);
    background-size: 4px 4px;
    border: 4px solid #39ff14;
    box-shadow: 8px 8px 0px #ff00ff, 0 0 10px rgba(57, 255, 20, 0.7);
}

/* KPI Boxes */
.kpi-container {
    display: flex;
    justify-content: space-between;
    margin-bottom: 20px;
}

.kpi-box {
    font-family: 'VT323', monospace;
    text-align: center;
    background-color: #0a0a0a;
    color: #fff;
    padding: 15px;
    border: 3px solid;
    box-shadow: 5px 5px 0px #000, 0 0 8px rgba(255, 255, 255, 0.2);
    width: 23%;
}

.kpi-title {
    font-size: 1.2rem;
    margin-bottom: 5px;
    text-shadow: 0 0 4px rgba(255, 255, 255, 0.5);
}

.kpi-value {
    font-size: 2rem;
    font-weight: bold;
    text-shadow: 0 0 8px currentColor;
}

/* Sidebar */
.css-1d391kg, .css-12oz5g7, [data-testid="stSidebar"] {
    background-color: #0a0a0a !important;
    background-image: linear-gradient(90deg, #0a0a0a 25%, #1f1f1f 25%, #1f1f1f 50%, #0a0a0a 50%, #0a0a0a 75%, #1f1f1f 75%, #1f1f1f 100%);
    background-size: 4px 4px;
}

.css-1v0mbdj, [data-testid="stSidebarNav"] li div {
    font-family: 'VT323', monospace;
    font-size: 1.5rem;
    color: #39ff14 !important;
    text-shadow: 2px 2px 0px #ff00ff, 0 0 5px #39ff14;
}

/* Filters */
.stSelectbox div[data-baseweb="select"] {
    border: 2px solid #39ff14 !important;
    font-family: 'Space Mono', monospace;
}

.stMultiSelect div[data-baseweb="select"] {
    border: 2px solid #39ff14 !important;
    font-family: 'Space Mono', monospace;
}

/* Button */
.stButton button {
    font-family: 'VT323', monospace !important;
    font-size: 1.2rem !important;
    background-color: #000 !important;
    color: #39ff14 !important;
    border: 3px solid #39ff14 !important;
    box-shadow: 5px 5px 0px #ff00ff !important;
    transition: all 0.2s !important;
}

.stButton button:hover {
    transform: translate(2px, 2px) !important;
    box-shadow: 3px 3px 0px #ff00ff !important;
}

/* Loading animation */
.stProgress .st-bo {
    background-color: #39ff14 !important;
}

/* Chart styling */
.chart-container {
    background-color: #0a0a0a;
    border: 3px solid #39ff14;
    box-shadow: 8px 8px 0px #ff00ff, 0 0 10px rgba(57, 255, 20, 0.3);
    padding: 15px;
    margin-bottom: 20px;
}

/* Tables */
.dataframe {
    font-family: 'Space Mono', monospace !important;
    border: 2px solid #39ff14 !important;
    box-shadow: 0 0 10px rgba(57, 255, 20, 0.3) !important;
}

.dataframe th {
    background-color: #0a0a0a !important;
    color: #39ff14 !important;
    font-family: 'VT323', monospace !important;
    font-size: 1.2rem !important;
    text-shadow: 0 0 5px rgba(57, 255, 20, 0.5) !important;
}

.dataframe td {
    background-color: #1f1f1f !important;
    color: #fff !important;
    text-shadow: 0 0 2px rgba(255, 255, 255, 0.5) !important;
}

/* Section Headers */
.section-header {
    font-family: 'VT323', monospace;
    font-size: 2rem;
    color: #ff00ff;
    text-shadow: 2px 2px 0px #39ff14, 0 0 8px #ff00ff;
    margin: 20px 0 10px 0;
    border-left: 8px solid #39ff14;
    padding-left: 10px;
    background-color: rgba(10, 10, 10, 0.7);
    padding: 5px 10px;
    border-radius: 0 4px 4px 0;
}

/* Tooltip */
div[data-testid="stTooltipIcon"] {
    color: #ff00ff !important;
}

/* Plotly styling */
.js-plotly-plot {
    background-color: #0a0a0a !important;
}

/* Make plots more readable */
.js-plotly-plot .gtitle, .js-plotly-plot .xtitle, .js-plotly-plot .ytitle {
    text-shadow: 0 0 5px currentColor !important;
}

.js-plotly-plot .traces {
    filter: drop-shadow(0 0 3px rgba(255, 255, 255, 0.3)) !important;
}

/* Custom color palette for charts */
.retro-palette {
    --color1: #39ff14; /* Neon Green */
    --color2: #ff00ff; /* Magenta */
    --color3: #00ffff; /* Cyan */
    --color4: #ffff00; /* Yellow */
    --color5: #ff8000; /* Orange */
}

/* Animated Background Effects */
/* Global background animation container */
body::before {
    content: "";
    position: fixed;
    top: 0;
    left: 0;
    width: 100%;
    height: 100%;
    z-index: -10;
    background-color: #0a0a0a;
    background-image: 
        linear-gradient(90deg, rgba(0, 0, 0, 0.3) 50%, transparent 50%),
        linear-gradient(rgba(0, 0, 0, 0.3) 50%, transparent 50%);
    background-size: 2px 2px;
    pointer-events: none;
}

/* Scanline effect */
body::after {
    content: "";
    position: fixed;
    top: 0;
    left: 0;
    width: 100%;
    height: 100%;
    z-index: 1000;
    background: linear-gradient(
        to bottom,
        rgba(255, 255, 255, 0) 0%,
        rgba(255, 255, 255, 0.03) 50%,
        rgba(255, 255, 255, 0) 100%
    );
    animation: scanline 8s linear infinite;
    pointer-events: none;
    opacity: 0.3;
}

@keyframes scanline {
    0% {
        transform: translateY(-100vh);
    }
    100% {
        transform: translateY(100vh);
    }
}

/* Grid background */
.grid-background {
    position: fixed;
    top: 0;
    left: 0;
    right: 0;
    bottom: 0;
    z-index: -5;
    background: 
        linear-gradient(rgba(19, 42, 76, 0.1) 1px, transparent 1px),
        linear-gradient(90deg, rgba(19, 42, 76, 0.1) 1px, transparent 1px);
    background-size: 20px 20px;
    background-position: center center;
    animation: gridMove 120s linear infinite;
    transform: perspective(500px) rotateX(60deg);
    transform-origin: center bottom;
    pointer-events: none;
}

@keyframes gridMove {
    0% {
        background-position: 0 0;
    }
    100% {
        background-position: 0 1000px;
    }
}

/* Star particles */
.stars {
    position: fixed;
    top: 0;
    left: 0;
    width: 100%;
    height: 100%;
    z-index: -8;
    overflow: hidden;
    pointer-events: none;
}

.star {
    position: absolute;
    background-color: white;
    width: 2px;
    height: 2px;
    border-radius: 50%;
    opacity: 0;
    animation-name: starTwinkle;
    animation-timing-function: linear;
    animation-iteration-count: infinite;
}

@keyframes starTwinkle {
    0% {
        opacity: 0;
        transform: translateY(0);
    }
    10% {
        opacity: 1;
    }
    90% {
        opacity: 1;
    }
    100% {
        opacity: 0;
        transform: translateY(-1000px);
    }
}

/* CRT flicker effect */
.crt-flicker {
    position: fixed;
    top: 0;
    left: 0;
    width: 100%;
    height: 100%;
    z-index: 999;
    background-color: transparent;
    opacity: 0.03;
    pointer-events: none;
    animation: flicker 0.15s infinite alternate;
}

@keyframes flicker {
    0% {
        opacity: 0.01;
    }
    100% {
        opacity: 0.02;
    }
}

/* Glitch effect */
@keyframes glitch {
    0% {
        clip-path: inset(40% 0 61% 0);
        transform: translate(-20px, -10px);
    }
    20% {
        clip-path: inset(92% 0 1% 0);
        transform: translate(20px, 10px);
    }
    40% {
        clip-path: inset(43% 0 1% 0);
        transform: translate(-20px, -10px);
    }
    60% {
        clip-path: inset(25% 0 58% 0);
        transform: translate(20px, 10px);
    }
    80% {
        clip-path: inset(54% 0 7% 0);
        transform: translate(-20px, -10px);
    }
    100% {
        clip-path: inset(58% 0 43% 0);
        transform: translate(20px, 10px);
    }
}

/* Retro Animation Overlay */
.retro-overlay {
    position: fixed;
    top: 0;
    left: 0;
    width: 100%;
    height: 100%;
    background-image: radial-gradient(
        ellipse at center,
        transparent 0%,
        rgba(10, 10, 10, 0.1) 30%,
        rgba(10, 10, 10, 0.3) 100%
    );
    pointer-events: none;
    z-index: -3;
}

/* Neon glow pulse for section headers */
@keyframes neonPulse {
    0% {
        text-shadow: 2px 2px 0px #39ff14, 0 0 8px #ff00ff, 0 0 11px #ff00ff;
    }
    50% {
        text-shadow: 2px 2px 0px #39ff14, 0 0 18px #ff00ff, 0 0 21px #ff00ff;
    }
    100% {
        text-shadow: 2px 2px 0px #39ff14, 0 0 8px #ff00ff, 0 0 11px #ff00ff;
    }
}

/* Number Highlighter Effect */
.number-highlight {
    position: relative;
    display: inline-block;
    color: white;
    font-weight: bold;
    text-shadow: 0 0 8px currentColor;
    z-index: 1;
}

.number-highlight::before {
    content: "";
    position: absolute;
    top: 0;
    left: -2px;
    right: -2px;
    bottom: 0;
    background: linear-gradient(to right, rgba(0, 102, 255, 0.4), rgba(0, 195, 255, 0.7), rgba(0, 102, 255, 0.4));
    z-index: -1;
    border-radius: 3px;
    animation: pulse 2s infinite;
    box-shadow: 0 0 8px rgba(0, 153, 255, 0.7);
}

@keyframes pulse {
    0% { opacity: 0.7; }
    50% { opacity: 1; }
    100% { opacity: 0.7; }
}

/* For metrics in charts */
.js-plotly-plot .textpoint {
    filter: drop-shadow(0 0 5px rgba(0, 153, 255, 0.8)) !important;
}

/* Number-specific styles in tables */
.dataframe td:nth-child(n+5) {
    background: linear-gradient(to right, rgba(0, 102, 255, 0.2), rgba(0, 153, 255, 0.3), rgba(0, 102, 255, 0.2)) !important;
    font-weight: bold;
    text-shadow: 0 0 3px rgba(0, 153, 255, 0.8) !important;
}

/* Make the background dark but not pure black for better contrast */
body {
    background-color: #121212 !important;
    color: #fff !important;
}

/* Additional text contrast enhancement */
p, span, div {
    text-shadow: 0 0 2px rgba(255, 255, 255, 0.2);
}

/* Add text outlines to improve readability */
.stMarkdown h1, .stMarkdown h2, .stMarkdown h3 {
    text-shadow: 0 0 3px rgba(255, 255, 255, 0.3);
}

/* Make the background dark but not pure black for better contrast */
body {
    background-color: #121212 !important;
    color: #fff !important;
}

/* Additional text contrast enhancement */
p, span, div {
    text-shadow: 0 0 2px rgba(255, 255, 255, 0.2);
}

/* Add text outlines to improve readability */
.stMarkdown h1, .stMarkdown h2, .stMarkdown h3 {
    text-shadow: 0 0 3px rgba(255, 255, 255, 0.3);
}

</style>
"""

st.markdown(retro_css, unsafe_allow_html=True)

# Loading animation with enhanced visuals
def loading_animation():
    progress_text = "LOADING... PLEASE WAIT..."
    st.markdown("""
    <style>
    @keyframes pixelScanline {{
        0% {{ background-position: -100% 0; }}
        100% {{ background-position: 200% 0; }}
    }}
    .loading-container {{
        position: relative;
        height: 40px;
        margin: 20px 0;
        border: 3px solid #39ff14;
        overflow: hidden;
        background-color: #0a0a0a;
        box-shadow: 0 0 15px rgba(57, 255, 20, 0.5);
    }}
    .loading-text {{
        position: absolute;
        top: 50%;
        left: 50%;
        transform: translate(-50%, -50%);
        font-family: 'VT323', monospace;
        font-size: 24px;
        color: white;
        text-shadow: 0 0 5px #39ff14;
        z-index: 2;
    }}
    .loading-bar {{
        height: 100%;
        width: 0%;
        background: linear-gradient(90deg, 
            rgba(57, 255, 20, 0.6),
            rgba(57, 255, 20, 0.8),
            rgba(57, 255, 20, 0.6));
        transition: width 0.05s linear;
        z-index: 1;
    }}
    .loading-scanline {{
        position: absolute;
        top: 0;
        left: 0;
        width: 100%;
        height: 100%;
        background: linear-gradient(90deg,
            transparent 0%,
            rgba(57, 255, 20, 0.4) 50%,
            transparent 100%);
        background-size: 200% 100%;
        animation: pixelScanline 1s linear infinite;
        z-index: 3;
        pointer-events: none;
    }}
    </style>
    <div class="loading-container">
        <div class="loading-text">{}</div>
        <div class="loading-bar" id="loadingBar"></div>
        <div class="loading-scanline"></div>
    </div>
    <script>
        const loadingBar = document.getElementById('loadingBar');
        let width = 0;
        const interval = setInterval(() => {{
            if (width >= 100) {{
                clearInterval(interval);
            }} else {{
                width += 5;
                loadingBar.style.width = width + '%';
            }}
        }}, 50);
    </script>
    """.format(progress_text), unsafe_allow_html=True)
    
    # Simulate loading time
    time.sleep(2.5)
    
    # Clear the loading animation
    st.empty()

# Title with animation
st.markdown('<div class="retro-title">BRUT ENGAGEMENT SNAPSHOT</div>', unsafe_allow_html=True)

# Add animated background elements
st.markdown("""
<div class="grid-background"></div>
<div class="retro-overlay"></div>
<div class="crt-flicker"></div>

<div class="stars" id="stars"></div>

<script>
// Create animated stars
function createStars() {{
    const stars = document.getElementById('stars');
    const count = 50;
    
    for (let i = 0; i < count; i++) {{
        const star = document.createElement('div');
        star.className = 'star';
        
        // Random position
        star.style.left = Math.random() * 100 + 'vw';
        star.style.top = Math.random() * 100 + 'vh';
        
        // Random size
        const size = Math.random() * 2 + 1;
        star.style.width = size + 'px';
        star.style.height = size + 'px';
        
        // Random animation duration and delay
        const duration = Math.random() * 30 + 20;
        const delay = Math.random() * 30;
        star.style.animationDuration = duration + 's';
        star.style.animationDelay = delay + 's';
        
        stars.appendChild(star);
    }}
}}

// Initialize animations after a short delay
setTimeout(() => {{
    createStars();
    
    // Add occasional glitch effect
    setInterval(() => {{
        const title = document.querySelector('.retro-title');
        if (title) {{
            title.style.animation = 'glitch 0.5s linear';
            setTimeout(() => {{
                title.style.animation = '';
            }}, 500);
        }}
    }}, 10000);
}}, 1000);
</script>
""", unsafe_allow_html=True)

# Load Data
@st.cache_data
def load_data():
    try:
        # Try to read the CSV file
        df = pd.read_csv('brut_social_media_data.csv')
        df['timestamp'] = pd.to_datetime(df['timestamp'])
        return df
    except FileNotFoundError:
        # If file doesn't exist, generate synthetic data
        st.warning("Data file not found. Generating synthetic data...")
        
        # This is a simplified version of the data generation code
        # In a real application, you would import the data generator module
        # For demo purposes, we'll create a simple dataset here
        
        import numpy as np
        from datetime import datetime, timedelta
        import random
        
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
        
        # Generate 1000 posts with realistic patterns
        for _ in range(1000):
            date = random.choice(dates)
            platform = random.choice(platforms)
            region = random.choice(regions)
            theme = random.choice(themes)
            
            # Simplified metrics generation
            views = np.random.randint(5000, 100000)
            likes = int(views * np.random.uniform(0.05, 0.2))
            shares = int(views * np.random.uniform(0.01, 0.05))
            comments = int(views * np.random.uniform(0.01, 0.05))
            
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
        df.to_csv('brut_social_media_data.csv', index=False)
        return df

# Show loading animation
loading_animation()

# Load data
df = load_data()

# Calculate additional metrics
df['engagement_rate'] = ((df['likes'] + df['comments'] + df['shares']) / df['views'] * 100).round(2)

# Sidebar with retro styling
st.sidebar.markdown("""
<style>
@keyframes sidebarHover {{
    0% {{ border-left: 3px solid #39ff14; }}
    50% {{ border-left: 10px solid #39ff14; box-shadow: 0 0 10px rgba(57, 255, 20, 0.5); }}
    100% {{ border-left: 3px solid #39ff14; }}
}}
.game-controls-title {{
    font-family: 'VT323', monospace;
    color: #39ff14;
    text-shadow: 2px 2px 0px #ff00ff, 0 0 10px rgba(57, 255, 20, 0.7);
    animation: neonPulse 3s infinite;
    padding-left: 5px;
    border-left: 3px solid #39ff14;
    transition: all 0.3s ease;
}}
.game-controls-title:hover {{
    animation: sidebarHover 2s infinite;
}}
</style>
<h1 class="game-controls-title">GAME CONTROLS</h1>
""", unsafe_allow_html=True)

# Date Range Filter
st.sidebar.markdown("""
<style>
@keyframes sectionPulse {{
    0% {{ border-left: 3px solid #ff00ff; }}
    50% {{ border-left: 8px solid #ff00ff; box-shadow: 0 0 8px rgba(255, 0, 255, 0.5); }}
    100% {{ border-left: 3px solid #ff00ff; }}
}}
.sidebar-section {{
    font-family: 'VT323', monospace;
    font-size: 1.5rem;
    color: #ff00ff;
    text-shadow: 2px 2px 0px #39ff14, 0 0 8px rgba(255, 0, 255, 0.5);
    padding-left: 5px;
    border-left: 3px solid #ff00ff;
    margin-top: 20px;
    animation: sectionPulse 4s infinite;
}}
</style>
<div class="sidebar-section">TIME WINDOW</div>
""", unsafe_allow_html=True)
min_date = df['timestamp'].min().date()
max_date = df['timestamp'].max().date()
start_date = st.sidebar.date_input('START DATE', min_date, min_value=min_date, max_value=max_date)
end_date = st.sidebar.date_input('END DATE', max_date, min_value=min_date, max_value=max_date)

# Platform Filter
st.sidebar.markdown('<div class="sidebar-section">PLATFORMS</div>', unsafe_allow_html=True)
all_platforms = df['platform'].unique().tolist()
selected_platforms = st.sidebar.multiselect('SELECT PLATFORMS', all_platforms, default=all_platforms)

# Region Filter
st.sidebar.markdown('<div class="sidebar-section">REGIONS</div>', unsafe_allow_html=True)
all_regions = df['region'].unique().tolist()
selected_regions = st.sidebar.multiselect('SELECT REGIONS', all_regions, default=all_regions)

# Content Theme Filter
st.sidebar.markdown('<div class="sidebar-section">CONTENT THEMES</div>', unsafe_allow_html=True)
all_themes = df['content_theme'].unique().tolist()
selected_themes = st.sidebar.multiselect('SELECT THEMES', all_themes, default=all_themes)

# Filter data based on selections
filtered_df = df[
    (df['timestamp'].dt.date >= start_date) & 
    (df['timestamp'].dt.date <= end_date) &
    (df['platform'].isin(selected_platforms)) &
    (df['region'].isin(selected_regions)) &
    (df['content_theme'].isin(selected_themes))
]

# Reset button with retro styling
if st.sidebar.button('RESET FILTERS'):
    st.experimental_rerun()

# Check if data is available after filtering
if filtered_df.empty:
    st.error("NO DATA AVAILABLE FOR SELECTED FILTERS. PLEASE ADJUST YOUR SELECTION.")
    st.stop()

# Section headers with animated neon pulse
st.markdown('<div class="section-header" style="animation: neonPulse 2s infinite;">PERFORMANCE STATS</div>', unsafe_allow_html=True)

# Calculate KPIs
total_views = filtered_df['views'].sum()
avg_likes = int(filtered_df['likes'].mean())
avg_engagement = filtered_df['engagement_rate'].mean()
total_posts = len(filtered_df)

# Create 4 columns for KPIs
kpi1, kpi2, kpi3, kpi4 = st.columns(4)

with kpi1:
    st.markdown(f'''
    <div class="kpi-box" style="border-color: #39ff14; box-shadow: 5px 5px 0px #39ff14, 0 0 10px rgba(57, 255, 20, 0.5);">
        <div class="kpi-title">TOTAL VIEWS</div>
        <div class="kpi-value" style="color: #39ff14; text-shadow: 0 0 8px #39ff14;">
            <span class="number-highlight">{total_views:,}</span>
        </div>
    </div>
    ''', unsafe_allow_html=True)

with kpi2:
    st.markdown(f'''
    <div class="kpi-box" style="border-color: #ff00ff; box-shadow: 5px 5px 0px #ff00ff, 0 0 10px rgba(255, 0, 255, 0.5);">
        <div class="kpi-title">AVG LIKES</div>
        <div class="kpi-value" style="color: #ff00ff; text-shadow: 0 0 8px #ff00ff;">
            <span class="number-highlight">{avg_likes:,}</span>
        </div>
    </div>
    ''', unsafe_allow_html=True)

with kpi3:
    st.markdown(f'''
    <div class="kpi-box" style="border-color: #00ffff; box-shadow: 5px 5px 0px #00ffff, 0 0 10px rgba(0, 255, 255, 0.5);">
        <div class="kpi-title">AVG ENGAGEMENT</div>
        <div class="kpi-value" style="color: #00ffff; text-shadow: 0 0 8px #00ffff;">
            <span class="number-highlight">{avg_engagement:.2f}%</span>
        </div>
    </div>
    ''', unsafe_allow_html=True)

with kpi4:
    st.markdown(f'''
    <div class="kpi-box" style="border-color: #ffff00; box-shadow: 5px 5px 0px #ffff00, 0 0 10px rgba(255, 255, 0, 0.5);">
        <div class="kpi-title">TOTAL POSTS</div>
        <div class="kpi-value" style="color: #ffff00; text-shadow: 0 0 8px #ffff00;">
            <span class="number-highlight">{total_posts:,}</span>
        </div>
    </div>
    ''', unsafe_allow_html=True)

# Visualizations section with animated header
st.markdown('<div class="section-header" style="animation: neonPulse 2s infinite;">DATA VISUALIZATIONS</div>', unsafe_allow_html=True)

# Create two columns for charts
col1, col2 = st.columns(2)

with col1:
    st.markdown('<div style="font-family: \'VT323\', monospace; font-size: 1.5rem; color: #39ff14; margin-bottom: 10px; animation: pulse 2s infinite;">ENGAGEMENT BY PLATFORM</div>', unsafe_allow_html=True)
    
    # Prepare data for platform comparison
    platform_data = filtered_df.groupby('platform').agg({
        'views': 'sum',
        'likes': 'sum',
        'comments': 'sum',
        'shares': 'sum',
        'engagement_rate': 'mean'
    }).reset_index()
    
    # Create a custom bar chart with plotly and retro gaming colors
    fig = go.Figure()
    
    # Define retro colors
    colors = ['#39ff14', '#ff00ff', '#00ffff', '#ffff00', '#ff8000']
    
    # Add bars with gradient fill for better visibility and number highlighting
    fig.add_trace(go.Bar(
        x=platform_data['platform'],
        y=platform_data['engagement_rate'],
        name='Engagement Rate (%)',
        marker=dict(
            color='#39ff14',
            line=dict(color='#ffffff', width=1)
        ),
        text=platform_data['engagement_rate'].apply(lambda x: f'{x:.2f}%'),
        textposition='auto',
        textfont=dict(
            family='VT323, monospace',
            size=16,
            color='#ffffff',
            # Can't directly use CSS classes in Plotly, but we can simulate the blue highlight effect
            shadow=10  # This will make the text appear to glow
        ),
        hovertemplate='<span style="font-family: VT323, monospace; color: white; text-shadow: 0 0 8px #0066ff;">%{y:.2f}%</span><extra></extra>'
    ))
    
    # Customize layout
    fig.update_layout(
        paper_bgcolor='#0a0a0a',
        plot_bgcolor='#0a0a0a',
        font=dict(
            family='VT323, monospace',
            size=16,
            color='#ffffff'
        ),
        xaxis=dict(
            title='Platform',
            titlefont=dict(color='#39ff14'),
            tickfont=dict(color='#ffffff'),
            showgrid=False,
            gridcolor='#333333'
        ),
        yaxis=dict(
            title='Engagement Rate (%)',
            titlefont=dict(color='#39ff14'),
            tickfont=dict(color='#ffffff'),
            showgrid=True,
            gridcolor='#333333',
            gridwidth=0.5
        ),
        margin=dict(l=50, r=50, t=30, b=50)
    )
    
    # Add pixelated border effect using shapes
    fig.update_layout(
        shapes=[
            # Top border
            dict(type="rect", xref="paper", yref="paper", x0=0, y0=0.99, x1=1, y1=1, 
                 line=dict(color="#39ff14", width=4)),
            # Bottom border
            dict(type="rect", xref="paper", yref="paper", x0=0, y0=0, x1=1, y1=0.01, 
                 line=dict(color="#39ff14", width=4)),
            # Left border
            dict(type="rect", xref="paper", yref="paper", x0=0, y0=0, x1=0.01, y1=1, 
                 line=dict(color="#39ff14", width=4)),
            # Right border
            dict(type="rect", xref="paper", yref="paper", x0=0.99, y0=0, x1=1, y1=1, 
                 line=dict(color="#39ff14", width=4))
        ]
    )
    
    st.plotly_chart(fig, use_container_width=True)

with col2:
    st.markdown('<div style="font-family: \'VT323\', monospace; font-size: 1.5rem; color: #ff00ff; margin-bottom: 10px; animation: pulse 2s infinite;">TOP PERFORMING THEMES</div>', unsafe_allow_html=True)
    
    # Prepare data for content theme analysis
    theme_data = filtered_df.groupby('content_theme').agg({
        'views': 'sum',
        'engagement_rate': 'mean'
    }).reset_index().sort_values('engagement_rate', ascending=False).head(5)
    
    # Create a retro-styled horizontal bar chart
    fig = go.Figure()
    
    # Add bars with gradient fill for better visibility
    fig.add_trace(go.Bar(
        y=theme_data['content_theme'],
        x=theme_data['engagement_rate'],
        orientation='h',
        marker=dict(
            color='#ff00ff',
            line=dict(color='#ffffff', width=1)
        ),
        text=theme_data['engagement_rate'].apply(lambda x: f'{x:.2f}%'),
        textposition='auto',
        textfont=dict(
            family='VT323, monospace',
            size=16,
            color='#ffffff'
        )
    ))
    
    # Customize layout
    fig.update_layout(
        paper_bgcolor='#0a0a0a',
        plot_bgcolor='#0a0a0a',
        font=dict(
            family='VT323, monospace',
            size=16,
            color='#ffffff'
        ),
        xaxis=dict(
            title='Engagement Rate (%)',
            titlefont=dict(color='#ff00ff'),
            tickfont=dict(color='#ffffff'),
            showgrid=True,
            gridcolor='#333333',
            gridwidth=0.5
        ),
        yaxis=dict(
            title='Content Theme',
            titlefont=dict(color='#ff00ff'),
            tickfont=dict(color='#ffffff'),
            showgrid=False
        ),
        margin=dict(l=50, r=50, t=30, b=50)
    )
    
    # Add pixelated border effect using shapes
    fig.update_layout(
        shapes=[
            # Top border
            dict(type="rect", xref="paper", yref="paper", x0=0, y0=0.99, x1=1, y1=1, 
                 line=dict(color="#ff00ff", width=4)),
            # Bottom border
            dict(type="rect", xref="paper", yref="paper", x0=0, y0=0, x1=1, y1=0.01, 
                 line=dict(color="#ff00ff", width=4)),
            # Left border
            dict(type="rect", xref="paper", yref="paper", x0=0, y0=0, x1=0.01, y1=1, 
                 line=dict(color="#ff00ff", width=4)),
            # Right border
            dict(type="rect", xref="paper", yref="paper", x0=0.99, y0=0, x1=1, y1=1, 
                 line=dict(color="#ff00ff", width=4))
        ]
    )
    
    st.plotly_chart(fig, use_container_width=True)

# Time series visualization with animated header
st.markdown('<div style="font-family: \'VT323\', monospace; font-size: 1.5rem; color: #00ffff; margin-bottom: 10px; animation: pulse 2s infinite;">ENGAGEMENT TRENDS OVER TIME</div>', unsafe_allow_html=True)

# Prepare time series data
time_data = filtered_df.copy()
time_data['date'] = time_data['timestamp'].dt.date
time_series = time_data.groupby('date').agg({
    'views': 'sum',
    'likes': 'sum',
    'comments': 'sum',
    'shares': 'sum'
}).reset_index()

time_series['engagement_rate'] = ((time_series['likes'] + time_series['comments'] + time_series['shares']) / time_series['views'] * 100).round(2)

# Create a retro-styled line chart
fig = go.Figure()

# Add line
fig.add_trace(go.Scatter(
    x=time_series['date'],
    y=time_series['engagement_rate'],
    mode='lines+markers',
    name='Engagement Rate',
    line=dict(color='#00ffff', width=3),
    marker=dict(
        color='#000000',
        size=8,
        line=dict(
            color='#00ffff',
            width=2
        )
    )
))

# Customize layout
fig.update_layout(
    paper_bgcolor='#000000',
    plot_bgcolor='#000000',
    font=dict(
        family='VT323, monospace',
        size=16,
        color='#ffffff'
    ),
    xaxis=dict(
        title='Date',
        titlefont=dict(color='#00ffff'),
        tickfont=dict(color='#ffffff'),
        showgrid=False,
        gridcolor='#333333'
    ),
    yaxis=dict(
        title='Engagement Rate (%)',
        titlefont=dict(color='#00ffff'),
        tickfont=dict(color='#ffffff'),
        showgrid=True,
        gridcolor='#333333',
        gridwidth=0.5
    ),
    margin=dict(l=50, r=50, t=30, b=50)
)

# Add pixelated grid background effect
grid_lines = []
for i in range(0, 101, 10):  # Horizontal grid lines
    grid_lines.append(
        dict(type="line", xref="paper", yref="y", x0=0, y0=i, x1=1, y1=i, 
             line=dict(color="#333333", width=1, dash="dot"))
    )

fig.update_layout(shapes=grid_lines)

# Add pixelated border effect
fig.update_layout(
    shapes=grid_lines + [
        # Top border
        dict(type="rect", xref="paper", yref="paper", x0=0, y0=0.99, x1=1, y1=1, 
             line=dict(color="#00ffff", width=4)),
        # Bottom border
        dict(type="rect", xref="paper", yref="paper", x0=0, y0=0, x1=1, y1=0.01, 
             line=dict(color="#00ffff", width=4)),
        # Left border
        dict(type="rect", xref="paper", yref="paper", x0=0, y0=0, x1=0.01, y1=1, 
             line=dict(color="#00ffff", width=4)),
        # Right border
        dict(type="rect", xref="paper", yref="paper", x0=0.99, y0=0, x1=1, y1=1, 
             line=dict(color="#00ffff", width=4))
    ]
)

st.plotly_chart(fig, use_container_width=True)

# Animated data table section header
st.markdown('<div class="section-header" style="animation: neonPulse 2s infinite;">DATA TABLE</div>', unsafe_allow_html=True)

# Prepare display data
display_df = filtered_df.copy()
display_df['timestamp'] = display_df['timestamp'].dt.strftime('%Y-%m-%d %H:%M')
display_df = display_df.sort_values('timestamp', ascending=False)

# Custom CSS for dataframe
st.markdown("""
<style>
    .styled-table {
        font-family: 'Space Mono', monospace;
        border: 3px solid #39ff14;
        background-color: #000000;
        width: 100%;
        color: #ffffff;
        margin-bottom: 20px;
    }
    .styled-table thead tr {
        background-color: #111111;
        color: #39ff14;
        text-align: left;
        font-family: 'VT323', monospace;
        font-size: 1.2rem;
    }
    .styled-table th, .styled-table td {
        padding: 8px 12px;
        border-bottom: 1px solid #333333;
    }
    .styled-table tbody tr {
        border-bottom: 1px solid #333333;
    }
    .styled-table tbody tr:nth-of-type(even) {
        background-color: #111111;
    }
    .styled-table tbody tr:last-of-type {
        border-bottom: 3px solid #39ff14;
    }
</style>
""", unsafe_allow_html=True)

# Display dataframe
st.dataframe(
    display_df.head(10),
    column_config={
        "timestamp": "Date & Time",
        "platform": "Platform",
        "region": "Region",
        "content_theme": "Content Theme",
        "views": st.column_config.NumberColumn("Views", format="%d"),
        "likes": st.column_config.NumberColumn("Likes", format="%d"),
        "shares": st.column_config.NumberColumn("Shares", format="%d"),
        "comments": st.column_config.NumberColumn("Comments", format="%d"),
        "engagement_rate": st.column_config.NumberColumn("Engagement Rate", format="%.2f%%")
    },
    use_container_width=True,
    hide_index=True
)

# Footer with animated pixelated style
st.markdown("""
<div style="text-align: center; margin-top: 30px; font-family: 'VT323', monospace; color: #ffffff; padding: 10px; background-color: #0a0a0a; border-top: 3px solid #39ff14; position: relative; overflow: hidden;">
    <div class="pixel-scanline" style="position: absolute; top: 0; left: 0; width: 100%; height: 100%; background: linear-gradient(90deg, transparent 0%, rgba(57, 255, 20, 0.2) 50%, transparent 100%); background-size: 200% 100%; animation: pixelScan 2s linear infinite;"></div>
    <p style="font-size: 1.2rem; position: relative;">BRUT CONTENT ENGAGEMENT DASHBOARD</p>
    <p style="font-size: 0.9rem; position: relative;">© 2025 - RETRO GAMING EDITION</p>
    <div style="font-size: 0.8rem; margin-top: 5px; position: relative; animation: blink 1s infinite;">PRESS START TO CONTINUE</div>
</div>

<style>
@keyframes pixelScan {{
    0% {{ background-position: -100% 0; }}
    100% {{ background-position: 200% 0; }}
}}
@keyframes blink {{
    0%, 100% {{ opacity: 1; }}
    50% {{ opacity: 0; }}
}}
</style>
""", unsafe_allow_html=True)

# Easter egg - click to get a "high score" animation
if st.button('🎮 HIGH SCORES'):
    st.balloons()
    st.markdown("""
    <div style="text-align: center; margin-top: 20px; font-family: 'VT323', monospace; color: #39ff14; font-size: 2rem;">
        NEW HIGH SCORE!<br>
        BRUT ENGAGEMENT: 9999999
    </div>
    """, unsafe_allow_html=True)