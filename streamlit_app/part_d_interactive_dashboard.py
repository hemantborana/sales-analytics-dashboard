import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import numpy as np

# page config
st.set_page_config(
    page_title="Sales Analytics Dashboard",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="expanded"
)

# load data with caching
@st.cache_data
def load_data():
    sales = pd.read_csv('superstore_sales.csv')
    sales['Order_Date'] = pd.to_datetime(sales['Order_Date'])
    sales['Year'] = sales['Order_Date'].dt.year
    sales['Month'] = sales['Order_Date'].dt.month
    sales['Quarter'] = sales['Order_Date'].dt.quarter
    sales['Month_Name'] = sales['Order_Date'].dt.strftime('%b %Y')
    
    operations = pd.read_csv('operations_data.csv')
    operations['Date'] = pd.to_datetime(operations['Date'])
    
    financial = pd.read_csv('financial_data.csv')
    financial['Month'] = pd.to_datetime(financial['Month'])
    
    customer = pd.read_csv('customer_data.csv')
    
    return sales, operations, financial, customer

sales, operations, financial, customer = load_data()

# custom CSS
st.markdown("""
    <style>
    .stMetric {
        background-color: #f8f9fa;
        padding: 20px;
        border-radius: 10px;
        border: 1px solid #dee2e6;
    }
    .stMetric label {
        color: #495057 !important;
        font-size: 14px !important;
        font-weight: 600 !important;
    }
    .stMetric [data-testid="stMetricValue"] {
        color: #212529 !important;
        font-size: 32px !important;
        font-weight: bold !important;
    }
    .stMetric [data-testid="stMetricDelta"] {
        color: #6c757d !important;
    }
    </style>
""", unsafe_allow_html=True)

# sidebar filters
st.sidebar.header("Filters & Controls")

# date range filter
min_date = sales['Order_Date'].min()
max_date = sales['Order_Date'].max()

date_range = st.sidebar.date_input(
    "Select Date Range",
    value=(min_date, max_date),
    min_value=min_date,
    max_value=max_date
)

if len(date_range) == 2:
    start_date, end_date = date_range
    sales = sales[(sales['Order_Date'] >= pd.to_datetime(start_date)) & 
                  (sales['Order_Date'] <= pd.to_datetime(end_date))]

# region filter
regions = ['All'] + sorted(sales['Region'].unique().tolist())
selected_region = st.sidebar.selectbox("Select Region", regions)

if selected_region != 'All':
    sales = sales[sales['Region'] == selected_region]

# category filter
categories = ['All'] + sorted(sales['Category'].unique().tolist())
selected_category = st.sidebar.selectbox("Select Category", categories)

if selected_category != 'All':
    sales = sales[sales['Category'] == selected_category]

# segment filter
segments = st.sidebar.multiselect(
    "Select Segments",
    options=sales['Segment'].unique(),
    default=sales['Segment'].unique()
)

sales = sales[sales['Segment'].isin(segments)]

st.sidebar.markdown("---")

# view selector
view_mode = st.sidebar.radio(
    "Dashboard View",
    ["Executive Summary", "Detailed Analysis", "Drill-Down Explorer", "What-If Scenario"]
)

st.sidebar.markdown("---")

# export button
if st.sidebar.button("Export Data"):
    csv = sales.to_csv(index=False)
    st.sidebar.download_button(
        label="Download CSV",
        data=csv,
        file_name="filtered_sales_data.csv",
        mime="text/csv"
    )

# main dashboard
st.title("Interactive Sales Analytics Dashboard")
st.markdown("### Self-Service Business Intelligence Platform")

# ===================================
# EXECUTIVE SUMMARY VIEW
# ===================================

