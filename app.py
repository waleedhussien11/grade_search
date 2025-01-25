import pandas as pd
import streamlit as st

# Custom CSS for styling the app
st.markdown(
    """
    <style>
    /* Background color */
    body {
        background-color: #f7f9fc;
    }

    /* App title styling */
    .title {
        font-size: 40px;
        color: #3498db;
        text-align: center;
        font-weight: bold;
        margin-bottom: 20px;
    }

    /* Animation for the logo */
    @keyframes bounce {
        0%, 100% {
            transform: translateY(0);
        }
        50% {
            transform: translateY(-10px);
        }
    }

    /* Logo styling */
    .logo {
        display: block;
        margin-left: auto;
        margin-right: auto;
        width: 150px;
        animation: bounce 2s infinite;
    }

    /* Dropdown styling */
    .stSelectbox {
        font-size: 18px !important;
    }

    /* Table styling */
    .dataframe {
        margin: 0 auto;
        border: 1px solid #ddd;
        font-size: 18px;
        text-align: center;
    }

    /* Input box styling */
    .stTextInput {
        font-size: 18px !important;
    }
    </style>
    """,
    unsafe_allow_html=True,
)

# Add logo with animation
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
    "المرحلة الأولى الإعدادية": "https://raw.githubusercontent.com/waleedhussien11/grade_search/main/grade7.csv",
    "المرحلة الثانية الإعدادية": "https://raw.githubusercontent.com/waleedhussien11/grade_search/main/grade8.csv",
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

                # Enhance the transposed DataFrame with styling
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
            else:
                st.warning(f"⚠️ لا توجد سجلات لرقم الجلوس: {seat_number}")
    except Exception as e:
        st.error(f"⚠️ حدث خطأ أثناء تحميل الملف: {e}")
