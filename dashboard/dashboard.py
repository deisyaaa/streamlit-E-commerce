import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import streamlit as st

# Set style seaborn
sns.set(style='darkgrid')

# Load data
@st.cache_data
def load_data():
    df = pd.read_csv("main_data.zip")
    df["order_purchase_timestamp"] = pd.to_datetime(df["order_purchase_timestamp"])
    return df

df = load_data()

# --- SIDEBAR (FITUR INTERAKTIF) ---
with st.sidebar:
    st.title("Deisa Anggella Adista")
    st.markdown("**ID Dicoding:** CDCC525D6X0090")
    
    st.write("### Filter Data")
    
    # Mengambil nilai minimum dan maksimum dari kolom tanggal
    min_date = df["order_purchase_timestamp"].dt.date.min()
    max_date = df["order_purchase_timestamp"].dt.date.max()
    
    # Menambahkan widget date_input
    try:
        start_date, end_date = st.date_input(
            label='Pilih Rentang Waktu',
            min_value=min_date,
            max_value=max_date,
            value=[min_date, max_date]
        )
    except ValueError:
        st.error("Silakan pilih tanggal mulai dan tanggal akhir.")
        st.stop()

# --- FILTER DATAFRAME UTAMA ---
# Dataframe ini yang akan digunakan untuk semua visualisasi di bawah agar dinamis
# Ditambahkan .copy() agar tidak muncul warning di terminal
main_df = df[(df["order_purchase_timestamp"].dt.date >= start_date) & 
             (df["order_purchase_timestamp"].dt.date <= end_date)].copy()

# --- MAIN PAGE ---
st.title('E-Commerce Dashboard 🛒')

# Menampilkan informasi ringkas berdasarkan filter
st.markdown(f"**Menampilkan data dari: {start_date} hingga {end_date}**")
st.write(f"Total Pesanan: **{main_df['order_id'].nunique()}** pesanan")

# Membuat Tab
tab1, tab2, tab3, tab4 = st.tabs(["Tren Pesanan", "Demografi", "Produk Terlaris", "RFM Analysis"])

# TAB 1: Tren Pesanan
with tab1:
    st.subheader("Tren Jumlah Pesanan")
    # Menggunakan main_df agar dinamis
    main_df['year_month'] = main_df['order_purchase_timestamp'].dt.strftime('%Y-%m')
    monthly_orders = main_df.groupby('year_month')['order_id'].nunique().reset_index()

    if not monthly_orders.empty:
        fig, ax = plt.subplots(figsize=(10, 5))
        sns.lineplot(x='year_month', y='order_id', data=monthly_orders, marker='o', color="#72BCD4", linewidth=2)
        plt.xticks(rotation=45)
        ax.set_xlabel("Bulan")
        ax.set_ylabel("Jumlah Pesanan")
        st.pyplot(fig)
    else:
        st.warning("Tidak ada data pada rentang waktu yang dipilih.")

# TAB 2: Demografi Pelanggan
with tab2:
    st.subheader("Top 10 Kota Pelanggan")
    top_cities = main_df['customer_city'].value_counts().head(10).reset_index()
    top_cities.columns = ['customer_city', 'customer_count']

    if not top_cities.empty:
        fig, ax = plt.subplots(figsize=(10, 5))
        sns.barplot(x='customer_count', y='customer_city', data=top_cities, color="#72BCD4")
        ax.set_xlabel("Jumlah Pelanggan")
        ax.set_ylabel("Kota")
        st.pyplot(fig)
    else:
        st.warning("Tidak ada data pada rentang waktu yang dipilih.")

# TAB 3: Performa Produk
with tab3:
    st.subheader("5 Kategori Produk Terlaris")
    top_products = main_df['product_category_name_english'].value_counts().head(5).reset_index()
    top_products.columns = ['product_category', 'quantity_sold']

    if not top_products.empty:
        fig, ax = plt.subplots(figsize=(10, 5))
        sns.barplot(x="quantity_sold", y="product_category", data=top_products, color="#72BCD4")
        ax.set_xlabel("Jumlah Terjual")
        ax.set_ylabel("Kategori Produk")
        st.pyplot(fig)
    else:
        st.warning("Tidak ada data pada rentang waktu yang dipilih.")

# TAB 4: RFM Analysis
with tab4:
    st.subheader("RFM Analysis (Top 5 Pelanggan)")
    if not main_df.empty:
        recent_date = main_df['order_purchase_timestamp'].dt.date.max()
        rfm_df = main_df.groupby('customer_id', as_index=False).agg({
            'order_purchase_timestamp': 'max',
            'order_id': 'nunique',
            'price': 'sum'
        })
        rfm_df.columns = ['customer_id', 'max_order_timestamp', 'frequency', 'monetary']
        rfm_df['max_order_timestamp'] = rfm_df['max_order_timestamp'].dt.date
        rfm_df['recency'] = rfm_df['max_order_timestamp'].apply(lambda x: (recent_date - x).days)

        fig, ax = plt.subplots(nrows=1, ncols=3, figsize=(15, 5))
        
        sns.barplot(y="recency", x="customer_id", data=rfm_df.sort_values(by="recency", ascending=True).head(5), color="#72BCD4", ax=ax[0])
        ax[0].set_title("Recency")
        ax[0].set_xticks([]) # Menyembunyikan teks ID yang terlalu panjang
        ax[0].set_xlabel("Customer")

        sns.barplot(y="frequency", x="customer_id", data=rfm_df.sort_values(by="frequency", ascending=False).head(5), color="#72BCD4", ax=ax[1])
        ax[1].set_title("Frequency")
        ax[1].set_xticks([])
        ax[1].set_xlabel("Customer")

        sns.barplot(y="monetary", x="customer_id", data=rfm_df.sort_values(by="monetary", ascending=False).head(5), color="#72BCD4", ax=ax[2])
        ax[2].set_title("Monetary")
        ax[2].set_xticks([])
        ax[2].set_xlabel("Customer")

        st.pyplot(fig)
    else:
        st.warning("Tidak ada data pada rentang waktu yang dipilih.")

st.caption("E-Commerce Public Dataset Dashboard")