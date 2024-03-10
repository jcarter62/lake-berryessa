import requests
import csv
from io import StringIO

class URLDataLoader:
    def __init__(self, url):
        self.url = url
        self.data = []

    def fetch_and_load_data(self):
        try:
            response = requests.get(self.url)
            response.raise_for_status()  # Raises an HTTPError if the response status code is not 200
            data_string = StringIO(response.text)
            csv_reader = csv.reader(data_string, delimiter=',')
            next(csv_reader, None)  # Skip the header row if there is one
            self.data = [row for row in csv_reader]
        except requests.RequestException as e:
            print(f"An error occurred while fetching data: {e}")

    def get_data(self):
        return self.data

# # Usage
# url = "https://www.scwamonitoring.com/images/LBWS_Level_3Day.csv"
# loader = URLDataLoader(url)
# loader.fetch_and_load_data()
# data = loader.get_data()
# print(data)
