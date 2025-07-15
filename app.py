
import streamlit as st
from PIL import Image
import pytesseract
from docx import Document
from io import BytesIO

st.set_page_config(page_title="Điền đơn hành chính", layout="centered")
st.title("📝 Tự động điền đơn hành chính từ giấy tờ")

def extract_info_from_image(uploaded_img):
    image = Image.open(uploaded_img)
    text = pytesseract.image_to_string(image, lang='eng+vie')
    info = {'Họ và tên': '', 'Ngày sinh': '', 'Số định danh': '', 'Quê quán': '', 'Nơi thường trú': ''}
    lines = text.split("\n")
    for line in lines:
        if 'Họ tên' in line or 'Họ và tên' in line:
            info['Họ và tên'] = line.split(":")[-1].strip()
        elif 'Ngày sinh' in line:
            info['Ngày sinh'] = line.split(":")[-1].strip()
        elif 'Số' in line and 'CCCD' in line:
            info['Số định danh'] = ''.join(filter(str.isdigit, line))
        elif 'Quê quán' in line:
            info['Quê quán'] = line.split(":")[-1].strip()
        elif 'Thường trú' in line:
            info['Nơi thường trú'] = line.split(":")[-1].strip()
    return info

def fill_docx_template(template_path, data_dict):
    doc = Document(template_path)
    for p in doc.paragraphs:
        for key, val in data_dict.items():
            if key in p.text:
                p.text = p.text.replace(key, val)
    output = BytesIO()
    doc.save(output)
    output.seek(0)
    return output

st.subheader("1. Tải ảnh CCCD hoặc giấy tờ")
uploaded_img = st.file_uploader("Tải ảnh giấy tờ (JPG/PNG)", type=['jpg', 'jpeg', 'png'])

user_data = {'Họ và tên': '', 'Ngày sinh': '', 'Số định danh': '', 'Quê quán': '', 'Nơi thường trú': ''}
if uploaded_img:
    st.image(uploaded_img, caption="Ảnh đã tải", use_column_width=True)
    with st.spinner("Đang trích xuất thông tin..."):
        user_data = extract_info_from_image(uploaded_img)
    st.success("✅ Trích xuất thành công!")

st.subheader("2. Điền thông tin bổ sung")
with st.form("form_thong_tin"):
    for field in user_data:
        user_data[field] = st.text_input(f"{field}", value=user_data[field])
    submitted = st.form_submit_button("Xác nhận thông tin")

if submitted:
    st.subheader("3. Tạo mẫu đơn")
    mau = st.radio("Chọn mẫu đơn:", ("Khai sinh", "Cư trú"))
    template_file = "to-khai-khai-sinh.doc" if mau == "Khai sinh" else "to-khai-cu-tru.doc"
    final_docx = fill_docx_template(template_file, {
        'Họ, chữ đệm, tên người yêu cầu': user_data['Họ và tên'],
        'Ngày, tháng, năm sinh': user_data['Ngày sinh'],
        'Số định danh cá nhân/CMND': user_data['Số định danh'],
        'Quê quán': user_data['Quê quán'],
        'Nơi thường trú': user_data['Nơi thường trú'],
        'Nơi cư trú': user_data['Nơi thường trú'],
    })
    st.download_button("📥 Tải đơn đã điền", data=final_docx, file_name="don_hoan_chinh.docx", mime="application/vnd.openxmlformats-officedocument.wordprocessingml.document")
