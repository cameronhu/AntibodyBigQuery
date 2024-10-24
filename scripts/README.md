# Test Scripts

## test_rdms.py

Testing of both the transform and load packages. Can call test_rdms.py from the command line with an argument of the number of files to sample. For example:

`python3 test_rdms.py 10` 

This script samples n files from the paired human, unpaired heavy human, and unpaired heavy light directories as a test.

## First timing outputs

```
python3 test_rdms.py 1
Processing and uploading of 1 files completed in 36.87 seconds.
 Paired processing took: 13.570555448532104 seconds 
 Heavy processing took: 12.317015647888184 seconds 
 Light processing took: 10.984614372253418 seconds
 ```

 ### Detailed breakdown of process vs upload
```
Function 'process_file' executed in 0.9166s
Function 'upload_all' executed in 11.2491s
Function 'process_file' executed in 0.0047s
Function 'upload_all' executed in 9.4761s
Function 'process_file' executed in 0.2081s
Function 'upload_all' executed in 10.2085s
Processing and uploading of 1 files per paired, heavy, and light chains completed in 32.06 seconds.
 Paired chain processing of 17908 sequences took: 12.17 seconds (process: 0.92 seconds, upload: 11.25 seconds)
 Heavy chain processing of 2 took: 9.48 seconds (process: 0.00 seconds, upload: 9.48 seconds)
 Light chain processing of 4098 took: 10.42 seconds (process: 0.21 seconds, upload: 10.21 seconds)
 ```

22,008 sequences were uploaded over 32.06 seconds. ~686 sequences per second. ~2915452 seconds, ~809 hours, ~34 days

### Breakdown with metadata as Dataframe instead of Json
Function 'process_file' executed in 1.4373s
Function 'upload_all' executed in 18.9563s
Function 'process_file' executed in 0.0048s
Function 'upload_all' executed in 7.8246s
Function 'process_file' executed in 0.3267s
Function 'upload_all' executed in 8.0602s
Processing and uploading of 1 files per paired, heavy, and light chains completed in 36.61 seconds.
 Paired chain processing of 17908 sequences took: 20.39 seconds (process: 1.44 seconds, upload: 18.96 seconds)
 Heavy chain processing of 2 took: 7.83 seconds (process: 0.00 seconds, upload: 7.82 seconds)
 Light chain processing of 4098 took: 8.39 seconds (process: 0.33 seconds, upload: 8.06 seconds)

### Breakdown with metadata as Dataframe instead of Json, Fireducks


## Timing test of DataManager implementation (manual batching)
```
Processing and uploading of 1 batches per paired, heavy, and light chains
Total processing of 104800 completed in 57.27 seconds.

Paired chain processing of 71316 sequences took: 28.00 seconds (process: 4.70 seconds, upload: 23.30 seconds)
Heavy chain processing of 285 took: 9.67 seconds (process: 0.28 seconds, upload: 9.39 seconds)
Light chain processing of 33199 took: 19.61 seconds (process: 3.08 seconds, upload: 16.53 seconds)
```

104,800 sequences in 57.27 seconds. ~1830 sequences / second. For 2 bill sequences, ~1092896 seconds, ~303.6 hours, ~12.6 days

## Timing test of DataManager implementation (Batch class batching)

Function 'process_files' executed in 159.0953s
Function 'upload_all' executed in 129.3483s
For batch 0, 1896620 processed, uploading took: 129.34832466000034, processing took: 159.0953004349999
Function 'process_files' executed in 117.2710s
Function 'upload_all' executed in 132.6003s
For batch 0, 1905859 processed, uploading took: 132.60034026500034, processing took: 117.27096974100004
Function 'process_files' executed in 113.9589s
Function 'upload_all' executed in 133.2201s
For batch 0, 1978491 processed, uploading took: 133.22009472900027, processing took: 113.95885420500053

~ 4 days of processing time

## Memory and timing test for increased batches (5)

Need to ensure enough RAM for Pandas processes when running the major job. Want to also document the maximum amount of memory used for the 5 batches.

From personal observation via `htop`, the max RAM used occurs during merge operations and I think uploading operations. Max RAM used personally observed got up to 50 GB out of the 98.2 GB

### Timing
Function 'upload_all' executed in 9.4270s
For batch 3, 594 processed, uploading took: 9.42696184500005, processing took: 0.08975392399997872
Function 'process_files' executed in 238.9650s                                  
Function 'upload_all' executed in 187.4388s
For batch 4, 4030641 processed, uploading took: 187.43884475899995, processing took: 238.9649895030002
Function 'process_files' executed in 112.8231s
Function 'upload_all' executed in 133.4009s                                                    
For batch 0, 1978491 processed, uploading took: 133.4009297810003, processing took: 112.82306368299987
Function 'process_files' executed in 126.2715s
Function 'upload_all' executed in 125.0341s
For batch 1, 2173960 processed, uploading took: 125.03410934299973, processing took: 126.2715166920002
Function 'process_files' executed in 250.4073s
Function 'upload_all' executed in 205.2993s
For batch 2, 4446576 processed, uploading took: 205.299349806, processing took: 250.4073148829998
Function 'process_files' executed in 110.0403s
Function 'upload_all' executed in 138.8709s
For batch 3, 1980461 processed, uploading took: 138.87089849199992, processing took: 110.04027091399985
Function 'process_files' executed in 116.9063s
Function 'upload_all' executed in 129.4772s
For batch 4, 2187713 processed, uploading took: 129.4772040849998, processing took: 116.90629718499986
Processing and uploading of 5 batches per paired, heavy, and light chains
 Total processing of 26826785 completed in 3221.14 seconds.

Paired chain processing of 3908158 sequences took: 622.53 seconds (process: 330.78 seconds, upload: 291.75 seconds)
 Heavy chain processing of 10151426 took: 1150.08 seconds (process: 583.01 seconds, upload: 567.07 seconds)
 Light chain processing of 12767201 took: 1448.53 seconds (process: 716.45 seconds, upload: 732.08 seconds)

 Sequence process and upload at rate of 8328.34 sequences per second.
 Predicted time for full 2 * 10^9 OAS sequences to be processed: 240143.87 seconds, 66.71 hours, 2.78 days


## Sanity Checks

For testing with 5 batches in the test_data_manager.py script.

**Human Paired Sequences** - A total of 3,908,158 paired human "sequences" were processed and uploaded. There are 1,954,079 paired human sequences in OAS. For the sequence table, the heavy and light chains are split, leading to double the number of sequences. 1,954,079 * 2 = 3,908,158. This sanity check passes.

**Metadata Files** - There should be the same number of metdata entries as files parsed. Checking the batch lists and counting the number of files is N files. This is equal to the M metadata entries in BigQuery.

 # Next Steps

 Confirmed that the processing portion is not the bottleneck, but the upload into Google BigQuery is. Thus, should look into optimized/alternative uploading methods:

 - Potentially upload all the files into GCP Buckets first 
 - Concatentate individual dataframes into a larger dataframe, with some limit for how long the dataframe will be. This will decrease the number of individual calls to upload to BigQuery but increase the amount of data uploaded per call.

### Debugging Errors

`DtypeWarning: Columns (109,125,126,127,128,155,191) have mixed types. Specify dtype option on import or set low_memory=False.
  sequence_df = pd.read_csv(self.data_unit_file, header=1)`