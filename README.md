# Sales Analytics Dashboard

A comprehensive data reporting and analytics solution featuring interactive visualizations, advanced tables, executive dashboards, and self-service business intelligence capabilities.

![Python](https://img.shields.io/badge/Python-3.8+-blue.svg)
![Plotly](https://img.shields.io/badge/Plotly-5.0+-green.svg)
![Streamlit](https://img.shields.io/badge/Streamlit-1.28+-red.svg)
![License](https://img.shields.io/badge/License-MIT-yellow.svg)

## Overview

This project demonstrates a complete data reporting toolkit built with modern visualization technologies. It includes 15+ interactive chart types, advanced table displays, drill-down capabilities, and a self-service analytics platform that empowers users to explore data and generate insights independently.

### Key Features

- **15 Interactive Visualizations**: Line charts, bar charts, scatter plots, heatmaps, treemaps, Sankey diagrams, radar charts, waterfall charts, and more
- **Advanced Tables**: Conditional formatting, pivot tables, data bars, comparison views
- **Executive Dashboards**: KPI cards, trend analysis, regional performance
- **Self-Service Analytics**: Real-time filtering, drill-down exploration, what-if scenario modeling
- **Professional Documentation**: Complete user manuals, technical docs, and design standards

## Demo

### Interactive Dashboard Views

**Executive Summary**
- Real-time KPI metrics
- Sales and profit trends
- Category and regional analysis

**Detailed Analysis**
- Product performance deep-dives
- Time-based analysis
- Profitability heatmaps

**Drill-Down Explorer**
- Multi-level data navigation
- Category to sub-category drilling
- Region to state breakdown

**What-If Scenarios**
- Price change modeling
- Volume impact analysis
- Cost adjustment simulations

## Technology Stack

- **Python 3.8+** - Core programming language
- **Plotly 5.x** - Interactive visualizations
- **Streamlit 1.28+** - Dashboard framework
- **Pandas 2.x** - Data manipulation and analysis
- **NumPy** - Numerical computations
- **Tableau Public** - Business intelligence dashboards

## Project Structure

```
sales-analytics-dashboard/
├── data/                          # Source datasets (4 CSV files)
│   ├── superstore_sales.csv
│   ├── operations_data.csv
│   ├── financial_data.csv
│   └── customer_data.csv
│
├── python_code/                   # Visualization generation scripts
│   ├── data_generation.py
│   ├── part_a_statistical_charts.py
│   ├── part_a_advanced_charts.py
│   └── part_b_advanced_tables.py
│
├── visualizations/
│   ├── charts/                   # 15 interactive chart HTML files
│   │   ├── 1_line_chart_sales_trend.html
│   │   ├── 2_bar_chart_category.html
│   │   └── ...
│   │
│   └── tables/                   # 6 advanced table HTML files
│       ├── 16_summary_table.html
│       ├── 17_detailed_table.html
│       └── ...
│
├── tableau/                       # Tableau dashboard files
│   └── Executive_Dashboard.twb
│
├── documentation/                 # Complete documentation (5 PDFs)
│   ├── tool_comparison_report.pdf
│   ├── Design_Standards_Guide.pdf
│   ├── User_manual.pdf
│   ├── Technical_Document.pdf
│   └── Case_Study.pdf
│
├── streamlit_app/                # Interactive dashboard application
│   ├── part_d_interactive_dashboard.py
│   ├── requirements.txt
│   └── [data files]
│
├── README.md                     # This file
└── run_dashboard.bat             # Quick launch script (Windows)
```

## Quick Start

### Prerequisites

- Python 3.8 or higher
- pip (Python package manager)
- Modern web browser (Chrome, Firefox, Safari, Edge)

### Installation

1. **Clone the repository**
   ```bash
   git clone https://github.com/hemantborana/sales-analytics-dashboard.git
   cd sales-analytics-dashboard
   ```

2. **Install dependencies**
   ```bash
   cd streamlit_app
   pip install -r requirements.txt
   ```

3. **Run the interactive dashboard**
   ```bash
   streamlit run part_d_interactive_dashboard.py
   ```

4. **Access the dashboard**
   - Browser opens automatically at `http://localhost:8501`
   - Or navigate manually to the URL

### Quick Launch (Windows)

Simply double-click `run_dashboard.bat` in the project root directory.

## Usage

### Viewing Static Visualizations

1. Navigate to `visualizations/charts/` or `visualizations/tables/`
2. Open any HTML file in your web browser
3. Interact with charts (zoom, pan, hover for details)

### Using the Interactive Dashboard

1. **Select Filters** (left sidebar):
   - Date range
   - Region
   - Category
   - Customer segment

2. **Choose View Mode**:
   - Executive Summary - High-level KPIs and trends
   - Detailed Analysis - Deep-dive into products and profitability
   - Drill-Down Explorer - Navigate through data hierarchies
   - What-If Scenario - Model business scenarios

3. **Explore Data**:
   - Hover over charts for detailed information
   - Click elements to drill down
   - Adjust sliders for scenario modeling
   - Export filtered data as CSV

### Tableau Dashboards

1. Install Tableau Public (free): https://public.tableau.com/
2. Open `tableau/Executive_Dashboard.twb`
3. Explore interactive dashboards with filters and drill-downs

## Features in Detail

### Visualization Types

**Statistical Charts:**
- Line charts with trend lines
- Grouped and stacked bar charts
- Histograms with statistical annotations
- Scatter plots with correlation analysis
- Box plots for distribution analysis

**Advanced Visualizations:**
- Correlation heatmaps
- Geographic heatmaps
- Hierarchical treemaps
- Flow Sankey diagrams
- Multi-dimensional radar charts
- Financial waterfall charts
- Combination charts (bar + line)

**Table Displays:**
- Summary tables with conditional formatting
- Detailed transaction listings
- Year-over-year comparisons
- Pivot tables with cross-tabulation
- Data bars and status icons
- Financial statement formats

### Interactivity Features

- Real-time filtering across all visualizations
- Multi-select capabilities
- Date range selection
- Drill-down navigation
- What-if scenario modeling
- Data export functionality
- Responsive design for different screen sizes

## Data

The project uses synthetic datasets generated to simulate realistic business data:

- **Sales Data**: 5,000 transactions (2022-2024)
- **Operations Data**: ~2,000 operational records
- **Financial Data**: 36 monthly financial records
- **Customer Data**: 1,500 customer profiles

All data is randomly generated and does not represent real business information.

## Documentation

Comprehensive documentation is provided in the `documentation/` folder:

1. **Tool Comparison Report** - Analysis of Python vs Tableau
2. **Design Standards Guide** - Visualization best practices
3. **User Manual** - Complete usage instructions
4. **Technical Documentation** - Implementation details
5. **Case Study Analysis** - Lessons learned and recommendations

## Performance

- **Initial Load**: 2-3 seconds
- **Filter Application**: <1 second
- **Chart Rendering**: 1-2 seconds
- **Data Export**: <1 second

Optimizations include data caching, efficient aggregations, and selective rendering.

## Browser Compatibility

- Chrome (recommended)
- Firefox
- Safari
- Microsoft Edge
- Opera

JavaScript must be enabled for full functionality.

## Development

### Regenerating Visualizations

```bash
# Generate fresh data
cd python_code
python data_generation.py

# Create statistical charts
python part_a_statistical_charts.py

# Create advanced visualizations
python part_a_advanced_charts.py

# Create tables
python part_b_advanced_tables.py
```

### Project Dependencies

See `streamlit_app/requirements.txt` for complete list:
- pandas>=2.0.0
- plotly>=5.0.0
- streamlit>=1.28.0
- numpy>=1.24.0
- scipy>=1.10.0

## Design Principles

This project follows data visualization best practices:

- **Clarity**: Simple, focused visualizations
- **Consistency**: Unified color schemes and styling
- **Accessibility**: WCAG 2.1 compliant color contrasts
- **Interactivity**: Progressive disclosure of information
- **Performance**: Optimized for smooth user experience

## Use Cases

This dashboard is suitable for:

- Sales performance monitoring
- Business intelligence reporting
- Data exploration and analysis
- Executive decision support
- Trend identification
- Scenario planning
- Academic demonstrations
- Portfolio projects

## Limitations

- Synthetic data (not real business data)
- No user authentication (suitable for public data only)
- Session-based state (resets on refresh)
- Single-user optimization (not enterprise-scaled)

For production deployment, consider adding:
- Database backend
- User authentication
- Role-based access control
- Automated data refresh
- Scalability enhancements

## Future Enhancements

Potential improvements:
- Machine learning integration for predictions
- Real-time data streaming
- Mobile app version
- Advanced forecasting capabilities
- Anomaly detection
- Natural language queries
- Automated report scheduling
- Email alerts and notifications

## Contributing

Contributions are welcome! Areas for improvement:
- Additional visualization types
- Enhanced interactivity features
- Performance optimizations
- Documentation improvements
- Bug fixes

## License

This project is licensed under the MIT License - see below for details.

```
MIT License

Copyright (c) 2024

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
```

## Acknowledgments

- Built as part of Data Analytics and Reporting coursework
- Inspired by modern business intelligence platforms
- Uses open-source technologies and libraries

## Contact

For questions, suggestions, or issues:
- Open an issue on GitHub
- Refer to documentation in the `documentation/` folder


---

**Last Updated:** December 30, 2024  
**Version:** 1.0  
**Status:** Complete and Production-Ready