import pandas as pd
import streamlit as st
from io import BytesIO

# Custom CSS for styling, animations, and supervisor text
st.markdown(
    """
    <style>
    /* Background Gradient */
    body {
        background: linear-gradient(135deg, #6dd5ed, #2193b0);
        color: white;
        font-family: 'Arial', sans-serif;
    }

    /* Supervisor Text Styling */
    .supervisor {
        font-size: 30px;
        color: #ffffff;
        text-align: center;
        font-weight: bold;
        margin-bottom: 20px;
        text-shadow: 2px 2px 4px #000000;
    }

    /* Title Styling */
    .title {
        font-size: 48px;
        color: #ffffff;
        text-align: center;
        font-weight: bold;
        margin-bottom: 30px;
        text-shadow: 2px 2px 4px #000000;
    }

    /* Logo Animation */
    .logo {
        display: block;
        margin-left: auto;
        margin-right: auto;
        width: 250px;
        animation: bounce 2s infinite;
    }

    /* Keyframes for logo animation */
    @keyframes bounce {
        0%, 100% {
            transform: translateY(0);
        }
        50% {
            transform: translateY(-15px);
        }
    }

    /* Dropdown Menu Styling */
    .stSelectbox {
        font-size: 18px !important;
    }

    /* Input Field Styling */
    .stTextInput {
        font-size: 18px !important;
    }

    /* Table Styling */
    table.dataframe {
        border-collapse: collapse;
        width: 100%;
        background-color: white;
        color: black;
        border: 1px solid #ddd;
        text-align: center;
        font-size: 18px;
    }
    table.dataframe th {
        background-color: #3498db;
        color: white;
        font-size: 18px;
        border: 1px solid #ddd;
    }
    table.dataframe td {
        border: 1px solid #ddd;
        padding: 8px;
    }

    /* Hide Streamlit footer */
    footer {
        visibility: hidden;
    }

    /* Hide "Made with Streamlit" branding */
    #MainMenu {
        visibility: hidden;
    }

    /* Hide any other unwanted information */
    .reportview-container .main footer {
        visibility: hidden;
        height: 0px;
    }
    .viewerBadge_container__1QSob {
        visibility: hidden;
    }
    </style>
    """,
    unsafe_allow_html=True,
)

# Add supervisor text at the top
st.markdown(
    '<div class="supervisor">تحت إشراف مدير المجمع أ\\محمد رمضان مصطفى</div>',
    unsafe_allow_html=True,
)

# Add larger animated logo
logo_url = "https://raw.githubusercontent.com/waleedhussien11/grade_search/main/Picture4.jpg"  # Replace with your actual logo URL
st.markdown(f'<img src="{logo_url}" alt="School Logo" class="logo">', unsafe_allow_html=True)

# Add title with styling and animation
st.markdown('<div class="title">البحث عن رقم الجلوس حسب المرحلة التعليمية</div>', unsafe_allow_html=True)

# Dictionary to map levels to their respective file URLs
level_files = {
    "الصف الثالث الابتدائي": "https://raw.githubusercontent.com/waleedhussien11/grade_search/main/grade3.csv",
    " الصف الرابع الابتدائي": "https://raw.githubusercontent.com/waleedhussien11/grade_search/main/grade4_new.csv",
    "الصف الخامس الابتدائي": "https://raw.githubusercontent.com/waleedhussien11/grade_search/main/grade5_new.csv",
    "الصف السادس الابتدائي": "https://raw.githubusercontent.com/waleedhussien11/grade_search/main/grade6_new.csv",
    "الصف الأولى الاعدادي": "https://raw.githubusercontent.com/waleedhussien11/grade_search/main/grade1.csv",
    "الصف الثاني الاعدادي": "https://raw.githubusercontent.com/waleedhussien11/grade_search/main/grade2.csv",
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
            # Convert "رقم الجلوس" column to string
            data["رقم الجلوس"] = data["رقم الجلوس"].astype(str)

            # Search for the entered seat number
            record = data[data["رقم الجلوس"] == seat_number]

            # Display results
            if not record.empty:
                st.success("✅ السجلات الموجودة:")
                record_transposed = record.transpose()

                st.markdown(
                    record_transposed.style
                    .set_table_styles(
                        [
                            {"selector": "th", "props": [("font-size", "18px"), ("text-align", "center"), ("background-color", "#3498db"), ("color", "white"), ("border", "1px solid black")]},
                            {"selector": "td", "props": [("font-size", "16px"), ("text-align", "center"), ("border", "1px solid black")]},
                        ]
                    )
                    .set_properties(**{"text-align": "center"})
                    .to_html(),
                    unsafe_allow_html=True,
                )

                # Function to convert the DataFrame to HTML for download
                def convert_to_html(df):
                    html = df.to_html(index=False)
                    buffer = BytesIO()
                    buffer.write(html.encode('utf-8'))
                    buffer.seek(0)
                    return buffer

                # Add download button for HTML
                st.download_button(
                    label="⬇️ تنزيل النتائج كملف HTML",
                    data=convert_to_html(record),
                    file_name=f"record_{seat_number}.html",
                    mime="text/html",
                )
            else:
                st.warning(f"⚠️ لا توجد سجلات لرقم الجلوس: {seat_number}")
    except Exception as e:
        st.error(f"⚠️ حدث خطأ أثناء تحميل الملف: {e}")
