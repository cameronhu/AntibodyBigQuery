# OAS Extract Transform Load Functionality

This package contains the basic ETL functionality for processing raw OAS data files into the standard relational database structure, as defined by the Antibody ERD diagram.

## Modules 

**Transform** - defines an OASDataProcessor class that parses a single OAS file, and returns three tabular datasets matching the ERD.

**Load** - leverages the Google Cloud BigQuery API to load the tabular outputs of Transform to Google BigQuery. 