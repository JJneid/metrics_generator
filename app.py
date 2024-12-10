import streamlit as st
import plotly.express as px
import plotly.graph_objects as go
from anthropic import Anthropic
import sqlparse
import json
import pandas as pd
import numpy as np
from typing import List, Dict, Any
import re

class SchemaAnalyzer:
    def __init__(self, anthropic_key: str):
        self.client = Anthropic(api_key=anthropic_key)
    
    def parse_sql_file(self, sql_content: str) -> str:
        parsed = sqlparse.parse(sql_content)
        cleaned = '\n'.join(str(stmt) for stmt in parsed if stmt.get_type() != 'UNKNOWN')
        return cleaned
    
    def analyze_schema(self, schema_content: str, description: str) -> Dict[str, Any]:
        prompt = f"""Given this database schema:
        {schema_content}
        
        And this use case description:
        {description}
        
        Propose key metrics to track over time for monitoring this application through its database.
        Return the response as a JSON object with this structure:
        {{
            "metrics": [
                {{
                    "name": "metric name",
                    "description": "what this metric measures",
                    "sql_query": "SQL query to calculate this metric",
                    "visualization_type": "recommended plot type (line/bar/etc)",
                    "update_frequency": "how often this should update"
                }}
            ]
        }}"""
        
        response = self.client.messages.create(
            model="claude-3-sonnet-20240229",
            max_tokens=2000,
            messages=[{"role": "user", "content": prompt}]
        )
        
        return json.loads(response.content[0].text)

    def generate_sample_visualization(self, metric: Dict[str, Any]) -> go.Figure:
        """Generate a sample visualization based on metric type"""
        # Generate sample data
        dates = pd.date_range(start='2024-01-01', periods=30)
        
        if metric['visualization_type'].lower() == 'line':
            values = np.cumsum(np.random.normal(10, 2, 30))  # Trending line
            fig = px.line(x=dates, y=values, title=metric['name'])
            
        elif metric['visualization_type'].lower() == 'bar':
            values = np.random.randint(10, 100, 30)
            fig = px.bar(x=dates, y=values, title=metric['name'])
            
        elif metric['visualization_type'].lower() == 'pie':
            labels = ['Category A', 'Category B', 'Category C', 'Category D']
            values = np.random.randint(10, 100, 4)
            fig = px.pie(values=values, names=labels, title=metric['name'])
            
        else:  # Default to scatter plot
            values = np.random.randint(10, 100, 30)
            fig = px.scatter(x=dates, y=values, title=metric['name'])
        
        fig.update_layout(
            title_x=0.5,
            margin=dict(t=50, l=20, r=20, b=20),
            height=400
        )
        return fig

    def generate_dashboard_code(self, metrics: List[Dict[str, Any]]) -> str:
        """Generate complete dashboard code"""
        dashboard_code = """import dash
from dash import html, dcc
from dash.dependencies import Input, Output
import plotly.express as px
import plotly.graph_objects as go
import pandas as pd
import numpy as np
from datetime import datetime, timedelta
import psycopg2  # For PostgreSQL connection

# Initialize the Dash app
app = dash.Dash(__name__)

# Database connection function
def get_db_connection():
    return psycopg2.connect(
        dbname="your_database",
        user="your_user",
        password="your_password",
        host="your_host",
        port="your_port"
    )

# Layout
app.layout = html.Div([
    html.H1("Database Metrics Dashboard", style={'textAlign': 'center'}),
    html.Div([
        dcc.Tabs(id='metric-tabs', value='tab-0', children=[
"""
        
        # Add tabs for each metric
        for i, metric in enumerate(metrics['metrics']):
            dashboard_code += f"""            dcc.Tab(label='{metric["name"]}', value='tab-{i}'),\n"""
        
        dashboard_code += """        ]),
        html.Div(id='metric-content')
    ])
])

# Callback to update content
@app.callback(
    Output('metric-content', 'children'),
    Input('metric-tabs', 'value')
)
def update_metric(tab):
    metrics = {\n"""
        
        # Add metric queries and visualizations
        for i, metric in enumerate(metrics['metrics']):
            dashboard_code += f"""        'tab-{i}': {{
            'name': '{metric["name"]}',
            'query': '''{metric["sql_query"]}''',
            'type': '{metric["visualization_type"]}'
        }},\n"""
        
        dashboard_code += """    }
    
    if tab not in metrics:
        return html.Div("No metric selected")
    
    # Execute query and get data
    try:
        conn = get_db_connection()
        df = pd.read_sql_query(metrics[tab]['query'], conn)
        conn.close()
        
        # Create visualization based on type
        if metrics[tab]['type'].lower() == 'line':
            fig = px.line(df, x='timestamp', y='value', title=metrics[tab]['name'])
        elif metrics[tab]['type'].lower() == 'bar':
            fig = px.bar(df, x='timestamp', y='value', title=metrics[tab]['name'])
        else:
            fig = px.scatter(df, x='timestamp', y='value', title=metrics[tab]['name'])
            
        return html.Div([
            dcc.Graph(figure=fig)
        ])
    except Exception as e:
        return html.Div(f"Error: {str(e)}")

if __name__ == '__main__':
    app.run_server(debug=True)
"""
        return dashboard_code

