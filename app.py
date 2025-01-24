import pandas as pd
import streamlit as st

# Title for the Streamlit app
st.title("البحث عن رقم الجلوس")

# File upload section
uploaded_file = st.file_uploader("قم بتحميل ملف CSV يحتوي على البيانات", type=["csv"])

if uploaded_file:
    # Load the CSV file
    grade6 = pd.read_csv(uploaded_file)

    # Show the loaded DataFrame
    st.write("📄 عرض البيانات:")
    st.dataframe(grade6)

    # Check if "رقم الجلوس" column exists
    if "رقم الجلوس" in grade6.columns:
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
    else:
        st.error("⚠️ الملف لا يحتوي على عمود 'رقم الجلوس'.")
else:
    st.info("📤 قم بتحميل ملف CSV لبدء البحث.")
