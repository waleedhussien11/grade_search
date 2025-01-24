import pandas as pd
import streamlit as st

# Title for the Streamlit app
st.title("البحث عن رقم الجلوس")

# Raw URL to the CSV file on your GitHub repository
file_url = "https://raw.githubusercontent.com/waleedhussien11/grade_search/main/grade6.csv"

try:
    # Load the CSV file from the URL
    grade6 = pd.read_csv(file_url)

    # Input from the user
    seat_number = st.text_input("أدخل رقم الجلوس للبحث عنه:")

    if seat_number:
        # Convert "رقم الجلوس" column to string for consistent comparison
        grade6["رقم الجلوس"] = grade6["رقم الجلوس"].astype(str)

        # Search for the entered seat number
        record = grade6[grade6["رقم الجلوس"] == seat_number]

        # Display results
        if not record.empty:
            st.success("✅ السجلات الموجودة:")
            st.dataframe(record)
        else:
            st.warning(f"⚠️ لا توجد سجلات لرقم الجلوس: {seat_number}")
except Exception as e:
    st.error(f"⚠️ حدث خطأ أثناء تحميل الملف: {e}")
