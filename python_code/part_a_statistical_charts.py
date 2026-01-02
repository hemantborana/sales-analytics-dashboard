import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import numpy as np
from scipy import stats

# Load data
sales = pd.read_csv('superstore_sales.csv')
operations = pd.read_csv('operations_data.csv')
financial = pd.read_csv('financial_data.csv')

# convert dates
sales['Order_Date'] = pd.to_datetime(sales['Order_Date'])
operations['Date'] = pd.to_datetime(operations['Date'])
financial['Month'] = pd.to_datetime(financial['Month'])

print("Creating statistical visualizations...")

# ==========================================
# 1. LINE CHART - Time series trends
# ==========================================

# monthly sales over time
monthly_sales = sales.groupby(sales['Order_Date'].dt.to_period('M'))['Sales'].sum().reset_index()
monthly_sales['Order_Date'] = monthly_sales['Order_Date'].apply(lambda x: x.to_timestamp())

fig1 = go.Figure()

fig1.add_trace(go.Scatter(
    x=monthly_sales['Order_Date'],
    y=monthly_sales['Sales'],
    mode='lines+markers',
    name='Actual Sales',
    line=dict(color='#2E86AB', width=2),
    marker=dict(size=6),
    hovertemplate='<b>Date:</b> %{x|%b %Y}<br><b>Sales:</b> $%{y:,.0f}<extra></extra>'
))

# add trend line
z = np.polyfit(range(len(monthly_sales)), monthly_sales['Sales'], 1)
p = np.poly1d(z)
fig1.add_trace(go.Scatter(
    x=monthly_sales['Order_Date'],
    y=p(range(len(monthly_sales))),
    mode='lines',
    name='Trend',
    line=dict(color='red', dash='dash', width=2),
    hoverinfo='skip'
))

fig1.update_layout(
    title='Monthly Sales Trend (2022-2024)',
    xaxis_title='Month',
    yaxis_title='Sales ($)',
    hovermode='x unified',
    height=500,
    template='plotly_white'
)

fig1.write_html('1_line_chart_sales_trend.html')
print("✓ Line chart created")


# ==========================================
# 2. BAR CHART - Category comparisons
# ==========================================

category_sales = sales.groupby('Category').agg({
    'Sales': 'sum',
    'Profit': 'sum',
    'Quantity': 'sum'
}).reset_index()

fig2 = go.Figure()

fig2.add_trace(go.Bar(
    x=category_sales['Category'],
    y=category_sales['Sales'],
    name='Sales',
    marker_color='#A23B72',
    text=category_sales['Sales'].apply(lambda x: f'${x:,.0f}'),
    textposition='outside',
    hovertemplate='<b>%{x}</b><br>Sales: $%{y:,.0f}<extra></extra>'
))

fig2.add_trace(go.Bar(
    x=category_sales['Category'],
    y=category_sales['Profit'],
    name='Profit',
    marker_color='#F18F01',
    text=category_sales['Profit'].apply(lambda x: f'${x:,.0f}'),
    textposition='outside',
    hovertemplate='<b>%{x}</b><br>Profit: $%{y:,.0f}<extra></extra>'
))

fig2.update_layout(
    title='Sales vs Profit by Category',
    xaxis_title='Category',
    yaxis_title='Amount ($)',
    barmode='group',
    height=500,
    template='plotly_white',
    showlegend=True
)

fig2.write_html('2_bar_chart_category.html')
print("✓ Bar chart created")


# ==========================================
# 3. HISTOGRAM - Distribution analysis
# ==========================================

fig3 = go.Figure()

fig3.add_trace(go.Histogram(
    x=sales['Sales'],
    nbinsx=50,
    name='Sales Distribution',
    marker=dict(
        color='#06A77D',
        line=dict(color='white', width=1)
    ),
    hovertemplate='Sales Range: $%{x}<br>Count: %{y}<extra></extra>'
))

# add mean and median lines
mean_val = sales['Sales'].mean()
median_val = sales['Sales'].median()

fig3.add_vline(x=mean_val, line_dash="dash", line_color="red", 
               annotation_text=f"Mean: ${mean_val:.0f}")
fig3.add_vline(x=median_val, line_dash="dash", line_color="blue",
               annotation_text=f"Median: ${median_val:.0f}")

