# Synthea Patient Test Data
Randomly generated patient medical records

###### Dataset Generation
Generated using [Synthea](https://github.com/synthetichealth/synthea) using

    $ ./run_synthea -s 981 -p 1000 Washington

*Set `exporter.pretty_print = false` in `src/main/resources/synthea.properties` to reduce output size*

### 20230929.synthea/
Folder containing synthetic patient data Bundles

- fhir/
    - 1000 patient medical records
    - One patient record bundle per file
- metadata/
    - Contains metadata file with generation information 

