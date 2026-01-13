# SANER Test Data
Randomly generated MeasureReports based on SANER test Measures

###### Dataset Generation
Generated using https://github.com/uwcirg/saner-connectathon-01-23/blob/main/generateMeasureReports.ipynb

### 20230525.MeasureReport.ndjson
File of MeasureReports formatted for Bulk Import

> *Note: resources do not contain valid references to 'subject' and 'reporter'*

- Daily reports from 2021-01-01 to 2023-01-01 (2 years)
- 18250 MeasureReports
- 5 subjects with randomized capacities
- 5 Measures:
  - [CDCPatientImpactAndHospitalCapacity](https://github.com/uwcirg/saner-connectathon-01-23/blob/main/template_CDCPatientImpactAndHospitalCapacity.json)
  - [FEMADailyHospitalCOVID19Reporting](https://github.com/uwcirg/saner-connectathon-01-23/blob/main/template_FEMADailyHospitalCOVID19Reporting.json)
  - [ICUBedsCurrentOccupancy](https://github.com/uwcirg/saner-connectathon-01-23/blob/main/template_ICUBedCurrentOccupancy.json)
  - [ICUBedStaffedCapacity](https://github.com/uwcirg/saner-connectathon-01-23/blob/main/template_ICUBedStaffedCapacity.json)
  - [ICUBedReporting](https://github.com/uwcirg/saner-connectathon-01-23/blob/main/template_ICUBedsReporting.json)

### 20230721.MeasureReports.full/
Folder containing MeasureReport data files for Bulk Import

- Daily reports from 2021-01-01 to 2022-01-01 (1 year)
- 547,500 MeasureReports
- 100 'hospital' subjects (50-500 beds)
- 200 'clinic' subjects (< 50 beds)
- 5 Measures:
  - [CDCPatientImpactAndHospitalCapacity](https://github.com/uwcirg/saner-connectathon-01-23/blob/main/template_CDCPatientImpactAndHospitalCapacity.json)
  - [FEMADailyHospitalCOVID19Reporting](https://github.com/uwcirg/saner-connectathon-01-23/blob/main/template_FEMADailyHospitalCOVID19Reporting.json)
  - [ICUBedsCurrentOccupancy](https://github.com/uwcirg/saner-connectathon-01-23/blob/main/template_ICUBedCurrentOccupancy.json)
  - [ICUBedStaffedCapacity](https://github.com/uwcirg/saner-connectathon-01-23/blob/main/template_ICUBedStaffedCapacity.json)
  - [ICUBedReporting](https://github.com/uwcirg/saner-connectathon-01-23/blob/main/template_ICUBedsReporting.json)

- Referential integrity maintained through contained resources

### 20230721.MeasureReports.partial/
Folder containing a subset of files from 20230721.MeasureReports.full

- Daily reports from 2021-01-01 to 2022-01-01 (1 year)
- 27,375 MeasureReports
- 5 'hospital' subjects (50-500 beds)
- 10 'clinic' subjects (< 50 beds)
- 5 Measures:
  - [CDCPatientImpactAndHospitalCapacity](https://github.com/uwcirg/saner-connectathon-01-23/blob/main/template_CDCPatientImpactAndHospitalCapacity.json)
  - [FEMADailyHospitalCOVID19Reporting](https://github.com/uwcirg/saner-connectathon-01-23/blob/main/template_FEMADailyHospitalCOVID19Reporting.json)
  - [ICUBedsCurrentOccupancy](https://github.com/uwcirg/saner-connectathon-01-23/blob/main/template_ICUBedCurrentOccupancy.json)
  - [ICUBedStaffedCapacity](https://github.com/uwcirg/saner-connectathon-01-23/blob/main/template_ICUBedStaffedCapacity.json)
  - [ICUBedReporting](https://github.com/uwcirg/saner-connectathon-01-23/blob/main/template_ICUBedsReporting.json)

- Referential integrity maintained through contained resources
