import asyncio
from . import search_pubmed, search_biorxiv

async def query(query_text=""):
    """
    Query both PubMed and bioRxiv for a given text.

    This function queries both PubMed and bioRxiv asynchronously and
    combines the results.

    Args:
        query_text (str): The text to search for.

    Returns:
        tuple: A tuple containing three lists: combined citations,
               combined abstracts, and combined IDs (PMIDs and DOIs).
    """
    # We need to make sure the pubmed query is async
    pubmed_task = asyncio.create_task(search_pubmed.query(query_text))
    biorxiv_task = asyncio.create_task(search_biorxiv.query(query_text))

    results = await asyncio.gather(pubmed_task, biorxiv_task)

    pubmed_citations, pubmed_abstracts, pubmed_ids = results[0]
    biorxiv_citations, biorxiv_abstracts, biorxiv_dois = results[1]

    combined_citations = pubmed_citations + biorxiv_citations
    combined_abstracts = pubmed_abstracts + biorxiv_abstracts
    combined_ids = pubmed_ids + biorxiv_dois

    return combined_citations, combined_abstracts, combined_ids

if __name__ == '__main__':
    async def main():
        citations, abstracts, ids = await query("crispr")
        print(f"Found {len(citations)} articles.")
        for c in citations:
            print(c)

    asyncio.run(main())
