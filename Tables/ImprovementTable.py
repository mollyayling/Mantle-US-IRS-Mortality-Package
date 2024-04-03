from .Table import Table

class ImprovementTable(Table):
    """A subclass of the abstract Table class for improvement tables."""

    max_year = 2178
    min_age = 15

    def load(self):
        """Load the table from the .csv file into a dictionary and extrapolate it."""
        table = super().load()
        return ImprovementTable.extrapolate(table)

    @classmethod
    def extrapolate(cls, table):
        """Extrapolate the improvement table to the maximum year and minimum age."""
        last_year = list(table.keys())[-1]
        first_age = list(table[last_year].keys())[0]

        #Extrapolate to minimum age.
        if first_age > 15:
            for year in table.keys():
                new_dict = {age: table[year][first_age] for age in range(15, first_age)}
                new_dict.update(table[year])
                table[year] = new_dict

        #Extrapolate to maximum year.
        if last_year < cls.max_year:
            last_improvement = table[last_year]
            extra_improvements = {year : last_improvement for year in range(last_year + 1, cls.max_year + 1)}
            table.update(extra_improvements)
        return table
            

            