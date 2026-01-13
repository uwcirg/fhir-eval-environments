#!/bin/bash

filetype="json"
# Navigate to the directory containing the files
directory=/c/Users/danie/Documents/src/fhir-eval-environments/test/data/patients/20230929.synthea/fhir
cd "${directory}"
# Counter for the sequential number
count=1

# Loop through all files in the directory
for file in *; do
  # Check if the item is a file (not a directory)
  if [ -f "$file" ]; then
    # Get the file's extension (if it has one)
    extension="${file##*.}"
    if [ "$extension" = "$filetype" ]; then
      # Remove the extension (if any) to work with the file name only
      file_name="${file%.*}"
      new_name="${file_name}_Bundle.${extension}"

        # # Rename the file with a sequential number
        # new_name="${count}.MeasureReport.${extension}"
        # # Increment the counter for the next file
        # ((count++))
        # # Rename the file
    	mv "$file" "$new_name"
    fi
  fi
done
