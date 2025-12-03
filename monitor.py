import os
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


def send_slack_alert(message: str) -> None:
    """Send an alert message to Slack via incoming webhook."""
    webhook_url = os.getenv("SLACK_WEBHOOK_URL")
    if not webhook_url:
        logging.warning("SLACK_WEBHOOK_URL not set; skipping Slack alert.")
        return

    payload = {"text": message}

    try:
        resp = requests.post(webhook_url, json=payload, timeout=5)
        if resp.status_code >= 400:
            logging.error(
                "Slack webhook failed with status %s: %s",
                resp.status_code,
                resp.text[:200],
            )
    except requests.RequestException as e:
        logging.error("Error sending Slack alert: %s", e)


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
    failures = []  # list of (name, url) pairs

    for page in pages:
        name = page["name"]
        url = page["url"]
        expected = page.get("expected_text")

        ok = check_url(name, url, expected_text=expected)
        if not ok:
            all_ok = False
            failures.append((name, url))

    if all_ok:
        logging.info("All DMS pages look healthy ✔️")
    else:
        logging.warning("One or more DMS pages have issues ")

        # Build Slack message
        lines = [
            ":rotating_light: *DMS URL Health Monitor* found issues:",
            "",
        ]
        for name, url in failures:
            lines.append(f"• *{name}* – <{url}>")

        message = "\n".join(lines)
        send_slack_alert(message)


if __name__ == "__main__":
    main()
