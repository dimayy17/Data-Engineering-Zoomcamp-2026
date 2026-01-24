# Base image: Python versi FIX (3.13.11) dan varian slim supaya image lebih kecil
FROM python:3.13.11-slim

# Copy binary uv dari image resmi Astral ke image ini
# Tujuannya: pakai uv tanpa install via pip (lebih cepat & bersih)
COPY --from=ghcr.io/astral-sh/uv:latest /uv /bin/

# Set working directory di dalam container
# Semua perintah berikutnya akan dijalankan di folder /code
WORKDIR /code

# Tambahkan path virtual environment ke PATH
# Supaya python & pip yang dipakai adalah dari .venv
# Tanpa perlu "source .venv/bin/activate"
ENV PATH="/code/.venv/bin:$PATH"

# Copy file konfigurasi dependency terlebih dahulu
# Ini penting untuk Docker layer caching
# Kalau kode berubah tapi dependency tidak, Docker tidak reinstall ulang
COPY pyproject.toml .python-version uv.lock ./

# Install semua dependency sesuai uv.lock (locked & reproducible)
# --locked memastikan versi TIDAK berubah
RUN uv sync --locked 

# Copy source code aplikasi ke dalam container
COPY pipeline.py .

# Perintah default saat container dijalankan
# Artinya: docker run image -> python pipeline.py
ENTRYPOINT ["python", "pipeline.py"]
