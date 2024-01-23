# Synthea Patient Test Data
Randomly generated patient medical records

###### Dataset Generation
Generated using [Synthea](https://github.com/synthetichealth/synthea) using

    $ ./run_synthea -s 981 -p 1000 Washington

*Set `exporter.pretty_print = false` in `src/main/resources/synthea.properties` to reduce output size*

### 20230929.synthea.full/
Folder containing synthetic patient data Bundles

- fhir/
    - 1000 patient medical records
    - One patient record bundle per file
- metadata/
    - Contains metadata file with generation information 

Generation

`$ ./run_synthea -s 981 -p 1000 Washington`

### 20230929.synthea.partial/
Folder containing synthetic patient data Bundles

- fhir/
    - 12 patient medical records
    - One patient record bundle per file
- metadata/
    - Contains metadata file with generation information

Generation
 - First 12 files from the .full dataset alphabetically
 - References customized to avoid some reference mismatching

### 20240122.synthea.partial/
Folder containing synthetic patient data Bundles

- fhir/
    - 16 patient medical records
    - One patient record bundle per file
    - 14,337 patient records
    - 205 hospital/practitioner records
- metadata/
    - Contains metadata file with generation information

Generation

`$ ./run_synthea -s 981 -p 15 Washington`
