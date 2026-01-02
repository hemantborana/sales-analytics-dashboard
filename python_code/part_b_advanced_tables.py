import pandas as pd
import plotly.graph_objects as go
import plotly.express as px
from plotly.subplots import make_subplots
import numpy as np

sales = pd.read_csv('superstore_sales.csv')
operations = pd.read_csv('operations_data.csv')
financial = pd.read_csv('financial_data.csv')
customer = pd.read_csv('customer_data.csv')

sales['Order_Date'] = pd.to_datetime(sales['Order_Date'])
financial['Month'] = pd.to_datetime(financial['Month'])

print("Creating advanced table visualizations...")

# ==========================================
# 1. SUMMARY TABLE with aggregations
# ==========================================

summary = sales.groupby('Category').agg({
    'Sales': ['sum', 'mean', 'count'],
    'Profit': ['sum', 'mean'],
    'Quantity': 'sum',
    'Discount': 'mean'
}).round(2)

summary.columns = ['Total Sales', 'Avg Sale', 'Orders', 'Total Profit', 'Avg Profit', 'Units Sold', 'Avg Discount']
summary = summary.reset_index()

# add profit margin
summary['Profit Margin %'] = ((summary['Total Profit'] / summary['Total Sales']) * 100).round(1)

# conditional formatting colors
def get_color(val, col_data):
    min_val = col_data.min()
    max_val = col_data.max()
    normalized = (val - min_val) / (max_val - min_val) if max_val != min_val else 0.5
    
    # green to red scale
    if normalized > 0.66:
        return '#d4edda'
    elif normalized > 0.33:
        return '#fff3cd'
    else:
        return '#f8d7da'

fill_colors = []
for col in summary.columns:
    if col == 'Category':
        fill_colors.append(['#f8f9fa'] * len(summary))
    else:
        colors = [get_color(val, summary[col]) for val in summary[col]]
        fill_colors.append(colors)

fig1 = go.Figure(data=[go.Table(
    header=dict(
        values=[f'<b>{col}</b>' for col in summary.columns],
        fill_color='#343a40',
        font=dict(color='white', size=12),
        align='center',
        height=35
    ),
    cells=dict(
        values=[summary[col] for col in summary.columns],
        fill_color=fill_colors,
        align=['left'] + ['right'] * (len(summary.columns) - 1),
        font=dict(size=11),
        height=30,
        format=[None, '$,.0f', '$,.0f', ',d', '$,.0f', '$,.0f', ',d', '.2f', '.1f']
    )
)])

fig1.update_layout(
    title='Sales Summary by Category (with Conditional Formatting)',
    height=350,
    margin=dict(l=20, r=20, t=60, b=20)
)

fig1.write_html('16_summary_table.html')
print("✓ Summary table created")


# ==========================================
# 2. DETAILED TABLE with pagination style
# ==========================================

# top 50 transactions
top_sales = sales.nlargest(50, 'Sales')[['Order_ID', 'Order_Date', 'Category', 
                                          'Sub_Category', 'Sales', 'Profit', 
                                          'Quantity', 'Region', 'Segment']].copy()

top_sales['Order_Date'] = top_sales['Order_Date'].dt.strftime('%Y-%m-%d')
top_sales['Profit_Color'] = top_sales['Profit'].apply(
    lambda x: '#d4edda' if x > 0 else '#f8d7da'
)

