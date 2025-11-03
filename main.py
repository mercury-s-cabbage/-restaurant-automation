from enum import Enum
from fastapi import FastAPI, Query, HTTPException, Body
from fastapi.responses import PlainTextResponse, StreamingResponse
from pydantic import BaseModel

from Src.Logics.response_markdown import response_markdown
from Src.start_service import start_service
from Src.Logics.response_csv import response_scv
from Src.Logics.response_xml import response_xml
from Src.Logics.response_json import response_json
import io
import uvicorn
from collections import defaultdict
from datetime import datetime
from Src.Models.transaction_model import transaction_model
from Src.Dtos.transaction_dto import transaction_dto
import logging

logger = logging.getLogger("uvicorn.error")
#http://127.0.0.1:8081/docs#/default/add_transaction_api_transactions_post

app = FastAPI()

# создаём и запускаем сервис
service = start_service()
service.file_name = "settings.json"
try:
    service.start()
except Exception as e:
    print(f"Ошибка при запуске startservice: {e}")

repo_keys = service.repository.keys()
RepoKeyEnum = Enum('RepoKeyEnum', [(key, key) for key in repo_keys], type=str)

@app.get("/api/accessibility", response_class=PlainTextResponse)
async def formats():
    return "SUCCESS"

@app.get("/api/dictionary", response_class=PlainTextResponse)
async def get_dictionary(
    name: str = Query(..., description="Название справочника"),
    format_: str = Query(None, alias="format", description="Формат вывода (markdown, csv, xml)")
):
    data_list = service.repository.data.get(name, [])

    if not format_:
        format_ = service.default_format

    if format_ == "markdown":
        response = response_markdown()
        text = response.build(data_list)
    elif format_ == "csv":
        response = response_scv()
        text = response.build(data_list)
    elif format_ == "xml":
        response = response_xml()
        text = response.build(data_list)
    else:
        raise HTTPException(status_code=400, detail="Unsupported format")

    return text

@app.get("/api/file")
async def get_file(name: str = Query(..., description="Название справочника")):
    data_list = service.repository.data.get(name, [])
    response = response_json()
    text = response.build(data_list)

    json_bytes = io.BytesIO()
    json_bytes.write(text.encode('utf-8'))
    json_bytes.seek(0)

    filename = f"{name}.json" if name else "dictionary.json"

    return StreamingResponse(
        json_bytes,
        media_type="application/json",
        headers={"Content-Disposition": f"attachment; filename={filename}"},
    )

class TransactionCreateRequest(BaseModel):
    date: str
    nomenclature_id: str
    storage_id: str
    quantity: float
    unit_id: str
@app.post("/api/transactions", response_class=PlainTextResponse)
async def add_transaction(date: str = Query(..., description="Дата транзакции"),
                          nomenclature_id: str = Query(..., description="id номенклатуры"),
                          storage_id: str = Query(..., description="id склада"),
                          quantity: float = Query(..., description="id склада"),
                          unit_id: str = Query(..., description="id склада")
                                                ):
    dto = transaction_dto()
    dto.date = date
    dto.nomenclature_id = nomenclature_id
    dto.storage_id = storage_id
    dto.quantity = quantity
    dto.unit_id = unit_id

    # Создаем модель из DTO, передаем кэш из сервиса
    item = transaction_model.from_dto(dto, service.cache)

    # Добавляем в репозиторий
    service.repository.data.setdefault(service.repository.transactions_key(), []).append(item)

    return item.unique_code
@app.get("/api/transactions_report")
async def get_transactions_report(
    start_date: str = Query(..., description="Дата начала в формате ISO 8601, например 2025-11-01T00:00:00"),
    end_date: str = Query(..., description="Дата окончания в формате ISO 8601, например 2025-11-30T23:59:59"),
    storage_id: str = Query(..., description="ID склада")
):
    # Преобразуем строки в datetime
    try:
        start_dt = datetime.strptime(start_date, "%Y-%m-%dT%H:%M:%S")
        end_dt = datetime.strptime(end_date, "%Y-%m-%dT%H:%M:%S")
    except ValueError:
        raise HTTPException(status_code=400, detail="Неверный формат даты")

    # Получаем все транзакции из репозитория
    transactions = service.repository.data.get(service.repository.transactions_key(), [])

    # Отфильтруем по дате и складу
    filtered = [
        t for t in transactions
        if (start_dt <= t.date <= end_dt) and (t.storage.unique_code == storage_id)
    ]

    # Словари для подсчёта остатков и движений
    opening_balance = defaultdict(float)
    incoming = defaultdict(float)
    outgoing = defaultdict(float)
    unit_map = {}

    # Пройдём по всем транзакциям для расчёта начального остатка
    for t in transactions:
        if t.storage.unique_code == storage_id and t.date < start_dt:
            key = t.nomenclature.unique_code
            qty = t.quantity
            opening_balance[key] += qty
            if key not in unit_map:
                unit_map[key] = t.unit.name  # или id, по вашей модели

    # Пройдём по транзакциям в заданном периоде для подсчёта прихода и расхода
    for t in filtered:
        key = t.nomenclature.unique_code
        qty = t.quantity
        if key not in unit_map:
            unit_map[key] = t.unit.name

        if qty > 0:
            incoming[key] += qty
        elif qty < 0:
            outgoing[key] += abs(qty)  # учитываем положительное значение для расхода

    # Сформируем итоговый отчет
    result = []
    for nom_id in set(list(opening_balance.keys()) + list(incoming.keys()) + list(outgoing.keys())):
        start_bal = opening_balance.get(nom_id, 0)
        inc = incoming.get(nom_id, 0)
        out = outgoing.get(nom_id, 0)
        end_bal = start_bal + inc - out

        row = {
            "NomenclatureId": nom_id,
            "Unit": unit_map.get(nom_id, ""),
            "OpeningBalance": start_bal,
            "Incoming": inc,
            "Outgoing": out,
            "EndingBalance": end_bal,
        }
        result.append(row)

    return result

if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=8081, reload=True)
