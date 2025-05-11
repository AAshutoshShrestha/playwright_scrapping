A Python web scraper built with Playwright to extract floor sheet data from Nepal Stock Exchange (NEPSE) website.

## Default Behavior

By default, the script will:
- Scrape **5 pages** of data
- Display **20 items per page**
- Save the output as `floor_sheet_YYYYMMDD_HHMMSS.csv`

## Customized usage example:

line 79 floor_sheet_data = await scrape_floor_sheet(
    page,
    10,     # Scrape 10 pages
    50      # Show 50 items per page
)


### Create and activate a virtual environment
```bash
python -m venv venv

venv\Scripts\Activate
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