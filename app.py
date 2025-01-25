import pandas as pd
import streamlit as st
from io import BytesIO
import matplotlib.pyplot as plt
from PIL import Image
from fpdf import FPDF


# Custom CSS for styling and animations
st.markdown(
    """
    <style>
    /* Background color */
    body {
        background-color: #f0f4f8;
        animation: background-fade 5s infinite alternate;
    }

    /* Animation for background */
    @keyframes background-fade {
        0% { background-color: #f0f4f8; }
        100% { background-color: #eaf2f8; }
    }

    /* App title styling with animation */
    .title {
        font-size: 48px;
        color: #1e88e5;
        text-align: center;
        font-weight: bold;
        animation: fade-in 2s ease-in-out;
        margin-bottom: 30px;
    }

    /* Keyframes for title animation */
    @keyframes fade-in {
        from { opacity: 0; }
        to { opacity: 1; }
    }

    /* Animated and larger logo */
    .logo {
        display: block;
        margin-left: auto;
        margin-right: auto;
        width: 200px;  /* Bigger logo */
        animation: bounce 2s infinite;
    }

    /* Keyframes for logo bounce */
    @keyframes bounce {
        0%, 100% { transform: translateY(0); }
        50% { transform: translateY(-15px); }
    }
    </style>
    """,
    unsafe_allow_html=True,
)

# Add larger logo with animation
logo_url = "https://raw.githubusercontent.com/waleedhussien11/grade_search/main/Picture4.jpg"  # Replace with your actual logo URL
st.markdown(f'<img src="{logo_url}" alt="School Logo" class="logo">', unsafe_allow_html=True)

# Add title with styling and animation
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
                # Transpose the DataFrame for vertical display
                record_transposed = record.transpose()

                # Display the styled table
                st.dataframe(record)

                # Convert table to image
                def convert_to_image(record):
                    fig, ax = plt.subplots(figsize=(8, 2 + len(record) * 0.5))
                    ax.axis("off")
                    table = plt.table(
                        cellText=record.values,
                        colLabels=record.columns,
                        cellLoc="center",
                        loc="center",
                    )
                    table.auto_set_font_size(False)
                    table.set_fontsize(12)
                    table.auto_set_column_width(col=list(range(len(record.columns))))
                    buffer = BytesIO()
                    plt.savefig(buffer, format="png", bbox_inches="tight", dpi=300)
                    buffer.seek(0)
                    plt.close(fig)
                    return buffer

                # Convert table to PDF
                def convert_to_pdf(record):
                    pdf = FPDF()
                    pdf.add_page()
                    pdf.set_font("Arial", size=12)
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

                # Download options
                col1, col2 = st.columns(2)
                with col1:
                    st.download_button(
                        "⬇️ تنزيل الجدول كصورة",
                        data=convert_to_image(record),
                        file_name="record.png",
                        mime="image/png",
                    )
                with col2:
                    st.download_button(
                        "⬇️ تنزيل الجدول كملف PDF",
                        data=convert_to_pdf(record),
                        file_name="record.pdf",
                        mime="application/pdf",
                    )
            else:
                st.warning(f"⚠️ لا توجد سجلات لرقم الجلوس: {seat_number}")
    except Exception as e:
        st.error(f"⚠️ حدث خطأ أثناء تحميل الملف: {e}")
