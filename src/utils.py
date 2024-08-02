from llama_index.readers.web import SimpleWebPageReader, BeautifulSoupWebReader
from llama_index.core import Document
import re

# Base URLs for social media handles
SOCIAL_MEDIA_URLS = [
    "https://www.facebook.com/",
    "https://www.linkedin.com",
    "https://www.youtube.com/",
    "https://www.instagram.com/",
    "https://twitter.com/",
]


def get_social_media_set(sitemap: set) -> set:
    """
    Returns set of social media links from given sitemap.
    """
    # Create a set of social media URLs for comparison
    return set(
        link
        for link in sitemap
        if any(link.startswith(sm_url) for sm_url in SOCIAL_MEDIA_URLS)
    )


def extract_links_from_markdown(content: str, base_url: str) -> set:
    # Regular expression to find markdown links
    md_link_pattern = re.compile(r"\[([^\[]+)\]\((http[s]?://[^\)]+)\)")
    links = re.findall(md_link_pattern, content)

    # Extract only the URLs from the tuples
    excluded_extensions = (".pdf", ".png", ".jpg")

    urls = set(
        link[1]
        for link in links
        if (
            link[1].startswith(base_url)
            or any(link[1].startswith(sm_url) for sm_url in SOCIAL_MEDIA_URLS)
        )
        and not link[1].endswith(excluded_extensions)
    )

    return urls


def update_sitemap_recursively(sitemap: set, host_name: str, depth: int = 2) -> set:
    """
    Recursively update sitemap with all links at given depth.
    """
    if depth == 0:
        return sitemap
    else:
        sub_docs = SimpleWebPageReader(html_to_text=True).load_data(
            list(sitemap.difference(get_social_media_set(sitemap)))
        )
        for i in sub_docs:
            sitemap.update(extract_links_from_markdown(i.get_text(), host_name))
        return update_sitemap_recursively(sitemap, host_name, depth - 1)


def get_site_text(sitemap: set) -> list[Document]:
    return BeautifulSoupWebReader().load_data(
        sitemap, include_url_in_text=True
    )  # Resource intensive, takes around 2 mins for depth=2 sitemap
