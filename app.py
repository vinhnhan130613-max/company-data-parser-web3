import streamlit as st
from main import parse_raw_data
from streamlit_copy_to_clipboard import st_copy_to_clipboard

st.title("Company Data Parser (Raw Data)")

st.write("Dán dữ liệu thô của công ty vào ô dưới đây:")

raw_text = st.text_area("Dữ liệu thô")

if st.button("Phân tích dữ liệu"):
    if raw_text.strip():
        try:
            result = parse_raw_data(raw_text)
            st.subheader("Kết quả phân tích")

            # Hiển thị từng trường với nút copy
            for k, v in result.items():
                st.markdown(f"**{k}**: {v}")
                st_copy_to_clipboard(v, f"📋 Copy {k}")

        except Exception as e:
            st.error(f"Đã xảy ra lỗi khi phân tích dữ liệu: {e}")
    else:
        st.warning("Vui lòng nhập dữ liệu thô trước khi phân tích.")
