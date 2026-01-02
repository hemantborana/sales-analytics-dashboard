import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import numpy as np

sales = pd.read_csv('superstore_sales.csv')
operations = pd.read_csv('operations_data.csv')
financial = pd.read_csv('financial_data.csv')

sales['Order_Date'] = pd.to_datetime(sales['Order_Date'])
operations['Date'] = pd.to_datetime(operations['Date'])
financial['Month'] = pd.to_datetime(financial['Month'])

print("Creating advanced visualizations...")

# ==========================================
# 8. HEATMAP - Correlation matrix
# ==========================================

# create correlation matrix for numerical columns
corr_data = sales[['Sales', 'Quantity', 'Discount', 'Profit']].corr()

fig8 = go.Figure(data=go.Heatmap(
    z=corr_data.values,
    x=corr_data.columns,
    y=corr_data.columns,
    colorscale='RdBu',
    zmid=0,
    text=np.round(corr_data.values, 2),
    texttemplate='%{text}',
    textfont={"size": 14},
    hovertemplate='%{y} vs %{x}<br>Correlation: %{z:.3f}<extra></extra>'
))

fig8.update_layout(
    title='Sales Metrics Correlation Matrix',
    height=500,
    width=600,
    template='plotly_white'
)

fig8.write_html('8_heatmap_correlation.html')
print("✓ Heatmap created")


# ==========================================
# 9. HEATMAP - Sales by region and category
# ==========================================

region_category = sales.pivot_table(
    values='Sales',
    index='Region',
    columns='Category',
    aggfunc='sum'
)

fig9 = go.Figure(data=go.Heatmap(
    z=region_category.values,
    x=region_category.columns,
    y=region_category.index,
    colorscale='Viridis',
    text=np.round(region_category.values, 0),
    texttemplate='$%{text:,.0f}',
    textfont={"size": 12},
    hovertemplate='Region: %{y}<br>Category: %{x}<br>Sales: $%{z:,.0f}<extra></extra>'
))

fig9.update_layout(
    title='Sales Heatmap: Region vs Category',
    xaxis_title='Category',
    yaxis_title='Region',
    height=500,
    template='plotly_white'
)

fig9.write_html('9_heatmap_region_category.html')
print("✓ Geographic heatmap created")


# ==========================================
# 10. TREEMAP - Hierarchical sales
# ==========================================

treemap_data = sales.groupby(['Category', 'Sub_Category'])['Sales'].sum().reset_index()

fig10 = px.treemap(
    treemap_data,
    path=['Category', 'Sub_Category'],
    values='Sales',
    title='Sales Distribution - Category Hierarchy',
    color='Sales',
    color_continuous_scale='Blues',
    hover_data={'Sales': ':$,.0f'}
)

fig10.update_traces(
    textinfo='label+value',
    texttemplate='<b>%{label}</b><br>$%{value:,.0f}',
    hovertemplate='<b>%{label}</b><br>Sales: $%{value:,.0f}<extra></extra>'
)

fig10.update_layout(
    height=600,
    template='plotly_white'
)

fig10.write_html('10_treemap_hierarchy.html')
print("✓ Treemap created")


# ==========================================
# 11. SANKEY DIAGRAM - Customer flow
# ==========================================

# segment -> region -> category flow
sankey_df = sales.groupby(['Segment', 'Region', 'Category'])['Sales'].sum().reset_index()

# create nodes
segments = sales['Segment'].unique().tolist()
regions = sales['Region'].unique().tolist()
categories = sales['Category'].unique().tolist()

all_nodes = segments + regions + categories

# create links
source = []
target = []
value = []

# segment to region
for _, row in sales.groupby(['Segment', 'Region'])['Sales'].sum().reset_index().iterrows():
    source.append(all_nodes.index(row['Segment']))
    target.append(all_nodes.index(row['Region']))
    value.append(row['Sales'])

