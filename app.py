
import streamlit as st
from docx import Document
from io import BytesIO

def create_khai_sinh_doc(data):
    doc = Document()
    doc.add_heading("TỜ KHAI KHAI SINH", 0)
    doc.add_paragraph(f"Họ và tên: {data['Họ và tên']}")
    doc.add_paragraph(f"Ngày sinh: {data['Ngày sinh']}")
    doc.add_paragraph(f"Giới tính: {data['Giới tính']}")
    doc.add_paragraph(f"Dân tộc: {data['Dân tộc']}")
    doc.add_paragraph(f"Quốc tịch: {data['Quốc tịch']}")
    doc.add_paragraph(f"Nơi sinh: {data['Nơi sinh']}")
    buffer = BytesIO()
    doc.save(buffer)
    buffer.seek(0)
    return buffer

def create_cu_tru_doc(data):
    doc = Document()
    doc.add_heading("TỜ KHAI CƯ TRÚ", 0)
    doc.add_paragraph(f"Họ và tên: {data['Họ và tên']}")
    doc.add_paragraph(f"Số CCCD: {data['Số CCCD']}")
    doc.add_paragraph(f"Địa chỉ thường trú: {data['Địa chỉ thường trú']}")
    doc.add_paragraph(f"Nơi ở hiện tại: {data['Nơi ở hiện tại']}")
    buffer = BytesIO()
    doc.save(buffer)
    buffer.seek(0)
    return buffer

st.title("📝 Tự động điền đơn hành chính")

form_type = st.selectbox("Chọn mẫu đơn", ["Khai sinh", "Cư trú"])

data = {}
if form_type == "Khai sinh":
    data['Họ và tên'] = st.text_input("Họ và tên")
    data['Ngày sinh'] = st.text_input("Ngày sinh")
    data['Giới tính'] = st.selectbox("Giới tính", ["Nam", "Nữ"])
    data['Dân tộc'] = st.text_input("Dân tộc")
    data['Quốc tịch'] = st.text_input("Quốc tịch", value="Việt Nam")
    data['Nơi sinh'] = st.text_input("Nơi sinh")
    if st.button("Tạo đơn"):
        docx_file = create_khai_sinh_doc(data)
        st.download_button("Tải đơn khai sinh", data=docx_file, file_name="to_khai_khai_sinh.docx")

elif form_type == "Cư trú":
    data['Họ và tên'] = st.text_input("Họ và tên")
    data['Số CCCD'] = st.text_input("Số CCCD")
    data['Địa chỉ thường trú'] = st.text_input("Địa chỉ thường trú")
    data['Nơi ở hiện tại'] = st.text_input("Nơi ở hiện tại")
    if st.button("Tạo đơn"):
        docx_file = create_cu_tru_doc(data)
        st.download_button("Tải đơn cư trú", data=docx_file, file_name="to_khai_cu_tru.docx")
