import streamlit as st
import yfinance as yf
import plotly.graph_objs as go
from plotly.subplots import make_subplots
from crew_simple import run_analysis
import json

# Page Configuration
st.set_page_config(
    layout="wide", 
    page_title="FinWisely - AI Financial Advisor",
    page_icon="💰",
    initial_sidebar_state="expanded"
)

# Custom CSS for Modern Styling
def add_custom_css():
    st.markdown("""
        <style>
            /* Main Background */
            .stApp {
                background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            }
            
            /* Sidebar Styling */
            [data-testid="stSidebar"] {
                background: linear-gradient(180deg, #1e3c72 0%, #2a5298 100%);
            }
            
            [data-testid="stSidebar"] .stMarkdown {
                color: white;
            }
            
            /* Header Styling */
            .main-header {
                background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
                padding: 2rem;
                border-radius: 15px;
                text-align: center;
                margin-bottom: 2rem;
                box-shadow: 0 8px 32px rgba(0, 0, 0, 0.1);
            }
            
            .main-title {
                font-size: 3rem;
                font-weight: 800;
                color: #F5F5DC;
                margin: 0;
                text-shadow: 2px 2px 4px rgba(0, 0, 0, 0.2);
            }
            
            .main-subtitle {
                font-size: 1.2rem;
                color: #f0f0f0;
                margin-top: 0.5rem;
            }
            
            /* Card Styling */
            .info-card {
                background: rgba(255, 255, 255, 0.95);
                border-radius: 15px;
                padding: 2rem;
                margin: 1rem 0;
                box-shadow: 0 8px 32px rgba(0, 0, 0, 0.1);
                backdrop-filter: blur(10px);
                border: 1px solid rgba(255, 255, 255, 0.2);
            }
            
            .analysis-card {
                background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
                border-radius: 15px;
                padding: 2rem;
                margin: 1rem 0;
                box-shadow: 0 8px 32px rgba(0, 0, 0, 0.2);
                color: white;
            }
            
            .report-card {
                background: white;
                border-radius: 15px;
                padding: 2rem;
                margin: 1rem 0;
                box-shadow: 0 8px 32px rgba(0, 0, 0, 0.1);
                border-left: 5px solid #667eea;
            }
            
            /* Button Styling */
            .stButton>button {
                background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
                color: white;
                border: none;
                border-radius: 10px;
                padding: 0.75rem 2rem;
                font-size: 1.1rem;
                font-weight: 600;
                transition: all 0.3s ease;
                box-shadow: 0 4px 15px rgba(102, 126, 234, 0.4);
            }
            
            .stButton>button:hover {
                transform: translateY(-2px);
                box-shadow: 0 6px 20px rgba(102, 126, 234, 0.6);
            }
            
            /* Input Styling */
            .stTextInput>div>div>input {
                border-radius: 10px;
                border: 2px solid #667eea;
                padding: 0.75rem;
            }
            
            .stSelectbox>div>div>select {
                border-radius: 10px;
                border: 2px solid #667eea;
            }
            
            /* Metric Cards */
            .metric-card {
                background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
                border-radius: 15px;
                padding: 1.5rem;
                text-align: center;
                color: white;
                box-shadow: 0 4px 15px rgba(0, 0, 0, 0.1);
            }
            
            .metric-value {
                font-size: 2.5rem;
                font-weight: 700;
                margin: 0.5rem 0;
            }
            
            .metric-label {
                font-size: 1rem;
                opacity: 0.9;
            }
            
            /* Success/Error Messages */
            .stSuccess {
                background: linear-gradient(135deg, #11998e 0%, #38ef7d 100%);
                color: white;
                border-radius: 10px;
                padding: 1rem;
            }
            
            .stError {
                background: linear-gradient(135deg, #eb3349 0%, #f45c43 100%);
                color: white;
                border-radius: 10px;
                padding: 1rem;
            }
            
            /* Spinner */
            .stSpinner > div {
                border-top-color: #667eea !important;
            }
            
            /* Section Headers */
            .section-header {
                font-size: 2rem;
                font-weight: 700;
                color: white;
                margin: 2rem 0 1rem 0;
                padding-bottom: 0.5rem;
                border-bottom: 3px solid white;
            }
        </style>
    """, unsafe_allow_html=True)
