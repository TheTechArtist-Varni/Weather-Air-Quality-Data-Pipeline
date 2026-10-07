FROM python:3.11-slim
WORKDIR /app
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
COPY . .
ENV PYTHONUNBUFFERED=1
# Default: run the whole pipeline once. Override with:
#   docker run -p 8501:8501 IMAGE streamlit run dashboard/app.py --server.address 0.0.0.0
CMD ["python", "-m", "pipeline.flow"]
