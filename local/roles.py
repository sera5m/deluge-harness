"""Model roles. Director on the laptop. Summarizer on scythe.

GTX 1660 is 6 GB. Bonsai (1.2 GB) fits and can run while the laptop
runs deepseek-r1:32b. A 7B is tight on that card; bonsai is the Engels.
"""
import os

DIRECTOR = os.environ.get("DELUGE_DIRECTOR", "deepseek-r1:32b")
SUMMARIZER = os.environ.get("DELUGE_SUMMARIZER", "digitsflow/bonsai-8b:latest")

DIRECTOR_HOST = os.environ.get("DELUGE_DIRECTOR_HOST", "http://127.0.0.1:11434")
SUMMARIZER_HOST = os.environ.get("DELUGE_SUMMARIZER_HOST", "http://scythe:11434")
