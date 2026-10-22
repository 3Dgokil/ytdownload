import os
import re
import shutil
import tempfile
import streamlit as st
import yt_dlp

st.set_page_config(
    page_title="YouTube to MP3 Converter",
    page_icon="🎵",
    layout="centered"
)

st.title("🎵 YouTube to MP3 Converter")
st.caption("Unduh audio YouTube langsung ke format MP3 dan simpan ke folder internal/POP_LAWAS.")

# Membuat folder internal/POP_LAWAS jika belum ada
TARGET_DIR = os.path.join("internal", "POP_LAWAS")
os.makedirs(TARGET_DIR, exist_ok=True)

url = st.text_input("Masukkan URL YouTube:", placeholder="https://www.youtube.com/watch?v=...")

def clean_filename(title: str) -> str:
    return re.sub(r'[\\/*?:"<>|]', "", title)

if st.button("Proses & Konversi", type="primary"):
    if not url.strip():
        st.warning("Silakan masukkan URL YouTube terlebih dahulu.")
    else:
        status_box = st.empty()
        status_box.info("Sedang mengambil informasi dan mengunduh video...")

        try:
            with tempfile.TemporaryDirectory() as temp_dir:
                ydl_opts = {
                    "format": "bestaudio/best",
                    "outtmpl": os.path.join(temp_dir, "%(title)s.%(ext)s"),
                    "postprocessors": [
                        {
                            "key": "FFmpegExtractAudio",
                            "preferredcodec": "mp3",
                            "preferredquality": "320",
                        },
                        {
                            "key": "FFmpegMetadata",
                            "add_metadata": True,
                        },
                        {
                            "key": "EmbedThumbnail",
                        },
                    ],
                    "writethumbnail": True,
                    "quiet": True,
                    "no_warnings": True,
                }

                with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                    info = ydl.extract_info(url, download=True)
                    video_title = info.get("title", "audio")
                    thumbnail_url = info.get("thumbnail")

                mp3_files = [f for f in os.listdir(temp_dir) if f.endswith(".mp3")]

                if not mp3_files:
                    status_box.error("Gagal mengonversi file ke format MP3.")
                else:
                    source_file = os.path.join(temp_dir, mp3_files[0])
                    safe_name = f"{clean_filename(video_title)}.mp3"
                    internal_save_path = os.path.join(TARGET_DIR, safe_name)

                    # Salin file ke folder internal/POP_LAWAS
                    shutil.copy2(source_file, internal_save_path)

                    with open(source_file, "rb") as f:
                        mp3_bytes = f.read()

                    status_box.success(f"Berhasil! File tersimpan di: {internal_save_path}")

                    if thumbnail_url:
                        st.image(thumbnail_url, caption=video_title, use_container_width=True)

                    st.audio(mp3_bytes, format="audio/mp3")

                    st.download_button(
                        label="⬇️ Download MP3 ke Perangkat",
                        data=mp3_bytes,
                        file_name=safe_name,
                        mime="audio/mpeg",
                        type="primary"
                    )

        except Exception as err:
            status_box.error(f"Terjadi kesalahan saat memproses video: {err}")
