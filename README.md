# MMReality Scraper

This repository contains a Python script for scraping real estate listings from MM Reality using their API. The script is designed to collect data such as index, title, description, price, location, category, country, district, area, and URL of the listings.

## Features

- Scraping real estate data from MM Reality API.
- Data transformation into a pandas DataFrame.
- Exporting data to an Excel file.
- Creating a PostgreSQL database table with the scraped data.

## Prerequisites

Before you begin, ensure you have met the following requirements:

- Python 3.x installed on your system.
- Required Python packages installed: `requests`, `pandas`, `sqlalchemy`.
- Access to a PostgreSQL database.

## Installation

Clone the repository to your local machine:

```bash
git clone https://github.com/your-username/mmreality-scraper.git
cd mmreality-scraper
```

Install the required packages:

```bash
pip install -r requirements.txt
```

## Usage

To run the scraper, execute the following command:

```bash
python main.py
```

The script will start scraping data and will perform the following actions:

1. Scrape data from the MM Reality API.
2. Create a pandas DataFrame from the scraped data.
3. Save the DataFrame to an Excel file named `mmreality_dataset_YYYY-MM-DD.xlsx`.
4. Create a new table in the PostgreSQL database with the current date in its name and insert the data.

## Configuration

To configure the database connection, modify the `create_postgre_table` method in the `MmrealityScraper` class with your database credentials:

```python
engine = sqlalchemy.create_engine('postgresql://username:password@localhost:5432/database_name')
```

Replace `username`, `password`, and `database_name` with your PostgreSQL credentials.

## Contributing

Contributions are welcome! For major changes, please open an issue first to discuss what you would like to change.

## License

Distributed under the MIT License. See `LICENSE` for more information.

## Contact

Your Name – [@your_twitter](https://twitter.com/your_twitter) – email@example.com

Project Link: [https://github.com/your-username/mmreality-scraper](https://github.com/your-username/mmreality-scraper)

**Note:**

This script is for educational purposes only. Be mindful of Daft.ie's terms of service when scraping their website.
