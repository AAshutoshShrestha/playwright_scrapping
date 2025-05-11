import asyncio
from playwright.async_api import async_playwright
import pandas as pd
from datetime import datetime

async def scrape_floor_sheet(page, max_pages=5, items_per_page=20):
    """Scrape floor sheet data from Nepal Stock Exchange."""
    print("Starting scraping...")
    data = []   # Stores scrap data
    
    # Select the desired option
    await page.wait_for_selector('.table__perpage select', timeout=5000)
    await page.select_option('.table__perpage select', str(items_per_page))

    # click filter button
    await page.click('button.box__filter--search')

    # Wait for the table to reload with new settings
    await asyncio.sleep(2) 
    print(f"Filter data set to {items_per_page}")
    
    for page_num in range(1, max_pages + 1):
        print(f"Scraping page {page_num}...")
        
        # Wait for the table to load
        await page.wait_for_selector('app-floor-sheet table.table')
        
        # Table rows
        rows = await page.query_selector_all('app-floor-sheet table.table tbody tr')
        
        for row in rows:
            cells = await row.query_selector_all('td')
            row_data = [await cell.text_content() for cell in cells]
            
            if len(row_data) >= 8:  # Ensure we have all columns
                # Clean and format the data
                cleaned_data = {
                    'S.N.': row_data[0].strip(),
                    'Contract No': row_data[1].strip(),
                    'Stock Symbol': row_data[2].strip(),
                    'Buyer Broker': row_data[3].strip(),
                    'Seller Broker': row_data[4].strip(),
                    'Quantity': int(row_data[5].replace(',', '')),
                    'Rate (Rs)': float(row_data[6].replace(',', '')),
                    'Amount (Rs)': float(row_data[7].replace(',', ''))
                }
                data.append(cleaned_data)
        
        # Click next page if not on last page
        if page_num < max_pages:
            next_button = await page.query_selector('li.pagination-next a')
            if next_button:
                await next_button.click()
                await asyncio.sleep(2)  # Add delay to avoid being blocked    
    return data

async def main():
    url = "https://nepalstock.com.np/floor-sheet"
    
    async with async_playwright() as p:
        # Launch browser (use chromium by default)
        browser = await p.chromium.launch(headless=False)  # Set headless=True for production
        page = await browser.new_page()
        
        # Set user agent to mimic a real browser
        await page.set_extra_http_headers({
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
        })
        
        try:
            # Navigate to the page
            await page.goto(url, timeout=60000)
            print(f"Navigated to {url}")
            
            # Wait for the page to load completely
            await page.wait_for_selector('app-floor-sheet', timeout=30000)
            
            # Scrape data
            floor_sheet_data = await scrape_floor_sheet(page,3,50)   # Default scrap max_pages 5 & item_per_page 20
            
            # Create DataFrame and save to CSV
            if floor_sheet_data:
                df = pd.DataFrame(floor_sheet_data)
                timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
                output_file = f"floor_sheet_{timestamp}.csv"
                df.to_csv(output_file, index=False)
                print(f"Successfully saved data to {output_file}")
                print(f"Total records scraped: {len(df)}")
            else:
                print("No data was scraped.")
                
        except Exception as e:
            print(f"An error occurred: {str(e)}")
            
        finally:
            # Close browser
            await browser.close()

if __name__ == "__main__":
    asyncio.run(main())