if view_mode == "Executive Summary":
    
    # KPI metrics row
    col1, col2, col3, col4 = st.columns(4)
    
    total_sales = sales['Sales'].sum()
    total_profit = sales['Profit'].sum()
    total_orders = sales['Order_ID'].nunique()
    avg_order = total_sales / total_orders if total_orders > 0 else 0
    
    with col1:
        st.metric(
            label="Total Sales",
            value=f"${total_sales:,.0f}",
            delta=f"{(total_sales/1000000):.2f}M"
        )
    
    with col2:
        profit_margin = (total_profit/total_sales*100) if total_sales > 0 else 0
        st.metric(
            label="Total Profit",
            value=f"${total_profit:,.0f}",
            delta=f"{profit_margin:.1f}% margin"
        )
    
    with col3:
        st.metric(
            label="Total Orders",
            value=f"{total_orders:,}",
            delta="Active"
        )
    
    with col4:
        st.metric(
            label="Avg Order Value",
            value=f"${avg_order:,.2f}",
            delta="Per order"
        )
    
    st.markdown("---")
    
    # row 1: trend and category
    col1, col2 = st.columns([2, 1])
    
    with col1:
        st.subheader("Sales & Profit Trend")
        
        monthly = sales.groupby('Month_Name').agg({
            'Sales': 'sum',
            'Profit': 'sum'
        }).reset_index()
        
        fig = make_subplots(specs=[[{"secondary_y": True}]])
        
        fig.add_trace(
            go.Scatter(
                x=monthly['Month_Name'],
                y=monthly['Sales'],
                name="Sales",
                fill='tozeroy',
                line=dict(color='#3498db', width=2)
            ),
            secondary_y=False
        )
        
        fig.add_trace(
            go.Scatter(
                x=monthly['Month_Name'],
                y=monthly['Profit'],
                name="Profit",
                line=dict(color='#2ecc71', width=3)
            ),
            secondary_y=True
        )
        
        fig.update_layout(
            height=400,
            hovermode='x unified',
            template='plotly_white'
        )
        
        st.plotly_chart(fig, use_container_width=True)
    
    with col2:
        st.subheader("Category Split")
        
        category_data = sales.groupby('Category')['Sales'].sum().reset_index()
        
        fig = px.pie(
            category_data,
            values='Sales',
            names='Category',
            hole=0.4,
            color_discrete_sequence=px.colors.qualitative.Set3
        )
        
        fig.update_traces(
            textposition='inside',
            textinfo='percent+label'
        )
        
        fig.update_layout(height=400)
        
        st.plotly_chart(fig, use_container_width=True)
    
    st.markdown("---")
    
    # row 2: regional and segment
    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader("Regional Performance")
        
        region_data = sales.groupby('Region').agg({
            'Sales': 'sum',
            'Profit': 'sum'
        }).reset_index()
        
        region_data['Profit_Margin'] = (region_data['Profit'] / region_data['Sales'] * 100)
        
        fig = go.Figure()
        
        fig.add_trace(go.Bar(
            x=region_data['Region'],
            y=region_data['Sales'],
            name='Sales',
            marker_color='#3498db',
            text=region_data['Sales'].apply(lambda x: f'${x/1000:.0f}K'),
            textposition='outside'
        ))
        
        fig.update_layout(
            height=400,
            template='plotly_white',
            showlegend=False
        )
        
        st.plotly_chart(fig, use_container_width=True)
    
    with col2:
        st.subheader("Segment Analysis")
        
        segment_data = sales.groupby('Segment').agg({
            'Sales': 'sum',
            'Profit': 'sum',
            'Order_ID': 'nunique'
        }).reset_index()
        
        fig = px.bar(
            segment_data,
            x='Segment',
            y='Sales',
            color='Profit',
            color_continuous_scale='RdYlGn',
            text='Sales'
        )
        
        fig.update_traces(
            texttemplate='$%{text:.2s}',
            textposition='outside'
        )
        
        fig.update_layout(height=400, template='plotly_white')
        
        st.plotly_chart(fig, use_container_width=True)

# ===================================
# DETAILED ANALYSIS VIEW
# ===================================

