import streamlit as st
import json
import os
import pandas as pd
import plotly.express as px
from datetime import date


# =========================================================
# PAGE CONFIGURATION
# =========================================================

st.set_page_config(
    page_title="Expense Tracker",
    page_icon="💰",
    layout="wide"
)


# =========================================================
# FILE SETTINGS
# =========================================================

DATA_FILE = "expenses.json"


# =========================================================
# CUSTOM CSS
# =========================================================

st.markdown(
    """
    <style>

    .main-title {
        text-align: center;
        font-size: 40px;
        font-weight: bold;
        margin-bottom: 5px;
    }

    .subtitle {
        text-align: center;
        color: #666666;
        font-size: 17px;
        margin-bottom: 30px;
    }

    </style>
    """,
    unsafe_allow_html=True
)


# =========================================================
# JSON FILE FUNCTIONS
# =========================================================

def load_expenses():
    """
    Read expenses from the local JSON file.
    """

    if not os.path.exists(DATA_FILE):
        return []

    try:
        with open(DATA_FILE, "r") as file:
            data = json.load(file)

        return data

    except (json.JSONDecodeError, FileNotFoundError):
        return []


def save_expenses(expenses):
    """
    Save expenses into the local JSON file.
    """

    with open(DATA_FILE, "w") as file:
        json.dump(
            expenses,
            file,
            indent=4
        )


# =========================================================
# SESSION STATE
# =========================================================

if "expenses" not in st.session_state:
    st.session_state.expenses = load_expenses()


# =========================================================
# HELPER FUNCTION
# =========================================================

def get_next_id():
    """
    Generate the next expense ID.
    """

    if not st.session_state.expenses:
        return 1

    return max(
        expense["id"]
        for expense in st.session_state.expenses
    ) + 1


# =========================================================
# CREATE - ADD EXPENSE
# =========================================================

def add_expense(
    expense_date,
    description,
    category,
    amount,
    payment_method
):

    new_expense = {
        "id": get_next_id(),
        "date": expense_date.strftime("%Y-%m-%d"),
        "description": description,
        "category": category,
        "amount": float(amount),
        "payment_method": payment_method
    }

    st.session_state.expenses.append(new_expense)

    save_expenses(st.session_state.expenses)


# =========================================================
# UPDATE - EDIT EXPENSE
# =========================================================

def update_expense(
    expense_id,
    expense_date,
    description,
    category,
    amount,
    payment_method
):

    for expense in st.session_state.expenses:

        if expense["id"] == expense_id:

            expense["date"] = expense_date.strftime(
                "%Y-%m-%d"
            )

            expense["description"] = description

            expense["category"] = category

            expense["amount"] = float(amount)

            expense["payment_method"] = payment_method

            break

    save_expenses(st.session_state.expenses)


# =========================================================
# DELETE - REMOVE EXPENSE
# =========================================================

def delete_expense(expense_id):

    st.session_state.expenses = [
        expense
        for expense in st.session_state.expenses
        if expense["id"] != expense_id
    ]

    save_expenses(st.session_state.expenses)


# =========================================================
# PAGE TITLE
# =========================================================

st.markdown(
    '<div class="main-title">💰 EXPENSE TRACKER</div>',
    unsafe_allow_html=True
)

st.markdown(
    '<div class="subtitle">'
    'Track, manage and analyze your expenses'
    '</div>',
    unsafe_allow_html=True
)


# =========================================================
# SIDEBAR NAVIGATION
# =========================================================

st.sidebar.title("📌 Navigation")

page = st.sidebar.radio(
    "Select a section",
    [
        "Dashboard",
        "Add Expense",
        "View Expenses",
        "Edit Expense",
        "Delete Expense",
        "Analytics"
    ]
)


# =========================================================
# DASHBOARD
# =========================================================