# Main Function
def main():
    add_custom_css()
    
    # Header
    st.markdown("""
        <div class="main-header">
            <h1 class="main-title">💰 FinWisely</h1>
            <p class="main-subtitle">Your AI-Powered Financial Advisor using Multi-Agent Systems</p>
        </div>
    """, unsafe_allow_html=True)
    
    # Welcome Card
    st.markdown("""
        <div class="info-card">
            <h2 style="color: #667eea; margin-top: 0;">🚀 Welcome to FinWisely!</h2>
            <p style="font-size: 1.1rem; line-height: 1.8; color: #333;">
                Revolutionize your financial journey with cutting-edge AI technology. FinWisely combines 
                <strong>technical analysis</strong>, <strong>fundamental research</strong>, and 
                <strong>sentiment analysis</strong> to provide you with comprehensive investment insights.
            </p>
            <p style="font-size: 1rem; color: #666; margin-top: 1rem;">
                ✨ Powered by Google Gemini AI | 📈 Real-time Market Data | 🧠 Smart Analytics
            </p>
        </div>
    """, unsafe_allow_html=True)
    
    # Sidebar Navigation
    st.sidebar.markdown("<h2 style='color: white; text-align: center;'>🧭 Navigation</h2>", unsafe_allow_html=True)
    options = st.sidebar.radio(
        "",
        ["📈 Stock Analysis", "📚 Financial Literacy", "💳 Budgeting"],
        label_visibility="collapsed"
    )

    if options == "📈 Stock Analysis":
        stock_analysis_section()
    elif options == "📚 Financial Literacy":
        financial_literacy_section()
    elif options == "💳 Budgeting":
        budgeting_section()

def stock_analysis_section():
    st.markdown('<h2 class="section-header">📈 AI-Powered Stock Analysis</h2>', unsafe_allow_html=True)
    
    # Sidebar Inputs
    st.sidebar.markdown("<h3 style='color: white;'>⚙️ Analysis Settings</h3>", unsafe_allow_html=True)
    stock_symbol = st.sidebar.text_input("🎯 Stock Symbol", value="AAPL", help="Enter stock ticker (e.g., AAPL, GOOGL, MSFT)")
    time_period = st.sidebar.selectbox("📅 Time Period", ['3mo', '6mo', '1y', '2y', '5y'], index=2)
    indicators = st.sidebar.multiselect(
        "📊 Technical Indicators", 
        ['Moving Averages', 'Volume', 'RSI', 'MACD'],
        default=['Volume']
    )
    
    analyze_button = st.sidebar.button("🚀 Analyze Stock", use_container_width=True)
    
    if analyze_button:
        # Fetch stock data
        with st.spinner(f"🔍 Fetching data for {stock_symbol}..."):
            stock_data = yf.Ticker(stock_symbol).history(period=time_period, interval="1d")
        
        if not stock_data.empty:
            # Display stock metrics
            col1, col2, col3, col4 = st.columns(4)
            
            current_price = stock_data['Close'].iloc[-1]
            price_change = stock_data['Close'].iloc[-1] - stock_data['Close'].iloc[0]
            price_change_pct = (price_change / stock_data['Close'].iloc[0]) * 100
            
            with col1:
                st.markdown(f"""
                    <div class="metric-card">
                        <div class="metric-label">Current Price</div>
                        <div class="metric-value">${current_price:.2f}</div>
                    </div>
                """, unsafe_allow_html=True)
            
            with col2:
                st.markdown(f"""
                    <div class="metric-card">
                        <div class="metric-label">Change</div>
                        <div class="metric-value">{price_change_pct:+.2f}%</div>
                    </div>
                """, unsafe_allow_html=True)
            
            with col3:
                st.markdown(f"""
                    <div class="metric-card">
                        <div class="metric-label">High</div>
                        <div class="metric-value">${stock_data['High'].max():.2f}</div>
                    </div>
                """, unsafe_allow_html=True)
            
            with col4:
                st.markdown(f"""
                    <div class="metric-card">
                        <div class="metric-label">Low</div>
                        <div class="metric-value">${stock_data['Low'].min():.2f}</div>
                    </div>
                """, unsafe_allow_html=True)
            
            # Chart
            st.plotly_chart(plot_stock_chart(stock_data, indicators), use_container_width=True)
            
            # AI Analysis
            analysis = perform_crew_analysis(stock_symbol)
            
            if analysis:
                st.markdown("""
                    <div class="analysis-card">
                        <h3 style="margin-top: 0;">✅ Analysis Complete!</h3>
                        <p>Our AI agents have successfully analyzed {stock_symbol} across multiple dimensions.</p>
                    </div>
                """.format(stock_symbol=stock_symbol), unsafe_allow_html=True)
        else:
            st.error("❌ Unable to fetch stock data. Please check the symbol and try again.")
        
