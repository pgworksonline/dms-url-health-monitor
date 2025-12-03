import json
import logging
import time
from pathlib import Path
from typing import List, Dict, Optional

import requests


def setup_logging() -> None:
    """Log to console and file."""
    logs_dir = Path("logs")
    logs_dir.mkdir(exist_ok=True)

    log_file = logs_dir / "monitor.log"

    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s [%(levelname)s] %(message)s",
        handlers=[
            logging.FileHandler(log_file),
            logging.StreamHandler()
        ]
    )


def load_urls() -> List[Dict[str, str]]:
    """Load the pages to check from urls.json."""
    config_path = Path("urls.json")
    if not config_path.exists():
        raise FileNotFoundError("urls.json not found")

    with config_path.open() as f:
        data = json.load(f)

    if not isinstance(data, list):
        raise ValueError("urls.json must contain a list")

    return data


def check_url(
    name: str,
    url: str,
    expected_text: Optional[str] = None,
    timeout: float = 8.0,
) -> bool:
    """Check that a URL is up and (optionally) contains expected text."""
    start = time.time()
    try:
        response = requests.get(url, timeout=timeout)
        elapsed = (time.time() - start) * 1000  # ms

        is_up = response.status_code < 400
        content_ok = True

        if expected_text:
            if expected_text not in response.text:
                content_ok = False
                logging.warning(
                    f"[CONTENT MISSING] {name} – expected text not found: {expected_text!r}"
                )

        status = "UP" if (is_up and content_ok) else "ISSUE"

        logging.info(
            f"[{status}] {name} – {url} | status={response.status_code} | {elapsed:.1f}ms"
        )

        if not is_up:
            logging.error(
                f"[DOWN] {name} – returned status {response.status_code}"
            )

        return is_up and content_ok

    except requests.RequestException as e:
        elapsed = (time.time() - start) * 1000
        logging.error(
            f"[DOWN] {name} – {url} | error={e} after {elapsed:.1f}ms"
        )
        return False


def main() -> None:
    setup_logging()
    pages = load_urls()

    all_ok = True

    for page in pages:
        name = page["name"]
        url = page["url"]
        expected = page.get("expected_text")

        ok = check_url(name, url, expected_text=expected)
        if not ok:
            all_ok = False

    if all_ok:
        logging.info("All DMS pages look healthy ✔️")
    else:
        logging.warning("One or more DMS pages have issues ")


if __name__ == "__main__":
    main()
