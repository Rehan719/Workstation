FROM python:3.12-slim
WORKDIR /app
COPY . .
RUN pip install poetry && poetry install
ENV APP_MODE=COMMERCIAL
ENV FEATURE_TOGGLE_ENTERPRISE=true
CMD ["python", "sdk/dual_mode_scraper.py"]
