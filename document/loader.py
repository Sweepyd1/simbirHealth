from src.database.database import DatabaseManager
from src.database.Crud import Crud
from src.database.models import History
from config import DATABASE_URL, ES_HOST

import asyncpg
from elasticsearch import AsyncElasticsearch
from sqlalchemy import create_engine, select

db = Crud(DatabaseManager(database_url=DATABASE_URL))

db_start = DatabaseManager(DATABASE_URL)

es = AsyncElasticsearch(hosts=[ES_HOST],http_auth=("elastic", "130706"))

async def index_history_records(database_manager:DatabaseManager):
		async with database_manager.get_session() as session:
			try:
				# Извлечение всех записей из таблицы History
				result = await session.execute(select(History))
				rows = result.scalars().all()  # Получаем все записи как список объектов History

				# Индексация каждой записи в Elasticsearch
				for row in rows:
					document = row.to_dict()  # Используем метод to_dict для преобразования в словарь
					await es.index(index="history", id=row.id, body=document)
					print(f"Indexed document {row.id}")

			except Exception as e:
				print(f"Error indexing records: {str(e)}")

async def create_index_if_not_exists(index_name: str):
    # Определение настроек и маппинга
    index_settings = {
        "settings": {
            "number_of_shards": 1,
            "number_of_replicas": 1
        },
        "mappings": {
            "properties": {
                "id": {"type": "integer"},
                "date": {"type": "date"},
                "pacient_id": {"type": "integer"},
                "hospital_id": {"type": "integer"},
                "doctor_id": {"type": "integer"},
                "room": {"type": "text"},
                "data": {"type": "text"}
            }
        }
    }

    try:
        # Проверка существования индекса
        if not await es.indices.exists(index=index_name):
            # Создание индекса
            await es.indices.create(index=index_name, body=index_settings)
            print(f"Индекс '{index_name}' успешно создан.")
        else:
            print(f"Индекс '{index_name}' уже существует.")

    except Exception as e:
        print(f"Ошибка при создании индекса: {str(e)}")