def main():
    st.set_page_config(page_title="Database Metrics Dashboard Generator", layout="wide")
    st.title("Database Metrics Dashboard Generator")
    
    # Sidebar for inputs
    with st.sidebar:
        st.header("Configuration")
        anthropic_key = st.text_input("Anthropic API Key", type="password")
        uploaded_file = st.file_uploader("Upload Schema File", type=['sql', 'prisma', 'txt'])
        description = st.text_area("Use Case Description", 
            placeholder="Describe your application and what you want to monitor...")
    
    if not anthropic_key or not uploaded_file or not description:
        st.info("Please provide all required inputs in the sidebar to generate the dashboard.")
        return
    
    try:
        # Initialize analyzer
        analyzer = SchemaAnalyzer(anthropic_key)
        
        # Read and parse schema file
        schema_content = uploaded_file.read().decode('utf-8')
        if uploaded_file.name.endswith('.sql'):
            schema_content = analyzer.parse_sql_file(schema_content)
        
        # Analyze schema and get metrics
        with st.spinner("Analyzing schema and generating metrics..."):
            metrics = analyzer.analyze_schema(schema_content, description)
        
        # Create tabs
        tab1, tab2, tab3 = st.tabs(["Proposed Metrics", "Sample Dashboard", "Dashboard Code"])
        
        # Tab 1: Metrics and SQL queries
        with tab1:
            st.header("Proposed Metrics")
            for metric in metrics['metrics']:
                with st.expander(f"📊 {metric['name']}", expanded=True):
                    st.write(f"**Description:** {metric['description']}")
                    st.write(f"**Update Frequency:** {metric['update_frequency']}")
                    st.write(f"**Visualization Type:** {metric['visualization_type']}")
                    st.code(metric['sql_query'], language='sql')
        
        # Tab 2: Sample visualizations
        with tab2:
            st.header("Sample Dashboard Preview")
            cols = st.columns(2)
            for i, metric in enumerate(metrics['metrics']):
                col = cols[i % 2]
                with col:
                    fig = analyzer.generate_sample_visualization(metric)
                    st.plotly_chart(fig, use_container_width=True)
        
        # Tab 3: Generated dashboard code
        with tab3:
            st.header("Generated Dashboard Code")
            st.write("""
            This is a complete Dash application that you can deploy. Make sure to:
            1. Install required packages: `pip install dash pandas psycopg2-binary plotly`
            2. Update the database connection parameters
            3. Save this code to a file (e.g., `app.py`) and run with `python app.py`
            """)
            dashboard_code = analyzer.generate_dashboard_code(metrics)
            st.code(dashboard_code, language='python')
            
            # Add download button
            st.download_button(
                label="Download Dashboard Code",
                data=dashboard_code,
                file_name="dashboard_app.py",
                mime="text/plain"
            )
    
    except Exception as e:
        st.error(f"An error occurred: {str(e)}")

if __name__ == "__main__":
    main()