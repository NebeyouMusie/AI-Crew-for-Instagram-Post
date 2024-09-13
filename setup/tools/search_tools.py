import sys
from pathlib import Path

# Add the parent directory to the system path
current_dir = Path(__file__).resolve().parent
parent_dir = current_dir.parent
sys.path.append(str(parent_dir))

import os
import json

import requests
from langchain.tools import tool

from lib.config import get_serperdev_api_key

serperdev_api_key = get_serperdev_api_key()

class SearchTools:

  @tool("Search internet")
  def search_internet(query):
    """Useful to search the internet about a given topic and return relevant
    results."""
    return SearchTools.search(query)

  @tool("Search instagram")
  def search_instagram(query):
    """Useful to search for instagram post about a given topic and return relevant
    results."""
    query = f"site:instagram.com {query}"
    return SearchTools.search(query)

  def search(query, n_results=5):
    url = "https://google.serper.dev/search"
    payload = json.dumps({"q": query})
    headers = {
        'X-API-KEY': serperdev_api_key,
        'content-type': 'application/json'
    }
    response = requests.request("POST", url, headers=headers, data=payload)
    results = response.json()['organic']
    string = []
    for result in results[:n_results]:
      try:
        string.append('\n'.join([
            f"Title: {result['title']}", f"Link: {result['link']}",
            f"Snippet: {result['snippet']}", "\n-----------------"
        ]))
      except KeyError:
        next

    content = '\n'.join(string)
    return f"\nSearch result: {content}\n"