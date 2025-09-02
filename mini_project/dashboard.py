import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import numpy as np
from datetime import datetime

# Page config
st.set_page_config(
    page_title="HR Analytics Dashboard",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS
st.markdown("""
<style>
    .main-header {
        font-size: 2.5rem;
        font-weight: bold;
        color: #1f77b4;
        text-align: center;
        margin-bottom: 2rem;
    }
    .metric-card {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        padding: 1rem;
        border-radius: 10px;
        color: white;
        text-align: center;
        margin: 0.5rem 0;
    }
    .sidebar .sidebar-content {
        background: linear-gradient(135deg, #f5f7fa 0%, #c3cfe2 100%);
    }
</style>
""", unsafe_allow_html=True)

@st.cache_data
def load_data():
    """Load all processed data files"""
    try:
        # Load main enriched data
        df_main = pd.read_csv("employees_enriched.csv")
        df_main['JoiningDate'] = pd.to_datetime(df_main['JoiningDate'])
        
        # Load department summary
        dept_summary = pd.read_csv("dept_summary.csv")
        
        # Load highest paid employees
        highest_paid = pd.read_csv("highest_paid.csv")
        
        # Create job title summary (fixing step6 issue)
        job_summary = df_main.groupby("JobTitle").agg(
            Avg_Salary=("Salary","mean"),
            Total_Salary=("Salary","sum"),
            Employee_Count=("EmpID","count")
        ).reset_index().sort_values("Avg_Salary", ascending=False)
        
        return df_main, dept_summary, highest_paid, job_summary
    except FileNotFoundError as e:
        st.error(f"Data file not found: {e}")
        st.info("Please run your 7-step pipeline first to generate the CSV files.")
        return None, None, None, None

def create_salary_distribution_chart(df):
    """Create salary distribution histogram"""
    fig = px.histogram(
        df, x='Salary', nbins=20,
        title='Salary Distribution Across All Employees',
        color_discrete_sequence=['#1f77b4']
    )
    fig.update_layout(
        xaxis_title="Salary ($)",
        yaxis_title="Number of Employees",
        showlegend=False
    )
    return fig

def create_dept_salary_chart(dept_summary):
    """Create department-wise salary analysis"""
    fig = make_subplots(
        rows=1, cols=2,
        subplot_titles=('Average Salary by Department', 'Employee Count by Department'),
        specs=[[{"secondary_y": False}, {"secondary_y": False}]]
    )
    
    # Average salary bar chart
    fig.add_trace(
        go.Bar(
            x=dept_summary['Department'],
            y=dept_summary['Avg_Salary'],
            name='Avg Salary',
            marker_color='#2E86AB',
            text=[f'${x:,.0f}' for x in dept_summary['Avg_Salary']],
            textposition='outside'
        ),
        row=1, col=1
    )
    
    # Employee count bar chart
    fig.add_trace(
        go.Bar(
            x=dept_summary['Department'],
            y=dept_summary['Employee_Count'],
            name='Employee Count',
            marker_color='#A23B72',
            text=dept_summary['Employee_Count'],
            textposition='outside'
        ),
        row=1, col=2
    )
    
    fig.update_layout(height=500, showlegend=False)
    fig.update_xaxes(title_text="Department", row=1, col=1)
    fig.update_xaxes(title_text="Department", row=1, col=2)
    fig.update_yaxes(title_text="Average Salary ($)", row=1, col=1)
    fig.update_yaxes(title_text="Number of Employees", row=1, col=2)
    
    return fig

def create_salary_vs_experience_scatter(df):
    """Create scatter plot of salary vs years of service"""
    fig = px.scatter(
        df, x='YearsOfService', y='Salary', 
        color='Department', size='Salary',
        hover_data=['Name', 'JobTitle'],
        title='Salary vs Years of Service by Department',
        color_discrete_sequence=px.colors.qualitative.Set2
    )
    fig.update_layout(
        xaxis_title="Years of Service",
        yaxis_title="Salary ($)"
    )
    return fig

def create_hiring_timeline(df):
    """Create hiring timeline chart"""
    df_hiring = df.groupby([df['JoiningDate'].dt.year, 'Department']).size().reset_index()
    df_hiring.columns = ['Year', 'Department', 'Hires']
    
    fig = px.line(
        df_hiring, x='Year', y='Hires', 
        color='Department', markers=True,
        title='Hiring Timeline by Department',
        color_discrete_sequence=px.colors.qualitative.Set1
    )
    fig.update_layout(
        xaxis_title="Year",
        yaxis_title="Number of Hires"
    )
    return fig

def create_top_earners_chart(df, n=10):
    """Create top earners horizontal bar chart"""
    top_earners = df.nlargest(n, 'Salary')[['Name', 'Department', 'JobTitle', 'Salary']]
    
    fig = px.bar(
        top_earners, 
        x='Salary', y='Name', 
        color='Department',
        orientation='h',
        title=f'Top {n} Highest Paid Employees',
        text='Salary',
        color_discrete_sequence=px.colors.qualitative.Pastel
    )
    fig.update_traces(texttemplate='$%{text:,.0f}', textposition='outside')
    fig.update_layout(
        xaxis_title="Salary ($)",
        yaxis_title="Employee",
        yaxis={'categoryorder':'total ascending'}
    )
    return fig

def main():
    st.markdown('<h1 class="main-header">📊 HR Analytics Dashboard</h1>', unsafe_allow_html=True)
    
    # Load data
    df_main, dept_summary, highest_paid, job_summary = load_data()
    
    if df_main is None:
        return
    
    # Sidebar filters
    st.sidebar.header("🔧 Filters & Controls")
    
    # Department filter
    departments = ['All'] + sorted(df_main['Department'].unique().tolist())
    selected_dept = st.sidebar.selectbox("Select Department", departments)
    
    # Salary range filter
    min_salary, max_salary = st.sidebar.slider(
        "Salary Range ($)",
        min_value=int(df_main['Salary'].min()),
        max_value=int(df_main['Salary'].max()),
        value=(int(df_main['Salary'].min()), int(df_main['Salary'].max())),
        step=1000
    )
    
    # Years of service filter
    min_years, max_years = st.sidebar.slider(
        "Years of Service",
        min_value=0,
        max_value=int(df_main['YearsOfService'].max()),
        value=(0, int(df_main['YearsOfService'].max()))
    )
    
    # Apply filters
    filtered_df = df_main.copy()
    if selected_dept != 'All':
        filtered_df = filtered_df[filtered_df['Department'] == selected_dept]
    filtered_df = filtered_df[
        (filtered_df['Salary'] >= min_salary) & 
        (filtered_df['Salary'] <= max_salary) &
        (filtered_df['YearsOfService'] >= min_years) & 
        (filtered_df['YearsOfService'] <= max_years)
    ]
    
    # Key Metrics Row
    st.header("📈 Key Metrics")
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.metric(
            label="Total Employees",
            value=len(filtered_df),
            delta=f"{len(filtered_df) - len(df_main)} from total"
        )
    
    with col2:
        avg_salary = filtered_df['Salary'].mean()
        overall_avg = df_main['Salary'].mean()
        st.metric(
            label="Average Salary",
            value=f"${avg_salary:,.0f}",
            delta=f"${avg_salary - overall_avg:+,.0f}"
        )
    
    with col3:
        total_cost = filtered_df['Salary'].sum()
        st.metric(
            label="Total Salary Cost",
            value=f"${total_cost:,.0f}"
        )
    
    with col4:
        avg_experience = filtered_df['YearsOfService'].mean()
        st.metric(
            label="Avg Years of Service",
            value=f"{avg_experience:.1f} years"
        )
    
    st.divider()
    
    # Charts Section
    st.header("📊 Data Visualizations")
    
    # Row 1: Distribution charts
    col1, col2 = st.columns(2)
    
    with col1:
        st.plotly_chart(
            create_salary_distribution_chart(filtered_df),
            width='stretch'
        )
    
    with col2:
        st.plotly_chart(
            create_dept_salary_chart(dept_summary),
            width='stretch'
        )
    
    # Row 2: Scatter and Timeline
    col1, col2 = st.columns(2)
    
    with col1:
        st.plotly_chart(
            create_salary_vs_experience_scatter(filtered_df),
            width='stretch'
        )
    
    with col2:
        st.plotly_chart(
            create_hiring_timeline(df_main),
            width='stretch'
        )
    
    # Row 3: Top earners
    st.plotly_chart(
        create_top_earners_chart(filtered_df),
        width='stretch'
    )
    
    st.divider()
    
    # Data Tables Section
    st.header("📋 Detailed Analysis")
    
    tab1, tab2, tab3, tab4 = st.tabs(["Department Summary", "Job Title Analysis", "Highest Paid", "Raw Data"])
    
    with tab1:
        st.subheader("Department Performance")
        st.dataframe(
            dept_summary.style.format({
                'Avg_Salary': '${:,.0f}',
                'Total_Salary': '${:,.0f}'
            }),
            width='stretch'
        )
    
    with tab2:
        st.subheader("Job Title Analysis")
        st.dataframe(
            job_summary.style.format({
                'Avg_Salary': '${:,.0f}',
                'Total_Salary': '${:,.0f}'
            }),
            width='stretch'
        )
    
    with tab3:
        st.subheader("Highest Paid Employees by Department")
        st.dataframe(
            highest_paid.style.format({'Salary': '${:,.0f}'}),
            width='stretch'
        )
    
    with tab4:
        st.subheader("Filtered Employee Data")
        st.dataframe(
            filtered_df.style.format({'Salary': '${:,.0f}'}),
            width='stretch'
        )
    
    # Export Section
    st.divider()
    st.header("💾 Export Data")
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        if st.button("📊 Export Department Summary"):
            csv = dept_summary.to_csv(index=False)
            st.download_button(
                label="Download CSV",
                data=csv,
                file_name="department_summary.csv",
                mime="text/csv"
            )
    
    with col2:
        if st.button("💼 Export Job Analysis"):
            csv = job_summary.to_csv(index=False)
            st.download_button(
                label="Download CSV",
                data=csv,
                file_name="job_analysis.csv",
                mime="text/csv"
            )
    
    with col3:
        if st.button("📈 Export Filtered Data"):
            csv = filtered_df.to_csv(index=False)
            st.download_button(
                label="Download CSV",
                data=csv,
                file_name="filtered_employees.csv",
                mime="text/csv"
            )

if __name__ == "__main__":
    main()