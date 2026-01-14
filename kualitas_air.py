import streamlit as st
import pandas as pd
import numpy as np
import plotly.graph_objects as go
from datetime import datetime
import os

# --- KONFIGURASI HALAMAN ---
st.set_page_config(
    page_title="Sistem Pakar Penilaian Kualitas Air Tambak Ikan",
    page_icon="🐟",
    layout="wide",
    initial_sidebar_state="expanded"
)

# --- STYLING CSS CUSTOM ---
st.markdown("""
<style>
    /* Font & Warna Tema */
    @import url('https://fonts.googleapis.com/css2?family=Poppins:wght@300;400;500;600;700&display=swap');
    
    * {
        font-family: 'Poppins', sans-serif;
    }
    
    /* Tema Warna Biru Laut */
    :root {
        --primary-color: #1a6fa0;
        --secondary-color: #2e9cca;
        --accent-color: #33cccc;
        --light-color: #e6f7ff;
        --dark-color: #0d3b66;
        --success-color: #2ecc71;
        --warning-color: #f39c12;
        --danger-color: #e74c3c;
        --bg-gradient: linear-gradient(135deg, #f5f7fa 0%, #e6f7ff 100%);
        --card-shadow: 0 8px 16px rgba(26, 111, 160, 0.15);
    }
    
    /* Background Utama */
    .stApp {
        background: var(--bg-gradient);
    }
    
    /* Sidebar */
    [data-testid="stSidebar"] {
        background: linear-gradient(180deg, var(--dark-color) 0%, var(--primary-color) 100%);
        color: white;
    }
    
    [data-testid="stSidebar"] .stRadio > div {
        background: rgba(255, 255, 255, 0.1);
        padding: 8px;
        border-radius: 10px;
    }
    
    [data-testid="stSidebar"] .stRadio label {
        color: white !important;
        font-weight: 500;
    }
    
    [data-testid="stSidebar"] .stRadio div[data-baseweb="radio"] {
        margin-bottom: 10px;
    }
    
    /* Header */
    .main-header {
        background: linear-gradient(90deg, var(--primary-color) 0%, var(--secondary-color) 100%);
        color: white;
        padding: 1.5rem;
        border-radius: 15px;
        margin-bottom: 2rem;
        box-shadow: var(--card-shadow);
        text-align: center;
    }
    
    .main-header h1 {
        color: white;
        font-weight: 700;
        margin-bottom: 0.5rem;
        font-size: 2.5rem;
    }
    
    .main-header p {
        color: rgba(255, 255, 255, 0.9);
        font-size: 1.1rem;
    }
    
    /* Cards */
    .custom-card {
        background: white;
        border-radius: 15px;
        padding: 1.5rem;
        box-shadow: var(--card-shadow);
        border: none;
        margin-bottom: 1.5rem;
        border-left: 5px solid var(--accent-color);
    }
    
    .metric-card {
        background: linear-gradient(135deg, #ffffff 0%, #f8fdff 100%);
        border-radius: 12px;
        padding: 1.2rem;
        box-shadow: 0 4px 12px rgba(0, 0, 0, 0.05);
        border: 1px solid rgba(51, 204, 204, 0.2);
        text-align: center;
        transition: transform 0.3s ease;
    }
    
    .metric-card:hover {
        transform: translateY(-5px);
    }
    
    /* Tombol */
    .stButton button {
        background: linear-gradient(90deg, var(--primary-color) 0%, var(--secondary-color) 100%);
        color: white;
        border: none;
        padding: 0.75rem 2rem;
        border-radius: 8px;
        font-weight: 600;
        font-size: 1rem;
        transition: all 0.3s ease;
        width: 100%;
    }
    
    .stButton button:hover {
        background: linear-gradient(90deg, var(--secondary-color) 0%, var(--accent-color) 100%);
        transform: translateY(-2px);
        box-shadow: 0 6px 12px rgba(46, 156, 202, 0.3);
    }
    
    /* File Uploader */
    .stFileUploader {
        border: 2px dashed var(--primary-color);
        border-radius: 10px;
        padding: 2rem;
        background: rgba(230, 247, 255, 0.5);
    }
    
    .stFileUploader:hover {
        border-color: var(--accent-color);
        background: rgba(51, 204, 204, 0.1);
    }
    
    /* Slider */
    .stSlider div[data-baseweb="slider"] {
        margin-top: 10px;
        margin-bottom: 20px;
    }
    
    /* Tabs & Divider */
    .stTabs [data-baseweb="tab-list"] {
        background: transparent;
        gap: 2px;
    }
    
    .stTabs [data-baseweb="tab"] {
        background: white;
        border-radius: 8px 8px 0 0;
        padding: 10px 20px;
        font-weight: 500;
    }
    
    .stTabs [aria-selected="true"] {
        background: var(--primary-color) !important;
        color: white !important;
    }
    
    /* Status Badges */
    .status-badge {
        display: inline-block;
        padding: 0.4rem 1rem;
        border-radius: 20px;
        font-weight: 600;
        font-size: 0.9rem;
        text-transform: uppercase;
        letter-spacing: 0.5px;
    }
    
    .status-good {
        background: linear-gradient(90deg, #2ecc71, #27ae60);
        color: white;
    }
    
    .status-fair {
        background: linear-gradient(90deg, #f39c12, #e67e22);
        color: white;
    }
    
    .status-poor {
        background: linear-gradient(90deg, #e74c3c, #c0392b);
        color: white;
    }
    
    /* Animations */
    @keyframes fadeIn {
        from { opacity: 0; transform: translateY(10px); }
        to { opacity: 1; transform: translateY(0); }
    }
    
    .fade-in {
        animation: fadeIn 0.5s ease-out;
    }
    
    /* Footer */
    .footer {
        text-align: center;
        padding: 1.5rem;
        margin-top: 3rem;
        color: var(--dark-color);
        font-size: 0.9rem;
        border-top: 1px solid rgba(13, 59, 102, 0.1);
    }
    
    /* Dataset Info Card */
    .dataset-card {
        background: linear-gradient(135deg, #ffffff 0%, #f0f9ff 100%);
        border-radius: 12px;
        padding: 1.5rem;
        border: 2px solid var(--accent-color);
        margin-bottom: 1.5rem;
    }
    
    .dataset-info {
        display: flex;
        justify-content: space-between;
        align-items: center;
        margin-bottom: 1rem;
    }
    
    .dataset-stats {
        display: grid;
        grid-template-columns: repeat(auto-fit, minmax(120px, 1fr));
        gap: 1rem;
        margin-top: 1rem;
    }
    
    .stat-item {
        text-align: center;
        padding: 0.8rem;
        background: rgba(230, 247, 255, 0.5);
        border-radius: 8px;
    }
</style>
""", unsafe_allow_html=True)