# Fetch Stock Data
def get_stock_data(stock_symbol, period='1y'):
    try:
        return yf.download(stock_symbol, period=period)
    except Exception as e:
        st.error(f"Error fetching stock data: {e}")
        return None

# Plot Stock Chart
def plot_stock_chart(stock_data, indicators):
    if stock_data.empty or stock_data.isnull().any().any():
        return None

    fig = make_subplots(
        rows=2, cols=1,
        shared_xaxes=True,
        vertical_spacing=0.03,
        row_heights=[0.7, 0.3]
    )

    # Candlestick chart
    fig.add_trace(
        go.Candlestick(
            x=stock_data.index,
            open=stock_data['Open'],
            high=stock_data['High'],
            low=stock_data['Low'],
            close=stock_data['Close'],
            name="Price",
            increasing_line_color='#11998e',
            decreasing_line_color='#eb3349'
        ),
        row=1, col=1
    )

    # Volume chart
    if 'Volume' in indicators:
        colors = ['#11998e' if stock_data['Close'].iloc[i] >= stock_data['Open'].iloc[i] 
                  else '#eb3349' for i in range(len(stock_data))]
        fig.add_trace(
            go.Bar(
                x=stock_data.index,
                y=stock_data['Volume'],
                name="Volume",
                marker=dict(color=colors)
            ),
            row=2, col=1
        )

    # Update layout
    fig.update_layout(
        height=700,
        title=dict(
            text="Stock Price Chart",
            font=dict(size=24, color='white')
        ),
        xaxis_rangeslider_visible=False,
        plot_bgcolor='rgba(0,0,0,0.1)',
        paper_bgcolor='rgba(0,0,0,0)',
        font=dict(color='white', size=12),
        yaxis=dict(
            title="Price ($)",
            gridcolor='rgba(255,255,255,0.1)'
        ),
        yaxis2=dict(
            title="Volume",
            gridcolor='rgba(255,255,255,0.1)'
        ),
        xaxis=dict(
            gridcolor='rgba(255,255,255,0.1)'
        ),
        xaxis2=dict(
            gridcolor='rgba(255,255,255,0.1)'
        ),
        hovermode='x unified'
    )

    return fig


def perform_crew_analysis(stock_symbol):
    with st.spinner("🤖 AI Agents analyzing... This may take a moment..."):
        try:
            analysis_result = run_analysis(stock_symbol)
            st.write(analysis_result['report'])
            return analysis_result

        except Exception as e:
            st.error(f"⚠️ Analysis failed: {str(e)}")
            return None