# region to category
for _, row in sales.groupby(['Region', 'Category'])['Sales'].sum().reset_index().iterrows():
    source.append(all_nodes.index(row['Region']))
    target.append(all_nodes.index(row['Category']))
    value.append(row['Sales'])

fig11 = go.Figure(data=[go.Sankey(
    node=dict(
        pad=15,
        thickness=20,
        line=dict(color='black', width=0.5),
        label=all_nodes,
        color=['#FF6B6B', '#4ECDC4', '#45B7D1', '#FFA07A', '#98D8C8', '#F7DC6F',
               '#BB8FCE', '#85C1E2', '#F8B739']
    ),
    link=dict(
        source=source,
        target=target,
        value=value,
        color='rgba(0,0,0,0.2)'
    )
)])

fig11.update_layout(
    title='Sales Flow: Segment → Region → Category',
    height=600,
    template='plotly_white',
    font=dict(size=12)
)

fig11.write_html('11_sankey_flow.html')
print("✓ Sankey diagram created")


# ==========================================
# 12. RADAR CHART - Regional performance
# ==========================================

# calculate metrics for each region
region_metrics = sales.groupby('Region').agg({
    'Sales': 'sum',
    'Profit': 'sum',
    'Quantity': 'sum',
    'Order_ID': 'count'
}).reset_index()

region_metrics.columns = ['Region', 'Sales', 'Profit', 'Quantity', 'Orders']

# normalize to 0-100 scale for better comparison
for col in ['Sales', 'Profit', 'Quantity', 'Orders']:
    max_val = region_metrics[col].max()
    region_metrics[col + '_norm'] = (region_metrics[col] / max_val) * 100

fig12 = go.Figure()

categories = ['Sales', 'Profit', 'Quantity', 'Orders']
colors = ['#FF6B6B', '#4ECDC4', '#45B7D1', '#FFA07A']

for i, region in enumerate(region_metrics['Region']):
    values = [
        region_metrics[region_metrics['Region'] == region]['Sales_norm'].values[0],
        region_metrics[region_metrics['Region'] == region]['Profit_norm'].values[0],
        region_metrics[region_metrics['Region'] == region]['Quantity_norm'].values[0],
        region_metrics[region_metrics['Region'] == region]['Orders_norm'].values[0]
    ]
    
    fig12.add_trace(go.Scatterpolar(
        r=values + [values[0]],
        theta=categories + [categories[0]],
        fill='toself',
        name=region,
        line=dict(color=colors[i]),
        hovertemplate='<b>%{theta}</b><br>Score: %{r:.1f}<extra></extra>'
    ))

fig12.update_layout(
    polar=dict(
        radialaxis=dict(
            visible=True,
            range=[0, 100]
        )
    ),
    title='Regional Performance Comparison (Radar)',
    height=600,
    template='plotly_white',
    showlegend=True
)

fig12.write_html('12_radar_performance.html')
print("✓ Radar chart created")


# ==========================================
# 13. WATERFALL CHART - Revenue breakdown
# ==========================================

# use financial data for waterfall
latest_month = financial.iloc[-1]

waterfall_values = [
    latest_month['Revenue'],
    -latest_month['COGS'],
    -latest_month['Operating_Expenses'],
    latest_month['Net_Profit']
]

waterfall_labels = ['Revenue', 'COGS', 'Operating Expenses', 'Net Profit']

fig13 = go.Figure(go.Waterfall(
    name='Financial',
    orientation='v',
    measure=['relative', 'relative', 'relative', 'total'],
    x=waterfall_labels,
    textposition='outside',
    text=[f'${v:,.0f}' for v in waterfall_values],
    y=waterfall_values,
    connector={'line': {'color': 'rgb(63, 63, 63)'}},
    increasing={'marker': {'color': '#2ECC71'}},
    decreasing={'marker': {'color': '#E74C3C'}},
    totals={'marker': {'color': '#3498DB'}},
    hovertemplate='<b>%{x}</b><br>Amount: $%{y:,.0f}<extra></extra>'
))

