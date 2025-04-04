import streamlit as st
import pandas as pd 
import os
import matplotlib.pyplot as plt
import altair as alt

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

try:
    # Pastikan kolom price sudah float
    df["price"] = pd.to_numeric(df["price"], errors='coerce')

    st.write(f"💸 Rata-rata harga: Rp {df['price'].mean():,.0f}")
    st.write(f"📈 Harga tertinggi: Rp {df['price'].max():,.0f}")
    st.write(f"📉 Harga terendah: Rp {df['price'].min():,.0f}")

    # Histogram
    st.subheader("📊 Distribusi Harga Properti (Histogram)")
    fig, ax = plt.subplots()
    ax.hist(df["price"].dropna(), bins=10, color="skyblue")
    ax.set_xlabel("Harga (Rp)")
    ax.set_ylabel("Jumlah Properti")
    ax.set_title("Distribusi Harga")
    st.pyplot(fig)

    # Harga vs Kamar Mandi / Kamar Tidur
    st.subheader("📈 Harga vs Jumlah Kamar Mandi")
    scatter_chart = alt.Chart(df).mark_circle(size=60).encode(
        x=alt.X('bathroom:Q', title='Jumlah Kamar Mandi'),
        y=alt.Y('price:Q', title='Harga Properti'),
        tooltip=['title', 'price', 'bathroom']
    ).interactive()
    st.altair_chart(scatter_chart, use_container_width=True)

    # Rata-rata Harga per Kota
    st.subheader("🏙️ Rata-rata Harga Properti per Kota")
    avg_price_per_city = df.groupby("city")["price"].mean().reset_index()

    bar_chart = alt.Chart(avg_price_per_city).mark_bar().encode(
        x=alt.X("city:N", sort='-y'),
        y=alt.Y("price:Q", title="Rata-rata Harga"),
        tooltip=["city", "price"]
    ).properties(width=700)

    st.altair_chart(bar_chart, use_container_width=True)

    # Boxplot
    st.subheader("Sebaran Harga Properti (Boxplot)")

    fig2, ax2 = plt.subplots()
    ax2.boxplot(df["price"], vert=False)
    ax2.set_xlabel("Harga (Rp)")
    st.pyplot(fig2)

    # Altair Chart (interaktif)
    st.subheader("📈 Visualisasi Interaktif Harga (Altair)")
    alt_chart = alt.Chart(df).mark_bar().encode(
        alt.X("price", bin=alt.Bin(maxbins=20), title="Harga (Rp)"),
        y='count()',
        tooltip=["count()"]
    ).properties(width=700, height=400)

    st.altair_chart(alt_chart, use_container_width=True)

except:
    st.warning("⚠️ Kolom harga tidak bisa dianalisis. Format harga bermasalah.")

# ================= Full Data ===================

if st.checkbox("Tampilkan semua kolom lengkap"):
    st.subheader("📄 Data Lengkap")
    st.dataframe(df)

# ================= FOOTER ===================
st.markdown("---")
st.caption("Build by Tiyas A")