def financial_literacy_section():
    st.markdown('<h2 class="section-header">📚 Financial Literacy Hub</h2>', unsafe_allow_html=True)
    
    st.markdown("""
        <div class="info-card">
            <h3 style="color: #667eea; margin-top: 0;">🎯 Learn & Grow</h3>
            <p style="font-size: 1.1rem; color: #333;">
                Master the fundamentals of personal finance with our comprehensive guides.
                Select a topic below to start your learning journey!
            </p>
        </div>
    """, unsafe_allow_html=True)

    topics = [
        ("💰 Budgeting Basics", "Learn how to create and maintain an effective budget"),
        ("📈 Investing 101", "Understand investment fundamentals and grow your wealth"),
        ("💳 Debt Management", "Strategies to manage and eliminate debt effectively"),
        ("🏛️ Retirement Planning", "Plan for a secure and comfortable retirement")
    ]
    
    cols = st.columns(2)
    for idx, (topic, desc) in enumerate(topics):
        with cols[idx % 2]:
            if st.button(topic, use_container_width=True, key=f"topic_{idx}"):
                st.markdown(f"""
                    <div class="info-card">
                        <h3 style="color: #667eea;">{topic}</h3>
                        <p style="font-size: 1.1rem; color: #333;">{desc}</p>
                    </div>
                """, unsafe_allow_html=True)

def budgeting_section():
    st.markdown('<h2 class="section-header">💳 Smart Budgeting Tool</h2>', unsafe_allow_html=True)
    
    st.markdown("""
        <div class="info-card">
            <h3 style="color: #667eea; margin-top: 0;">📊 Track Your Finances</h3>
            <p style="font-size: 1.1rem; color: #333;">
                Calculate your monthly savings and get personalized financial advice.
            </p>
        </div>
    """, unsafe_allow_html=True)
    
    col1, col2 = st.columns(2)
    
    with col1:
        income = st.number_input("💵 Monthly Income ($)", min_value=0.0, step=100.0, value=5000.0)
    
    with col2:
        expenses = st.number_input("💸 Monthly Expenses ($)", min_value=0.0, step=100.0, value=3000.0)

    if st.button("📊 Calculate Savings", use_container_width=True):
        savings = income - expenses
        savings_rate = (savings / income * 100) if income > 0 else 0
        
        if savings < 0:
            st.markdown(f"""
                <div class="info-card" style="border-left: 5px solid #eb3349;">
                    <h3 style="color: #eb3349;">⚠️ Budget Deficit</h3>
                    <p style="font-size: 1.5rem; color: #eb3349; font-weight: bold;">${-savings:.2f}</p>
                    <p style="color: #666;">Your expenses exceed your income. Consider reducing expenses or increasing income.</p>
                </div>
            """, unsafe_allow_html=True)
        else:
            st.markdown(f"""
                <div class="info-card" style="border-left: 5px solid #11998e;">
                    <h3 style="color: #11998e;">✅ Monthly Savings</h3>
                    <p style="font-size: 2rem; color: #11998e; font-weight: bold;">${savings:.2f}</p>
                    <p style="font-size: 1.2rem; color: #667eea;">Savings Rate: {savings_rate:.1f}%</p>
                </div>
            """, unsafe_allow_html=True)
            
            # Recommendations
            if savings_rate < 10:
                advice = "⚠️ Try to save at least 10-20% of your income for financial security."
                color = "#f45c43"
            elif savings_rate < 20:
                advice = "👍 Good start! Aim for 20% or more for optimal financial health."
                color = "#f39c12"
            else:
                advice = "🎉 Excellent! You're on track for strong financial health."
                color = "#11998e"
            
            st.markdown(f"""
                <div class="info-card" style="border-left: 5px solid {color};">
                    <p style="font-size: 1.1rem; color: #333;">{advice}</p>
                </div>
            """, unsafe_allow_html=True)

if __name__ == "__main__":
    main()
