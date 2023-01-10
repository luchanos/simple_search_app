from elasticsearch import AsyncElasticsearch, BadRequestError
from envparse import Env
import asyncio

env = Env()

ELASTIC_URL = env.str("ELASTIC_URL", default="http://0.0.0.0:9200")

MAPPING_FOR_INDEX = {
            "properties": {
                "iD": {
                    "type": "long",
                },
                "text": {
                    "type": "text"
                }
            },
        }


async def create_indexes():
    async with AsyncElasticsearch(ELASTIC_URL) as elastic_client:
        try:
            print(await elastic_client.indices.create(index="documents", mappings=MAPPING_FOR_INDEX))
        except BadRequestError as e:
            print(e)


if __name__ == "__main__":
    asyncio.run(create_indexes())