if page == "Dashboard":

    st.header("📊 Dashboard")

    expenses = st.session_state.expenses

    if len(expenses) == 0:

        st.info(
            "No expenses available. "
            "Add your first expense."
        )

    else:

        total_expense = sum(
            expense["amount"]
            for expense in expenses
        )

        number_of_expenses = len(expenses)

        highest_expense = max(
            expense["amount"]
            for expense in expenses
        )

        average_expense = (
            total_expense / number_of_expenses
        )

        col1, col2, col3, col4 = st.columns(4)

        with col1:
            st.metric(
                "💰 Total Expenses",
                f"₹{total_expense:,.2f}"
            )

        with col2:
            st.metric(
                "🧾 Number of Expenses",
                number_of_expenses
            )

        with col3:
            st.metric(
                "📈 Highest Expense",
                f"₹{highest_expense:,.2f}"
            )

        with col4:
            st.metric(
                "📊 Average Expense",
                f"₹{average_expense:,.2f}"
            )

        st.divider()

        st.subheader("Recent Expenses")

        recent_expenses = expenses[-5:]

        display_data = []

        for expense in reversed(recent_expenses):

            display_data.append(
                {
                    "ID": expense["id"],
                    "Date": expense["date"],
                    "Description": expense["description"],
                    "Category": expense["category"],
                    "Amount": f"₹{expense['amount']:,.2f}",
                    "Payment": expense["payment_method"]
                }
            )

        st.dataframe(
            pd.DataFrame(display_data),
            use_container_width=True,
            hide_index=True
        )


# =========================================================
# ADD EXPENSE - CREATE
# =========================================================

elif page == "Add Expense":

    st.header("➕ Add Expense")

    with st.form("add_expense_form"):

        expense_date = st.date_input(
            "Date",
            value=date.today()
        )

        description = st.text_input(
            "Description",
            placeholder="Example: Lunch"
        )

        category = st.selectbox(
            "Category",
            [
                "Food",
                "Travel",
                "Shopping",
                "Education",
                "Bills",
                "Entertainment",
                "Health",
                "Other"
            ]
        )

        amount = st.number_input(
            "Amount (₹)",
            min_value=0.0,
            step=1.0
        )

        payment_method = st.selectbox(
            "Payment Method",
            [
                "Cash",
                "UPI",
                "Debit Card",
                "Credit Card",
                "Bank Transfer"
            ]
        )

        submit = st.form_submit_button(
            "➕ Add Expense",
            use_container_width=True
        )

        if submit:

            if description.strip() == "":
                st.error(
                    "Please enter an expense description."
                )

            elif amount <= 0:
                st.error(
                    "Amount must be greater than 0."
                )

            else:

                add_expense(
                    expense_date,
                    description.strip(),
                    category,
                    amount,
                    payment_method
                )

                st.success(
                    "Expense added successfully!"
                )


# =========================================================
# VIEW EXPENSES - READ
# =========================================================

elif page == "View Expenses":

    st.header("📋 All Expenses")

    expenses = st.session_state.expenses

    if len(expenses) == 0:

        st.info("No expenses found.")

    else:

        display_data = []

        for expense in expenses:

            display_data.append(
                {
                    "ID": expense["id"],
                    "Date": expense["date"],
                    "Description": expense["description"],
                    "Category": expense["category"],
                    "Amount": f"₹{expense['amount']:,.2f}",
                    "Payment Method": expense["payment_method"]
                }
            )

        df = pd.DataFrame(display_data)

        st.dataframe(
            df,
            use_container_width=True,
            hide_index=True
        )

        st.write(
            f"**Total Records: {len(expenses)}**"
        )


# =========================================================
# EDIT EXPENSE - UPDATE
# =========================================================

