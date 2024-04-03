from abc import ABC
import csv

class Table(ABC):
    """An abstract class for a table of csv data.
    
    Attributes:
    ------------
    csv_table: A string representing the name of the .csv file containing the table.
    
    Methods:
    --------
    load: A method to load the table from the .csv file into a dictionary.
    """

    def __init__(self, input_file : str):
        """Initialise the table with a .csv file and validate the .csv file."""
        if input_file.split(".")[-1] != "csv":
            raise ValueError("Invalid file type. Only .csv files are supported.")
        self.csv_table = input_file
        self.table = None

    def load(self):
        """Load the table from the .csv file into a dictionary."""
        with open(self.csv_table, 'r') as f:
            reader = csv.DictReader(f)
            field_names = {name : int(name) if name.isdigit() else name for name in reader.fieldnames[1:]}
            reader_list = list(reader)
            self.table={field_names[fieldname] : {int(row['Age']): float(row[fieldname]) for row in reader_list} for fieldname in field_names.keys()}
            return self.table