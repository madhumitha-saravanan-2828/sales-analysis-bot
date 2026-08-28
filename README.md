# 🤖 Sales Agent Chatbot

> A simple AI-based chatbot for exploring and analyzing sales data using natural-language questions.

The **Sales Agent Chatbot** lets users upload a sales CSV file and ask questions about products, sales trends, rejected orders, delivery delays, billing status, and more.

Instead of manually filtering the dataset, users can simply ask a question and get the result through **tables, charts, or text responses**.

---

## 🚀 Live Demo

🌐 **Try the application:**
https://madhumithasaravanan28ed-a4xajczgtqw89zzugglpd6.streamlit.app/

> 🔐 The application is password protected.

---

## ✨ What Can It Do?

The chatbot can answer questions such as:

* 🏆 What are the top selling products?
* 📉 Show me the least sold items.
* 📅 What is the monthly sales trend?
* 🗓️ Show yearly sales trend.
* ❌ Show rejected orders.
* 🔍 What are the reasons for rejection?
* 📦 Show quantity discrepancies between ordered and delivered.
* 🚚 List delayed deliveries.
* 🧾 Compare billing and delivery statuses.
* 💱 Show billing currency distribution.

---

## 🛠️ Technologies Used

| Technology   | Usage                        |
| ------------ | ---------------------------- |
| 🐍 Python    | Application development      |
| 🎈 Streamlit | Web interface                |
| 🐼 Pandas    | Data processing and analysis |
| 📊 Plotly    | Interactive visualizations   |
| 🔗 LangChain | Agent and tool handling      |
| ⚡ Groq API   | LLM-based responses          |

---

## ⭐ Main Features

* 📁 Upload sales data through CSV
* 💬 Ask questions using natural language
* 🏆 Find top-selling products
* 📉 Find low-selling products
* 📅 Analyze monthly and yearly sales
* ❌ Analyze rejected orders
* 🔍 Find rejection reasons
* 📦 Detect quantity discrepancies
* 🚚 Identify delayed deliveries
* 🧾 Compare billing and delivery information
* 💱 Analyze billing currency distribution
* 📊 Display interactive charts using Plotly
* 🔐 Password-protected application

---

## ⚙️ How to Use

### 1️⃣ Open the Application

Open the Streamlit application:

👉 https://madhumithasaravanan28ed-a4xajczgtqw89zzugglpd6.streamlit.app/

### 2️⃣ Enter the Password

Enter the password provided by the project owner.

### 3️⃣ Enter a Groq API Key

Enter a Groq API key when prompted.

The application uses the **free Groq API** for testing/demo purposes. Free API usage has limits and availability can change. The API key used for the demo may only remain usable for a limited period, after which a new key may be required.

### 4️⃣ Upload Your CSV

Upload a compatible sales CSV file.

### 5️⃣ Ask Questions

Type your question in the chatbot and get the analysis.

---

## 📂 Project Structure

```text
Sales-Agent-Chatbot/
│
├── app_py.py
├── requirements.txt
├── README.md
│
└── screenshots/
    ├── home-page.png
    ├── chatbot.png
    ├── sales-analysis.png
    └── visualizations.png
```

---

## 🔐 Dataset & Privacy

The original sales dataset used while developing this project is **confidential** and has **not been uploaded to this repository**.

Users need to provide their own compatible CSV file to use the application.

The application expects columns such as:

```text
Material_Number
ShortText_Item
Net_Value
SaleOrder_Date
Rejection_Reason
Order_Quantity
Actual_Delivered_Quantity
Requested_Delivery_Date
Actual_Goods_Issue_Date
Billing_Document_Number
Billing_Currency
Sales_Doc_No
```

⚠️ **The confidential sales dataset is intentionally not included in this repository.**

---

## 🔑 API Key

This project uses the **Groq API** for the chatbot.

For demo/testing purposes, a **free Groq API key** can be used. Free-tier limits and model availability may change over time.

**Never upload your API key to GitHub or write it directly inside the source code.**

---

## 🔄 How It Works

```text
             👤 User
                │
                ▼
        📁 Upload Sales CSV
                │
                ▼
        🎈 Streamlit Interface
                │
                ▼
         💬 Natural Language
              Query
                │
                ▼
        ⚡ Groq LLM + LangChain
                │
                ▼
       🔧 Sales Analysis Tool
                │
                ▼
        🐼 Pandas Processing
                │
                ▼
       📊 Tables / Charts / Text
```

The chatbot receives the user's question and uses the appropriate analysis tool to process the uploaded sales data. Pandas performs the data analysis, while Plotly is used for interactive visualizations.

---

## 💡 Example

**User:**

> What are the top selling products?

**Chatbot:**

The application identifies the relevant sales analysis tool and displays the top-selling products along with an interactive chart.

---

## 📝 Notes

* A Groq API key is required to use the chatbot.
* The original sales dataset is confidential and is not included.
* Users should upload their own compatible sales CSV.
* Free API usage is subject to Groq's current limits and availability.
* The project is mainly intended for learning, demonstration, and practical data-analysis use.

---

## 👩‍💻 Author
 Madhumitha Saravanan

**B.Tech Artificial Intelligence and Data Science**

---

⭐ **If you found this project interesting, feel free to star the repository!**