# --- FUNGSI LOAD DATASET DARI FILE ---
def load_and_learn_data(file_path=None, uploaded_file=None):
    """
    Membaca CSV dari file path atau uploaded file dan mempelajari statistik dasar.
    """
    try:
        if uploaded_file is not None:
            # Baca dari uploaded file
            df = pd.read_csv(uploaded_file)
        else:
            # Baca dari file path
            df = pd.read_csv(file_path)
        
        # Validasi struktur file
        required_columns = ['pH', 'Temp', 'Turbidity', 'DO', 'Conductivity']
        
        # Cek apakah file memiliki kolom yang tepat
        if len(df.columns) >= 6:
            # Jika file memiliki lebih dari 6 kolom, ambil 6 kolom pertama
            df = df.iloc[:, :6]
            df.columns = ['ID', 'pH', 'Temp', 'Turbidity', 'DO', 'Conductivity']
        else:
            # Jika jumlah kolom tidak sesuai, tampilkan error
            st.error("Format file tidak valid. File harus memiliki minimal 6 kolom.")
            return None, None
        
        # 'Belajar' dari data: Menghitung statistik deskriptif
        stats = {
            'pH': {'mean': df['pH'].mean(), 'std': df['pH'].std(), 'ideal_min': 6.5, 'ideal_max': 8.5},
            'Temp': {'mean': df['Temp'].mean(), 'std': df['Temp'].std(), 'ideal_min': 20, 'ideal_max': 32},
            'Turbidity': {'mean': df['Turbidity'].mean(), 'std': df['Turbidity'].std(), 'ideal_max': 25},
            'DO': {'mean': df['DO'].mean(), 'std': df['DO'].std(), 'critical_min': 3, 'good_min': 5},
            'Conductivity': {'mean': df['Conductivity'].mean(), 'std': df['Conductivity'].std()}
        }
        return df, stats
    except Exception as e:
        st.error(f"Gagal memuat data: {str(e)}")
        return None, None

# --- FUNGSI VALIDASI FILE ---
def validate_file(file):
    """Validasi file yang diupload"""
    if file is None:
        return False, "File tidak ditemukan"
    
    # Cek ekstensi file
    if not file.name.endswith('.csv'):
        return False, "File harus berformat CSV"
    
    # Cek ukuran file (maksimal 10MB)
    if file.size > 10 * 1024 * 1024:
        return False, "Ukuran file maksimal 10MB"
    
    return True, "File valid"

# --- MESIN INFERENSI (LOGIKA PAKAR) ---
def calculate_quality(ph, temp, turb, do, cond, stats):
    """
    Menghitung skor kualitas air menggunakan metode Weighted Quality Index (WQI)
    yang disesuaikan dengan aturan pakar dan statistik data historis.
    """
    scores = []
    reasons = []
    actions = []

    # 1. Penilaian pH (Bobot: 20%)
    # Aturan: Ideal 6.5-8.5, atau dalam rentang deviasi data historis
    if 6.5 <= ph <= 8.5:
        ph_score = 100
    elif (stats['pH']['mean'] - 2*stats['pH']['std']) <= ph <= (stats['pH']['mean'] + 2*stats['pH']['std']):
        ph_score = 70 # Masih oke secara historis meski agak asam/basa
        reasons.append("pH sedikit di luar ideal tapi dalam batas historis.")
    else:
        ph_score = 40
        reasons.append("pH berada di level berbahaya.")
        if ph < 6.5: actions.append("Tambahkan Kapur (Lime) untuk menaikkan pH.")
        if ph > 8.5: actions.append("Ganti sebagian air atau aplikasi bahan organik fermentasi.")

    # 2. Penilaian Temperature (Bobot: 10%)
    if 20 <= temp <= 30:
        temp_score = 100
    else:
        temp_score = 50
        reasons.append(f"Suhu {temp}°C kurang optimal untuk pertumbuhan ikan.")
        actions.append("Pantau suhu, sesuaikan kedalaman air atau peneduh jika perlu.")

    # 3. Penilaian DO / Oksigen Terlarut (Bobot: 35%) - PALING KRITIS
    if do >= 5:
        do_score = 100
    elif 3 <= do < 5:
        do_score = 60
        reasons.append("Oksigen terlarut mulai rendah.")
        actions.append("Nyalakan kincir air/aerator segera.")
    else:
        do_score = 20
        reasons.append("BAHAYA: Oksigen sangat rendah (Hipoksia).")
        actions.append("DARURAT: Nyalakan semua aerator, kurangi pakan, ganti air baru.")

    # 4. Penilaian Turbidity / Kekeruhan (Bobot: 15%)
    if turb <= 10:
        turb_score = 100
    elif turb <= 30:
        turb_score = 70
    else:
        turb_score = 40
        reasons.append("Air terlalu keruh.")
        actions.append("Cek sirkulasi, endapkan partikel lumpur, atau cek filter.")

    # 5. Penilaian Conductivity (Bobot: 20%)
    # Menggunakan statistik data karena konduktivitas sangat bergantung lokasi
    lower_limit = stats['Conductivity']['mean'] - 2*stats['Conductivity']['std']
    upper_limit = stats['Conductivity']['mean'] + 2*stats['Conductivity']['std']
    
    if lower_limit <= cond <= upper_limit:
        cond_score = 100
    else:
        cond_score = 50
        reasons.append("Konduktivitas tidak wajar dibanding data historis.")
        actions.append("Cek salinitas atau kandungan mineral air.")

    # Hitung Final Weighted Score
    final_score = (ph_score * 0.20) + (temp_score * 0.10) + (do_score * 0.35) + (turb_score * 0.15) + (cond_score * 0.20)

    # Klasifikasi Output
    if final_score >= 80:
        status = "BAIK"
        color = "#2ecc71"
    elif 50 <= final_score < 80:
        status = "CUKUP"
        color = "#f39c12"
    else:
        status = "BURUK"
        color = "#e74c3c"

    return status, final_score, reasons, actions, color

# --- KOMPONEN UI YANG DIPERBAIKI ---
def create_metric_card(title, value, unit="", delta=None):
    """Membuat kartu metrik yang lebih menarik"""
    if delta:
        delta_text = f" ({delta})"
    else:
        delta_text = ""
    
    st.markdown(f"""
    <div class="metric-card fade-in">
        <h3 style="color: #1a6fa0; font-size: 1rem; margin-bottom: 0.5rem;">{title}</h3>
        <h2 style="color: #0d3b66; font-size: 2rem; margin: 0; font-weight: 700;">{value}{unit}</h2>
        <p style="color: #666; font-size: 0.9rem; margin-top: 0.5rem;">{delta_text}</p>
    </div>
    """, unsafe_allow_html=True)

def create_parameter_card(title, description, value, min_val, max_val, step):
    """Membuat kartu input parameter yang lebih baik"""
    st.markdown(f"""
    <div class="custom-card fade-in" style="margin-bottom:0.5rem;">
        <h3 style="color: #1a6fa0; margin-bottom: 0.5rem;">{title}</h3>
        <p style="color: #666; font-size: 0.9rem; margin-bottom: 1rem;">{description}</p>
    </div>
    """, unsafe_allow_html=True)
    
    return st.slider(f"**{title}**", min_value=min_val, max_value=max_val, value=value, step=step, label_visibility="collapsed")