elif view_mode == "Detailed Analysis":
    
    st.subheader("Detailed Performance Analysis")
    
    tab1, tab2, tab3 = st.tabs(["Product Analysis", "Time Analysis", "Profitability"])
    
    with tab1:
        col1, col2 = st.columns(2)
        
        with col1:
            st.markdown("#### Top 10 Products by Sales")
            
            top_products = sales.groupby('Product_Name')['Sales'].sum().nlargest(10).reset_index()
            
            fig = px.bar(
                top_products,
                y='Product_Name',
                x='Sales',
                orientation='h',
                color='Sales',
                color_continuous_scale='Blues'
            )
            
            fig.update_layout(height=400, showlegend=False)
            st.plotly_chart(fig, use_container_width=True)
        
        with col2:
            st.markdown("#### Sub-Category Performance")
            
            subcat = sales.groupby('Sub_Category').agg({
                'Sales': 'sum',
                'Profit': 'sum'
            }).reset_index()
            
            fig = px.scatter(
                subcat,
                x='Sales',
                y='Profit',
                size='Sales',
                color='Sub_Category',
                hover_data=['Sub_Category'],
                size_max=50
            )
            
            fig.update_layout(height=400)
            st.plotly_chart(fig, use_container_width=True)
    
    with tab2:
        st.markdown("#### Quarterly Trends")
        
        quarterly = sales.groupby(['Year', 'Quarter']).agg({
            'Sales': 'sum',
            'Profit': 'sum',
            'Order_ID': 'nunique'
        }).reset_index()
        
        quarterly['Period'] = quarterly['Year'].astype(str) + '-Q' + quarterly['Quarter'].astype(str)
        
        fig = go.Figure()
        
        fig.add_trace(go.Bar(
            x=quarterly['Period'],
            y=quarterly['Sales'],
            name='Sales',
            marker_color='lightblue'
        ))
        
        fig.add_trace(go.Scatter(
            x=quarterly['Period'],
            y=quarterly['Profit'],
            name='Profit',
            yaxis='y2',
            line=dict(color='green', width=3)
        ))
        
        fig.update_layout(
            yaxis2=dict(overlaying='y', side='right'),
            height=400,
            template='plotly_white'
        )
        
        st.plotly_chart(fig, use_container_width=True)
    
    with tab3:
        st.markdown("#### Profitability Heatmap")
        
        heatmap_data = sales.pivot_table(
            values='Profit',
            index='Category',
            columns='Region',
            aggfunc='sum'
        )
        
        fig = go.Figure(data=go.Heatmap(
            z=heatmap_data.values,
            x=heatmap_data.columns,
            y=heatmap_data.index,
            colorscale='RdYlGn',
            text=np.round(heatmap_data.values, 0),
            texttemplate='$%{text:,.0f}',
            textfont={"size": 12}
        ))
        
        fig.update_layout(height=400)
        st.plotly_chart(fig, use_container_width=True)

# ===================================
# DRILL-DOWN EXPLORER
# ===================================

elif view_mode == "Drill-Down Explorer":
    
    st.subheader("Interactive Drill-Down Explorer")
    
    st.info("Click on any chart element to drill down into details!")
    
    # level selector
    drill_level = st.radio(
        "Select Drill Level:",
        ["Category → Sub-Category", "Region → State", "Time → Month → Day"],
        horizontal=True
    )
    
    if drill_level == "Category → Sub-Category":
        
        col1, col2 = st.columns([1, 2])
        
        with col1:
            st.markdown("#### Step 1: Select Category")
            
            cat_sales = sales.groupby('Category')['Sales'].sum().reset_index()
            
            selected_cat = st.selectbox(
                "Choose a category to drill down:",
                cat_sales['Category'].tolist()
            )
            
            fig = px.bar(
                cat_sales,
                x='Category',
                y='Sales',
                color='Category',
                color_discrete_sequence=px.colors.qualitative.Bold
            )
            
            fig.update_layout(height=300, showlegend=False)
            st.plotly_chart(fig, use_container_width=True)
        
        with col2:
            st.markdown(f"#### Step 2: {selected_cat} - Sub-Categories")
            
            filtered = sales[sales['Category'] == selected_cat]
            subcat_data = filtered.groupby('Sub_Category').agg({
                'Sales': 'sum',
                'Profit': 'sum',
                'Quantity': 'sum'
            }).reset_index()
            
            fig = px.treemap(
                subcat_data,
                path=['Sub_Category'],
                values='Sales',
                color='Profit',
                color_continuous_scale='RdYlGn',
                hover_data=['Sales', 'Profit', 'Quantity']
            )
            
            fig.update_layout(height=400)
            st.plotly_chart(fig, use_container_width=True)
        
        # detailed table
        st.markdown("#### Step 3: Detailed Transactions")
        
        detail_data = filtered[['Order_ID', 'Order_Date', 'Sub_Category', 
                               'Product_Name', 'Sales', 'Profit', 'Quantity']].sort_values('Sales', ascending=False)
        
        st.dataframe(
            detail_data.head(20),
            use_container_width=True,
            hide_index=True
        )
    
    elif drill_level == "Region → State":
        
        col1, col2 = st.columns(2)
        
        with col1:
            st.markdown("#### Regional Overview")
            
            region_sales = sales.groupby('Region')['Sales'].sum().reset_index()
            
            selected_region = st.selectbox(
                "Select Region:",
                region_sales['Region'].tolist()
            )
            
            fig = px.pie(
                region_sales,
                values='Sales',
                names='Region',
                hole=0.5
            )
            
            fig.update_layout(height=400)
            st.plotly_chart(fig, use_container_width=True)
        
        with col2:
            st.markdown(f"#### {selected_region} - State Breakdown")
            
            state_data = sales[sales['Region'] == selected_region].groupby('State')['Sales'].sum().reset_index()
            state_data = state_data.sort_values('Sales', ascending=True).tail(10)
            
            fig = px.bar(
                state_data,
                y='State',
                x='Sales',
                orientation='h',
                color='Sales',
                color_continuous_scale='Viridis'
            )
            
            fig.update_layout(height=400)
            st.plotly_chart(fig, use_container_width=True)

