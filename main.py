import streamlit as st

# Assumptions for RADR
risk_free_rate_radr = 0.04
market_risk_premium_radr = 0.065
beta = 1.2

# Assumptions for CEQ
risk_free_rate_ceq = 0.04
market_risk_premium_ceq = 0.065
initial_market_std_dev = 0.145
final_market_std_dev = 0.3242
correlation = 0.195

def radr_valuation(revenues):
    riskless_cash_flow = revenues[0]  # Assume Year 0 revenue as riskless cash flow
    risky_cash_flows = revenues[1:]  # Assume all other revenues are risky cash flows
    
    total_risky_cash_flows = sum(risky_cash_flows)
    radr = risk_free_rate_radr + beta * market_risk_premium_radr
    present_value = riskless_cash_flow / (1 + risk_free_rate_radr) + total_risky_cash_flows / (1 + radr)
    
    return present_value

def ceq_valuation(revenues):
    total_cash_flows = sum(revenues)
    market_std_dev = initial_market_std_dev + (final_market_std_dev - initial_market_std_dev) / len(revenues)
    
    ceq = total_cash_flows / ((risk_free_rate_ceq - market_risk_premium_ceq * correlation) / market_std_dev)
    return ceq

# Dictionary to hold P/E ratio for different categories
pe_ratios = {
    "fintech": 13,
    "biotech": 15,
    "software": 7,
    "commerce": 5,
}

categories = ["fintech", "biotech", "software", "commerce"]

def pe_ratio_valuation(last_revenue, category):
    pe_ratio = pe_ratios.get(category, 10)  # Default to 15 if category not found
    valuation = last_revenue * pe_ratio
    return valuation

def dcf_valuation(revenues, discount_rate=0.1, terminal_growth_rate=0.05):
    terminal_year = len(revenues) + 10
    terminal_revenue = revenues[-1] * (1 + terminal_growth_rate)
    
    dcf_value = 0
    for i, revenue in enumerate(revenues, start=1):
        dcf_value += revenue / ((1 + discount_rate) ** i)
    dcf_value += terminal_revenue / ((1 + discount_rate) ** terminal_year)
    
    return dcf_value

st.title("🎓 Startup Valuation App")
st.markdown("This web application serves the purpose of determining your startup's valuation.")
st.header("Valuation Methods")
st.write("""
1. **P/E Ratio Valuation:** This method calculates the valuation based on the P/E ratio for the selected category.
2. **Discounted Cash Flow (DCF) Valuation:** This method calculates the present value of future cash flows, discounted back to the present.
3. **RADR (Risk-Adjusted Discount Rate) Valuation:** This method adjusts the discount rate based on the riskiness of the cash flows.
4. **CEQ (Cash-Flow-to-Equity) Valuation:** This method calculates the present value of cash flows relative to equity.
""")

category = st.sidebar.selectbox("Select Category", categories)

st.sidebar.markdown("---")

years_existed = st.sidebar.slider("Years of Company Existence", min_value=1, max_value=10, value=1, step=1)

st.sidebar.markdown("---")

st.sidebar.info("""
This web application serves the purpose of determining your startup's valuation using various methods.
""")

st.sidebar.image("cover-photo.jpeg", use_column_width=True)

revenues = []
for i in range(years_existed):
    revenue = st.number_input(f"Annual Revenue for Year {i+1}")
    revenues.append(revenue)

if st.button("Calculate Valuation"):
    st.subheader("Valuation Results")
    pe_value = pe_ratio_valuation(revenues[len(revenues)-1], category)
    dcf_value = dcf_valuation(revenues)
    st.write("**P/E Ratio Valuation:**", pe_value)
    st.write("**DCF Valuation:**", dcf_value)
    radr_value = radr_valuation(revenues)
    ceq_value = ceq_valuation(revenues)
    st.write("**RADR Valuation:**", radr_value)
    st.write("**CEQ Valuation:**", ceq_value)

st.info("Remember, this app is for informational purposes only and shouldn't be used for making investment decisions.")