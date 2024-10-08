import sys
from pathlib import Path

# Add the parent directory to the system path
current_dir = Path(__file__).resolve().parent
parent_dir = current_dir.parent
sys.path.append(str(parent_dir))

import os
import json

from textwrap import dedent

import requests
from crewai import Agent, Task, Crew
from langchain.tools import tool
from unstructured.partition.html import partition_html

from lib.utils import groq_llm
from lib.config import get_browserless_api_key

browserless_api_key = get_browserless_api_key()

class BrowserTools:
    
    @tool("Scrape website content")
    def scrape_and_summarize_website(website):
        """Useful to scrape and summarize a website content, just pass a string with
        only the full url, no need for a final slash `/`, eg: https://google.com or https://clearbit.com/about-us"""
        url = f"https://chrome.browserless.io/content?token={browserless_api_key}"
        payload = json.dumps({"url": website})
        headers = {'cache-control': 'no-cache', 'content-type': 'application/json'}
        response = requests.request("POST", url, headers=headers, data=payload)
        elements = partition_html(text=response.text)
        content = "\n\n".join([str(el) for el in elements])
        content = [content[i:i + 8000] for i in range(0, len(content), 8000)]
        summaries = []
        for chunk in content:
            agent = Agent(
                role='Principal Researcher',
                goal='Do amazing research and summaries based on the content you are working with',
                backstory="You're a Principal Researcher at a big company and you need to do research about a given topic.",
                llm=groq_llm(),
                allow_delegation=False
            )
            
            task = Task(
                agent=agent,
                description=(
                    f'Analyze and make a LONG summary of the content below. '
                    f'Make sure to include ALL relevant information in the summary. '
                    f'Return only the summary, nothing else.\n\nCONTENT\n----------\n{chunk}'
                ),
                expected_output=dedent("""\
                    A comprehensive, detailed summary of the content, 
                    including all key points and relevant information, 
                    ensuring that no significant detail is left out.
                """)
            )
            # Execute the crew
            crew = Crew(
                agents=[agent],
                tasks=[task],
                verbose=True
            )
            
            result = crew.kickoff()
            
            task_output = task.output
            summary = task_output.summary
            summaries.append(summary)
            content = "\n\n".join(summaries)
        return f'\nScrapped Content: {content}\n'