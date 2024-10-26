import io
import os

from fastapi import FastAPI, File, UploadFile, Form
from fastapi.responses import StreamingResponse
from typing import Optional
import pandas as pd
import uvicorn

from models.pipeline import Pipeline

# WORKDIR = "./backend/"
WORKDIR = ""
WEIGHTS_DIR = f"{WORKDIR}models/weights/"

app = FastAPI()


# from dotenv import load_dotenv 
# load_dotenv() 


def decode_binary_csv(binary_csv_file, parse_date_col):
    return pd.read_csv(io.StringIO(binary_csv_file.decode("cp1251")), sep=";", encoding="cp1251", parse_dates=[parse_date_col])


@app.post("/upload_csv/")
async def upload_files(
    transactions: UploadFile = File(...),
    clients: UploadFile = File(...),
    model_weights: Optional[str] = Form(None)
    ):
    transactions_data = await transactions.read()
    clients_data = await clients.read()

    # Обработка файлов
    decoded_transactions = decode_binary_csv(transactions_data, parse_date_col="oprtn_date")
    decoded_clients = decode_binary_csv(clients_data, parse_date_col="accnt_bgn_date")

    # Запуск пайплайна
    pipeline = Pipeline(path_to_weights=WEIGHTS_DIR, classifier_weights_name=model_weights)
    result_df = pipeline.forward(decoded_transactions, decoded_clients)

    # Сохраняем результат в CSV-формате
    csv_binary_data = io.StringIO()
    result_df.to_csv(csv_binary_data, index=False)
    csv_binary_data.seek(0)

    # Возвращаем CSV-данные как StreamingResponse
    return StreamingResponse(csv_binary_data, media_type="text/csv", headers={"Content-Disposition": "attachment; filename=generated_data.csv"})

@app.get("/get_model_names/")
async def get_model_names():
    return os.listdir(WEIGHTS_DIR)

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=int(os.getenv("BACKEND_PORT")))
