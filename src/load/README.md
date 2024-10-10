# Load Module

This module performs all interfacing with Google BigQuery. It leverages the Google Cloud BigQuery API to load the tabular outputs of Transform to Google BigQuery.

# Steps
1. Create the appropriate tabular structure in GCP BigQuery
   - Define schema for each of the relational database tables
2. Upload local tabular data into the existing cloud table structure

## BigQuery Table Creation

In order to upload data into Google BigQuery, one must first define the appropriate tables and the schema for each of those tables. We wish to initialize our relational databse following the designs set forth in the Antibdoy Database ERD. Additional table optimizations, including Clustered Table creation, will be explored as well.

## BigQuery Table Upload

Once the tabular structure is initialized with GCP BigQuery, we need to upload our local data (which needs to be in the same schema) to the cloud.