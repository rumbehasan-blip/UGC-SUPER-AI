
import streamlit as st
import replicate
import os

# --- 1. KONFIGURASI HALAMAN ---
st.set_page_config(page_title="UGC AI Generator", layout="wide")

# --- 2. TEMA VISUAL (DARK MODE) ---
st.markdown("""
    <style>
    .stApp { background-color: #0e1117; color: white; }
    [data-testid="stSidebar"] { background-color: #1a1c24; }
    .stButton>button { width: 100%; border-radius: 8px; background-color: #007bff; color: white; }
    </style>
    """, unsafe_allow_html=True)

# --- 3. FUNGSI UTAMA AI (REPLICATE) ---
def generate_ugc(model_img, product_img):
    # Mengambil token dari Secrets Streamlit
    replicate_token = st.secrets["REPLICATE_API_TOKEN"]
    os.environ["REPLICATE_API_TOKEN"] = replicate_token
    
    # Memanggil model IDM-VTON untuk hasil cepat & otomatis
    output = replicate.run(
        "yisol/idm-vton:c871d0bc",
        input={
            "human_img": model_img,
            "garm_img": product_img,
            "garment_des": "full outfit",
            "is_checked": True
        }
    )
    return output

# --- 4. ANTARMUKA PENGGUNA (UI) ---
st.title("👥 Generator UGC Full Body")

col1, col2 = st.columns(2)

with col1:
    st.header("📤 Unggah Foto")
    foto_model = st.file_uploader("Upload Foto Model", type=["jpg", "png"])
    foto_produk = st.file_uploader("Upload Foto Produk (Setelan)", type=["jpg", "png"])

with col2:
    st.header("🖼️ Hasil Preview")
    if st.button("🔥 Generate Sekarang"):
        if foto_model and foto_produk:
            with st.spinner("Sedang memproses..."):
                hasil = generate_ugc(foto_model, foto_produk)
                st.image(hasil, caption="Hasil UGC Otomatis")
        else:
            st.error("Silakan unggah kedua foto terlebih dahulu!")
