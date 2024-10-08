# Extract Transform Load Functionality

This package contains the basic ETL functionality for processing raw OAS data files.

## Process module

Processing of the raw OAS data file into the format described by the Antibody ERD is handled by the `OASDataProcesser` class. The `OASDataProcessor` is initialized with a path to the OAS file to be processed. Based off the metadata included in the file, the data is processed by either the paired or unpaired workflow. The final output of either input file type is the same, with each sequence having a unique identifier, as well as an antibody entity to which it is linked to. Each antibody entity is linked to its relevant metadata. 

### Unpaired Data

Paired data processing is relatively straightforward. A sequence UID as well as antibody UID is assigned to each sequence. The raw data contains 97 columns. 5 additional columns are added, for a total of 102 columns for every sequence. The added columns are:
- antibody_id
- sequence_id
- Isotype
- Chain
- Organism

### Paired Data

Paired data undergoes an additional transform through `split_paired_sequences`. This function handles parsing out the heavy and light chain data from a paired data file. However, relevant information is retained, such as chain type, sequence UIDs, and linkage to the same antibody entity.

All paired sequences should retain the same file structure, in which the first half of the columns pertain to the heavy chain, and the second half of the columns are the light chains. Instead of looping through each column and checking if they are subscript _heavy or _light, I manually mapped the heavy and light column indices as such:

- Heavy Chains: Columns 0 - 98 (inclusive)
- Light Chains: Columns 99 - 197 (inclusive)

For each component of the paired data (heavy/light), there should be 99 columns. This differs from the Unpaired data structure, but this is because `sequence_id` and `Isotype` are already included in the Paired Data. Thus, the only columns needed to be added to each of the heavy and light chains are:
- antibody_id
- Chain
- Organism