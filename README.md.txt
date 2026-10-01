# Company Data Parser (Streamlit Web App)

Ứng dụng Python giúp phân tích **dữ liệu thô** của công ty và tự động đưa vào các trường 1–9.

## 🚀 Tính năng
- **Trường 1**: Tên công ty gốc (Title Case).  
  - "TNHH" luôn viết hoa đầy đủ.  
  - "Cổ phần" → "CP".
- **Trường 2**: Lấy trực tiếp từ mục **Tên quốc tế** trong dữ liệu thô.  
  - Viết hoa chữ cái đầu mỗi từ.  
  - "Company Limited" → "Co Ltd".  
  - "JOINT STOCK COMPANY" → "JSC".  
  - "Cổ phần" → "CP".  
- **Trường 3**: Địa chỉ trước khi gặp Phường/Xã.  
- **Trường 4**: Dịch Trường 3 sang tiếng Anh (không dấu + hậu tố St/Quarter/Village/Hamlet).  
- **Trường 5**: Phường/Xã từ địa chỉ thuế.  
- **Trường 6**: Dịch sang tiếng Anh (Ward/Commune).  
- **Trường 7**: Giữ nguyên dữ liệu gốc (bao gồm khoảng trắng, dấu gạch nối).  
- **Trường 8**: Người đại diện (Title Case).  
- **Trường 9**: Tóm tắt ngày/tháng/năm + phone + xác nhận.

## 📦 Cài đặt
Clone repo về máy:
```bash
git clone https://github.com/your-username/company-data-parser.git
cd company-data-parser