# ===================================
# WHAT-IF SCENARIO ANALYSIS
# ===================================

elif view_mode == "What-If Scenario":
    
    st.subheader("What-If Scenario Modeling")
    
    st.info("Adjust parameters below to see impact on sales and profit")
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        price_change = st.slider(
            "Price Change (%)",
            min_value=-50,
            max_value=50,
            value=0,
            step=5
        )
    
    with col2:
        volume_change = st.slider(
            "Volume Change (%)",
            min_value=-50,
            max_value=50,
            value=0,
            step=5
        )
    
    with col3:
        cost_change = st.slider(
            "Cost Change (%)",
            min_value=-30,
            max_value=30,
            value=0,
            step=5
        )
    
    # calculate scenarios
    base_sales = sales['Sales'].sum()
    base_profit = sales['Profit'].sum()
    base_cost = base_sales - base_profit
    
    new_price_mult = 1 + (price_change / 100)
    new_volume_mult = 1 + (volume_change / 100)
    new_cost_mult = 1 + (cost_change / 100)
    
    new_sales = base_sales * new_price_mult * new_volume_mult
    new_cost = base_cost * new_cost_mult * new_volume_mult
    new_profit = new_sales - new_cost
    
    # display results
    st.markdown("---")
    st.markdown("### Scenario Results")
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        sales_delta = new_sales - base_sales
        st.metric(
            "Projected Sales",
            f"${new_sales:,.0f}",
            delta=f"${sales_delta:,.0f}"
        )
    
    with col2:
        profit_delta = new_profit - base_profit
        st.metric(
            "Projected Profit",
            f"${new_profit:,.0f}",
            delta=f"${profit_delta:,.0f}"
        )
    
    with col3:
        margin = (new_profit / new_sales * 100) if new_sales > 0 else 0
        base_margin = (base_profit / base_sales * 100)
        margin_delta = margin - base_margin
        st.metric(
            "Profit Margin",
            f"{margin:.1f}%",
            delta=f"{margin_delta:.1f}%"
        )
    
    # comparison chart
    comparison_df = pd.DataFrame({
        'Scenario': ['Current', 'Projected'],
        'Sales': [base_sales, new_sales],
        'Profit': [base_profit, new_profit]
    })
    
    fig = go.Figure()
    
    fig.add_trace(go.Bar(
        x=comparison_df['Scenario'],
        y=comparison_df['Sales'],
        name='Sales',
        marker_color='lightblue'
    ))
    
    fig.add_trace(go.Bar(
        x=comparison_df['Scenario'],
        y=comparison_df['Profit'],
        name='Profit',
        marker_color='lightgreen'
    ))
    
    fig.update_layout(
        height=400,
        barmode='group',
        template='plotly_white',
        title='Current vs Projected Performance'
    )
    
    st.plotly_chart(fig, use_container_width=True)

# footer
st.markdown("---")
st.markdown("**DAR Assignment 6 - Interactive Analytics Platform** | Built with Streamlit & Plotly")