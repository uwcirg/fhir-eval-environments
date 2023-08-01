#!/usr/bin/env python3
"""Util to upload all given, or available FHIR resources to the given FHIR server"""
import requests, sys

base_url= sys.argv.pop()

# base_url = "https://hapi.128.208.230.197.nip.io/fhir"
import_url = f"{base_url}/$import"

# https://smilecdr.com/docs/bulk/fhir_bulk_import.html#triggering-a-bulk-import
payload = {
    "resourceType": "Parameters",
    "parameter": [
        {
            "name": "inputFormat",
            "valueCode": "application/fhir+ndjson"
        }, 
        {
            "name": "inputSource",
            "valueUri": base_url,
        }, 
        {
            "name": "storageDetail",
            "part": [
                {
                    "name": "type",
                    "valueCode": "https"
                }, 
                {
                    "name": "maxBatchResourceCount",
                    "valueString": "1000"
                } 
            ]
        }, 
        # {
            # "name": "input",
            # "part": [
                # {
                    # "name": "type",
                    # "valueCode": "Measure"
                # }, 
                # {
                    # "name": "url",
                    # "valueUri": "https://raw.githubusercontent.com/uwcirg/fhir-eval-environments/bfa6570/tests/data/21340.Measure.ndjson"
                # } 
            # ]
        # } 
    ]
}


input_base_url = "https://raw.githubusercontent.com/uwcirg/fhir-eval-environments/22d319d/"


export_resources = (
    "tests/data/21340.Measure.ndjson",
    "tests/data/21364.Organization.ndjson",
    "tests/data/21365.Location.ndjson",

    "tests/data/21318.MeasureReport.ndjson",
    "tests/data/21319.MeasureReport.ndjson",
    "tests/data/21320.MeasureReport.ndjson",
    "tests/data/21321.MeasureReport.ndjson",
    "tests/data/21322.MeasureReport.ndjson",
    "tests/data/21323.MeasureReport.ndjson",
    "tests/data/21324.MeasureReport.ndjson",
    "tests/data/21325.MeasureReport.ndjson",
    "tests/data/21326.MeasureReport.ndjson",
    "tests/data/21327.MeasureReport.ndjson",
    "tests/data/21328.MeasureReport.ndjson",
    "tests/data/21329.MeasureReport.ndjson",
    "tests/data/21330.MeasureReport.ndjson",
    "tests/data/21331.MeasureReport.ndjson",
    "tests/data/21332.MeasureReport.ndjson",
    "tests/data/21333.MeasureReport.ndjson",
    "tests/data/21334.MeasureReport.ndjson",
    "tests/data/21335.MeasureReport.ndjson",
    "tests/data/21336.MeasureReport.ndjson",
    "tests/data/21337.MeasureReport.ndjson",
    "tests/data/21338.MeasureReport.ndjson",
)

input_file_parameters = []
for resource in export_resources:
    resource_type = resource.split(".")[-2]
    full_url = f"{input_base_url}{resource}"

    param = {
        "name": "input",
        "part": [
            {
                "name": "type",
                "valueCode": resource_type
            },
            {
                "name": "url",
                "valueUri": full_url
            }
        ]
    }

    input_file_parameters.append(param)

payload["parameter"].extend(input_file_parameters)

headers = {
    "Accept": "application/fhir+json",
    "Prefer": "respond-async",
    #'Authorization': 'Bearer <Auth Token>'
}

export_status_response = requests.request(
    method="POST",
    url=import_url,
    headers=headers,
    json=payload,
)

print(export_status_response.text)
