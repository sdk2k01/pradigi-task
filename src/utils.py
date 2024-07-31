from llama_index.readers.web import SimpleWebPageReader, BeautifulSoupWebReader
from llama_index.core import Document
import re


def extract_links_from_markdown(content: str, base_url: str) -> set:
    # Regular expression to find markdown links
    md_link_pattern = re.compile(r"\[([^\[]+)\]\((http[s]?://[^\)]+)\)")
    links = re.findall(md_link_pattern, content)

    # Extract only the URLs from the tuples
    excluded_extensions = (".pdf", ".png", ".jpg")
    urls = set(
        link[1]
        for link in links
        if link[1].startswith(base_url) and not link[1].endswith(excluded_extensions)
    )

    return urls


def update_sitemap_recursively(sitemap: set, depth: int = 2) -> set:
    """
    Recursively update sitemap with all links at given depth.
    """
    if depth == 0:
        return sitemap
    else:
        sub_docs = SimpleWebPageReader(html_to_text=True).load_data(list(sitemap))
        for i in sub_docs:
            sitemap.update(
                extract_links_from_markdown(i.get_text(), "https://pratham.org/")
            )
        return update_sitemap_recursively(sitemap, depth - 1)


def get_site_text(sitemap: set) -> list[Document]:
    return BeautifulSoupWebReader().load_data(
        sitemap
    )  # Resource intensive, takes around 2 mins for depth=2 sitemap