elif page == "Edit Expense":

    st.header("✏️ Edit Expense")

    expenses = st.session_state.expenses

    if len(expenses) == 0:

        st.info(
            "There are no expenses available to edit."
        )

    else:

        expense_options = {
            f"#{expense['id']} - "
            f"{expense['description']} - "
            f"₹{expense['amount']:,.2f}":
            expense["id"]
            for expense in expenses
        }

        selected_expense = st.selectbox(
            "Select an expense",
            list(expense_options.keys())
        )

        selected_id = expense_options[
            selected_expense
        ]

        selected = next(
            expense
            for expense in expenses
            if expense["id"] == selected_id
        )

        with st.form("edit_expense_form"):

            current_date = date.fromisoformat(
                selected["date"]
            )

            expense_date = st.date_input(
                "Date",
                value=current_date
            )

            description = st.text_input(
                "Description",
                value=selected["description"]
            )

            categories = [
                "Food",
                "Travel",
                "Shopping",
                "Education",
                "Bills",
                "Entertainment",
                "Health",
                "Other"
            ]

            category = st.selectbox(
                "Category",
                categories,
                index=categories.index(
                    selected["category"]
                )
            )

            amount = st.number_input(
                "Amount (₹)",
                min_value=0.0,
                value=float(selected["amount"]),
                step=1.0
            )

            payment_methods = [
                "Cash",
                "UPI",
                "Debit Card",
                "Credit Card",
                "Bank Transfer"
            ]

            payment_method = st.selectbox(
                "Payment Method",
                payment_methods,
                index=payment_methods.index(
                    selected["payment_method"]
                )
            )

            update_button = st.form_submit_button(
                "💾 Update Expense",
                use_container_width=True
            )

            if update_button:

                if description.strip() == "":
                    st.error(
                        "Description cannot be empty."
                    )

                elif amount <= 0:
                    st.error(
                        "Amount must be greater than 0."
                    )

                else:

                    update_expense(
                        selected_id,
                        expense_date,
                        description.strip(),
                        category,
                        amount,
                        payment_method
                    )

                    st.success(
                        "Expense updated successfully!"
                    )

                    st.rerun()


# =========================================================
# DELETE EXPENSE - DELETE
# =========================================================

elif page == "Delete Expense":

    st.header("🗑️ Delete Expense")

    expenses = st.session_state.expenses

    if len(expenses) == 0:

        st.info(
            "There are no expenses available to delete."
        )

    else:

        expense_options = {
            f"#{expense['id']} - "
            f"{expense['description']} - "
            f"₹{expense['amount']:,.2f}":
            expense["id"]
            for expense in expenses
        }

        selected_expense = st.selectbox(
            "Select an expense to delete",
            list(expense_options.keys())
        )

        selected_id = expense_options[
            selected_expense
        ]

        st.warning(
            "Deleting an expense cannot be undone."
        )

        if st.button(
            "🗑️ Delete Expense",
            use_container_width=True
        ):

            delete_expense(selected_id)

            st.success(
                "Expense deleted successfully!"
            )

            st.rerun()


# =========================================================
# ANALYTICS
# =========================================================

elif page == "Analytics":

    st.header("📈 Expense Analytics")

    expenses = st.session_state.expenses

    if len(expenses) == 0:

        st.info(
            "Add some expenses to view analytics."
        )

    else:

        # Convert JSON data into DataFrame

        df = pd.DataFrame(expenses)

        df["date"] = pd.to_datetime(
            df["date"]
        )

        # -------------------------------------------------
        # CATEGORY CHART
        # -------------------------------------------------

        st.subheader(
            "💰 Expenses by Category"
        )

        category_data = (
            df.groupby("category")["amount"]
            .sum()
            .reset_index()
        )

        category_chart = px.bar(
            category_data,
            x="category",
            y="amount",
            title="Total Expense by Category",
            labels={
                "category": "Category",
                "amount": "Amount (₹)"
            },
            text_auto=".2f"
        )

        st.plotly_chart(
            category_chart,
            use_container_width=True
        )

        # -------------------------------------------------
        # MONTHLY CHART
        # -------------------------------------------------

        st.subheader(
            "📅 Monthly Expenses"
        )

        df["month"] = df["date"].dt.strftime(
            "%Y-%m"
        )

        monthly_data = (
            df.groupby("month")["amount"]
            .sum()
            .reset_index()
        )

        monthly_chart = px.line(
            monthly_data,
            x="month",
            y="amount",
            markers=True,
            title="Monthly Expense Trend",
            labels={
                "month": "Month",
                "amount": "Amount (₹)"
            }
        )

        st.plotly_chart(
            monthly_chart,
            use_container_width=True
        )

        # -------------------------------------------------
        # PAYMENT METHOD CHART
        # -------------------------------------------------

        st.subheader(
            "💳 Expenses by Payment Method"
        )

        payment_data = (
            df.groupby("payment_method")["amount"]
            .sum()
            .reset_index()
        )

        payment_chart = px.pie(
            payment_data,
            names="payment_method",
            values="amount",
            title="Expense Distribution by Payment Method"
        )

        st.plotly_chart(
            payment_chart,
            use_container_width=True
        )