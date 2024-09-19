# oas_onboarding

Onboarding of Observed Antibody Space data to Profluent local environmnent.

## Background

The Observed Antibody Space database, or OAS, is a project to collect and annotate immune repertoires for use in large-scale analysis. It currently contains over one billion sequences, from over 80 different studies. These repertoires cover diverse immune states, organisms (primarily human and mouse), and individuals. The OAS database provides clean, annotated, translated antibody repertoire data in a unified format that adheres to the AIRR-seq (Adaptive Immune Receptor Repertoire Sequencing) standards. OAS contains both unpaired VH and VL data, as well as paired VH/VL data. The amount of unpaired data is significantly larger due to higher throughput capabilities of Illumina sequencing versus 10xGenomics sequencing (required for paired chain data). 

A web interface and more information can be found at https://opig.stats.ox.ac.uk/webapps/oas/

## Shell Scripts

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

## Outline of Steps

1. Complete raw downloads of all relevant antibody information from OAS: paired, unpaired, human, mouse, etc.
2. Organize Paired and Unpaired data, and organism data
3. ETL Data into BigQuery
4. Explore Dockerization of the process. This may not be relevant as it appears OAS is not regularly updated.

### Download Notes
- The number of files matches the number of wget lines for the paired sequences and unpaired human heavy/light chains. 
- The number files and wget commands also corresponds for the unpaired nonhuman sequences.