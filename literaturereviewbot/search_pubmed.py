#!/usr/bin/env python3

from Bio import Entrez

"""
sort_by possible strings for PubMed:
----
pub_date - descending sort by publication date
Author - ascending sort by first author
JournalName - ascending sort by journal name
relevance - default sort order, (“Best Match”) on web PubMed
"""
sort_by = "pub_date"


def search_article(query, number_of_articles=100):
    Entrez.email = "mail4sunit@gmail.com"  # Always provide your email

    handle = Entrez.esearch(
        db="pubmed",
        term=query,
        retmax=number_of_articles,
        # sort=sort_by
    )
    record = Entrez.read(handle)
    handle.close()
    return record["IdList"]


def fetch_details(pmid):
    handle = Entrez.efetch(db="pubmed", id=pmid, retmode="xml")
    records = Entrez.read(handle)
    handle.close()
    return records


def parse_article(pmid, details):
    ##########################
    ## abstract of the article
    ##########################
    try:
        abstract_text = details["PubmedArticle"][0]["MedlineCitation"]["Article"][
            "Abstract"
        ]["AbstractText"][0]
    except (KeyError, IndexError):
        return None
    ##################
    ## article details
    ##################
    article = details["PubmedArticle"][0]["MedlineCitation"]["Article"]
    journal = article["Journal"]
    # pubmed_data = details["PubmedArticle"][0]["PubmedData"]

    # Article Title
    title = article.get("ArticleTitle", "No title available")

    try:
        # Authors
        authors = article["AuthorList"]
        author_str = ", ".join([f"{a['LastName']} {a['ForeName'][0]}" for a in authors])

        # Journal Info
        journal_title = journal.get("Title", "No journal title available")
        journal_volume = journal["JournalIssue"].get("Volume", "No volume")
        journal_issue = journal["JournalIssue"].get("Issue", "No issue")
        pub_date = article.get(
            "ArticleDate", [{"Year": "No year", "Month": "No month", "Day": "No day"}]
        )[0]
        pub_year = pub_date["Year"]
        pub_month = pub_date["Month"]
        pub_day = pub_date["Day"]
        pages = article["Pagination"].get("StartPage", "No pages")
        citation = f"{author_str}. {title}. {journal_title}. {pub_year} {pub_month} {pub_day};{journal_volume}({journal_issue}):{pages}. PMID: {pmid}."
    except (KeyError, IndexError):
        citation = f"{title}. {journal_title}. PMID: {pmid}."

    return citation, abstract_text


def query(query_text="scrna seq analysis methods"):
    citation_arr = []
    abstract_arr = []

    pmid_list = search_article(query_text)
    if not pmid_list:
        return None

    for pmid in pmid_list:
        details = fetch_details(pmid)
        citation, abstract = parse_article(pmid, details)
        citation_arr.append(citation)
        abstract_arr.append(abstract)

    print(f"Num citations:  {len(citation_arr)}")
    print(f"Num abstracts:  {len(abstract_arr)}")
    print(f"Num pubmed_ids:  {len(pmid_list)}")
    return citation_arr, abstract_arr, pmid_list
