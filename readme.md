# Database Metrics Dashboard Generator

## Overview
This tool automatically generates customized database monitoring dashboards by analyzing your database schema and use case description. Using AI (Claude), it identifies relevant metrics and creates a complete dashboard application with visualizations tailored to your specific needs.

## Features
- **Schema Analysis**: Supports various database schema formats (SQL, Prisma)
- **AI-Powered Metrics**: Automatically suggests relevant KPIs based on your schema and use case
- **Interactive Preview**: View sample visualizations before deployment
- **Code Generation**: Creates a ready-to-deploy Dash application
- **Multiple Visualization Types**: Supports line charts, bar charts, pie charts, and more
- **SQL Query Generation**: Automatically generates optimized SQL queries for each metric
- **Customizable**: Generated code can be modified to suit specific needs

## Prerequisites
- Python 3.8 or higher
- An Anthropic API key for Claude
- PostgreSQL database (for the generated dashboard)

## Installation

1. Clone the repository:
```bash
git clone [repository-url]
cd database-metrics-dashboard
```

2. Create a virtual environment:
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. Install dependencies:
```bash
pip install -r requirements.txt
```

## Usage

### 1. Starting the Application
```bash
streamlit run app.py
```

### 2. Using the Interface

1. **Configure Settings**:
   - Enter your Anthropic API key in the sidebar
   - Upload your database schema file
   - Provide a description of your use case/application

2. **Review Generated Content** (3 tabs available):
   - **Proposed Metrics**: View suggested metrics and their SQL queries
   - **Sample Dashboard**: Preview how your metrics will look
   - **Dashboard Code**: Get the complete code for your custom dashboard

3. **Deploy Your Dashboard**:
   - Download the generated code
   - Update database connection parameters
   - Deploy using the instructions provided

### Example Use Case Description
```
This is an e-commerce platform where users can browse products, make purchases, 
and leave reviews. We want to track user engagement, sales performance, and 
inventory management metrics over time.
```

## Generated Dashboard Features
- Automatic database connection handling
- Dynamic metric tabs
- Real-time data updates
- Error handling
- Responsive design
- Easy customization options

## Configuration

### Database Connection
Update the following in the generated dashboard code:
```python
def get_db_connection():
    return psycopg2.connect(
        dbname="your_database",
        user="your_user",
        password="your_password",
        host="your_host",
        port="your_port"
    )
```

### Environment Variables
Create a `.env` file:
```
ANTHROPIC_API_KEY=your_api_key
DATABASE_URL=your_database_url
```

## Contributing
Feel free to submit issues, fork the repository, and create pull requests for any improvements.

## Security Notes
- Never commit your API keys or database credentials
- Always use environment variables for sensitive information
- Review generated SQL queries before execution in production

## Limitations
- Currently supports PostgreSQL databases
- Requires manual review of generated metrics
- Sample visualizations use dummy data
- Connection parameters need manual configuration

## License
MIT License - feel free to use this tool for any purpose

## Support
For issues or questions:
1. Check existing GitHub issues
2. Create a new issue with:
   - Your schema file (sanitized)
   - Use case description
   - Error messages if any
   - Expected vs actual behavior

## Roadmap
- [ ] Support for additional database types
- [ ] Custom visualization templates
- [ ] Advanced metric correlation analysis
- [ ] Export to various dashboard platforms
- [ ] Automated testing of generated queries
