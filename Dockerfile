# ============================================================
# 🐳 Dockerfile — Trading Terminal Backend (FastAPI)
# ============================================================
FROM python:3.11-slim

# Set working directory
WORKDIR /app

# Copy project files into the container
COPY . .

# Upgrade pip and install dependencies
RUN pip install --upgrade pip
RUN pip install -r requirements.txt

# Expose backend port
EXPOSE 9000

# Start FastAPI server
CMD ["uvicorn", "System_2_TradingTerminal.api.api_bridge:app", "--host", "0.0.0.0", "--port", "9000"]
