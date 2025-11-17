from enum import Enum
from fastapi import FastAPI, Query, HTTPException, Body
from fastapi.responses import PlainTextResponse, StreamingResponse
from Src.Logics.response_markdown import response_markdown
from Src.start_service import start_service
from Src.Logics.response_csv import response_scv
from Src.Logics.response_xml import response_xml
from Src.Logics.response_json import response_json
import io
from typing import Dict, Any, List
import uvicorn
from Src.Models.transaction_model import transaction_model
from Src.Dtos.transaction_dto import transaction_dto
import logging
from Src.Core.prototype import prototype
from Src.Dtos.filter_dto import filter_dto
from Src.Core.validator import argument_exception
from collections import defaultdict

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

# Проверка доступа
@app.get("/api/accessibility", response_class=PlainTextResponse)
async def formats():
    return "SUCCESS"

# Вывести справочник всех моделей
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

# Скачать справочник всех моделей
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



# Добавить новую транзакцию
@app.post("/api/transactions", response_class=PlainTextResponse)
async def add_transaction(date: str = Query(..., description="Дата транзакции"),
                          nomenclature_id: str = Query(..., description="id номенклатуры"),
                          storage_id: str = Query(..., description="id склада"),
                          quantity: float = Query(..., description="количество"),
                          unit_id: str = Query(..., description="единица измерения")
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

# Сохранить текущее состояние репозитория
@app.post("/api/save_repository", response_class=PlainTextResponse)
async def save_repository(filename: str = Body(..., embed=True)) -> str:
    try:
        result = service.save(filename)
        if result:
            return "Репозиторий успешно сохранён"
        return "Ошибка при сохранении репозитория"
    except Exception as e:
        return f"Ошибка: {e}"

# Получить отфильтрованные модели
@app.post("/api/{model_name}/filter")
async def filter_model(
    model_name: str,
    request: Dict[str, Any]
):

    # динамически получаем ключ для модели из репозитория
    if hasattr(service.repository, f"{model_name}_key"):
        model_key = getattr(service.repository, f"{model_name}_key")()
    else:
        raise argument_exception("Некорректное имя модели")

    # первичный прототип со всеми данными указанной модели
    model_data = service.repository.data.get(model_key, [])
    result = prototype(model_data)

    # ключ, по которому будут храниться прототипы (будет дописываться)
    repo_key = f"{model_name}"

    # сортируем фильтры по полю filter_name чтобы в ключах они были в одном порядке
    sorted_filters = sorted(request["filters"], key=lambda f: f["filter_name"])

    # перебираем пришедшие фильтры
    for filter in sorted_filters:

        # создаем ДТО фильтра
        filter_obj = filter_dto()
        for key, value in filter.items():
            if hasattr(filter_obj, key):
                setattr(filter_obj, key, str(value))

        # дополняем ключ прототипа согласно полю фильтрации
        repo_key += f"_{filter["filter_name"]}_{filter["filter_type"]}_{filter["filter_value"]}" # например range_equal_kg
        print(f"filter key = {repo_key}\n")

        # проверяем на наличие уже существующего прототипа
        if repo_key in service.repository.data:
            result = service.repository.data[repo_key]
        else:
            # сохраняем в репозиторий в случае, если там нету
            result = result.filter(filter_obj)
            service.repository.data.setdefault(repo_key, result)

        # если прототип пустой, нет смысла фильтровать дальше
        if result == []:
            break

    return result

    # Получить ОСВ


@app.post("/api/transactions_report")
async def get_transactions_report(
        request: Dict[str, Any]  # фильтры в теле запроса
):
    pass


if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=8081, reload=True)
