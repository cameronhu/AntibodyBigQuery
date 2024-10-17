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

 # Next Steps

 Confirmed that the processing portion is not the bottleneck, but the upload into Google BigQuery is. Thus, should look into optimized/alternative uploading methods:

 - Potentially upload all the files into GCP Buckets first 
 - Concatentate individual dataframes into a larger dataframe, with some limit for how long the dataframe will be. This will decrease the number of individual calls to upload to BigQuery but increase the amount of data uploaded per call.