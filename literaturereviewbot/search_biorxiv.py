import asyncio
import httpx
from datetime import datetime, timedelta

PAGE_SIZE = 100

async def query(query_text=""):
    """
    Search bioRxiv for a given query text.

    This function fetches preprints from the last 30 days from the bioRxiv API
    and filters them based on whether the query text appears in the title or abstract.

    Args:
        query_text (str): The text to search for.

    Returns:
        tuple: A tuple containing three lists: citations, abstracts, and DOIs.
    """
    date_to = datetime.now()
    date_from = date_to - timedelta(days=30)

    date_to_str = date_to.strftime('%Y-%m-%d')
    date_from_str = date_from.strftime('%Y-%m-%d')

    url = f"https://api.biorxiv.org/details/biorxiv/{date_from_str}/{date_to_str}"

    citations = []
    abstracts = []
    dois = []

    async with httpx.AsyncClient() as client:
        cursor = 0
        while True:
            paginated_url = f"{url}/{cursor}/json"
            response = await client.get(paginated_url)

            if response.status_code != 200:
                break

            data = response.json()
            messages = data.get('messages', [{}])
            if messages and messages[0].get('status', '') == 'no results':
                break

            for article in data.get('collection', []):
                title = article.get('title', '')
                abstract = article.get('abstract', '')

                if query_text.lower() in title.lower() or query_text.lower() in abstract.lower():
                    authors = article.get('authors', [])
                    author_str = ", ".join([f"{a.get('name', '')}" for a in authors])
                    doi = article.get('doi', '')
                    date = article.get('date', '')

                    citation = f"{author_str}. {title}. bioRxiv {doi} ({date})"

                    citations.append(citation)
                    abstracts.append(abstract)
                    dois.append(doi)

            # bioRxiv API returns 100 results at a time. We need to paginate.
            # The 'count' in messages gives total results for the query.
            # 'cursor' is the starting point of the next page.
            try:
                count = int(messages[0].get('count', 0))
                cursor = int(messages[0].get('cursor', 0)) + PAGE_SIZE
            except (ValueError, TypeError):
                break

            if cursor >= count:
                break

    return citations, abstracts, dois

if __name__ == '__main__':
    async def main():
        citations, abstracts, dois = await query("crispr")
        for c in citations:
            print(c)
    asyncio.run(main())