fig3.update_layout(
    title='Distribution of Order Values',
    xaxis_title='Sales Amount ($)',
    yaxis_title='Frequency',
    height=500,
    template='plotly_white',
    showlegend=False
)

fig3.write_html('3_histogram_distribution.html')
print("✓ Histogram created")


# ==========================================
# 4. SCATTER PLOT - Correlation analysis
# ==========================================

# sales vs profit with discount as color
fig4 = px.scatter(
    sales,
    x='Sales',
    y='Profit',
    color='Discount',
    size='Quantity',
    hover_data=['Category', 'Region'],
    color_continuous_scale='Viridis',
    title='Sales vs Profit Analysis (Bubble Chart)',
    labels={'Sales': 'Sales ($)', 'Profit': 'Profit ($)', 'Discount': 'Discount Rate'}
)

# add regression line
x = sales['Sales']
y = sales['Profit']
z = np.polyfit(x, y, 1)
p = np.poly1d(z)

fig4.add_trace(go.Scatter(
    x=sorted(x),
    y=p(sorted(x)),
    mode='lines',
    name='Trend Line',
    line=dict(color='red', dash='dash', width=2),
    showlegend=True
))

# calculate correlation
corr = sales['Sales'].corr(sales['Profit'])
fig4.add_annotation(
    text=f'Correlation: {corr:.3f}',
    xref='paper', yref='paper',
    x=0.05, y=0.95,
    showarrow=False,
    bgcolor='white',
    bordercolor='black',
    borderwidth=1
)

fig4.update_layout(
    height=600,
    template='plotly_white'
)

fig4.write_html('4_scatter_correlation.html')
print("✓ Scatter plot created")


# ==========================================
# 5. BOX PLOT - Statistical distribution
# ==========================================

fig5 = go.Figure()

for region in sales['Region'].unique():
    region_data = sales[sales['Region'] == region]['Profit']
    
    fig5.add_trace(go.Box(
        y=region_data,
        name=region,
        boxmean='sd',
        marker_color=px.colors.qualitative.Set2[list(sales['Region'].unique()).index(region)],
        hovertemplate='<b>%{fullData.name}</b><br>Value: $%{y:.0f}<extra></extra>'
    ))

fig5.update_layout(
    title='Profit Distribution by Region (with outliers)',
    yaxis_title='Profit ($)',
    xaxis_title='Region',
    height=500,
    template='plotly_white',
    showlegend=False
)

fig5.write_html('5_boxplot_regions.html')
print("✓ Box plot created")


# ==========================================
# 6. MULTIPLE SERIES LINE CHART
# ==========================================

# compare categories over time
monthly_category = sales.groupby([
    sales['Order_Date'].dt.to_period('M'), 
    'Category'
])['Sales'].sum().reset_index()
monthly_category['Order_Date'] = monthly_category['Order_Date'].apply(lambda x: x.to_timestamp())

fig6 = px.line(
    monthly_category,
    x='Order_Date',
    y='Sales',
    color='Category',
    title='Category Sales Comparison Over Time',
    labels={'Sales': 'Sales ($)', 'Order_Date': 'Month'},
    color_discrete_sequence=px.colors.qualitative.Bold
)

fig6.update_traces(mode='lines+markers', line=dict(width=2), marker=dict(size=5))

fig6.update_layout(
    height=500,
    template='plotly_white',
    hovermode='x unified'
)

fig6.write_html('6_multi_line_categories.html')
print("✓ Multi-series line chart created")


# ==========================================
# 7. STACKED BAR CHART
# ==========================================

segment_region = sales.groupby(['Region', 'Segment'])['Sales'].sum().reset_index()

fig7 = px.bar(
    segment_region,
    x='Region',
    y='Sales',
    color='Segment',
    title='Sales by Region and Segment (Stacked)',
    labels={'Sales': 'Total Sales ($)'},
    color_discrete_sequence=px.colors.qualitative.Pastel,
    text_auto='.2s'
)

fig7.update_layout(
    height=500,
    template='plotly_white',
    barmode='stack'
)

fig7.write_html('7_stacked_bar_segment.html')
print("✓ Stacked bar chart created")


print("\n=== Statistical Charts Complete ===")
print("7 chart files created with full interactivity")
print("All charts include zoom, pan, hover tooltips, and export options")