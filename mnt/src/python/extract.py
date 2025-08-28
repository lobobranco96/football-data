from bs4 import BeautifulSoup
import logging

# Configure logging to show INFO level messages
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

class ExtractWikiData:
    """
    A class to extract football teams data from the Brazilian Championship Wikipedia page.

    Attributes:
        driver (webdriver.Chrome): Selenium WebDriver instance to load web pages.
        url (str): The URL of the Wikipedia page to scrape.
    """

    def __init__(self, driver):
        """
        Initializes the ExtractWikiData instance with a Selenium driver and a URL.

        Args:
            driver (webdriver.Chrome): Selenium WebDriver instance.
            url (str): The Wikipedia page URL to scrape.
        """
        self.driver = driver

    def brasileirao_teams(self, url):
        """
        Extracts the Brazilian Championship "Brasileirão 2025" teams from the Wikipedia page.
        url (str): The Wikipedia page URL to scrape.
        Steps:
            1. Load the page using Selenium.
            2. Parse the page source with BeautifulSoup.
            3. Find the table with class 'wikitable sortable'.
            4. Extract column headers.
            5. Extract each row of the table.
            6. Combine columns and rows into a list of dictionaries.

        Returns:
            List[Dict[str, str]]: A list where each element is a dictionary representing a team,
            with column names as keys and cell values as values.
        """
        try:
            logging.info(f"Accessing URL: {self.url}")
            self.driver.get(self.url)
        except Exception as e:
            logging.error(f"Error accessing the URL: {e}")
            raise

        # Wait until the table with both classes is present
        wait = WebDriverWait(self.driver, 10)
        wait.until(EC.presence_of_element_located(
            (By.CSS_SELECTOR, "table.wikitable.sortable")
        ))

        soup = BeautifulSoup(self.driver.page_source, "lxml")
        wiki_data = soup.select_one("table.wikitable.sortable")  

        if wiki_data is None:
            raise ValueError("Table 'wikitable sortable' not found in page")

        # Extract column headers
        columns = [th.get_text(strip=True) for th in wiki_data.find("tr").find_all("th")]

        # Extract all rows
        rows = []
        for tr in wiki_data.find_all("tr")[1:]:  # Skip the header row
            teams = tr.find_all("td")
            if teams:
                # Extract text from each cell in the row
                row = [td.get_text(" ", strip=True) for td in teams]
                rows.append(row)

        # Combine columns and rows into a list of dictionaries
        return [dict(zip(columns, row)) for row in rows]