fig2 = go.Figure(data=[go.Table(
    header=dict(
        values=['<b>Order ID</b>', '<b>Date</b>', '<b>Category</b>', 
                '<b>Sub-Category</b>', '<b>Sales</b>', '<b>Profit</b>', 
                '<b>Qty</b>', '<b>Region</b>', '<b>Segment</b>'],
        fill_color='#495057',
        font=dict(color='white', size=11),
        align='center',
        height=30
    ),
    cells=dict(
        values=[
            top_sales['Order_ID'],
            top_sales['Order_Date'],
            top_sales['Category'],
            top_sales['Sub_Category'],
            top_sales['Sales'].apply(lambda x: f'${x:,.2f}'),
            top_sales['Profit'].apply(lambda x: f'${x:,.2f}'),
            top_sales['Quantity'],
            top_sales['Region'],
            top_sales['Segment']
        ],
        fill_color=[['white'] * len(top_sales)] * 4 + 
                   [['#fff3cd'] * len(top_sales)] +
                   [top_sales['Profit_Color'].tolist()] +
                   [['white'] * len(top_sales)] * 3,
        align=['left', 'center', 'left', 'left', 'right', 'right', 'center', 'center', 'center'],
        font=dict(size=10),
        height=25
    )
)])

fig2.update_layout(
    title='Top 50 Sales Transactions (Detail View)',
    height=600,
    margin=dict(l=20, r=20, t=60, b=20)
)

fig2.write_html('17_detailed_table.html')
print("✓ Detailed table created")


# ==========================================
# 3. COMPARISON TABLE - side by side
# ==========================================

# compare 2023 vs 2024
sales['Year'] = sales['Order_Date'].dt.year
comparison = sales[sales['Year'].isin([2023, 2024])].groupby(['Year', 'Category']).agg({
    'Sales': 'sum',
    'Profit': 'sum',
    'Order_ID': 'count'
}).reset_index()

comparison_pivot = comparison.pivot(index='Category', columns='Year', values=['Sales', 'Profit', 'Order_ID'])
comparison_pivot.columns = [f'{col[0]} {col[1]}' for col in comparison_pivot.columns]
comparison_pivot = comparison_pivot.reset_index()

# calculate growth
comparison_pivot['Sales Growth %'] = (
    (comparison_pivot['Sales 2024'] - comparison_pivot['Sales 2023']) / 
    comparison_pivot['Sales 2023'] * 100
).round(1)

comparison_pivot['Profit Growth %'] = (
    (comparison_pivot['Profit 2024'] - comparison_pivot['Profit 2023']) / 
    comparison_pivot['Profit 2023'] * 100
).round(1)

# color coding for growth
def growth_color(val):
    if val > 5:
        return '#d4edda'
    elif val > 0:
        return '#fff3cd'
    else:
        return '#f8d7da'

sales_growth_colors = [growth_color(x) for x in comparison_pivot['Sales Growth %']]
profit_growth_colors = [growth_color(x) for x in comparison_pivot['Profit Growth %']]

fig3 = go.Figure(data=[go.Table(
    header=dict(
        values=['<b>Category</b>', '<b>Sales 2023</b>', '<b>Sales 2024</b>', 
                '<b>Growth %</b>', '<b>Profit 2023</b>', '<b>Profit 2024</b>', 
                '<b>Growth %</b>', '<b>Orders 2023</b>', '<b>Orders 2024</b>'],
        fill_color='#6c757d',
        font=dict(color='white', size=11),
        align='center',
        height=35
    ),
    cells=dict(
        values=[
            comparison_pivot['Category'],
            comparison_pivot['Sales 2023'].apply(lambda x: f'${x:,.0f}'),
            comparison_pivot['Sales 2024'].apply(lambda x: f'${x:,.0f}'),
            comparison_pivot['Sales Growth %'].apply(lambda x: f'{x:+.1f}%'),
            comparison_pivot['Profit 2023'].apply(lambda x: f'${x:,.0f}'),
            comparison_pivot['Profit 2024'].apply(lambda x: f'${x:,.0f}'),
            comparison_pivot['Profit Growth %'].apply(lambda x: f'{x:+.1f}%'),
            comparison_pivot['Order_ID 2023'].astype(int),
            comparison_pivot['Order_ID 2024'].astype(int)
        ],
        fill_color=[
            ['white'] * len(comparison_pivot),
            ['#e9ecef'] * len(comparison_pivot),
            ['#e9ecef'] * len(comparison_pivot),
            sales_growth_colors,
            ['#dee2e6'] * len(comparison_pivot),
            ['#dee2e6'] * len(comparison_pivot),
            profit_growth_colors,
            ['#f8f9fa'] * len(comparison_pivot),
            ['#f8f9fa'] * len(comparison_pivot)
        ],
        align=['left'] + ['right'] * 8,
        font=dict(size=11),
        height=30
    )
)])

