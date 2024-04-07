import datetime
import requests
import pandas as pd
import sqlalchemy
from sqlalchemy.exc import SQLAlchemyError


class MmrealityScraper:
    """
    A scraper class for extracting data from the MM Reality real estate listings.
    """
    
    def __init__(self):
        """
        Initializes the scraper with specific URL, headers, and data payload for the POST request.
        """
        # Endpoint URL for the API.
        self.url = 'https://mediator.stormm.cz/api/offers/query'
        
        # Headers to mimic a real browser request.
        self.headers = {
            # Various accepted content types.
            'accept': 'application/json, text/plain, */*',
            # Preferred languages.
            'accept-language': 'sk-SK,sk;q=0.9,cs;q=0.8,en-US;q=0.7,en;q=0.6',
            # Content type of the request.
            'content-type': 'application/json;charset=UTF-8',
            # Origin of the request.
            'origin': 'https://www.mmreality.cz',
            # Referrer header.
            'referer': 'https://www.mmreality.cz/',
            # Browser information.
            'sec-ch-ua': '"Google Chrome";v="123", "Not:A-Brand";v="8", "Chromium";v="123"',
            # Mobile device information.
            'sec-ch-ua-mobile': '?0',
            # Operating system information.
            'sec-ch-ua-platform': '"Windows"',
            # Fetch metadata.
            'sec-fetch-dest': 'empty',
            'sec-fetch-mode': 'cors',
            'sec-fetch-site': 'cross-site',
            # User agent string.
            'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/123.0.0.0 Safari/537.36',
        }
        
        # Data payload for the POST request.
        self.data = {
            # Filter criteria for the API.
            "filter": {
                # Common filters.
                "common": {
                    "status": [1],
                    "category": 10,
                    "price": None,
                    "participant": None,
                    "active": 1
                },
                # Geographical filters.
                "geography": {
                    "locations": [],
                    "tolerance": None
                },
                # Group filters.
                "groups": [
                    {
                        "group": 11,
                        "types": [],
                        "energyClassifications": [],
                        "conditions": [],
                        "constructions": [],
                        "ownerships": [],
                        "placements": [],
                        "situations": [],
                        "rooms": [],
                        "equipments": []
                    }
                ]
            },
            # Pagination settings.
            "pagination": {
                "limit": 12,
                "offset": 0,
                "initialOffset": 12,
                "page": 1,
                "pagesCount": 135
            },
            # Sorting criteria.
            "sorting": {
                "descending": True,
                "order": "createdAt"
            }
        }

    def get_scrape_data(self):
        """
        Scrapes data from the MM Reality API and returns a dictionary of lists containing the data.
        """
        # Initialize a dictionary to store the scraped data.
        list_data = {
            'ID': [],
            'URL': [],
            'Category': [],
            'Title': [],
            'Description': [],
            'Area': [],
            'Price': [],
            'Location': [],
            'Country': [],
            'District': [],
        }
        
        # Reset pagination settings before starting the scrape.
        self.data['pagination']['offset'] = 0
        self.data['pagination']['page'] = 1
        
        # Flag to control the scraping loop.
        proced = True
        while proced:
            try:
                # Make a POST request to the API.
                response = requests.post(self.url, headers=self.headers, json=self.data)
                # If the response was unsuccessful, raise an HTTPError.
                response.raise_for_status()
                # Parse the JSON response.
                json_data = response.json()
            except requests.exceptions.HTTPError as e:
                print(f"HTTP error occurred: {e}")
                break
            except requests.exceptions.RequestException as e:
                print(f"Error during requests to {self.url}: {e}")
                break
            except ValueError as e:
                print(f"Value error: {e}")
                break

            # Extract the offers from the JSON data.
            start_point = json_data.get('offers', [])

            print(f'Current page: {self.data["pagination"]["page"]}')
            
            # If no offers are found, stop the loop.
            if not start_point:
                proced = False
            else:
                # Iterate over each offer and collect the data.
                for item in start_point:
                    BASE_URL = 'https://www.mmreality.cz/'
                    detail_url = f'nemovitosti/{item.get('id', 'None')}/?context=list'

                    list_data['ID'].append(item.get('id', 'None'))
                    list_data['Title'].append(item.get('shortTitle', 'None')[8:].strip())
                    list_data['Description'].append(item.get('description', 'None'))
                    list_data['Price'].append(item.get('price', 'None'))
                    list_data['Location'].append(item.get('location', 'None'))
                    list_data['Category'].append(item.get('category', {}).get('name', 'None'))
                    list_data['Country'].append(item.get('country', 'None'))
                    list_data['District'].append(item.get('district', 'None'))
                    list_data['Area'].append(item.get('totalArea', 'None'))
                    list_data['URL'].append(BASE_URL + detail_url)

                # Update the pagination settings for the next loop iteration.
                self.data['pagination']['offset'] += 12
                self.data['pagination']['page'] += 1
                
        return list_data
    
    def create_df(self, df_data):
        """
        Creates a DataFrame from the scraped data.
        
        :param df_data: The data to be converted into a DataFrame.
        :return: A DataFrame if successful, None otherwise.
        """
        try:
            # Attempt to create a DataFrame from the data.
            df = pd.DataFrame(df_data)
            return df
        except ValueError as e:
            print(f"ValueError: {e}")
            return None
        except pd.errors.EmptyDataError as e:
            print(f"EmptyDataError: {e}")
            return None
        except Exception as e:
            print(f"An unexpected error occurred while creating DataFrame: {e}")
            return None
    
    @staticmethod    
    def create_postgre_table(current_date: str, df: pd.DataFrame):
        """
        Creates a new table in a PostgreSQL database from the DataFrame.
        
        :param current_date: The current date to be used in the table name.
        :param df: The DataFrame to be written to the database.
        """
        try:
            # Check if the DataFrame is empty.
            if df.empty:
                raise ValueError("The DataFrame is empty and cannot be written to the database.")
            
            # Connect to the PostgreSQL database.
            engine = sqlalchemy.create_engine('postgresql://postgres:postgres@localhost:5432/postgres')
            
            # Create a new table with the current date in its name.
            table_name = f'mmreality_dataset_{current_date}'
            df.to_sql(table_name, engine, if_exists='replace')
            print(f"Table '{table_name}' created successfully.")
        except ValueError as e:
            print(f"An error occurred: {e}")
        except SQLAlchemyError as e:
            print(f"An error occurred with the database: {e}")
        except Exception as e:
            print(f"An unexpected error occurred: {e}")

if __name__ == '__main__':
    try:
        # Get the current date in YYYY-MM-DD format.
        current_date = datetime.datetime.now().strftime("%Y-%m-%d")
        
        # Instantiate the scraper.
        scraper = MmrealityScraper()
        # Scrape the data.
        df_data = scraper.get_scrape_data()
        
        # If data scraping is successful, proceed to create a DataFrame.
        if df_data is not None:
            df = scraper.create_df(df_data)
            
            # If DataFrame creation is successful, proceed to save it as an Excel file and create a database table.
            if df is not None:
                file_path = f'scrape mmreality/mmreality_dataset_{current_date}.xlsx'
                df.to_excel(file_path, index=False)
                print(f'Dataset mmreality_dataset_{current_date}.xlsx created successfully.')
                
                # Create a table in the PostgreSQL database.
                scraper.create_postgre_table(current_date, df)
            else:
                print("DataFrame creation failed.")
        else:
            print("Data scraping failed.")
            
    except pd.errors.ExcelWriterError as e:
        print(f"Failed to write DataFrame to Excel: {e}")
    except Exception as e:
        print(f"An unexpected error occurred: {e}")