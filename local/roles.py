"""Model roles. Director thinks. Summarizer compresses."""

DIRECTOR = "deepseek-r1:32b"
SUMMARIZER = "digitsflow/bonsai-8b:latest"

ROLES = {
    "director": DIRECTOR,
    "summarizer": SUMMARIZER,
}