fig3.update_layout(
    title='Year-over-Year Comparison: 2023 vs 2024',
    height=350,
    margin=dict(l=20, r=20, t=60, b=20)
)

fig3.write_html('18_comparison_table.html')
print("✓ Comparison table created")


# ==========================================
# 4. PIVOT TABLE - Cross-tabulation
# ==========================================

pivot_data = sales.pivot_table(
    values='Sales',
    index='Region',
    columns='Segment',
    aggfunc='sum',
    margins=True,
    margins_name='Total'
).round(0)

# normalize for heatmap effect
pivot_normalized = pivot_data.div(pivot_data.max().max()) * 100

def pivot_color(val):
    if pd.isna(val):
        return 'white'
    if val > 75:
        return '#198754'
    elif val > 50:
        return '#20c997'
    elif val > 25:
        return '#ffc107'
    else:
        return '#dc3545'

# create color matrix
colors = []
for col in pivot_normalized.columns:
    col_colors = [pivot_color(val) for val in pivot_normalized[col]]
    colors.append(col_colors)

fig4 = go.Figure(data=[go.Table(
    header=dict(
        values=['<b>Region</b>'] + [f'<b>{col}</b>' for col in pivot_data.columns],
        fill_color='#212529',
        font=dict(color='white', size=12),
        align='center',
        height=35
    ),
    cells=dict(
        values=[pivot_data.index.tolist()] + 
               [[f'${val:,.0f}' if not pd.isna(val) else '-' for val in pivot_data[col]] 
                for col in pivot_data.columns],
        fill_color=[['#f8f9fa'] * len(pivot_data)] + colors,
        align=['left'] + ['right'] * len(pivot_data.columns),
        font=dict(size=11, color=['black'] * len(pivot_data)),
        height=30
    )
)])

fig4.update_layout(
    title='Sales Pivot Table: Region × Segment (with Heat Shading)',
    height=400,
    margin=dict(l=20, r=20, t=60, b=20)
)

fig4.write_html('19_pivot_table.html')
print("✓ Pivot table created")


# ==========================================
# 5. DATA BARS & ICONS table
# ==========================================

region_perf = sales.groupby('Region').agg({
    'Sales': 'sum',
    'Profit': 'sum',
    'Order_ID': 'count'
}).reset_index()

region_perf.columns = ['Region', 'Sales', 'Profit', 'Orders']
region_perf['Profit_Margin'] = (region_perf['Profit'] / region_perf['Sales'] * 100).round(1)

# normalize for bar width
max_sales = region_perf['Sales'].max()
region_perf['Bar_Width'] = (region_perf['Sales'] / max_sales * 100).round(0)

# create visual bars
def create_bar(width, color='#0d6efd'):
    bar = '█' * int(width / 5)
    return f'<span style="color:{color}">{bar}</span>'

visual_bars = [create_bar(w) for w in region_perf['Bar_Width']]

# add trend icons
def trend_icon(margin):
    if margin > 20:
        return '🟢'
    elif margin > 15:
        return '🟡'
    else:
        return '🔴'

icons = [trend_icon(m) for m in region_perf['Profit_Margin']]

