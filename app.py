import streamlit as st
from main import parse_raw_data

st.title("Company Data Parser (Raw Data)")

raw_text = st.text_area("Dữ liệu thô")

if st.button("Phân tích dữ liệu"):
    if raw_text.strip():
        try:
            result = parse_raw_data(raw_text)
            st.subheader("Kết quả phân tích")

            # Hiển thị từng trường với nút copy bằng HTML/JS
            for k, v in result.items():
                st.markdown(f"**{k}**: {v}")
                st.markdown(
                    f"""
                    <button style="margin-bottom:10px;"
                            onclick="navigator.clipboard.writeText('{v}')">
                            📋 Copy {k}
                    </button>
                    """,
                    unsafe_allow_html=True
                )

        except Exception as e:
            st.error(f"Lỗi khi phân tích dữ liệu: {e}")
    else:
        st.warning("Vui lòng nhập dữ liệu thô trước khi phân tích.")
