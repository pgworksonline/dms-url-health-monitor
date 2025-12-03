# 🌐 DMS URL Health Dashboard

![CI](https://github.com/PGWORKSONLINE/dms-url-health-monitor/actions/workflows/ci.yml/badge.svg)

This page shows the current monitoring setup for Designer's Moving Service URLs.
The checks are run automatically via GitHub Actions.

---

## 🔍 Monitored Pages

| Name        | URL                                                      | Expected Text                               |
|------------|-----------------------------------------------------------|---------------------------------------------|
| Home Page  | https://designersmovingservice.com                        | `For a seamless and stress-free move`       |
| Quote Page | https://designersmovingservice.com/get-a-quote           | _(status code only)_                        |

---

## 🚦 How to Read the Status

- **CI badge green (passing)** → Last run of `monitor.py` succeeded for all pages.
- **CI badge red (failing)** → At least one page is down or missing expected content.
  - Check the **Actions** tab → open the latest run → view logs for details.

---

## 🧠 Behind the Scenes

- `monitor.py` sends HTTP requests to each URL in `urls.json`.
- It validates:
  - HTTP status `< 400`
  - Optional `expected_text` on the page
- It logs any issues and exits with a non-zero code if something is wrong.
- GitHub Actions runs this as part of the **CI** workflow:
  - On every push to `main` or `dev`
  - (Optional) On a daily schedule if you add a cron workflow

---

## 🔧 Useful Links

- **Repository:** https://github.com/PGWORKSONLINE/dms-url-health-monitor  
- **CI Workflow:** https://github.com/PGWORKSONLINE/dms-url-health-monitor/actions  
- **Main Site:** https://designersmovingservice.com  
- **Quote Page:** https://designersmovingservice.com/getaquote
