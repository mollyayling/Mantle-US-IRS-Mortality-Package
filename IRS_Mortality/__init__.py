"""Module for initialising the tables used in the IRS_Rates package."""

from Tables.BaseTable import BaseTable
from Tables.ImprovementTable import ImprovementTable
from Tables.ProjectionYears import ProjectionYears
from Tables.Published430 import PublishedTables
from Tables.Blending import BlendingTable
from Tables.Published417e import Published_417e

# Create the base table object.
pri_2012 = BaseTable('./Data/Base Tables/Pri-2012.csv')

# Create the improvement table objects.
MP_2021_Adj_Females = ImprovementTable('./Data/Improvement Tables/MP2021_Adj_Females.csv')
MP_2021_Adj_Males = ImprovementTable('./Data/Improvement Tables/MP2021_Adj_Males.csv')

# Create the projection years object.
projection_years = ProjectionYears('./Data/Projection Methods/Projection Years.csv')

# Create the published tables objects.
published_430 = PublishedTables('./Data/Published Tables/430_Published')
published_417e = Published_417e('./Data/Published Tables/417e Published.csv')

# Create the blending table object.
blending_table = BlendingTable('./Data/Projection Methods/Blending.csv')