def create_status_badge(status):
    """Membuat badge status dengan styling yang lebih baik"""
    if status == "BAIK":
        badge_class = "status-good"
    elif status == "CUKUP":
        badge_class = "status-fair"
    else:
        badge_class = "status-poor"
    
    st.markdown(f"""
    <div class="fade-in" style="text-align: center; margin: 1.5rem 0;">
        <span class="status-badge {badge_class}">
            {status}
        </span>
    </div>
    """, unsafe_allow_html=True)

def display_dataset_info(df, stats, source):
    """Menampilkan informasi dataset yang telah dimuat"""
    st.markdown(f"""
    <div class="dataset-card fade-in">
        <div class="dataset-info">
            <div>
                <h3 style="color: #1a6fa0; margin: 0;">📊 Dataset Berhasil Dimuat</h3>
                <p style="color: #666; margin: 0.5rem 0 0 0;">Sumber: {source}</p>
            </div>
            <div style="text-align: right;">
                <span style="background: var(--success-color); color: white; padding: 0.3rem 0.8rem; border-radius: 20px; font-size: 0.9rem;">
                    ✅ Ready
                </span>
            </div>
        </div>       
        <div class="dataset-stats">
            <div class="stat-item">
                <h4 style="color: var(--primary-color); margin: 0;">Total Data</h4>
                <p style="color: var(--dark-color); font-size: 1.5rem; font-weight: bold; margin: 0.5rem 0 0 0;">{len(df)}</p>
            </div>
            <div class="stat-item">
                <h4 style="color: var(--primary-color); margin: 0;">Kolom</h4>
                <p style="color: var(--dark-color); font-size: 1.5rem; font-weight: bold; margin: 0.5rem 0 0 0;">6</p>
            </div>
            <div class="stat-item">
                <h4 style="color: var(--primary-color); margin: 0;">Parameter</h4>
                <p style="color: var(--dark-color); font-size: 1.5rem; font-weight: bold; margin: 0.5rem 0 0 0;">5</p>
            </div>
            <div class="stat-item">
                <h4 style="color: var(--primary-color); margin: 0;">Format</h4>
                <p style="color: var(--dark-color); font-size: 1.5rem; font-weight: bold; margin: 0.5rem 0 0 0;">CSV</p>
            </div>
        </div>
    </div>
    """, unsafe_allow_html=True)
    
    # Tampilkan preview data
    with st.expander("📋 Lihat Preview Data", expanded=False):
        
        st.dataframe(df.head(10).style.background_gradient(subset=['pH', 'Temp', 'DO', 'Turbidity', 'Conductivity'], 
                                                              cmap='Blues'), use_container_width=True)
        
        st.markdown("""
            <div style="background: #e6f7ff; padding: 1rem; border-radius: 10px; margin-top: 1rem;">
                <h4 style="color: #0d3b66; margin-top: 0;">ℹ️ Struktur File</h4>
                <ul style="color: #0d3b66; font-size: 0.9rem; padding-left: 1.2rem;">
                    <li>Kolom 1: ID</li>
                    <li>Kolom 2: pH</li>
                    <li>Kolom 3: Suhu</li>
                    <li>Kolom 4: Kekeruhan</li>
                    <li>Kolom 5: DO</li>
                    <li>Kolom 6: Konduktivitas</li>
                </ul>
            </div>
            """, unsafe_allow_html=True)

