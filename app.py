import pandas as pd
import streamlit as st
from fpdf import FPDF
from io import BytesIO

# Custom CSS for styling and animations
st.markdown(
    """
    <style>
    /* Background color */
    body {
        background-color: #f0f4f8;
        animation: background-fade 5s infinite alternate;
    }

    /* App title styling */
    .title {
        font-size: 48px;
        color: #1e88e5;
        text-align: center;
        font-weight: bold;
        margin-bottom: 30px;
    }

    /* Animated and larger logo */
    .logo {
        display: block;
        margin-left: auto;
        margin-right: auto;
        width: 200px;  /* Bigger logo */
    }
    </style>
    """,
    unsafe_allow_html=True,
)

# Add larger logo with animation
logo_url = "https://raw.githubusercontent.com/waleedhussien11/grade_search/main/Picture4.jpg"  # Replace with your actual logo URL
st.markdown(f'<img src="{logo_url}" alt="School Logo" class="logo">', unsafe_allow_html=True)

# Add title with styling
st.markdown('<div class="title">البحث عن رقم الجلوس حسب المرحلة التعليمية</div>', unsafe_allow_html=True)

# Dictionary to map levels to their respective file URLs
level_files = {
    "المرحلة الثالثه الابتدائيه": "https://raw.githubusercontent.com/waleedhussien11/grade_search/main/grade3.csv",
    " المرحلة الرابعه الابتدائيه": "https://raw.githubusercontent.com/waleedhussien11/grade_search/main/grade4_new.csv",
    "المرحلة الخامسه الابتدائيه": "https://raw.githubusercontent.com/waleedhussien11/grade_search/main/grade5_new.csv",
    "المرحلة السادسه الابتدائيه": "https://raw.githubusercontent.com/waleedhussien11/grade_search/main/grade6_new.csv",
    "المرحلة الأولى الإعدادية": "https://raw.githubusercontent.com/waleedhussien11/grade_search/main/grade1.csv",
    "المرحلة الثانية الإعدادية": "https://raw.githubusercontent.com/waleedhussien11/grade_search/main/grade2.csv",
}

# Dropdown menu to select the education level
selected_level = st.selectbox("اختر المرحلة التعليمية:", list(level_files.keys()))

if selected_level:
    # Get the file URL for the selected level
    file_url = level_files[selected_level]
    
    try:
        # Load the CSV file from the URL
        data = pd.read_csv(file_url)
        
        # Input from the user
        seat_number = st.text_input(f"أدخل رقم الجلوس للبحث عنه ({selected_level}):")

        if seat_number:
            # Convert "رقم الجلوس" column to string for consistent comparison
            data["رقم الجلوس"] = data["رقم الجلوس"].astype(str)

            # Search for the entered seat number
            record = data[data["رقم الجلوس"] == seat_number]

            # Display results
            if not record.empty:
                st.success("✅ السجلات الموجودة:")
                # Display the record as a table
                st.dataframe(record)

                # Function to convert the record to PDF
                def convert_to_pdf(record):
                    pdf = FPDF()
                    pdf.add_page()
                    pdf.set_font("Arial", size=12)
                    pdf.cell(200, 10, txt="نتيجة البحث", ln=True, align="C")
                    pdf.ln(10)  # Add a line break
                    # Add the table
                    for col in record.columns:
                        pdf.cell(40, 10, col, 1, 0, "C")
                    pdf.ln()
                    for row in record.values:
                        for cell in row:
                            pdf.cell(40, 10, str(cell), 1, 0, "C")
                        pdf.ln()
                    buffer = BytesIO()
                    pdf.output(buffer)
                    buffer.seek(0)
                    return buffer

                # Add download button for the PDF
                st.download_button(
                    label="⬇️ تنزيل الجدول كملف PDF",
                    data=convert_to_pdf(record),
                    file_name="record.pdf",
                    mime="application/pdf",
                )
            else:
                st.warning(f"⚠️ لا توجد سجلات لرقم الجلوس: {seat_number}")
    except Exception as e:
        st.error(f"⚠️ حدث خطأ أثناء تحميل الملف: {e}")
