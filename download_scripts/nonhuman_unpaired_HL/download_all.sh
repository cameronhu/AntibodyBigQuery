#!/bin/bash

# Name of the new directory to be created
NEW_DIR="/export/share/cameronhu/oas/unpaired/non-human"

# Create the new directory
mkdir -p "$NEW_DIR"

# Loop through each script in the current directory
for script in *.sh; do

    chmod +x "$script"

    # Check if the file is a bash script
    if [[ -f "$script" && -x "$script" && "$script" != "download_all.sh" ]]; then
        echo "Running $script in $NEW_DIR"
        # Run the script, making sure it runs within the new directory
        cp "$script" "$NEW_DIR"
        (cd "$NEW_DIR" && bash "$script")
    else
        echo "Skipping $script: Not an executable script."
    fi
done

echo "All scripts have been run in $NEW_DIR."
