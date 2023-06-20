#!/usr/bin/env python3
"""Util to upload all given, or available FHIR resources to the given FHIR server"""
import requests

base_url = "https://hapi.128.208.230.197.nip.io/fhir"
url = f"{base_url}/$import"
# {fileNumber}.{ResourceType}.ndjson
payload = {
    "inputFormat": "application/fhir+ndjson",
    # URI for tracking this set of imported data throughout its lifecycle.
    # MAY be used to specify a FHIR endpoint that can by the importing system when matching references to previously imported data.
    "inputSource": base_url,
    "storageDetail": { "type": "https" },
    "input": [
        {
            "type": "Patient",
            "url": "https://localhost/patient_ndjson.ndjson"
        }
    ]
}

payload = {
  "resourceType": "Parameters",
  "parameter": [
    {
      "name": "exportUrl",
      "valueUrl": "https://bulk-data.smarthealthit.org/fhir/$export"
    },
    {
      "name": "exportType",
      "valueCode": "dynamic"
    }
  ]
}

# https://smilecdr.com/docs/bulk/fhir_bulk_import.html#triggering-a-bulk-import
payload = {
  "resourceType": "Parameters",
  "parameter": [ {
    "name": "inputFormat",
    "valueCode": "application/fhir+ndjson"
  }, {
    "name": "inputSource",
    "valueUri": "http://example.com/fhir/"
  }, {
    "name": "storageDetail",
    "part": [ {
      "name": "type",
      "valueCode": "https"
    }, {
      "name": "credentialHttpBasic",
      "valueString": "admin:password"
    }, {
      "name": "maxBatchResourceCount",
      "valueString": "500"
    } ]
  }, {
    "name": "input",
    "part": [ {
      "name": "type",
      "valueCode": "Observation"
    }, {
      "name": "url",
      "valueUri": "https://example.com/observations.ndjson"
    } ]
  }, {
    "name": "input",
    "part": [ {
      "name": "type",
      "valueCode": "Patient"
    }, {
      "name": "url",
      "valueUri": "https://example.com/patients.ndjson"
    } ]
  } ]
}


headers = {
    "Accept": "application/fhir+json",
    "Prefer": "respond-async",
    #'Content-Type': 'application/json',
    #'Authorization': 'Bearer <Auth Token>'
}

response = requests.request("POST", url, headers=headers, json=payload)

print(response.text)
