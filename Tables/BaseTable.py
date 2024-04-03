from .Table import Table
import csv

class BaseTable(Table):
    """A subclass of the abstract Table class for base tables."""
    def __init__(self, input_file : str):
        super().__init__(input_file)
        self.year = None

    def load(self):
        """Load the table from the .csv file into a dictionary."""
        with open(self.csv_table, 'r') as f:
            reader = csv.reader(f)
            self.year = int(next(reader)[0].split("-")[-1])
            header = next(reader)  
            reader = csv.DictReader(f, fieldnames=header)
            field_names = {name : int(name) if name.isdigit() else name for name in reader.fieldnames[1:]}
            reader_list = list(reader)
            self.table = {field_names[fieldname] : {int(row['Age']): float(row[fieldname]) for row in reader_list} for fieldname in field_names.keys()}
            return self.table, self.year

    






    