fig5 = go.Figure(data=[go.Table(
    columnwidth=[80, 120, 100, 100, 80, 100],
    header=dict(
        values=['<b>Region</b>', '<b>Sales Volume</b>', '<b>Sales ($)</b>', 
                '<b>Profit ($)</b>', '<b>Orders</b>', '<b>Margin %</b>'],
        fill_color='#0d6efd',
        font=dict(color='white', size=11),
        align='center',
        height=35
    ),
    cells=dict(
        values=[
            region_perf['Region'],
            visual_bars,
            region_perf['Sales'].apply(lambda x: f'${x:,.0f}'),
            region_perf['Profit'].apply(lambda x: f'${x:,.0f}'),
            region_perf['Orders'],
            [f'{icon} {val}%' for icon, val in zip(icons, region_perf['Profit_Margin'])]
        ],
        fill_color='white',
        align=['left', 'left', 'right', 'right', 'center', 'center'],
        font=dict(size=11),
        height=35
    )
)])

fig5.update_layout(
    title='Regional Performance with Data Bars & Icons',
    height=350,
    margin=dict(l=20, r=20, t=60, b=20)
)

fig5.write_html('20_databars_icons.html')
print("✓ Data bars table created")


# ==========================================
# 6. FINANCIAL STATEMENT table
# ==========================================

fin_statement = financial.tail(12).copy()
fin_statement['Month_Name'] = fin_statement['Month'].dt.strftime('%b %Y')

# calculate percentages
fin_statement['Gross_Margin_%'] = (fin_statement['Gross_Profit'] / fin_statement['Revenue'] * 100).round(1)
fin_statement['Net_Margin_%'] = (fin_statement['Net_Profit'] / fin_statement['Revenue'] * 100).round(1)
fin_statement['Budget_Var_%'] = ((fin_statement['Revenue'] - fin_statement['Budget_Revenue']) / 
                                  fin_statement['Budget_Revenue'] * 100).round(1)

fig6 = go.Figure(data=[go.Table(
    header=dict(
        values=['<b>Month</b>', '<b>Revenue</b>', '<b>Budget</b>', '<b>Var %</b>',
                '<b>COGS</b>', '<b>Gross Profit</b>', '<b>GM %</b>', 
                '<b>OpEx</b>', '<b>Net Profit</b>', '<b>NM %</b>'],
        fill_color='#198754',
        font=dict(color='white', size=10),
        align='center',
        height=30
    ),
    cells=dict(
        values=[
            fin_statement['Month_Name'],
            fin_statement['Revenue'].apply(lambda x: f'${x/1000:.0f}K'),
            fin_statement['Budget_Revenue'].apply(lambda x: f'${x/1000:.0f}K'),
            fin_statement['Budget_Var_%'].apply(lambda x: f'{x:+.1f}%'),
            fin_statement['COGS'].apply(lambda x: f'${x/1000:.0f}K'),
            fin_statement['Gross_Profit'].apply(lambda x: f'${x/1000:.0f}K'),
            fin_statement['Gross_Margin_%'].apply(lambda x: f'{x:.1f}%'),
            fin_statement['Operating_Expenses'].apply(lambda x: f'${x/1000:.0f}K'),
            fin_statement['Net_Profit'].apply(lambda x: f'${x/1000:.0f}K'),
            fin_statement['Net_Margin_%'].apply(lambda x: f'{x:.1f}%')
        ],
        fill_color=[['white'] * len(fin_statement)] * 2 +
                   [[growth_color(x) for x in fin_statement['Budget_Var_%']]] +
                   [['#f8f9fa'] * len(fin_statement)] * 2 +
                   [['#e9ecef'] * len(fin_statement)] +
                   [['#f8f9fa'] * len(fin_statement)] +
                   [['#e9ecef'] * len(fin_statement)] * 2,
        align=['left'] + ['right'] * 9,
        font=dict(size=9),
        height=25
    )
)])

fig6.update_layout(
    title='Financial Performance Statement (Last 12 Months)',
    height=500,
    margin=dict(l=20, r=20, t=60, b=20)
)

fig6.write_html('21_financial_table.html')
print("✓ Financial statement table created")


print("\n=== Advanced Tables Complete ===")
print("6 table types created:")
print("  - Summary with conditional formatting")
print("  - Detailed transaction view")
print("  - Year-over-year comparison")
print("  - Pivot table with heatmap")
print("  - Data bars & icons")
print("  - Financial statement")