import pandas as pd
import streamlit as st

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

    /* Dropdown styling */
    .stSelectbox {
        font-size: 18px !important;
    }

    /* Input box styling with animation */
    .stTextInput {
        font-size: 18px !important;
        animation: glow 2s infinite alternate;
    }

    /* Glow effect for input */
    @keyframes glow {
        0% { box-shadow: 0 0 10px #1e88e5; }
        100% { box-shadow: 0 0 20px #1e88e5; }
    }

    /* Table styling */
    .dataframe {
        margin: 0 auto;
        border: 2px solid #1e88e5;
        font-size: 18px;
        text-align: center;
        border-collapse: collapse;
    }

    .dataframe th, .dataframe td {
        border: 1px solid #ddd;
        padding: 8px;
    }

    .dataframe th {
        background-color: #1e88e5;
        color: white;
        font-size: 18px;
    }

    .dataframe td {
        font-size: 16px;
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

                # Enhance the transposed DataFrame with styling
                st.markdown(
                    record_transposed.style
                    .set_table_styles(
                        [
                            {"selector": "th", "props": [("font-size", "18px"), ("text-align", "center"), ("background-color", "#1e88e5"), ("color", "white"), ("border", "1px solid black")]},
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
