# Download Shell Scripts

Shell scripts are available on the OAS website to download antibody data corresponding to various search parameters, such as pairing, organism, chain type, antibody isotype, etc. For this download, I will download paired and unpaired sequences separately. Sequences can further be separated by organism type; human, mouse, rabbit, and additional organisms are sequenced.

Download the corresponding shell script from the OAS website, copy the script to the directory where the data will be housed, and run the following commands:

```
chmod u+rx [SCRIPT_NAME].sh
./[SCRIPT_NAME].sh
```

The two human unpaired download scripts are significantly larger, and are labled heavy/light_bulk_download respectively. I suggest running these scripts with nohup as the download may take significantly longer.

`nohup bash [SCRIPT_NAME].sh > output.log 2>&1 &`

## Initial Download Directory

Data downloaded from raw shell scripts are stored in the `/export/shared/cameronhu/oas` directory. The directory has been further subdivided into Paired and Unpaired, and then by organism. Unpaired sequences have been further subdivided into light and heavy chains.