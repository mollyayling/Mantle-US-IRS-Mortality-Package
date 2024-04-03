import csv
import os
from .Table import Table

class PublishedTables(Table):
    """A subclass of the abstract Table class for the published 430 tables."""

    def __init__(self, directory: str):
        """Initialise and validate directory containing 430 published tables.
        
        This method overrides the initialisation method in the Table superclass.
        """
        for file in os.listdir(directory):
            if file.split(".")[-1] != "csv":
                raise ValueError(f"Invalid file type for {file}. Only .csv files are supported.")
        self.directory = directory

    def load(self) -> dict:
        """Load the published tables into two dictionaries for 430 and 430 static rates and return them.
        
        This method overrides the load method in the Table superclass.
        """
        self.published_430_tables = {}
        self.published_430_static_tables = {}
        self.published_years = []
        headers = ["Male EE", "Male HA", "Female EE", "Female HA"]
        static_headers = ["Male","Female"]
        for file in os.listdir(self.directory):
            with open(os.path.join(self.directory, file), 'r') as f:
                year = int(next(f).split(",")[0])
                self.published_years.append(year)
                reader = list(csv.DictReader(f))
                self.published_430_tables[year] = {header : {int(row["Age"]): float(row[header]) for row in reader} for header in headers}
                self.published_430_static_tables[year] = {header : {int(row["Age"]): float(row[header]) for row in reader} for header in static_headers}
        return self.published_430_tables, self.published_430_static_tables
    
