# Transform Subpackage

Processing of the raw OAS data file into the format described by the Antibody ERD is handled by the `OASDataProcesser` class. The `OASDataProcessor` is initialized with a path to the OAS file to be processed. Based off the metadata included in the file, the data is processed by either the paired or unpaired workflow. The final output of either input file type is the same, with each sequence having a unique identifier, as well as an antibody entity to which it is linked to. Each antibody entity is linked to its relevant metadata. 

### Unpaired Data

Paired data processing is relatively straightforward. A sequence UID as well as antibody UID is assigned to each sequence. The raw data contains 97 columns. 5 additional columns are added, for a total of 102 columns for every sequence. The added columns are:
- antibody_id
- sequence_id
- Isotype
- Chain
- Species

### Paired Data

Paired data undergoes an additional transform through `split_paired_sequences`. This function handles parsing out the heavy and light chain data from a paired data file. However, relevant information is retained, such as chain type, sequence UIDs, and linkage to the same antibody entity.

All paired sequences should retain the same file structure, in which the first half of the columns pertain to the heavy chain, and the second half of the columns are the light chains. Instead of looping through each column and checking if they are subscript _heavy or _light, I manually mapped the heavy and light column indices as such:

- Heavy Chains: Columns 0 - 98 (inclusive)
- Light Chains: Columns 99 - 197 (inclusive)

An additional way to do this, which makes more sense, is to use a Pandas string comprehension on just the column Index object, to return just the columns that end with the suffix of interest. This is the approach I ended up using.

For each component of the paired data (heavy/light), there should be 99 columns. This differs from the Unpaired data structure, but this is because `sequence_id` and `Isotype` are already included in the Paired Data. Thus, the only columns needed to be added to each of the heavy and light chains are:
- antibody_id
- Chain
- Species

### Downstream Concatenation

Since we are dealing with a dataset on the order of billions of sequences and 100 columns, concatenation operations may not be efficient. Maintaining a consistent columnar structure (all the dataframe columns are ordered in with the same indices) will improve concatenation efficiency.

Using efficient libraries such as Dask, or ordering smaller chunks of the dataset could be appropriate approaches. Additionally, defining a single consistent column structure could make sense, and ordering all dfs to that structure before processing. 

Consistent structure:
`['sequence',
 'locus',
 'stop_codon',
 'vj_in_frame',
 'v_frameshift',
 'productive',
 'rev_comp',
 'complete_vdj',
 'v_call',
 'd_call',
 'j_call',
 'sequence_alignment',
 'germline_alignment',
 'sequence_alignment_aa',
 'germline_alignment_aa',
 'v_alignment_start',
 'v_alignment_end',
 'd_alignment_start',
 'd_alignment_end',
 'j_alignment_start',
 'j_alignment_end',
 'v_sequence_alignment',
 'v_sequence_alignment_aa',
 'v_germline_alignment',
 'v_germline_alignment_aa',
 'd_sequence_alignment',
 'd_sequence_alignment_aa',
 'd_germline_alignment',
 'd_germline_alignment_aa',
 'j_sequence_alignment',
 'j_sequence_alignment_aa',
 'j_germline_alignment',
 'j_germline_alignment_aa',
 'fwr1',
 'fwr1_aa',
 'cdr1',
 'cdr1_aa',
 'fwr2',
 'fwr2_aa',
 'cdr2',
 'cdr2_aa',
 'fwr3',
 'fwr3_aa',
 'fwr4',
 'fwr4_aa',
 'cdr3',
 'cdr3_aa',
 'junction',
 'junction_length',
 'junction_aa',
 'junction_aa_length',
 'v_score',
 'd_score',
 'j_score',
 'v_cigar',
 'd_cigar',
 'j_cigar',
 'v_support',
 'd_support',
 'j_support',
 'v_identity',
 'd_identity',
 'j_identity',
 'v_sequence_start',
 'v_sequence_end',
 'v_germline_start',
 'v_germline_end',
 'd_sequence_start',
 'd_sequence_end',
 'd_germline_start',
 'd_germline_end',
 'j_sequence_start',
 'j_sequence_end',
 'j_germline_start',
 'j_germline_end',
 'fwr1_start',
 'fwr1_end',
 'cdr1_start',
 'cdr1_end',
 'fwr2_start',
 'fwr2_end',
 'cdr2_start',
 'cdr2_end',
 'fwr3_start',
 'fwr3_end',
 'fwr4_start',
 'fwr4_end',
 'cdr3_start',
 'cdr3_end',
 'np1',
 'np1_length',
 'np2',
 'np2_length',
 'c_region',
 'ANARCI_numbering',
 'ANARCI_status',
 'Redundancy',
 'antibody_id',
 'Isotype',
 'Chain',
 'sequence_id',
 'Species']`