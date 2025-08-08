import asyncio
import httpx
import xml.etree.ElementTree as ET

BASE_URL = "https://eutils.ncbi.nlm.nih.gov/entrez/eutils/"

async def search_article(client, query, number_of_articles=100):
    """
    Search PubMed for a given query and return a list of PMIDs.
    """
    params = {
        "db": "pubmed",
        "term": query,
        "retmax": number_of_articles,
        "usehistory": "y"
    }
    try:
        response = await client.get(f"{BASE_URL}esearch.fcgi", params=params)
        response.raise_for_status()
        root = ET.fromstring(response.content)
        id_list = [id_elem.text for id_elem in root.findall(".//Id")]
        return id_list
    except httpx.HTTPStatusError as e:
        print(f"HTTP error occurred: {e}")
        return []
    except Exception as e:
        print(f"An error occurred: {e}")
        return []

async def fetch_details(client, pmid):
    """
    Fetch the details for a given PMID.
    """
    params = {
        "db": "pubmed",
        "id": pmid,
        "retmode": "xml"
    }
    try:
        response = await client.get(f"{BASE_URL}efetch.fcgi", params=params)
        response.raise_for_status()
        return response.text
    except httpx.HTTPStatusError as e:
        print(f"HTTP error occurred for pmid {pmid}: {e}")
        return None
    except Exception as e:
        print(f"An error occurred for pmid {pmid}: {e}")
        return None

def parse_article(pmid, xml_data):
    """
    Parse the XML data of an article to extract citation and abstract.
    """
    if not xml_data:
        return None, None

    try:
        root = ET.fromstring(xml_data)
        article = root.find(".//PubmedArticle")
        if article is None:
            return None, None

        title_elem = article.find(".//ArticleTitle")
        title = title_elem.text if title_elem is not None else "No title available"

        abstract_elem = article.find(".//Abstract/AbstractText")
        abstract = abstract_elem.text if abstract_elem is not None else ""

        author_list = article.findall(".//Author")
        authors = []
        for author in author_list:
            last_name_elem = author.find("LastName")
            fore_name_elem = author.find("ForeName")
            last_name = last_name_elem.text if last_name_elem is not None else ""
            fore_name = fore_name_elem.text if fore_name_elem is not None else ""
            if last_name:
                authors.append(f"{last_name} {fore_name[0] if fore_name else ''}")
        author_str = ", ".join(authors)

        journal_title_elem = article.find(".//Journal/Title")
        journal_title = journal_title_elem.text if journal_title_elem is not None else ""

        pub_date = article.find(".//PubDate")
        year = pub_date.find("Year").text if pub_date.find("Year") is not None else ""
        month = pub_date.find("Month").text if pub_date.find("Month") is not None else ""
        day = pub_date.find("Day").text if pub_date.find("Day") is not None else ""

        citation = f"{author_str}. {title}. {journal_title}. {year} {month} {day}; PMID: {pmid}."
        return citation, abstract
    except ET.ParseError:
        return None, None


async def query(query_text="scrna seq analysis methods"):
    """
    Query PubMed for a given text and return citations, abstracts, and PMIDs.
    """
    async with httpx.AsyncClient() as client:
        pmid_list = await search_article(client, query_text)
        if not pmid_list:
            return [], [], []

        tasks = [fetch_details(client, pmid) for pmid in pmid_list]
        results = await asyncio.gather(*tasks)

        citation_arr = []
        abstract_arr = []

        for pmid, xml_data in zip(pmid_list, results):
            if xml_data:
                citation, abstract = parse_article(pmid, xml_data)
                if citation and abstract:
                    citation_arr.append(citation)
                    abstract_arr.append(abstract)

    return citation_arr, abstract_arr, pmid_list

if __name__ == '__main__':
    async def main():
        citations, abstracts, pmids = await query("crispr")
        print(f"Found {len(citations)} articles.")
        for c in citations:
            print(c)
    asyncio.run(main())
