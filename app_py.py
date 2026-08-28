import os
import streamlit as st
import pandas as pd
import plotly.express as px
from langchain_core.messages import HumanMessage, AIMessage, SystemMessage
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain_groq import ChatGroq
from langchain.agents import create_openai_tools_agent, AgentExecutor
from langchain_core.tools import tool
# 🔐 Simple password protection
def check_password():
    def password_entered():
        if st.session_state["password"] == "madhu2828":  # 🔑 Set your password here
            st.session_state["password_correct"] = True
        else:
            st.session_state["password_correct"] = False

    if "password_correct" not in st.session_state:
        st.text_input("🔐 Enter password", type="password", on_change=password_entered, key="password")
        st.stop()
    elif not st.session_state["password_correct"]:
        st.text_input("🔐 Enter password", type="password", on_change=password_entered, key="password")
        st.warning("❌ Incorrect password")
        st.stop()

check_password()



# Streamlit Setup
st.set_page_config(page_title="🤖 Agentic Sales Chatbot", page_icon="📈")
st.title("🤖 Agentic Sales Chatbot with Groq + LLaMA 3")

# Sidebar Prompt Suggestions
with st.sidebar:
    st.markdown("### 💡 Suggested Prompts")
    st.markdown("""
    - What are the top selling products?
    - Show me the least sold items
    - What is the monthly sales trend?
    - Show yearly sales trend
    - Give me the sales trend monthly and yearly
    - Show rejected orders
    - What are the reasons for rejection?
    - Show quantity discrepancies between ordered and delivered
    - List delayed deliveries
    - Compare billing and delivery statuses
    - Show billing currency distribution
    """)

# File & API Key
uploaded_file = st.file_uploader("📁 Upload your Sales CSV", type="csv")
groq_api_key = os.getenv("GROQ_API_KEY") or st.text_input("🔐 Enter your Groq API key", type="password")

if not groq_api_key:
    st.warning("Please provide your Groq API Key to proceed.")
    st.stop()
if uploaded_file is None:
    st.info("👆 Upload your sales CSV file to begin.")
    st.stop()

# Load Data
df = pd.read_csv(uploaded_file)
df.dropna(axis=1, how="all", inplace=True)
df.fillna({col: "Unknown" if df[col].dtype == "object" else 0 for col in df.columns}, inplace=True)

# ----- Tool Functions -----
@tool
def top_products(input: str = "") -> str:
    """Get top selling products"""
    top = df.groupby(["Material_Number", "ShortText_Item"])["Net_Value"].sum().reset_index()
    top = top.sort_values("Net_Value", ascending=False).head(10)
    st.dataframe(top)
    st.plotly_chart(px.bar(top, x="ShortText_Item", y="Net_Value", text="Net_Value", title="Top Selling Products"), use_container_width=True, key="top_products_chart")
    return f"🏆 Top selling product is {top.iloc[0]['ShortText_Item']} with ₹{top.iloc[0]['Net_Value']:,.2f}"

@tool
def low_products(input: str = "") -> str:
    """Get lowest selling products"""
    low = df.groupby(["Material_Number", "ShortText_Item"])["Net_Value"].sum().reset_index()
    low = low.sort_values("Net_Value").head(10)
    st.dataframe(low)
    st.plotly_chart(px.bar(low, x="ShortText_Item", y="Net_Value", text="Net_Value", title="Lowest Selling Products"), use_container_width=True, key="low_products_chart")

    return f"🔻 Lowest selling product is {low.iloc[0]['ShortText_Item']} with ₹{low.iloc[0]['Net_Value']:,.2f}"

@tool
def monthly_sales(input: str = "") -> str:
    """Monthly sales trend"""
    df["SaleOrder_Date"] = pd.to_datetime(df["SaleOrder_Date"], errors="coerce")
    monthly = df.groupby(df["SaleOrder_Date"].dt.to_period("M"))["Net_Value"].sum().reset_index()
    monthly["SaleOrder_Date"] = monthly["SaleOrder_Date"].astype(str)
    st.dataframe(monthly)
    st.plotly_chart(px.line(monthly, x="SaleOrder_Date", y="Net_Value", markers=True, title="Monthly Sales Trend"), use_container_width=True, key="monthly_sales_chart")
    return "📅 Monthly sales trend shown."

@tool
def yearly_sales(input: str = "") -> str:
    """Yearly sales trend"""
    df["SaleOrder_Date"] = pd.to_datetime(df["SaleOrder_Date"], errors="coerce")
    yearly = df.groupby(df["SaleOrder_Date"].dt.year)["Net_Value"].sum().reset_index()
    yearly.columns = ["Year", "Net_Value"]
    st.dataframe(yearly)
    st.plotly_chart(px.line(yearly, x="Year", y="Net_Value", markers=True, title="Yearly Sales Trend"), use_container_width=True, key="yearly_sales_chart")
    return "🗓️ Yearly sales trend shown."

