import os
import re
import shutil
import tempfile
from pathlib import Path

import streamlit as st
import yt_dlp

st.set_page_config(
    page_title="YouTube to MP3 Converter",
    page_icon="🎵",
    layout="centered",
)

st.title("🎵 YouTube to MP3 Converter")
st.caption("Konversi audio ke MP3. Gunakan hanya audio yang Anda miliki atau diizinkan untuk diunduh.")

# Folder ini berada di server Streamlit. Untuk menyimpan di HP, gunakan tombol Download.
# Streamlit Cloud: ./internal/POP_LAWAS
# Termux: set YTMP3_OUTPUT_DIR to ~/storage/shared/POP_LAWAS in the launcher.
TARGET_DIR = Path(os.environ.get("YTMP3_OUTPUT_DIR", "internal/POP_LAWAS")).expanduser()
TARGET_DIR.mkdir(parents=True, exist_ok=True)

url = st.text_input(
    "Masukkan URL YouTube:",
    placeholder="https://www.youtube.com/watch?v=...",
)


def clean_filename(title: str) -> str:
    name = re.sub(r'[\\/*?:"<>|\x00-\x1f]', "", title).strip().rstrip(".")
    return name[:180] or "audio_youtube"


def is_youtube_url(value: str) -> bool:
    return bool(re.match(r"^https?://(www\.|m\.|music\.)?(youtube\.com|youtu\.be)/", value.strip(), re.I))


if st.button("Proses & Konversi", type="primary", use_container_width=True):
    if not url.strip():
        st.warning("Masukkan URL YouTube terlebih dahulu.")
    elif not is_youtube_url(url):
        st.warning("URL tidak dikenali. Masukkan tautan YouTube yang valid.")
    else:
        status = st.empty()
        status.info("Mengambil audio dan mengonversi ke MP3...")

        try:
            with tempfile.TemporaryDirectory(prefix="ytmp3_") as temp_dir:
                # Jangan memaksa client Android/iOS dengan User-Agent desktop palsu:
                # kombinasi tersebut sering menyebabkan URL media ditolak (HTTP 403).
                ydl_opts = {
                    "format": "bestaudio/best",
                    "outtmpl": os.path.join(temp_dir, "source.%(ext)s"),
                    "noplaylist": True,
                    "retries": 3,
                    "fragment_retries": 3,
                    "socket_timeout": 30,
                    "postprocessors": [
                        {
                            "key": "FFmpegExtractAudio",
                            "preferredcodec": "mp3",
                            "preferredquality": "320",
                        },
                        {"key": "FFmpegMetadata", "add_metadata": True},
                    ],
                    "quiet": True,
                    "no_warnings": True,
                }

                with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                    info = ydl.extract_info(url.strip(), download=True)
                    title = info.get("title") or "audio_youtube"

                mp3_candidates = list(Path(temp_dir).glob("*.mp3"))
                if not mp3_candidates:
                    raise RuntimeError("File MP3 tidak ditemukan setelah konversi. Pastikan FFmpeg terpasang.")

                mp3_path = mp3_candidates[0]
                filename = clean_filename(title) + ".mp3"
                save_path = TARGET_DIR / filename
                shutil.copy2(mp3_path, save_path)
                mp3_bytes = mp3_path.read_bytes()

                status.success("Konversi berhasil!")
                if os.environ.get("YTMP3_OUTPUT_DIR"):
                    st.caption(f"File juga disimpan di: `{save_path}`")
                else:
                    st.caption(f"Salinan di server: `{save_path}`. Pada Streamlit Cloud, gunakan tombol Download untuk menyimpan ke HP.")
                st.audio(mp3_bytes, format="audio/mpeg")
                st.download_button(
                    "⬇️ Download MP3 ke Perangkat",
                    data=mp3_bytes,
                    file_name=filename,
                    mime="audio/mpeg",
                    type="primary",
                    use_container_width=True,
                )

        except Exception as err:
            error_text = str(err)
            if "403" in error_text or "Forbidden" in error_text:
                st.error(
                    "YouTube menolak akses audio dari server aplikasi (HTTP 403). "
                    "Ini sering terjadi pada IP cloud dan tidak selalu bisa diselesaikan dari kode saja. "
                    "Coba perbarui dependency lalu redeploy. Jika masih gagal, jalankan aplikasi di perangkat/komputer "
                    "sendiri atau gunakan sumber audio yang memang diizinkan untuk diunduh."
                )
                with st.expander("Detail teknis"):
                    st.code(error_text)
            elif "ffmpeg" in error_text.lower() or "ffprobe" in error_text.lower():
                st.error("FFmpeg belum tersedia di server. Pastikan `packages.txt` berisi `ffmpeg`, lalu redeploy.")
                with st.expander("Detail teknis"):
                    st.code(error_text)
            else:
                st.error(f"Gagal memproses audio: {error_text}")
                st.caption("Pastikan dependency sudah diperbarui dan coba lagi.")
