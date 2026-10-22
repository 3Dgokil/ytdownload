YOUTUBE TO MP3 CONVERTER — PAKET STREAMLIT CLOUD + TERMUX

PENTING
- HTTP 403 dari YouTube dapat disebabkan pembatasan IP cloud dan tidak bisa dijamin selesai hanya dengan kode.
- Gunakan hanya audio yang Anda miliki atau yang memang diizinkan untuk diunduh.
- Streamlit Cloud menyimpan salinan di server cloud; gunakan tombol Download MP3 untuk menyimpan ke HP.
- Termux menyimpan salinan langsung ke Penyimpanan internal/POP_LAWAS.

A. STREAMLIT CLOUD
1. Ekstrak ZIP.
2. Upload app.py, requirements.txt, dan packages.txt ke root repository GitHub yang dipakai aplikasi.
3. Pastikan entry point Streamlit adalah app.py.
4. Commit/push, lalu tunggu aplikasi selesai redeploy.
5. Jika masih HTTP 403, kemungkinan akses YouTube dari IP cloud dibatasi. Versi Termux adalah alternatif untuk dicoba, tetapi tidak menjamin bebas 403.

B. TERMUX ANDROID
1. Pasang Termux dari sumber resminya.
2. Ekstrak paket ini di HP, lalu pindahkan folder ytmp3_dual ke folder yang mudah diakses Termux, misalnya ~/ytmp3_dual.
3. Di Termux, masuk ke folder proyek. Contoh:
   cd ~/ytmp3_dual
4. Jalankan launcher:
   bash termux/install_and_run.sh
5. Saat diminta, izinkan akses penyimpanan.
6. Buka browser HP dan kunjungi:
   http://127.0.0.1:8501
7. Hasil MP3 tersimpan di Penyimpanan internal/POP_LAWAS.
8. Biarkan Termux tetap berjalan selama aplikasi dipakai. Tekan Ctrl+C di Termux untuk menghentikan.

CATATAN TERMUX
- File app.py dan requirements.txt harus berada satu folder; folder termux berada di dalam folder proyek.
- Jika Anda sudah punya repository GitHub, jangan mengunggah folder termux sebagai entry point. Untuk Cloud, unggah tiga file di root saja.