fig13.update_layout(
    title=f'Revenue to Profit Breakdown - {latest_month["Month"].strftime("%B %Y")}',
    yaxis_title='Amount ($)',
    height=500,
    template='plotly_white',
    showlegend=False
)

fig13.write_html('13_waterfall_revenue.html')
print("✓ Waterfall chart created")


# ==========================================
# 14. WATERFALL CHART - Yearly comparison
# ==========================================

# yearly profit changes
financial['Year'] = financial['Month'].dt.year
yearly = financial.groupby('Year')['Net_Profit'].sum().reset_index()

waterfall_yearly = []
labels_yearly = []

for i in range(len(yearly)):
    if i == 0:
        waterfall_yearly.append(yearly.iloc[i]['Net_Profit'])
        labels_yearly.append(str(yearly.iloc[i]['Year']))
    else:
        change = yearly.iloc[i]['Net_Profit'] - yearly.iloc[i-1]['Net_Profit']
        waterfall_yearly.append(change)
        labels_yearly.append(f"{yearly.iloc[i]['Year']} Change")

waterfall_yearly.append(yearly.iloc[-1]['Net_Profit'])
labels_yearly.append('Final 2024')

measures = ['absolute'] + ['relative'] * (len(waterfall_yearly) - 2) + ['total']

fig14 = go.Figure(go.Waterfall(
    orientation='v',
    measure=measures,
    x=labels_yearly,
    textposition='outside',
    text=[f'${v:,.0f}' for v in waterfall_yearly],
    y=waterfall_yearly,
    connector={'line': {'color': 'rgb(63, 63, 63)'}},
    increasing={'marker': {'color': '#27AE60'}},
    decreasing={'marker': {'color': '#C0392B'}},
    totals={'marker': {'color': '#2980B9'}}
))

fig14.update_layout(
    title='Profit Evolution: 2022-2024',
    yaxis_title='Profit ($)',
    height=500,
    template='plotly_white'
)

fig14.write_html('14_waterfall_yearly.html')
print("✓ Yearly waterfall created")


# ==========================================
# 15. COMBO CHART - Multiple viz types
# ==========================================

monthly_perf = sales.groupby(sales['Order_Date'].dt.to_period('M')).agg({
    'Sales': 'sum',
    'Profit': 'sum',
    'Order_ID': 'count'
}).reset_index()
monthly_perf['Order_Date'] = monthly_perf['Order_Date'].apply(lambda x: x.to_timestamp())
monthly_perf['Profit_Margin'] = (monthly_perf['Profit'] / monthly_perf['Sales']) * 100

fig15 = make_subplots(specs=[[{"secondary_y": True}]])

fig15.add_trace(
    go.Bar(
        x=monthly_perf['Order_Date'],
        y=monthly_perf['Sales'],
        name='Sales',
        marker_color='#3498DB',
        hovertemplate='Sales: $%{y:,.0f}<extra></extra>'
    ),
    secondary_y=False
)

fig15.add_trace(
    go.Scatter(
        x=monthly_perf['Order_Date'],
        y=monthly_perf['Profit_Margin'],
        name='Profit Margin %',
        mode='lines+markers',
        line=dict(color='#E74C3C', width=3),
        marker=dict(size=8),
        hovertemplate='Margin: %{y:.1f}%<extra></extra>'
    ),
    secondary_y=True
)

fig15.update_xaxes(title_text='Month')
fig15.update_yaxes(title_text='Sales ($)', secondary_y=False)
fig15.update_yaxes(title_text='Profit Margin (%)', secondary_y=True)

fig15.update_layout(
    title='Sales Volume vs Profit Margin Trend',
    height=500,
    template='plotly_white',
    hovermode='x unified'
)

fig15.write_html('15_combo_chart.html')
print("✓ Combo chart created")


print("\n=== Advanced Charts Complete ===")
print("8 advanced visualizations created")
print("Total Part A: 15 interactive charts")