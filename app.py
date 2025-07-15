import streamlit as st
from docx import Document
from io import BytesIO
import requests
from PIL import Image
import pytesseract

# 1. Giao diện chính
st.title("📄 Tự động điền đơn hành chính từ giấy tờ")
st.subheader("1. Tải ảnh CCCD hoặc giấy tờ")

uploaded_file = st.file_uploader("Tải ảnh giấy tờ (JPG/PNG)", type=["jpg", "jpeg", "png"])

user_data = {}

if uploaded_file:
    image = Image.open(uploaded_file)
    st.image(image, caption="Ảnh đã tải", use_column_width=True)

    # OCR trích xuất văn bản
    extracted_text = pytesseract.image_to_string(image, lang="vie")
    st.text_area("📄 Văn bản trích xuất", extracted_text, height=200)

    # Đây là phần bạn có thể dùng RegEx hoặc xử lý thủ công
    # Ví dụ đơn giản:
    user_data['Họ và tên'] = st.text_input("Họ, tên người yêu cầu", "")
    user_data['Ngày sinh'] = st.text_input("Ngày sinh", "")
    user_data['Nơi thường trú'] = st.text_input("Nơi cư trú", "")

# 2. Chọn mẫu đơn
st.subheader("3. Tạo mẫu đơn")

selected_form = st.radio("Chọn mẫu đơn:", ["Khai sinh", "Cư trú"])

# 3. Hàm điền file Word
def fill_docx_template(template_path, context):
    doc = Document(template_path)
    for p in doc.paragraphs:
        for key, val in context.items():
            if f"<<{key}>>" in p.text:
                p.text = p.text.replace(f"<<{key}>>", val)
    return doc

# 4. Tạo mẫu đơn khi nhấn nút
if st.button("Tạo đơn"):
    if not user_data:
        st.warning("⚠️ Vui lòng tải ảnh và nhập thông tin cần thiết.")
    else:
        try:
            if selected_form == "Khai sinh":
                template_file = "to-khai-khai-sinh.docx"
            else:
                template_file = "to-khai-cu-tru.docx"

            filled_doc = fill_docx_template(template_file, user_data)

            output = BytesIO()
            filled_doc.save(output)
            output.seek(0)

            st.success("✅ Tạo đơn thành công!")
            st.download_button(
                label="📥 Tải đơn đã điền",
                data=output,
                file_name="don_hoan_thien.docx",
                mime="application/vnd.openxmlformats-officedocument.wordprocessingml.document"
            )
        except Exception as e:
            st.error(f"Đã xảy ra lỗi: {e}")