# --- MAIN APP ---
def main():
    # Inisialisasi Session State
    if 'history' not in st.session_state:
        st.session_state.history = []
    
    if 'dataset_loaded' not in st.session_state:
        st.session_state.dataset_loaded = False
    
    if 'df' not in st.session_state:
        st.session_state.df = None
    
    if 'stats' not in st.session_state:
        st.session_state.stats = None

    # Sidebar Navigasi dengan styling yang lebih baik
    with st.sidebar:
        st.markdown("""
        <div style="text-align: left;">
            <h1 style="color: white; font-size: 1.8rem; margin-bottom: 0.5rem;">🌊 AquaExpert</h1>
            <p style="color: rgba(255,255,255,0.8); font-size: 0.9rem;">Sistem Pakar Kualitas Air Tambak</p>
            <style>
                /* Mengubah warna teks pada setiap opsi radio button */
                div[role="radiogroup"] label p {
                    color: white !important;
                }

                /* Mengubah warna garis pemisah (---) menjadi putih */
                hr {
                    border: 0;
                    height: 1px;
                    background-image: linear-gradient(to right, rgba(255, 255, 255, 0), rgba(255, 255, 255, 0.75), rgba(255, 255, 255, 0));
                    background-color: white !important;
                }
            </style>
        </div>
        """, unsafe_allow_html=True)
        
        menu_options = ["📂 Load Dataset", "🏠 Beranda", "🔍 Penilaian Kualitas", "📜 Riwayat Penilaian", "ℹ️ Tentang Sistem"]
        menu = st.radio(
            "Navigasi Menu ",
            menu_options,
            label_visibility="collapsed"
        )
        
        st.markdown("---")
        
        # Tampilkan status dataset jika sudah dimuat
        if st.session_state.dataset_loaded and st.session_state.df is not None:
            st.markdown(f"""
            <div style="background: rgba(255, 255, 255, 0.1); padding: 0.8rem; border-radius: 10px; margin: 1rem 0;">
                <p style="color: white; margin: 0; font-size: 0.9rem;">
                    <strong>📊 Dataset:</strong> {len(st.session_state.df)} data
                </p>
                <p style="color: rgba(255, 255, 255, 0.8); margin: 0.3rem 0 0 0; font-size: 0.8rem;">
                    Status: ✅ Loaded
                </p>
            </div>
            """, unsafe_allow_html=True)
        
        st.markdown("""
        <div style="color: rgba(255,255,255,0.7); padding: 1rem 0; font-size: 0.85rem;">
            <p><strong>Python Version:</strong> 3.13</p>
            <p><strong>Last Updated:</strong> Januari 2026</p>
        </div>
        """, unsafe_allow_html=True)

    # Konten berdasarkan menu yang dipilih
    if menu == "📂 Load Dataset":
        st.markdown("""
        <div class="main-header">
            <h1>📂 Load Dataset</h1>
            <p>Muat dataset kualitas air tambak untuk memulai analisis</p>
        </div>
        """, unsafe_allow_html=True)
        
        # Tabs untuk pilihan load dataset
        tab1, tab2 = st.tabs(["📁 Upload File CSV", "📂 Gunakan Dataset Default"])
        
        with tab1:
            st.markdown("""
            <div class="custom-card">
                <h2 style="color: #1a6fa0;">📁 Upload Dataset CSV</h2>
                <p style="color: #666;">
                Unggah file CSV Anda yang berisi data kualitas air tambak. File harus memiliki struktur kolom sebagai berikut:
                </p>
                <ul style="color: #666; padding-left: 1.5rem;">
                    <li><strong>Kolom 1:</strong> ID (identifikasi unik)</li>
                    <li><strong>Kolom 2:</strong> pH (Derajat Keasaman)</li>
                    <li><strong>Kolom 3:</strong> Temp (Suhu dalam °C)</li>
                    <li><strong>Kolom 4:</strong> Turbidity (Kekeruhan dalam NTU)</li>
                    <li><strong>Kolom 5:</strong> DO (Oksigen Terlarut dalam mg/L)</li>
                    <li><strong>Kolom 6:</strong> Conductivity (Konduktivitas dalam µS/cm)</li>
                </ul>
            </div>
            """, unsafe_allow_html=True)
            
            # File uploader
            uploaded_file = st.file_uploader(
                "Pilih file CSV",
                type=['csv'],
                help="Upload file CSV dengan struktur yang sesuai"
            )
            
            if uploaded_file is not None:
                # Validasi file
                is_valid, message = validate_file(uploaded_file)
                
                if is_valid:
                    # Tampilkan info file
                    file_details = {
                        "Nama File": uploaded_file.name,
                        "Ukuran File": f"{uploaded_file.size / 1024:.2f} KB",
                        "Tipe File": uploaded_file.type
                    }
                    
                    col1, col2 = st.columns(2)
                    with col1:
                        st.markdown("""
                        <div style="background: #e6f7ff; padding: 1rem; border-radius: 10px;">
                            <h4 style="color: #0d3b66; margin-top: 0;">📄 Detail File</h4>
                        """, unsafe_allow_html=True)
                        for key, value in file_details.items():
                            st.markdown(f"**{key}:** {value}")
                        st.markdown("</div>", unsafe_allow_html=True)
                    
                    # Tombol untuk memuat file
                    if st.button("🚀 Load Dataset dari File", use_container_width=True, type="primary"):
                        with st.spinner("Memuat dataset..."):
                            df, stats = load_and_learn_data(uploaded_file=uploaded_file)
                            
                            if df is not None and stats is not None:
                                # Simpan ke session state
                                st.session_state.df = df
                                st.session_state.stats = stats
                                st.session_state.dataset_loaded = True
                                st.session_state.dataset_source = f"Uploaded: {uploaded_file.name}"
                                
                                # Tampilkan success message
                                st.success("✅ Dataset berhasil dimuat!")
                                st.balloons()
                                
                                # Tampilkan informasi dataset
                                display_dataset_info(df, stats, f"Uploaded File: {uploaded_file.name}")
                else:
                    st.error(f"⚠️ {message}")
        
        with tab2:
            st.markdown("""
            <div class="custom-card">
                <h2 style="color: #1a6fa0;">📂 Dataset Default</h2>
                <p style="color: #666;">
                Gunakan dataset default yang telah disediakan untuk demonstrasi sistem. Dataset ini berisi data contoh kualitas air tambak ikan.
                </p>
                <div style="background: #e6f7ff; padding: 1rem; border-radius: 10px; margin: 1rem 0;">
                    <h4 style="color: #0d3b66; margin-top: 0;">📋 Spesifikasi Dataset Default:</h4>
                    <ul style="color: #0d3b66;">
                        <li>1000 baris data contoh</li>
                        <li>6 kolom parameter kualitas air</li>
                        <li>Data sintetis berdasarkan parameter standar</li>
                        <li>Cocok untuk demonstrasi dan testing</li>
                    </ul>
                </div>
            </div>
            """, unsafe_allow_html=True)
            
            # Tombol untuk menggunakan dataset default
            
            if st.button("🎯 Gunakan Dataset Default", use_container_width=True, type="secondary"):
                    try:
                        # Coba load dataset default
                        default_file = "kualitas_air.csv"
                        
                        if os.path.exists(default_file):
                            with st.spinner("Memuat dataset default..."):
                                df, stats = load_and_learn_data(file_path=default_file)
                                
                                if df is not None and stats is not None:
                                    # Simpan ke session state
                                    st.session_state.df = df
                                    st.session_state.stats = stats
                                    st.session_state.dataset_loaded = True
                                    st.session_state.dataset_source = "Default Dataset"
                                    
                                    # Tampilkan success message
                                    st.success("✅ Dataset default berhasil dimuat!")
                                    
                                    # Tampilkan informasi dataset
                                    display_dataset_info(df, stats, "Default Dataset")
                        else:
                            st.error("⚠️ File dataset default (kualitas_air.csv) tidak ditemukan.")
                            st.info("Silakan upload file CSV Anda sendiri atau pastikan file 'kualitas_air.csv' tersedia di direktori aplikasi.")
                    except Exception as e:
                        st.error(f"⚠️ Gagal memuat dataset default: {str(e)}")
        
        # Informasi jika dataset sudah dimuat
        if st.session_state.dataset_loaded:
            st.markdown("""
            <div class="custom-card" style="background: linear-gradient(135deg, #d4edda, #e6ffe6); border-left: 5px solid #2ecc71;">
                <h3 style="color: #155724; margin-top: 0;">🎉 Dataset Siap Digunakan!</h3>
                <p style="color: #155724;">
                Anda dapat melanjutkan ke menu lain untuk menggunakan dataset ini:
                </p>
                <ul style="color: #155724; padding-left: 1.5rem;">
                    <li><strong>🏠 Beranda:</strong> Lihat statistik dan overview dataset</li>
                    <li><strong>🔍 Penilaian Kualitas:</strong> Lakukan analisis kualitas air</li>
                    <li><strong>📜 Riwayat Penilaian:</strong> Lihat dan kelola riwayat analisis</li>
                </ul>
                <div style="margin-top: 1rem; text-align: center;">
                    <span style="background: #2ecc71; color: white; padding: 0.5rem 1.5rem; border-radius: 8px; font-weight: bold;">
                        ✅ Dataset Aktif
                    </span>
                </div>
            </div>
            """, unsafe_allow_html=True)
    
    # Menu lainnya hanya dapat diakses jika dataset sudah dimuat
    elif not st.session_state.dataset_loaded:
        st.markdown("""
        <div class="main-header" style="background: linear-gradient(90deg, #f39c12, #e67e22);">
            <h1>⚠️ Dataset Belum Dimuat</h1>
            <p>Silakan muat dataset terlebih dahulu untuk menggunakan fitur aplikasi</p>
        </div>
        """, unsafe_allow_html=True)
        
        
        st.markdown("""
            <div class="custom-card" style="text-align: center; width: 100%; padding: 2rem 2rem;">
                <div style="font-size: 4rem; color: #f39c12; margin-bottom: 1rem;">
                    📂
                </div>
                <h2 style="color: #1a6fa0;">Dataset Diperlukan</h2>
                <p style="color: #666; margin: 1rem;">
                Untuk menggunakan fitur aplikasi, Anda perlu memuat dataset kualitas air terlebih dahulu.
                Dataset digunakan untuk pembelajaran sistem dan sebagai baseline analisis.
                </p>              
                <div style="background: #fff3cd; padding: 1.5rem; border-radius: 10px; margin: 2rem 0;">
                    <h4 style="color: #856404; margin-top: 0;">🎯 Langkah-langkah:</h4>
                    <ol style="color: #856404; text-align: left; padding-left: 1.5rem;">
                        <li>Pilih menu <strong>"📂 Load Dataset"</strong> di sidebar</li>
                        <li>Upload file CSV Anda atau gunakan dataset default</li>
                        <li>Tunggu hingga proses loading selesai</li>
                        <li>Kembali ke menu yang diinginkan</li>
                    </ol>
                </div>
            </div>
            """, unsafe_allow_html=True)
        
        # Tips untuk dataset
        st.markdown("""
        <div class="custom-card" style="padding: 2rem 2rem;">
            <h3 style="color: #1a6fa0;">💡 Tips untuk Dataset:</h3>
            <div style="display: grid; grid-template-columns: repeat(auto-fit, minmax(300px, 1fr)); gap: 1rem; margin-top: 1rem;">
                <div style="background: #e6f7ff; padding: 1rem; border-radius: 8px;">
                    <h4 style="color: #0d3b66; margin-top: 0;">📊 Format File</h4>
                    <p style="color: #0d3b66; margin: 0.5rem 0 0 0;">
                    Gunakan format CSV dengan 6 kolom sesuai struktur yang ditentukan.
                    </p>
                </div>
                <div style="background: #e6f7ff; padding: 1rem; border-radius: 8px;">
                    <h4 style="color: #0d3b66; margin-top: 0;">🔢 Data Contoh</h4>
                    <p style="color: #0d3b66; margin: 0.5rem 0 0 0;">
                    Dataset default tersedia untuk testing jika Anda tidak memiliki data.
                    </p>
                </div>
                <div style="background: #e6f7ff; padding: 1rem; border-radius: 8px;">
                    <h4 style="color: #0d3b66; margin-top: 0;">📈 Ukuran Data</h4>
                    <p style="color: #0d3b66; margin: 0.5rem 0 0 0;">
                    Minimal 50 data untuk hasil analisis yang lebih akurat.
                    </p>
                </div>
            </div>
        </div>
        """, unsafe_allow_html=True)
        
        # Footer untuk halaman ini
        st.markdown("""
        <div class="footer">
            <p>© 2026 AquaExpert System | Sistem Pakar Penilaian Kualitas Air Tambak Ikan</p>
            <p style="font-size: 0.8rem; color: #888;">
            Dibangun dengan ❤️ menggunakan Streamlit, Plotly, dan Python
            </p>
        </div>
        """, unsafe_allow_html=True)
        
        return  # Stop eksekusi jika dataset belum dimuat
    
    # Kode untuk menu lainnya (hanya dieksekusi jika dataset sudah dimuat)
    elif menu == "🏠 Beranda":
        # Akses dataset dari session state
        df = st.session_state.df
        stats = st.session_state.stats
        
        # Header Beranda
        st.markdown(f"""
        <div class="main-header">
            <h1>🌊 AquaExpert</h1>
            <p>Sistem Pakar Penilaian Kualitas Air Tambak Ikan Berbasis AI | Dataset: {st.session_state.get('dataset_source', 'Loaded')}</p>
        </div>
        """, unsafe_allow_html=True)
        
        col1, col2 = st.columns([2, 1])
        
        with col1:
            st.markdown("""
            <div class="custom-card">
                <h2 style="color: #1a6fa0;">Selamat Datang di AquaExpert</h2>
                <p style="color: #555; line-height: 1.6;">
                Aplikasi cerdas yang dirancang khusus untuk membantu petambak ikan dalam memantau 
                dan menganalisis kualitas air tambak secara real-time. Dengan menggabungkan 
                <strong>Rule-Based Reasoning</strong> dan <strong>Data-Driven Logic</strong>, 
                sistem ini memberikan penilaian akurat dan rekomendasi tindakan berbasis 
                pengetahuan pakar akuakultur.
                </p>                
                <div style="background: #e6f7ff; padding: 1rem; border-radius: 10px; margin: 1.5rem 0;">
                <h4 style="color: #0d3b66; margin-top: 0;">✨ Fitur Unggulan:</h4>
                <ul style="color: #555;">
                    <li>Analisis kualitas air dengan 5 parameter kunci</li>
                    <li>Rekomendasi tindakan spesifik berbasis kondisi</li>
                    <li>Riwayat penilaian lengkap dengan grafik</li>
                    <li>Visualisasi data yang interaktif dan mudah dipahami</li>
                    <li>Sistem pembelajaran dari data historis</li>
                </ul>
                </div>
            </div>
            """, unsafe_allow_html=True)
        
        with col2:
            st.markdown("""
            <div class="custom-card">
                <h3 style="color: #1a6fa0; text-align: center;">⚡ Mulai Analisis</h3>
                <p style="color: #555; text-align: center; margin-bottom: 1.5rem;">
                Klik menu <strong>Penilaian Kualitas</strong> di sidebar untuk memulai analisis kondisi air tambak Anda.
                </p>
                <div style="text-align: center; font-size: 3rem; color: #33cccc; margin: 1rem 0;">
                    🐟
                </div>
                <div style="text-align: center; margin-top: 1rem;">
                    <span style="background: #e6f7ff; color: #1a6fa0; padding: 0.5rem 1rem; border-radius: 20px; font-size: 0.9rem;">
                        📊 Dataset: {len(df)} data
                    </span>
                </div>
            </div>
            """, unsafe_allow_html=True)
        
        # Statistik Data
        st.markdown("""
        <div class="custom-card">
            <h2 style="color: #1a6fa0;">📊 Statistik Data Historis</h2>
            <p style="color: #666;">Analisis statistik dari data kualitas air yang telah terkumpul:</p>
        </div>
        """, unsafe_allow_html=True)
        
        if df is not None and stats is not None:
            col1, col2, col3 = st.columns(3)
            
            with col1:
                create_metric_card("pH Rata-rata", f"{stats['pH']['mean']:.2f}", "")
            with col2:
                create_metric_card("Suhu Rata-rata", f"{stats['Temp']['mean']:.1f}", "°C")
            with col3:
                create_metric_card("DO Rata-rata", f"{stats['DO']['mean']:.1f}", "mg/L")
            
            st.markdown("<div style='margin-top: 1rem;'></div>", unsafe_allow_html=True)

            col1, col2 = st.columns(2)
            with col1:
                create_metric_card("Kekeruhan", f"{stats['Turbidity']['mean']:.1f}", "NTU")
            with col2:
                create_metric_card("Konduktivitas", f"{stats['Conductivity']['mean']:.0f}", "µS/cm")
        
        # Preview Data
        st.markdown("""
        <div class="custom-card" style="margin-top: 1rem;">
            <h2 style="color: #1a6fa0;">📋 Preview Data Historis</h2>
        </div>
        """, unsafe_allow_html=True)	
        
        with st.expander("Lihat Data Historis", expanded=False):
            st.dataframe(df.head(10).style.background_gradient(subset=['pH', 'Temp', 'DO', 'Turbidity', 'Conductivity'], 
                                                              cmap='Blues'), use_container_width=True)
            
    elif menu == "🔍 Penilaian Kualitas":
        # Akses dataset dari session state
        df = st.session_state.df
        stats = st.session_state.stats
        
        # Header Penilaian
        st.markdown(f"""
        <div class="main-header">
            <h1>🔍 Penilaian Kualitas Air</h1>
            <p>Masukkan parameter air terkini untuk mendapatkan analisis dan rekomendasi | Dataset: {len(df)} data</p>
        </div>
        """, unsafe_allow_html=True)
        
        col1, col2 = st.columns([1, 1.2], gap="medium")
        
        with col1:
            st.markdown("""
            <div class="custom-card">
                <h2 style="color: #1a6fa0;">⚙️ Input Parameter</h2>
                <p style="color: #666;">Masukkan data hasil pengukuran alat di lapangan:</p>
            </div>
            """, unsafe_allow_html=True)
            
            # Input Parameter dengan styling yang lebih baik
            in_ph = create_parameter_card(
                "pH (Derajat Keasaman)",
                "Ideal: 6.5 - 8.5",
                float(stats['pH']['mean']),
                0.0, 14.0, 0.1
            )
            
            in_temp = create_parameter_card(
                "Suhu / Temperature",
                "Ideal: 20°C - 30°C",
                float(stats['Temp']['mean']),
                0.0, 50.0, 0.1
            )
            
            in_do = create_parameter_card(
                "DO / Oksigen Terlarut",
                "Kritis jika < 3 mg/L",
                float(stats['DO']['mean']),
                0.0, 20.0, 0.1
            )
            
            in_turb = create_parameter_card(
                "Turbidity / Kekeruhan",
                "Satuan: NTU",
                float(stats['Turbidity']['mean']),
                0.0, 100.0, 0.1
            )
            
            in_cond = create_parameter_card(
                "Conductivity",
                "Satuan: µS/cm",
                float(stats['Conductivity']['mean']),
                0.0, 2000.0, 1.0
            )
            
            # Tombol Analisis
            if st.button("🔍 Analisis Kualitas Air", use_container_width=True, type="primary"):
                status, score, reasons, actions, color = calculate_quality(in_ph, in_temp, in_turb, in_do, in_cond, stats)
                
                # Simpan ke riwayat
                timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                result_entry = {
                    "Waktu": timestamp,
                    "pH": in_ph, "Suhu": in_temp, "DO": in_do, "NTU": in_turb, "Cond": in_cond,
                    "Status": status, "Skor": round(score, 2)
                }
                st.session_state.history.append(result_entry)
                
                # Tampilkan Hasil di Session State agar persist saat rerun
                st.session_state.last_result = (status, score, reasons, actions, color)
                
                # Show success message
                st.success("Analisis berhasil dilakukan!")
                
        with col2:
            if 'last_result' in st.session_state:
                status, score, reasons, actions, color = st.session_state.last_result
                
                st.markdown(f"""
                <div class="custom-card">
                    <h2 style="color: #1a6fa0;">📊 Hasil Diagnosis</h2>
                </div>
                """, unsafe_allow_html=True)
                
                # Tampilkan Status dengan Badge
                create_status_badge(status)
                
                # Gauge Chart
                fig = go.Figure(go.Indicator(
                    mode = "gauge+number+delta",
                    value = score,
                    title = {'text': f"Skor Kualitas Air: {score:.1f}/100", 'font': {'size': 20}},
                    delta = {'reference': 80, 'increasing': {'color': "green"}, 'decreasing': {'color': "red"}},
                    gauge = {
                        'axis': {'range': [None, 100], 'tickwidth': 1, 'tickcolor': "#1a6fa0"},
                        'bar': {'color': color},
                        'bgcolor': "white",
                        'borderwidth': 2,
                        'bordercolor': "#e6f7ff",
                        'steps': [
                            {'range': [0, 50], 'color': '#ffe6e6'},
                            {'range': [50, 80], 'color': '#fff7e6'},
                            {'range': [80, 100], 'color': '#e6ffe6'}],
                        'threshold': {
                            'line': {'color': "#0d3b66", 'width': 4},
                            'thickness': 0.75,
                            'value': score}}))
                
                fig.update_layout(
                    height=300,
                    margin=dict(l=20, r=20, t=50, b=20),
                    font={'family': "Poppins"}
                )
                
                st.plotly_chart(fig, use_container_width=True)
                
                # Rekomendasi Tindakan
                st.markdown("""
                <div class="custom-card">
                    <h3 style="color: #1a6fa0;">📋 Rekomendasi Tindakan</h3>
                </div>
                """, unsafe_allow_html=True)
                
                if status == "BAIK":
                    st.markdown("""
                    <div style="background: linear-gradient(90deg, #d4edda, #e6ffe6); padding: 1.5rem; border-radius: 10px; border-left: 5px solid #2ecc71;">
                        <h4 style="color: #155724; margin-top: 0;">✅ Kondisi Optimal</h4>
                        <p style="color: #155724; margin-bottom: 0;">
                        Kualitas air dalam kondisi optimal untuk pertumbuhan ikan. Pertahankan manajemen pakan, sirkulasi, dan monitoring rutin.
                        </p>
                    </div>
                    """, unsafe_allow_html=True)
                else:
                    # Tampilkan masalah jika ada
                    if reasons:
                        st.markdown("""
                        <div style="background: linear-gradient(90deg, #fff3cd, #fff7e6); padding: 1.5rem; border-radius: 10px; border-left: 5px solid #f39c12; margin-bottom: 1.5rem;">
                            <h4 style="color: #856404; margin-top: 0;">⚠️ Masalah Terdeteksi</h4>
                        """, unsafe_allow_html=True)
                        
                        for r in reasons:
                            st.markdown(f"""
                            <div style="background: rgba(255, 243, 205, 0.5); padding: 0.8rem; border-radius: 8px; margin: 0.5rem 0;">
                                <p style="color: #856404; margin: 0;">• {r}</p>
                            </div>
                            """, unsafe_allow_html=True)
                        
                        st.markdown("</div>", unsafe_allow_html=True)
                    
                    # Tampilkan saran perbaikan jika ada
                    if actions:
                        st.markdown("""
                        <div style="background: linear-gradient(90deg, #f8d7da, #ffe6e6); padding: 1.5rem; border-radius: 10px; border-left: 5px solid #e74c3c;">
                            <h4 style="color: #721c24; margin-top: 0;">🛠️ Saran Perbaikan</h4>
                        """, unsafe_allow_html=True)
                        
                        for i, a in enumerate(actions, 1):
                            st.markdown(f"""
                            <div style="background: rgba(248, 215, 218, 0.5); padding: 0.8rem; border-radius: 8px; margin: 0.5rem 0;">
                                <p style="color: #721c24; margin: 0; font-weight: 500;">{i}. {a}</p>
                            </div>
                            """, unsafe_allow_html=True)
                        
                        st.markdown("</div>", unsafe_allow_html=True)
            else:
                # Placeholder jika belum ada analisis
                st.markdown("""
                <div class="custom-card" style="text-align: center; padding: 4rem 2rem;">
                    <div style="font-size: 4rem; color: #33cccc; margin-bottom: 1rem;">
                        🔍
                    </div>
                    <h3 style="color: #1a6fa0;">Belum Ada Analisis</h3>
                    <p style="color: #666;">
                        Masukkan parameter air di kolom sebelah kiri dan klik tombol "Analisis Kualitas Air" 
                        untuk mendapatkan diagnosis dan rekomendasi.
                    </p>
                </div>
                """, unsafe_allow_html=True)
    
    elif menu == "📜 Riwayat Penilaian":
        # Header Riwayat
        st.markdown("""
        <div class="main-header">
            <h1>📜 Riwayat Penilaian</h1>
            <p>Data historis pemeriksaan kualitas air tambak</p>
        </div>
        """, unsafe_allow_html=True)
        
        if len(st.session_state.history) > 0:
            df_hist = pd.DataFrame(st.session_state.history)
            
            # Tampilkan statistik ringkas
            col1, col2, col3 = st.columns(3)
            with col1:
                avg_score = df_hist['Skor'].mean()
                create_metric_card("Rata-rata Skor", f"{avg_score:.1f}", "/100")
            with col2:
                last_status = df_hist.iloc[-1]['Status']
                create_metric_card("Status Terakhir", last_status)
            with col3:
                total_analysis = len(df_hist)
                create_metric_card("Total Analisis", str(total_analysis), "")
            
            # Tabel riwayat dengan styling
            st.markdown("""
            <div class="custom-card" style="margin-top: 1rem;">
                <h2 style="color: #1a6fa0;">📋 Detail Riwayat</h2>
            </div>
            """, unsafe_allow_html=True)
            
            # Fungsi untuk styling tabel
            def color_status(val):
                if val == 'BAIK':
                    return 'background-color: #d4edda; color: #155724; font-weight: bold'
                elif val == 'CUKUP':
                    return 'background-color: #fff3cd; color: #856404; font-weight: bold'
                else:
                    return 'background-color: #f8d7da; color: #721c24; font-weight: bold'
            
            # Format tabel
            styled_df = df_hist.style.applymap(color_status, subset=['Status'])
            
            # Tampilkan tabel dengan container
            st.dataframe(styled_df, use_container_width=True, height=400)
            
            # Tombol download
            csv = df_hist.to_csv(index=False).encode('utf-8')
            
            col1, col2, col3 = st.columns([1, 2, 1])
            with col2:
                st.download_button(
                    "📥 Unduh Laporan Lengkap (CSV)",
                    csv,
                    "laporan_kualitas_air.csv",
                    "text/csv",
                    use_container_width=True
                )
            
            # Grafik trend jika ada data cukup
            if len(df_hist) > 1:
                st.markdown("""
                <div class="custom-card">
                    <h2 style="color: #1a6fa0;">📈 Trend Kualitas Air</h2>
                </div>
                """, unsafe_allow_html=True)
                
                # Buat grafik trend
                fig = go.Figure()
                fig.add_trace(go.Scatter(
                    x=df_hist['Waktu'],
                    y=df_hist['Skor'],
                    mode='lines+markers',
                    name='Skor Kualitas',
                    line=dict(color='#1a6fa0', width=3),
                    marker=dict(size=8)
                ))

                fig.update_layout(
                    height=550,
                    xaxis_title="Waktu",
                    yaxis_title="Skor Kualitas",
                    plot_bgcolor='white',
                    paper_bgcolor='white',
                    font={'family': "Poppins"},
                    yaxis=dict(range=[0, 120]),
                    margin=dict(l=100, r=120, t=80, b=80),
                    xaxis=dict(
                        rangeslider=dict(visible=True, bgcolor="#f8f9fa", thickness=0.1, borderwidth=1, bordercolor="#dfe3e6"),
                        type="date"
                    )
                )

                # 1. Tambahkan Garis Horizontal
                fig.add_hline(y=80, line_dash="dash", line_color="#2ecc71")
                fig.add_hline(y=50, line_dash="dash", line_color="#f39c12")
                fig.add_hline(y=20, line_dash="dash", line_color="#e74c3c")

                # 2. Tambahkan Teks Keterangan di SEBELAH KANAN area grafik
                annotations = [
                    dict(y=80, text="<b>BAIK</b><br>(80-100)", color="#2ecc71"),
                    dict(y=50, text="<b>CUKUP</b><br>(50-79)", color="#f39c12"),
                    dict(y=20, text="<b>BURUK</b><br>(< 50)", color="#e74c3c")
                ]

                for ann in annotations:
                    fig.add_annotation(
                        x=1.02,          # Posisi di luar grafik sebelah kanan (1.0 adalah batas kanan)
                        y=ann['y'],
                        xref="paper",    # Koordinat X relatif terhadap lebar grafik
                        yref="y",        # Koordinat Y mengikuti nilai skor
                        text=ann['text'],
                        showarrow=False,
                        xanchor="left",  # Teks tumbuh ke arah kanan dari titik X
                        font=dict(color=ann['color'], size=11),
                        align="left"     # Rata kiri untuk teks berbaris
                    )

                st.plotly_chart(fig, use_container_width=True)


        else:
            # Tampilan jika belum ada riwayat
            st.markdown("""
            <div class="custom-card" style="text-align: center; padding: 4rem 2rem;">
                <div style="font-size: 4rem; color: #33cccc; margin-bottom: 1rem;">
                    📊
                </div>
                <h3 style="color: #1a6fa0;">Belum Ada Riwayat</h3>
                <p style="color: #666;">
                    Lakukan analisis kualitas air terlebih dahulu untuk melihat riwayat penilaian di sini.
                </p>
            </div>
            """, unsafe_allow_html=True)
    
    elif menu == "ℹ️ Tentang Sistem":
        # Header Tentang
        st.markdown("""
        <div class="main-header">
            <h1>ℹ️ Tentang Sistem</h1>
            <p>Informasi tentang metode dan teknologi yang digunakan</p>
        </div>
        """, unsafe_allow_html=True)
        
        # Konten Tentang Sistem
        tabs = st.tabs(["📚 Metodologi", "⚙️ Parameter", "🎯 Klasifikasi", "📖 Referensi"])
        
        with tabs[0]:
            st.markdown("""
            <div class="custom-card">
                <h2 style="color: #1a6fa0;">📚 Metodologi Sistem</h2>
                <p style="color: #555; line-height: 1.6;">
                Sistem ini mengadopsi pendekatan <strong>hibrida</strong> yang menggabungkan 
                <strong>Rule-Based Reasoning</strong> (aturan berbasis pengetahuan pakar) dengan 
                <strong>Data-Driven Logic</strong> menggunakan prinsip-prinsip <strong>Fuzzy Logic</strong> 
                untuk menangani ketidakpastian dan variabilitas data.
                </p>                
                <h3 style="color: #1a6fa0; margin-top: 1.5rem;">🔧 Cara Kerja Sistem:</h3>
                <ol style="color: #555; line-height: 1.6;">
                    <li><strong>Belajar dari Data Historis:</strong> Sistem memuat data historis dan menghitung statistik deskriptif untuk menetapkan baseline "normalitas lokal".</li>
                    <li><strong>Aturan Pakar:</strong> Menerapkan aturan biologis ikan yang telah ditetapkan oleh ahli akuakultur.</li>
                    <li><strong>Integrasi Fuzzy Logic:</strong> Menggunakan fungsi keanggotaan fuzzy untuk menghitung skor berdasarkan derajat kecocokan dengan kategori.</li>
                    <li><strong>Penilaian Terintegrasi:</strong> Menghasilkan skor akhir menggunakan Weighted Quality Index (WQI).</li>
                </ol>
            </div>
            """, unsafe_allow_html=True)
        
        with tabs[1]:
            st.markdown("""
            <div class="custom-card">
                <h2 style="color: #1a6fa0;">⚙️ Parameter dan Bobot Penilaian</h2>
                <p style="color: #555;">
                Sistem mengevaluasi lima parameter utama dengan bobot kepentingan sebagai berikut:
                </p>                
                <div style="margin-top: 1.5rem;">
                """, unsafe_allow_html=True)
            
            # Tabel parameter
            param_data = {
                "Parameter": ["Dissolved Oxygen (DO)", "pH", "Conductivity", "Turbidity", "Temperature"],
                "Bobot": ["35%", "20%", "20%", "15%", "10%"],
                "Ideal": [">= 5 mg/L", "6.5 - 8.5", "Berdasarkan data lokal", "≤ 10 NTU", "20-30°C"],
                "Kritis": ["< 3 mg/L", "< 6.5 atau > 8.5", "Diluar range historis", "> 30 NTU", "< 15°C atau > 35°C"]
            }
            
            param_df = pd.DataFrame(param_data)
            st.dataframe(param_df.style.highlight_max(subset=['Bobot'], color='#e6f7ff'), use_container_width=True)
            
            st.markdown("</div>", unsafe_allow_html=True)
        
        with tabs[2]:
            col1, col2 = st.columns(2)
            
            with col1:
                st.markdown("""
                <div class="custom-card">
                    <h3 style="color: #1a6fa0;">🎯 Klasifikasi Output</h3>
                    <div style="margin: 1.5rem 0;">
                        <div style="background: linear-gradient(90deg, #d4edda, #e6ffe6); padding: 1rem; border-radius: 8px; margin-bottom: 1rem;">
                            <h4 style="color: #155724; margin: 0;">🟢 BAIK (Skor ≥ 80)</h4>
                            <p style="color: #155724; margin: 0.5rem 0 0 0; font-size: 0.9rem;">
                            Kondisi air optimal untuk pertumbuhan ikan.
                            </p>
                        </div>                        
                        <div style="background: linear-gradient(90deg, #fff3cd, #fff7e6); padding: 1rem; border-radius: 8px; margin-bottom: 1rem;">
                            <h4 style="color: #856404; margin: 0;">🟠 CUKUP (Skor 50-79)</h4>
                            <p style="color: #856404; margin: 0.5rem 0 0 0; font-size: 0.9rem;">
                            Kondisi memerlukan perhatian, lakukan perbaikan minor.
                            </p>
                        </div>                        
                        <div style="background: linear-gradient(90deg, #f8d7da, #ffe6e6); padding: 1rem; border-radius: 8px;">
                            <h4 style="color: #721c24; margin: 0;">🔴 BURUK (Skor < 50)</h4>
                            <p style="color: #721c24; margin: 0.5rem 0 0 0; font-size: 0.9rem;">
                            Kondisi berbahaya, tindakan segera diperlukan.
                            </p>
                        </div>
                    </div>
                </div>
                """, unsafe_allow_html=True)
            
            with col2:
                st.markdown("""
                <div class="custom-card">
                    <h3 style="color: #1a6fa0;">✨ Keunggulan Sistem</h3>
                    <ul style="color: #555; line-height: 1.6;">
                        <li><strong>Adaptif:</strong> Belajar dari data historis untuk penyesuaian lokal</li>
                        <li><strong>Real-Time:</strong> Memberikan rekomendasi langsung</li>
                        <li><strong>User-Friendly:</strong> Antarmuka sederhana dengan visualisasi interaktif</li>
                        <li><strong>Akurat:</strong> Mengintegrasikan analisis statistik dengan logika fuzzy</li>
                        <li><strong>Komprehensif:</strong> Mempertimbangkan multiple parameter secara simultan</li>
                    </ul>
                </div>
                """, unsafe_allow_html=True)
        
        with tabs[3]:
            st.markdown("""
            <div class="custom-card">
                <h2 style="color: #1a6fa0;">📖 Referensi dan Sumber</h2>                
                <h3 style="color: #1a6fa0; margin-top: 1.5rem;">📚 Standar Kualitas Air:</h3>
                <ul style="color: #555; line-height: 1.6;">
                    <li>FAO (Food and Agriculture Organization) Guidelines for Aquaculture</li>
                    <li>USEPA (United States Environmental Protection Agency) Water Quality Standards</li>
                    <li>Badan Standardisasi Nasional Indonesia (BSNI) untuk Kualitas Air Budidaya</li>
                </ul>                
                <h3 style="color: #1a6fa0; margin-top: 1.5rem;">🔬 Penelitian Terkait:</h3>
                <ul style="color: #555; line-height: 1.6;">
                    <li>Water Quality Requirements for Finfish Aquaculture (Boyd, 1998)</li>
                    <li>Fuzzy Logic Applications in Aquaculture Monitoring Systems (Chen et al., 2018)</li>
                    <li>Real-time Water Quality Monitoring in Smart Aquaculture (IoT-based Systems)</li>
                </ul>                
                <div style="background: #e6f7ff; padding: 1rem; border-radius: 10px; margin-top: 1.5rem;">
                    <h4 style="color: #0d3b66; margin-top: 0;">ℹ️ Informasi Kontak:</h4>
                    <p style="color: #0d3b66; margin-bottom: 0;">
                    Untuk pertanyaan lebih lanjut, silakan hubungi tim pengembang melalui email: 
                    <strong>KelazBangetKING@co.id</strong>
                    </p>
                </div>
            </div>
            """, unsafe_allow_html=True)
    
    # Footer
    st.markdown("""
    <div class="footer">
        <p>© 2026 AquaExpert System | Sistem Pakar Penilaian Kualitas Air Tambak Ikan</p>
        <p style="font-size: 0.8rem; color: #888;">
        Dibangun dengan ❤️ menggunakan Streamlit, Plotly, dan Python
        </p>
    </div>
    """, unsafe_allow_html=True)

if __name__ == "__main__":
    main()