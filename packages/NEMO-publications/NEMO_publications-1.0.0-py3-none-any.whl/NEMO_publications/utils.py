import requests
from bibtexparser import bparser


def parse_bibtex(bibtex_string):
    bibtex_parsed = bparser.parse(bibtex_string)
    if len(bibtex_parsed.entries) != 1:
        raise Exception("multiple entries were found")
    else:
        return bibtex_parsed.entries[0]


# Fetch DOI metadata from https://doi.org
# key 'error' contains error message if an error was encountered
# key 'metadata' contains dict with metadata fields that were found
def fetch_publication_metadata_by_doi(doi):
    base_url = f"https://doi.org/{doi}"
    headers = {"Accept": "text/bibliography; style=bibtex"}
    result = {"metadata": {"doi": doi}}
    response = requests.get(base_url, headers=headers)
    if response.status_code == 200:
        bibtex_string = response.text.strip()
        try:
            publication_parsed_metadata = parse_bibtex(bibtex_string)
            result["metadata"] = {
                "doi": publication_parsed_metadata.get("doi", doi),
                "year": publication_parsed_metadata.get("year"),
                "journal": publication_parsed_metadata.get("journal"),
                "title": publication_parsed_metadata["title"],
                "bibtex": bibtex_string,
            }
        except Exception as parse_error:
            result["error"] = "Search returned invalid publication metadata, " + parse_error.__str__()
    elif response.status_code == 404:
        result["error"] = "Publication information was not found."
    else:
        result["error"] = "Search query has failed."
    return result
