import io
import os

from fastapi import FastAPI, File, UploadFile
from fastapi.responses import StreamingResponse
import pandas as pd
import uvicorn

from models.pipeline import Pipeline

# WORKDIR = "./backend/"
WORKDIR = ""
WEIGHTS_DIR = f"{WORKDIR}models/weights/"

app = FastAPI()


# from dotenv import load_dotenv 
# load_dotenv() 


def decode_binary_csv(binary_csv_file):
    return pd.read_csv(io.StringIO(binary_csv_file.decode("cp1251")), sep=";", encoding="cp1251")


@app.post("/upload_csv/")
async def upload_files(transactions: UploadFile = File(...), clients: UploadFile = File(...)):
    transactions_data = await transactions.read()
    clients_data = await clients.read()

    # Обработка файлов
    decoded_transactions = decode_binary_csv(transactions_data)
    decoded_clients = decode_binary_csv(clients_data)

    pipeline = Pipeline(path_to_weights=WEIGHTS_DIR, classifier_weights_name="bad_cls_v0.cbm")
    _, result_df = pipeline.forward(decoded_transactions, decoded_clients)

    csv_binary_data = io.StringIO()
    result_df.to_csv(csv_binary_data, index=False)
    csv_binary_data.seek(0)

    # Возвращаем CSV-данные как StreamingResponse
    return StreamingResponse(csv_binary_data, media_type="text/csv", headers={"Content-Disposition": "attachment; filename=generated_data.csv"})


if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=int(os.getenv("BACKEND_PORT")))
