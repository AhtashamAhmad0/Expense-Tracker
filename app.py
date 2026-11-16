from datetime import date

import pandas as pd
import streamlit as st

st.set_page_config(page_title="Expense Tracker", page_icon="💰", layout="wide")
st.title("💰 Expense Tracker")

CATEGORIES = ["Food", "Transport", "Shopping", "Bills", "Health", "Entertainment", "Other"]

if "expenses" not in st.session_state:
    st.session_state.expenses = []

# ---------- Sidebar: add expense ----------
with st.sidebar:
    st.header("Add expense")
    with st.form("add_expense", clear_on_submit=True):
        d = st.date_input("Date", date.today())
        category = st.selectbox("Category", CATEGORIES)
        amount = st.number_input("Amount", min_value=0.0, step=1.0, format="%.2f")
        note = st.text_input("Note (optional)")
        submitted = st.form_submit_button("➕ Add")

    if submitted:
        if amount > 0:
            st.session_state.expenses.append(
                {"Date": d, "Category": category, "Amount": amount, "Note": note}
            )
            st.success("Expense added!")
        else:
            st.warning("Amount must be greater than 0.")

# ---------- Main area ----------
if not st.session_state.expenses:
    st.info("No expenses yet. Add your first one from the sidebar 👈")
    st.stop()

df = pd.DataFrame(st.session_state.expenses)

# Metrics
c1, c2, c3, c4 = st.columns(4)
c1.metric("Total spent", f"{df['Amount'].sum():,.2f}")
c2.metric("Transactions", len(df))
c3.metric("Average", f"{df['Amount'].mean():,.2f}")
c4.metric("Top category", df.groupby("Category")["Amount"].sum().idxmax())

st.divider()

# Charts
left, right = st.columns(2)
with left:
    st.subheader("Spending by category")
    st.bar_chart(df.groupby("Category")["Amount"].sum())
with right:
    st.subheader("Spending over time")
    st.line_chart(df.groupby("Date")["Amount"].sum())

st.divider()

# Table
st.subheader("All expenses")
st.dataframe(df, use_container_width=True)

# Delete + download
col_a, col_b = st.columns(2)
with col_a:
    idx = st.selectbox(
        "Delete an expense",
        options=range(len(df)),
        format_func=lambda i: f"{df.loc[i, 'Date']} | {df.loc[i, 'Category']} | {df.loc[i, 'Amount']:.2f}",
    )
    if st.button("🗑 Delete selected"):
        st.session_state.expenses.pop(idx)
        st.rerun()
with col_b:
    st.download_button(
        "⬇ Download CSV",
        df.to_csv(index=False).encode("utf-8"),
        file_name="expenses.csv",
        mime="text/csv",
    )