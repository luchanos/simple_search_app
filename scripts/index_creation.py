from elasticsearch import AsyncElasticsearch
from envparse import Env
import asyncio

env = Env()

ELASTIC_URL = env.str("ELASTIC_URL", default="http://0.0.0.0:9200")

MAPPING_FOR_INDEX = {
            "properties": {
                "id": {
                    "type": "long",
                },
                "text": {
                    "type": "text"}
                }
            }


async def main():
    elastic_client: AsyncElasticsearch = AsyncElasticsearch(ELASTIC_URL)
    print(await elastic_client.indices.create(index="documents", mappings=MAPPING_FOR_INDEX))


asyncio.run(main())
