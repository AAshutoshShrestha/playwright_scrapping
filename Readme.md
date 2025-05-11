A Python web scraper built with Playwright to extract floor sheet data from Nepal Stock Exchange (NEPSE) website.
Extracts Default number of page i.e. 5

on main() function pass the number of pages you want to scrap data scrape_floor_sheet(page,10).

### Create and activate a virtual environment
```bash
python -m venv venv

venv\Scripts\activate
```

### Install dependencies:
```bash
pip install -r requirements.txt
```

### Install Playwright browsers:

```bash
playwright install
```

### Run the scraper:

```bash
python main.py
```