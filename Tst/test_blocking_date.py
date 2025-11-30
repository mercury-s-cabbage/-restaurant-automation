import asyncio
import httpx

BASE_URL = "http://127.0.0.1:8081/api/transactions"

async def create_transaction(client):
    data = {
        "date": "2025-10-01T12:00:00",
        "nomenclature_id": f"123",
        "storage_id": "warehouse-001",
        "quantity": 10.0,
        "unit_id": "f8346e8b-7260-4db8-a673-c8c826ab08b7"
    }
    response = await client.post(f"{BASE_URL}/transactions", params=data)
    return response.status_code

# async def get_report(client):
#     # Предположим, что отчет генерируется POST запросом с телом, пример тела запроса нужен по конкретикам
#     report_request_data = {
#         "filters": [
#             {"filtername": "date", "filtertype": "startdate", "filtervalue": "2025-11-01"},
#             {"filtername": "date", "filtertype": "enddate", "filtervalue": "2025-11-30"},
#             {"filtername": "storage", "filtertype": "storage", "filtervalue": "storage1"},
#         ]
#     }
#     response = await client.post(f"{BASE_URL}/transactions/report", json=report_request_data)
#     return response.status_code, response.text

async def main():
    async with httpx.AsyncClient() as client:
        # Параллельно создаем 1000 транзакций
        create_tasks = [create_transaction(client) for i in range(2)]
        create_responses = await asyncio.gather(*create_tasks)
        print("Transactions creation statuses:", create_responses.count(200), "successful.")

        # # Запрашиваем отчет
        # status, report_content = await get_report(client)
        # print(f"Report request status: {status}")
        # # Здесь можно сохранять или анализировать report_content

if __name__ == "__main__":
    asyncio.run(main())
