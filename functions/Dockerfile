FROM python:3.10-slim
WORKDIR /app
COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt
COPY . .
COPY ./fullchain.pem .fullchain.pem
COPY ./privkey.pem .privkey.pem
EXPOSE 5001
# Use Gunicorn to run the Flask app
# -w 4 uses 4 workers
# "-b", "0.0.0.0:5001" means bind on all ip addresses on port 5001
# --reload tells the server to watch for changes
CMD ["gunicorn", "-w", "4", "-b", "0.0.0.0:5001", "--certfile", "./fullchain.pem", "--keyfile", "./privkey.pem", "app:app", "--reload"]
