"""
Visualization utilities for Brut Engagement Dashboard.
Contains functions for creating and styling charts.
"""

import plotly.graph_objects as go
import plotly.express as px
import pandas as pd

def create_platform_chart(platform_data):
    """
    Create a bar chart showing engagement by platform.
    
    Parameters:
    -----------
    platform_data : pandas.DataFrame
        Aggregated data by platform
    
    Returns:
    --------
    plotly.graph_objects.Figure
        The plotly figure object
    """
    # Create a custom bar chart with plotly and retro gaming colors
    fig = go.Figure()
    
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
    
    return fig

def create_theme_chart(theme_data):
    """
    Create a horizontal bar chart showing top performing themes.
    
    Parameters:
    -----------
    theme_data : pandas.DataFrame
        Aggregated data by theme
    
    Returns:
    --------
    plotly.graph_objects.Figure
        The plotly figure object
    """
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
    
    return fig

def create_timeseries_chart(time_series):
    """
    Create a line chart showing engagement trends over time.
    
    Parameters:
    -----------
    time_series : pandas.DataFrame
        Aggregated data by date
    
    Returns:
    --------
    plotly.graph_objects.Figure
        The plotly figure object
    """
    # Create a retro-styled line chart
    fig = go.Figure()

    # Add line with blue highlight effect for numbers
    fig.add_trace(go.Scatter(
        x=time_series['date'],
        y=time_series['engagement_rate'],
        mode='lines+markers',
        name='Engagement Rate',
        line=dict(color='#00ffff', width=3),
        marker=dict(
            color='#0066ff',
            size=8,
            line=dict(
                color='#00ffff',
                width=2
            )
        ),
        # Add custom text with blue highlight effect
        text=time_series['engagement_rate'].apply(lambda x: f'{x:.2f}%'),
        textposition='top center',
        textfont=dict(
            family='VT323, monospace',
            size=14,
            color='white'
        ),
        # Use hovertemplate to style the hover text
        hovertemplate='<span style="font-family: VT323, monospace; background: rgba(0, 102, 255, 0.4); padding: 3px; border-radius: 3px; color: white; text-shadow: 0 0 8px #0099ff;">%{y:.2f}%</span><extra></extra>'
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

    # Add grid lines for better readability
    grid_lines = []
    for i in range(0, 101, 10):  # Horizontal grid lines
        grid_lines.append(
            dict(type="line", xref="paper", yref="y", x0=0, y0=i, x1=1, y1=i, 
                 line=dict(color="#333333", width=1, dash="dot"))
        )

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
    
    return fig

def highlight_numbers(df):
    """
    Add styling to dataframe to highlight numbers with blue effect.
    
    Parameters:
    -----------
    df : pandas.DataFrame
        DataFrame to style
    
    Returns:
    --------
    pandas.io.formats.style.Styler
        Styled DataFrame
    """
    # Create styler object
    return df.style.format({
        'views': '{:,.0f}',
        'likes': '{:,.0f}',
        'shares': '{:,.0f}',
        'comments': '{:,.0f}',
        'engagement_rate': '{:.2f}%'
    }).applymap(
        lambda x: 'background-color: rgba(0, 102, 255, 0.2); color: white; text-shadow: 0 0 3px #0099ff;' 
        if isinstance(x, (int, float)) and pd.notna(x) else ''
    )