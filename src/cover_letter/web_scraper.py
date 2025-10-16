import os
from typing import List

from dotenv import load_dotenv
from langchain_core.documents import Document
from langchain_tavily import TavilyCrawl

load_dotenv()


tavily_crawl = TavilyCrawl()


def crawler(source: str) -> List[Document]:
    """Fetch a webpage and return it as a list of LangChain Document objects."""
    response = tavily_crawl.invoke(
        {
            "url": source,
            "max_depth": 1,
            "extract_depth": "advanced",
            "max_breadth": 1,
        }
    )

    all_docs = [
        Document(page_content=item["raw_content"], metadata={"source": item["url"]})
        for item in response["results"]
    ]

    return all_docs


if __name__ == "__main__":
    result = crawler(
        "https://eellak.ellak.gr/2025/10/02/software-engineer-python/?utm_medium=paid&utm_source=fb&utm_id=120234863720040414&utm_content=120234863721400414&utm_term=120234863720290414&utm_campaign=120234863720040414&fbclid=IwY2xjawNZYtxleHRuA2FlbQEwAGFkaWQBqyj4tioPvgEe7vNIRrbJxTR6h6_yvXwU165360dd2GkcAlXZsCYkjFsdaevoRuZ977Hue_8_aem_60_eIeNVUqENAlobqeXM4w"
    )
    print(result)