@tool
def rejected_orders(input: str = "") -> str:
    """List rejected orders"""
    rejected = df[df["Rejection_Reason"] != "Unknown"]
    st.dataframe(rejected[["Sales_Doc_No", "ShortText_Item", "Rejection_Reason", "Net_Value"]].head(10))
    return f"❌ Total rejected orders: {len(rejected)}. Sample shown above."

@tool
def rejection_reasons(input: str = "") -> str:
    """Display rejection reasons count"""
    counts = df[df["Rejection_Reason"] != "Unknown"]["Rejection_Reason"].value_counts().reset_index()
    counts.columns = ["Rejection_Reason", "Count"]
    st.dataframe(counts)
    st.plotly_chart(px.bar(counts, x="Rejection_Reason", y="Count", title="Rejection Reasons"), use_container_width=True, key="rejection_reason_chart")
    return "🔎 Rejection reason counts shown."

@tool
def quantity_discrepancy(input: str = "") -> str:
    """Quantity discrepancies"""
    df["Quantity_Diff"] = df["Order_Quantity"] - df["Actual_Delivered_Quantity"]
    mismatch = df[df["Quantity_Diff"] != 0]
    st.dataframe(mismatch[["Sales_Doc_No", "Order_Quantity", "Actual_Delivered_Quantity", "Quantity_Diff"]].head(10))
    return f"📦 Found {len(mismatch)} quantity discrepancies."

@tool
def delivery_delay(input: str = "") -> str:
    """Delivery delay in days"""
    df["Requested_Delivery_Date"] = pd.to_datetime(df["Requested_Delivery_Date"], errors="coerce")
    df["Actual_Goods_Issue_Date"] = pd.to_datetime(df["Actual_Goods_Issue_Date"], errors="coerce")
    df["Delay"] = (df["Actual_Goods_Issue_Date"] - df["Requested_Delivery_Date"]).dt.days.fillna(0).astype(int)
    delayed = df[df["Delay"] > 0]
    st.dataframe(delayed[["Sales_Doc_No", "Requested_Delivery_Date", "Actual_Goods_Issue_Date", "Delay"]].head(10))
    return f"🚚 Found {len(delayed)} delayed deliveries."

@tool
def billing_vs_delivery(input: str = "") -> str:
    """Billing and delivery status comparison"""
    billed = df[df["Billing_Document_Number"] != "Unknown"]
    delivered = df[df["Actual_Delivered_Quantity"] > 0]
    summary = pd.DataFrame({
        "Status": ["Billed", "Not Billed", "Delivered", "Not Delivered"],
        "Count": [len(billed), len(df)-len(billed), len(delivered), len(df)-len(delivered)]
    })
    st.dataframe(summary)
    st.dataframe(df[["Sales_Doc_No", "Billing_Document_Number", "Actual_Delivered_Quantity"]].head(10))
    return "📋 Billing vs Delivery comparison shown."

@tool
def billing_currency(input: str = "") -> str:
    """Billing currency distribution"""
    counts = df["Billing_Currency"].value_counts().reset_index()
    counts.columns = ["Currency", "Count"]
    st.dataframe(counts)
    st.plotly_chart(px.pie(counts, names="Currency", values="Count", title="Billing Currency Distribution"), use_container_width=True, key="billing_currency_chart")
    return "💱 Billing currency distribution shown."

# TOOLS LIST
tools = [
    top_products, low_products, monthly_sales, yearly_sales,
    rejected_orders, rejection_reasons, quantity_discrepancy,
    delivery_delay, billing_vs_delivery, billing_currency
]

system_prompt = """
You are a helpful assistant that analyzes uploaded sales data and always uses tools to answer.
"""

prompt = ChatPromptTemplate.from_messages([
    SystemMessage(content=system_prompt),
    MessagesPlaceholder("chat_history"),
    HumanMessage(content="{input}"),
    MessagesPlaceholder("agent_scratchpad")
])

llm = ChatGroq(
    model_name="openai/gpt-oss-20b",
    api_key=groq_api_key
)
agent = create_openai_tools_agent(llm=llm, tools=tools, prompt=prompt)
agent_executor = AgentExecutor(agent=agent, tools=tools, verbose=True)

if "chat_history" not in st.session_state:
    st.session_state.chat_history = []

user_input = st.chat_input("Ask me anything about your sales data...")
if user_input:
    st.session_state.chat_history.append(HumanMessage(content=user_input))
    with st.spinner("Analyzing..."):
        try:
            result = agent_executor.invoke({
                "input": user_input,
                "chat_history": st.session_state.chat_history
            })
            st.session_state.chat_history.append(AIMessage(content=result["output"]))
            st.chat_message("assistant").markdown(result["output"])
        except Exception as e:
            st.error(f"⚠️ {e}")

for msg in st.session_state.chat_history:
    role = "user" if isinstance(msg, HumanMessage) else "assistant"
    st.chat_message(role).markdown(msg.content)
