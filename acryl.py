import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import altair as alt

# Set page configuration and styling
st.set_page_config(
    page_title="Acryl Competitor ARR Estimator",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Force explicit color scheme that works in both modes
primary_color = "#4F46E5"  # Bright indigo that works in both modes
card_background = "#FFFFFF"  # White background for cards
dark_card_background = "#262730"  # Dark background for cards in dark mode
text_color_light = "#F9FAFB"  # Light text for dark backgrounds
text_color_dark = "#111827"  # Dark text for light backgrounds
border_color = "#E5E7EB"  # Light border
dark_border_color = "#4B5563"  # Dark border

# Company colors that are visible in both themes
collibra_color = "#818CF8"  # Bright indigo
alation_color = "#38BDF8"  # Bright sky blue

# Scenario colors that work in both themes
bear_color = "#F87171"  # Bright red
base_color = "#4ADE80"  # Bright green
bull_color = "#60A5FA"  # Bright blue

# Custom CSS with explicit backgrounds for both themes
st.markdown("""
<style>
    /* Light mode (default) */
    .main-header {
        font-size: 2.5rem;
        color: #4F46E5;
        margin-bottom: 1.5rem;
        text-align: center;
        padding: 1rem 0;
        border-bottom: 2px solid #E5E7EB;
    }
    .section-header {
        color: #4F46E5;
        padding-top: 1rem;
        padding-bottom: 0.5rem;
        border-bottom: 1px solid #E5E7EB;
        margin-bottom: 1rem;
    }
    .company-card {
        background-color: #FFFFFF;
        padding: 1.5rem;
        border-radius: 0.5rem;
        margin-bottom: 1rem;
        box-shadow: 0 1px 3px rgba(0,0,0,0.12), 0 1px 2px rgba(0,0,0,0.24);
    }
    .chart-container {
        background-color: #FFFFFF;
        padding: 1rem;
        border-radius: 0.5rem;
        margin-bottom: 1.5rem;
        box-shadow: 0 1px 3px rgba(0,0,0,0.12), 0 1px 2px rgba(0,0,0,0.24);
    }
    .metrics-container {
        display: flex;
        justify-content: space-between;
        flex-wrap: wrap;
        margin-bottom: 1rem;
    }
    .metric-card {
        background-color: #FFFFFF;
        padding: 1rem;
        border-radius: 0.5rem;
        margin-bottom: 1rem;
        box-shadow: 0 1px 3px rgba(0,0,0,0.12), 0 1px 2px rgba(0,0,0,0.24);
        text-align: center;
    }
    .footer {
        text-align: center;
        padding: 1.5rem 0;
        border-top: 1px solid #E5E7EB;
        margin-top: 2rem;
        font-size: 0.875rem;
    }
    .scenario-label {
        font-weight: bold;
        margin-bottom: 0.25rem;
    }
    .dataframe-container {
        border-radius: 0.5rem;
        overflow: hidden;
        margin-bottom: 1rem;
    }
    .info-box {
        background-color: #EFF6FF;
        padding: 1rem;
        border-radius: 0.5rem;
        margin-bottom: 2rem;
        border-left: 4px solid #4F46E5;
    }
    
    /* Dark mode overrides */
    [data-testid="stApp"][data-theme="dark"] .main-header {
        border-bottom-color: #4B5563;
    }
    [data-testid="stApp"][data-theme="dark"] .section-header {
        border-bottom-color: #4B5563;
    }
    [data-testid="stApp"][data-theme="dark"] .company-card {
        background-color: #262730;
        box-shadow: 0 1px 3px rgba(0,0,0,0.24), 0 1px 2px rgba(0,0,0,0.36);
    }
    [data-testid="stApp"][data-theme="dark"] .chart-container {
        background-color: #262730;
        box-shadow: 0 1px 3px rgba(0,0,0,0.24), 0 1px 2px rgba(0,0,0,0.36);
    }
    [data-testid="stApp"][data-theme="dark"] .metric-card {
        background-color: #262730;
        box-shadow: 0 1px 3px rgba(0,0,0,0.24), 0 1px 2px rgba(0,0,0,0.36);
    }
    [data-testid="stApp"][data-theme="dark"] .footer {
        border-top-color: #4B5563;
    }
    [data-testid="stApp"][data-theme="dark"] .info-box {
        background-color: #1E293B;
        border-left-color: #818CF8;
    }
    
    /* Ensure text is visible in both modes */
    [data-testid="stApp"][data-theme="dark"] .company-card h3,
    [data-testid="stApp"][data-theme="dark"] .company-card p,
    [data-testid="stApp"][data-theme="dark"] .company-card div,
    [data-testid="stApp"][data-theme="dark"] .chart-container h3,
    [data-testid="stApp"][data-theme="dark"] .chart-container p,
    [data-testid="stApp"][data-theme="dark"] .info-box p {
        color: #F9FAFB !important;
    }
    
    /* Make metric cards more visible in dark mode */
    [data-testid="stApp"][data-theme="dark"] div[data-testid="metric-container"] {
        background-color: #262730;
        padding: 1rem;
        border-radius: 0.5rem;
        box-shadow: 0 1px 3px rgba(0,0,0,0.24), 0 1px 2px rgba(0,0,0,0.36);
    }
    
    /* Handle dataframe styling */
    [data-testid="stApp"][data-theme="dark"] .dataframe {
        color: #F9FAFB;
    }
</style>
""", unsafe_allow_html=True)

# App header
st.markdown('<h1 class="main-header">Data Analytics Company ARR Estimator</h1>', unsafe_allow_html=True)

# App description with theme-compatible styling
st.markdown("""
<div class="info-box">
    <p style="margin: 0;">This interactive dashboard estimates the Annual Recurring Revenue (ARR) for <b>Collibra</b> and <b>Alation</b>
    based on their number of Full-Time Equivalent (FTE) employees and configurable revenue per employee ratios.
    Use the controls in the sidebar to adjust scenarios and view the impact on estimated ARR.</p>
</div>
""", unsafe_allow_html=True)

# Sidebar for controls
with st.sidebar:
    st.markdown(f'<h2 style="color: {primary_color}; text-align: center; padding-bottom: 0.5rem;">Control Panel</h2>', unsafe_allow_html=True)

    # Company data with bright colors that work in both themes
    companies = {
        "Collibra": {"fte": 974, "color": collibra_color},
        "Alation": {"fte": 612, "color": alation_color}
    }

    # Default ARR per FTE scenarios
    default_scenarios = {
        "bear": 100000,   # $100K per FTE in bear case
        "base": 150000,   # $150K per FTE in base case
        "bull": 200000    # $200K per FTE in bull case
    }

    # Create scenario sliders with bright, visible colors
    st.markdown(f'<h3 style="color: {primary_color}; font-size: 1.2rem; margin-bottom: 1rem;">ARR per FTE Scenarios</h3>', unsafe_allow_html=True)
    
    st.markdown('<p class="scenario-label" style="color: #F87171;">Bear Case (Conservative)</p>', unsafe_allow_html=True)
    bear_case = st.slider("", 50000, 200000, default_scenarios["bear"], step=10000, format="$%d", key="bear_slider")
    
    st.markdown('<p class="scenario-label" style="color: #4ADE80;">Base Case (Expected)</p>', unsafe_allow_html=True)
    base_case = st.slider("", 100000, 250000, default_scenarios["base"], step=10000, format="$%d", key="base_slider")
    
    st.markdown('<p class="scenario-label" style="color: #60A5FA;">Bull Case (Optimistic)</p>', unsafe_allow_html=True)
    bull_case = st.slider("", 150000, 300000, default_scenarios["bull"], step=10000, format="$%d", key="bull_slider")
    
    # Add some visual separation
    st.markdown("<hr>", unsafe_allow_html=True)
    
    # Custom ARR per FTE for individual company tuning
    st.markdown('<h3 style="color: #4F46E5; font-size: 1.2rem; margin-bottom: 1rem;">Company-Specific Tuning</h3>', unsafe_allow_html=True)
    
    st.markdown(f'<p class="scenario-label" style="color: {collibra_color};">Collibra Custom ARR per FTE</p>', unsafe_allow_html=True)
    custom_collibra = st.slider("", 50000, 300000, base_case, step=10000, format="$%d", key="collibra_slider")
    
    st.markdown(f'<p class="scenario-label" style="color: {alation_color};">Alation Custom ARR per FTE</p>', unsafe_allow_html=True)
    custom_alation = st.slider("", 50000, 300000, base_case, step=10000, format="$%d", key="alation_slider")

# Calculate ARR for each scenario
scenarios = {
    "Bear": {"value": bear_case, "color": bear_color},
    "Base": {"value": base_case, "color": base_color},
    "Bull": {"value": bull_case, "color": bull_color}
}

results = {}

for company, data in companies.items():
    results[company] = {
        scenario: data["fte"] * scenarios[scenario]["value"] for scenario in scenarios
    }
    # Add custom scenario
    if company == "Collibra":
        results[company]["Custom"] = data["fte"] * custom_collibra
    else:
        results[company]["Custom"] = data["fte"] * custom_alation

# Convert results to DataFrame for easier visualization
df_results = pd.DataFrame(results)

# Create tabs for organization
tab_summary, tab_detailed, tab_sensitivity = st.tabs(["📊 Summary Dashboard", "🔍 Detailed Analysis", "📈 Sensitivity Analysis"])

with tab_summary:
    # Company metrics in the top row
    st.markdown('<h2 class="section-header">Company Information</h2>', unsafe_allow_html=True)
    
    col1, col2 = st.columns(2)
    
    with col1:
        # For dark mode, adjust text color for card values
        card_text_color = text_color_dark if st.get_option("theme.base") == "dark" else "black"
        card_value_bg = card_background if st.get_option("theme.base") == "dark" else "white"

        st.markdown(f"""
        <div class="company-card" style="border-left: 4px solid {collibra_color}">
            <h3 style="color: {collibra_color}; margin-top: 0;">Collibra</h3>
            <p style="color: {card_text_color};"><b>FTE Count:</b> {companies['Collibra']['fte']:,}</p>
            <div style="display: flex; justify-content: space-between; margin-top: 1rem;">
                <div style="text-align: center; padding: 0.5rem; background-color: {card_value_bg}; border-radius: 0.25rem; width: 30%;">
                    <div style="color: {bear_color}; font-weight: bold;">Bear</div>
                    <div style="color: {card_text_color};">${results['Collibra']['Bear']/1000000:.1f}M</div>
                </div>
                <div style="text-align: center; padding: 0.5rem; background-color: {card_value_bg}; border-radius: 0.25rem; width: 30%;">
                    <div style="color: {base_color}; font-weight: bold;">Base</div>
                    <div style="color: {card_text_color};">${results['Collibra']['Base']/1000000:.1f}M</div>
                </div>
                <div style="text-align: center; padding: 0.5rem; background-color: {card_value_bg}; border-radius: 0.25rem; width: 30%;">
                    <div style="color: {bull_color}; font-weight: bold;">Bull</div>
                    <div style="color: {card_text_color};">${results['Collibra']['Bull']/1000000:.1f}M</div>
                </div>
            </div>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        st.markdown(f"""
        <div class="company-card" style="border-left: 4px solid {alation_color}">
            <h3 style="color: {alation_color}; margin-top: 0;">Alation</h3>
            <p style="color: {card_text_color};"><b>FTE Count:</b> {companies['Alation']['fte']:,}</p>
            <div style="display: flex; justify-content: space-between; margin-top: 1rem;">
                <div style="text-align: center; padding: 0.5rem; background-color: {card_value_bg}; border-radius: 0.25rem; width: 30%;">
                    <div style="color: {bear_color}; font-weight: bold;">Bear</div>
                    <div style="color: {card_text_color};">${results['Alation']['Bear']/1000000:.1f}M</div>
                </div>
                <div style="text-align: center; padding: 0.5rem; background-color: {card_value_bg}; border-radius: 0.25rem; width: 30%;">
                    <div style="color: {base_color}; font-weight: bold;">Base</div>
                    <div style="color: {card_text_color};">${results['Alation']['Base']/1000000:.1f}M</div>
                </div>
                <div style="text-align: center; padding: 0.5rem; background-color: {card_value_bg}; border-radius: 0.25rem; width: 30%;">
                    <div style="color: {bull_color}; font-weight: bold;">Bull</div>
                    <div style="color: {card_text_color};">${results['Alation']['Bull']/1000000:.1f}M</div>
                </div>
            </div>
        </div>
        """, unsafe_allow_html=True)
    
    # Summary metrics
    st.markdown('<h2 class="section-header">ARR Summary</h2>', unsafe_allow_html=True)
    
    # Calculate the differences
    collibra_diff = (results["Collibra"]["Bull"] - results["Collibra"]["Bear"]) / 1000000
    alation_diff = (results["Alation"]["Bull"] - results["Alation"]["Bear"]) / 1000000
    
    col1, col2, col3, col4 = st.columns(4)
    
    custom_diff = {
        "Collibra": (results["Collibra"]["Custom"] - results["Collibra"]["Base"]) / 1000000,
        "Alation": (results["Alation"]["Custom"] - results["Alation"]["Base"]) / 1000000
    }
    
    with col1:
        st.metric(
            "Collibra Base ARR", 
            f"${results['Collibra']['Base']/1000000:.1f}M",
            f"{custom_diff['Collibra']:.1f}M in Custom"
        )
    
    with col2:
        st.metric(
            "Alation Base ARR", 
            f"${results['Alation']['Base']/1000000:.1f}M",
            f"{custom_diff['Alation']:.1f}M in Custom"
        )
    
    with col3:
        st.metric(
            "Collibra ARR Range", 
            f"${collibra_diff:.1f}M",
            f"Bear to Bull spread"
        )
    
    with col4:
        st.metric(
            "Alation ARR Range", 
            f"${alation_diff:.1f}M",
            f"Bear to Bull spread"
        )
    
    # Main chart
    st.markdown('<h2 class="section-header">Scenario Comparison</h2>', unsafe_allow_html=True)
    
    st.markdown('<div class="chart-container">', unsafe_allow_html=True)
    
    # Prepare data for Altair chart in a more efficient way
    scenarios_list = ["Bear", "Base", "Bull", "Custom"]
    companies_list = list(companies.keys())
    
    chart_data = []
    for company in companies_list:
        for scenario in scenarios_list:
            chart_data.append({
                "Company": company,
                "Scenario": scenario,
                "ARR (Millions)": results[company][scenario] / 1000000
            })
    
    chart_df = pd.DataFrame(chart_data)
    
    # Create grouped bar chart
    chart = alt.Chart(chart_df).mark_bar().encode(
        x=alt.X('Company:N'),
        y=alt.Y('ARR (Millions):Q', title='ARR ($ Millions)'),
        color=alt.Color('Scenario:N', scale=alt.Scale(
            domain=scenarios_list,
            range=[bear_color, base_color, bull_color, '#9CA3AF']
        )),
        column=alt.Column('Scenario:N'),
        tooltip=['Company', 'Scenario', 'ARR (Millions)']
    ).properties(width=120)
    
    # Explicitly set a white background for charts to ensure visibility
    chart = chart.configure_view(
        strokeWidth=0,
        fill='white'  # Set chart background to white for best visibility
    ).configure_axis(
        labelColor='#111827',  # Dark text for labels
        titleColor='#111827'   # Dark text for titles
    )
    
    st.altair_chart(chart, use_container_width=True)
    st.markdown('</div>', unsafe_allow_html=True)

with tab_detailed:
    # Detailed data analysis
    st.markdown('<h2 class="section-header">Detailed ARR Estimates</h2>', unsafe_allow_html=True)
    
    col1, col2 = st.columns([2, 3])
    
    with col1:
        # Company FTE Information
        st.markdown('<div class="chart-container">', unsafe_allow_html=True)
        st.subheader("Company Information")
        company_df = pd.DataFrame({
            "Company": companies.keys(),
            "FTE Count": [data["fte"] for data in companies.values()],
            "Relative Size": ["100%", f"{companies['Alation']['fte']/companies['Collibra']['fte']*100:.1f}%"]
        })
        st.markdown('<div class="dataframe-container">', unsafe_allow_html=True)
        st.dataframe(company_df, use_container_width=True, hide_index=True)
        st.markdown('</div>', unsafe_allow_html=True)
        st.markdown('</div>', unsafe_allow_html=True)
        
        # Display ARR Estimates Table
        st.markdown('<div class="chart-container">', unsafe_allow_html=True)
        st.subheader("ARR Estimates ($ millions)")
        # Convert to millions and round to 1 decimal place
        display_df = df_results / 1000000
        display_df = display_df.round(1)
        # Transpose for better presentation
        display_df_t = display_df.T
        display_df_t.index.name = "Company"
        display_df_t.reset_index(inplace=True)
        st.markdown('<div class="dataframe-container">', unsafe_allow_html=True)
        st.dataframe(display_df_t, use_container_width=True, hide_index=True)
        st.markdown('</div>', unsafe_allow_html=True)
        st.markdown('</div>', unsafe_allow_html=True)
    
    with col2:
        # ARR per FTE comparison
        st.markdown('<div class="chart-container">', unsafe_allow_html=True)
        st.subheader("ARR per FTE Comparison")
        
        ratio_data = pd.DataFrame({
            "Scenario": ["Bear", "Base", "Bull", "Collibra Custom", "Alation Custom"],
            "ARR per FTE ($K)": [
                bear_case / 1000,
                base_case / 1000,
                bull_case / 1000,
                custom_collibra / 1000,
                custom_alation / 1000
            ]
        })
        
        bar_colors = [
            bear_color,
            base_color, 
            bull_color,
            collibra_color,
            alation_color
        ]
        
        ratio_chart = alt.Chart(ratio_data).mark_bar().encode(
            x=alt.X('Scenario:N', title='Scenario', sort=None),
            y=alt.Y('ARR per FTE ($K):Q', title='ARR per FTE ($K)'),
            color=alt.Color('Scenario:N', scale=alt.Scale(
                domain=ratio_data['Scenario'].tolist(),
                range=bar_colors
            )),
            tooltip=['Scenario', 'ARR per FTE ($K)']
        ).properties(height=300)
        
        st.altair_chart(ratio_chart, use_container_width=True)
        st.markdown('</div>', unsafe_allow_html=True)
        
        # Key insights
        st.markdown('<div class="chart-container">', unsafe_allow_html=True)
        st.subheader("Key Insights")
        
        st.markdown(f"""
        <ul>
            <li><b>Employee Count Difference:</b> Collibra has {companies["Collibra"]["fte"] - companies["Alation"]["fte"]} more employees than Alation ({(companies["Collibra"]["fte"] / companies["Alation"]["fte"] - 1) * 100:.1f}% larger)</li>
            <li><b>Collibra Range:</b> ${results["Collibra"]["Bear"]/1000000:.1f}M to ${results["Collibra"]["Bull"]/1000000:.1f}M (${collibra_diff:.1f}M difference)</li>
            <li><b>Alation Range:</b> ${results["Alation"]["Bear"]/1000000:.1f}M to ${results["Alation"]["Bull"]/1000000:.1f}M (${alation_diff:.1f}M difference)</li>
            <li><b>Custom Scenarios:</b> With custom settings, Collibra ARR is ${results["Collibra"]["Custom"]/1000000:.1f}M and Alation ARR is ${results["Alation"]["Custom"]/1000000:.1f}M</li>
        </ul>
        """, unsafe_allow_html=True)
        st.markdown('</div>', unsafe_allow_html=True)

with tab_sensitivity:
    # Sensitivity analysis
    st.markdown('<h2 class="section-header">Sensitivity Analysis</h2>', unsafe_allow_html=True)
    
    st.markdown("""
    <div class="info-box">
        <p style="margin: 0;">This analysis shows how ARR estimates change as ARR per FTE values vary. The vertical lines represent the Bear (red), Base (green), and Bull (blue) case scenarios.</p>
    </div>
    """, unsafe_allow_html=True)
    
    st.markdown('<div class="chart-container">', unsafe_allow_html=True)
    
    # Create a range of ARR per FTE values
    arr_per_fte_range = np.arange(50000, 300000, 10000)
    
    # Calculate ARR for each company across the range
    collibra_arr = [companies["Collibra"]["fte"] * arr for arr in arr_per_fte_range]
    alation_arr = [companies["Alation"]["fte"] * arr for arr in arr_per_fte_range]
    
    # Create a dataframe for the line chart
    sensitivity_df = pd.DataFrame({
        'ARR per FTE ($K)': arr_per_fte_range / 1000,
        'Collibra ARR ($M)': [arr / 1000000 for arr in collibra_arr],
        'Alation ARR ($M)': [arr / 1000000 for arr in alation_arr]
    })
    
    # Melt the dataframe for Altair
    sensitivity_melted = pd.melt(
        sensitivity_df, 
        id_vars=['ARR per FTE ($K)'], 
        value_vars=['Collibra ARR ($M)', 'Alation ARR ($M)'],
        var_name='Company', 
        value_name='ARR ($M)'
    )
    
    # Create the line chart
    line_chart = alt.Chart(sensitivity_melted).mark_line(
        strokeWidth=3
    ).encode(
        x=alt.X('ARR per FTE ($K):Q', title='ARR per FTE ($K)'),
        y=alt.Y('ARR ($M):Q', title='ARR ($ Millions)'),
        color=alt.Color('Company:N', scale=alt.Scale(
            domain=['Collibra ARR ($M)', 'Alation ARR ($M)'],
            range=[collibra_color, alation_color]
        )),
        tooltip=['Company', 'ARR per FTE ($K)', 'ARR ($M)']
    ).properties(
        height=500
    )
    
    # Add vertical lines for the scenario values
    bear_line = alt.Chart(pd.DataFrame({'x': [bear_case / 1000]})).mark_rule(
        color=bear_color, strokeDash=[5, 5], strokeWidth=2
    ).encode(x='x:Q')
    
    base_line = alt.Chart(pd.DataFrame({'x': [base_case / 1000]})).mark_rule(
        color=base_color, strokeDash=[5, 5], strokeWidth=2
    ).encode(x='x:Q')
    
    bull_line = alt.Chart(pd.DataFrame({'x': [bull_case / 1000]})).mark_rule(
        color=bull_color, strokeDash=[5, 5], strokeWidth=2
    ).encode(x='x:Q')
    
    # Add annotations for the scenario lines
    bear_text = alt.Chart(pd.DataFrame({'x': [bear_case / 1000], 'y': [sensitivity_df['Collibra ARR ($M)'].max() * 0.9]})).mark_text(
        align='left', baseline='middle', dx=5, color=bear_color, fontWeight='bold'
    ).encode(x='x:Q', y='y:Q', text=alt.value('Bear Case'))
    
    base_text = alt.Chart(pd.DataFrame({'x': [base_case / 1000], 'y': [sensitivity_df['Collibra ARR ($M)'].max() * 0.95]})).mark_text(
        align='left', baseline='middle', dx=5, color=base_color, fontWeight='bold'
    ).encode(x='x:Q', y='y:Q', text=alt.value('Base Case'))
    
    bull_text = alt.Chart(pd.DataFrame({'x': [bull_case / 1000], 'y': [sensitivity_df['Collibra ARR ($M)'].max()]})).mark_text(
        align='left', baseline='middle', dx=5, color=bull_color, fontWeight='bold'
    ).encode(x='x:Q', y='y:Q', text=alt.value('Bull Case'))
    
    # Display the chart with scenario lines and annotations
    final_chart = line_chart + bear_line + base_line + bull_line + bear_text + base_text + bull_text
    st.altair_chart(final_chart, use_container_width=True)
    st.markdown('</div>', unsafe_allow_html=True)
    
    # Sensitivity table
    st.markdown('<div class="chart-container">', unsafe_allow_html=True)
    st.subheader("Sensitivity Table: ARR ($ millions) at Selected ARR per FTE Values")
    
    # Create a more detailed sensitivity table for key values
    key_values = [100, 125, 150, 175, 200, 225, 250]
    sens_table_data = []
    
    for val in key_values:
        val_k = val * 1000  # Convert to actual value (e.g., 100K → 100,000)
        sens_table_data.append({
            "ARR per FTE": f"${val}K",
            "Collibra ARR": f"${companies['Collibra']['fte'] * val_k / 1000000:.1f}M",
            "Alation ARR": f"${companies['Alation']['fte'] * val_k / 1000000:.1f}M",
            "Difference": f"${(companies['Collibra']['fte'] - companies['Alation']['fte']) * val_k / 1000000:.1f}M"
        })
    
    sens_table = pd.DataFrame(sens_table_data)
    st.markdown('<div class="dataframe-container">', unsafe_allow_html=True)
    st.dataframe(sens_table, use_container_width=True, hide_index=True)
    st.markdown('</div>', unsafe_allow_html=True)
    st.markdown('</div>', unsafe_allow_html=True)

# Footer with instructions
st.markdown('<div class="footer">', unsafe_allow_html=True)
st.markdown("""
### How to Use This Tool:

1. Use the sliders in the sidebar to adjust the ARR per FTE values for different scenarios
2. Fine-tune company-specific ARR per FTE values using the "Company-Specific Tuning" sliders
3. Navigate between tabs to view different analyses:
   - **Summary Dashboard:** Quick overview of ARR estimates
   - **Detailed Analysis:** In-depth data tables and charts
   - **Sensitivity Analysis:** Examine how ARR changes with different ARR per FTE values

*Note: All calculations are based on the provided FTE counts (Collibra: 974, Alation: 612) and the ARR per FTE ratios.*
""")
st.markdown('</div>', unsafe_allow_html=True) 
