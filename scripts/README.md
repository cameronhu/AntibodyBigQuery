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

 ## Detailed breakdown of process vs upload
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