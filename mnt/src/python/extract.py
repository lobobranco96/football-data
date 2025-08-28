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
        rows = list()
        links = list() # store url pages from players team
        for tr in wiki_data.find_all("tr")[1:]:
            teams = tr.find_all("td")
            if teams:
                row = []
                for idx, td in enumerate(teams):
                    if idx == 0:
                        a_tag = td.find("a")
                        team_name = td.get_text(" ", strip=True).replace("\xa0", "")
                        href = a_tag.get("href") if a_tag else None
                        row.append(team_name)
                        links.append("https://pt.wikipedia.org" + href if href else None)
                    else:
                        row.append(td.get_text(" ", strip=True).replace("\xa0", ""))
                rows.append(row)

        # Combine columns and rows into a list of dictionaries
        return [dict(zip(columns, row)) for row in rows], links

    def collect_full_players_data(self, team_url_list):
      """
      Itera sobre todas as URLs de times e junta todos os jogadores em uma lista de dicionários.

      Args:
          lista_times (List[str]): Lista de URLs das páginas de cada time.

      Returns:
          List[Dict]: Lista com todos os jogadores de todos os times.
      """
      players = []

      for team_url in team_url_list:
          try:
              players_team = self.brasileirao_players(team_url)
              if players_team:
                  players.extend(players_team)
                  logging.info(f"Extraídos {len(players_team)} jogadores de {team_url}")
              else:
                  logging.warning(f"{team_url} - Falhou: retornou lista vazia")
          except Exception as e:
              logging.error(f"Erro ao extrair jogadores de {team_url}: {e}")


      return players

    def brasileirao_team_players(self, team_url):
        try:
            logging.info(f"Accessing URL: {self.url}")
            self.driver.get(team_url)
        except Exception as e:
            logging.error(f"Error accessing the URL: {e}")
            raise

        soup = BeautifulSoup(self.driver.page_source, "lxml")
        
        # Collect Team Name
        team_name_tag = soup.find("table", class_="infobox vcard vevent")
        team_name_tag = team_name_tag.find(class_="fn summary") if team_name_tag else None
        team_name = team_name_tag.get_text().strip() if team_name_tag else None

        # Localize the correct player data over class toccolours
        players_table = None
        for table in soup.find_all("table", class_="toccolours"):
            if "N.º" in table.get_text() and "Pos." in table.get_text():
                players_table = table
                break

        players_list = list()
        
        if players_table:
            for row in players_table.find_all("tr")[2:]:  # ignore headers
                columns = row.find_all("td")
                # Itera de 3 em 3 colunas (cada jogador)
                for i in range(0, len(columns), 3):
                    if i+2 < len(columns):
                        tshirt_number = columns[i].get_text(strip=True)
                        position = columns[i+1].get_text(strip=True)
                        player_name = columns[i+2].get_text(strip=True)

                        players_list.append({
                            "tshirt_number": tshirt_number,
                            "position": position,
                            "player_name": player_name,
                            "team_name": team_name
                        })

        return players_list



