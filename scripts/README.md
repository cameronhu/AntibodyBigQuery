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