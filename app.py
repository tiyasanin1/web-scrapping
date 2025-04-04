import streamlit as st
import pandas as pd 
import os

# Konfigurasi halaman
st.set_page_config(page_title="Bukit Vista Property", layout="wide")

# Judul aplikasi
st.title("Bukit Vista Property Listings")

# Load CSV dari folder data/
csv_path = os.path.join("data", "data_scraping.csv")
df = pd.read_csv(csv_path)

# Menampilkan jumlah data
st.subheader("Dataset Overview")
st.write(f"Jumlah properti yang tersedia: {len(df)}")
st.dataframe(df.drop(columns=['property_links']).head())

# ================= FILTER ===================

# Pencarian berdasarkan judul
st.subheader("🔎 Cari Properti")
search_term = st.text_input("Masukkan kata kunci judul properti:")

# Filter berdasarkan kota
city_list = ["All"] + sorted(df["city"].dropna().unique().tolist())
selected_city = st.selectbox("📍 Filter berdasarkan kota:", city_list)

# Terapkan filter
filtered_df = df.copy()

if search_term:
    filtered_df = filtered_df[filtered_df["title"].str.contains(search_term, case=False, na=False)]

if selected_city != "All":
    filtered_df = filtered_df[filtered_df["city"] == selected_city]

# ================= TAMPILAN ===================

# Tampilkan data setelah filter
st.subheader("Hasil Properti")
st.write(f"Menampilkan {len(filtered_df)} hasil properti")
st.dataframe(filtered_df.drop(columns=['property_links']))

# ================= STATISTIK ===================

st.subheader("Statistik Harga Properti")

# Bersihkan kolom harga: ubah string ke angka
try:
    df["price_clean"] = df["price"].str.replace(r"[^\d]", "", regex=True).astype(float)

    st.write(f"💸 Rata-rata harga: Rp {df['price_clean'].mean():,.0f}")
    st.write(f"📈 Harga tertinggi: Rp {df['price_clean'].max():,.0f}")
    st.write(f"📉 Harga terendah: Rp {df['price_clean'].min():,.0f}")

except:
    st.warning("⚠️ Kolom harga tidak bisa dianalisis. Format harga bermasalah.")

# ================= OPSIONAL TAMBAHAN ===================

if st.checkbox("Tampilkan semua kolom lengkap"):
    st.subheader("📄 Data Lengkap")
    st.dataframe(df)

# ================= FOOTER ===================
st.markdown("---")
st.caption("Build by Tiyas A")