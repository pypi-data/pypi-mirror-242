import os
from collections import namedtuple

VECTOR_STORE_INDEX_NAME = os.environ.get("VECTOR_STORE_INDEX_NAME", "dummy")
PINECONE_NAMESPACE = "bot-test"
PINECONE_TEXT_KEY = "text"

__all__ = [
    "VECTOR_STORE_INDEX_NAME",
    "PINECONE_NAMESPACE",
    "PINECONE_TEXT_KEY",
]

Queue = namedtuple('Queue', ['pdf_scraper_queue', 'web_scraper_queue'])

queues = Queue(
    pdf_scraper_queue="pdf_scraper_queue",
    web_scraper_queue="web_scraper_queue"
)