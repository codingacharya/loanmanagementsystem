import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

st.set_page_config(page_title='Loan Management System', layout='wide')

# File upload section
st.title("📊 Loan Management System")
st.markdown("Upload a CSV or Excel file to analyze loan data.")

uploaded_file = st.file_uploader("Upload Loan Data File", type=["csv", "xlsx"])

if uploaded_file:
    # Read the uploaded file
    if uploaded_file.name.endswith(".csv"):
        df = pd.read_csv(uploaded_file)
    else:
        df = pd.read_excel(uploaded_file)
    
    st.success("File uploaded successfully!")
    
    # Display basic information
    st.subheader("📋 Data Preview")
    st.dataframe(df.head())
    
    # Summary statistics
    st.subheader("📈 Summary Statistics")
    st.write(df.describe())
    
    # Loan Status Distribution
    if 'Loan_Status' in df.columns:
        st.subheader("📊 Loan Status Distribution")
        fig, ax = plt.subplots()
        sns.countplot(x=df['Loan_Status'], palette='coolwarm', ax=ax)
        ax.set_title("Loan Status Distribution")
        st.pyplot(fig)
    else:
        st.warning("Column 'Loan_Status' not found in dataset.")
    
    # Loan Amount Distribution
    if 'LoanAmount' in df.columns:
        st.subheader("💰 Loan Amount Distribution")
        fig, ax = plt.subplots()
        sns.histplot(df['LoanAmount'].dropna(), kde=True, bins=30, ax=ax)
        ax.set_title("Loan Amount Distribution")
        st.pyplot(fig)
    else:
        st.warning("Column 'LoanAmount' not found in dataset.")
    
    # Loan Approval by Property Area
    if 'Property_Area' in df.columns and 'Loan_Status' in df.columns:
        st.subheader("🏡 Loan Approval by Property Area")
        fig, ax = plt.subplots()
        sns.countplot(x='Property_Area', hue='Loan_Status', data=df, palette='viridis', ax=ax)
        ax.set_title("Loan Approvals by Property Area")
        st.pyplot(fig)
    else:
        st.warning("Columns 'Property_Area' or 'Loan_Status' not found in dataset.")
    
    # Interactive filtering
    st.subheader("🔍 Filter Data")
    min_loan = int(df['LoanAmount'].min()) if 'LoanAmount' in df.columns else 0
    max_loan = int(df['LoanAmount'].max()) if 'LoanAmount' in df.columns else 100
    loan_filter = st.slider("Select Loan Amount Range", min_loan, max_loan, (min_loan, max_loan))
    
    if 'LoanAmount' in df.columns:
        filtered_df = df[(df['LoanAmount'] >= loan_filter[0]) & (df['LoanAmount'] <= loan_filter[1])]
        st.dataframe(filtered_df)
    
    st.success("Analysis complete!")
