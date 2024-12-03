#!/usr/bin/env python3
"""Util to upload all resources in given directory to given FHIR server"""
import argparse, requests, sys, json, time


def obtain_filelist():
    owner = "uwcirg"
    repo = "fhir-mock-data"
    branch = "test-bulk-import"
    directory = "test-bulk-import"
    #src_url = f"https://api.github.com/repos/{owner}/{repo}/contents/{directory}"
    src_url = f"https://raw.githubusercontent.com/{owner}/{repo}/refs/heads/{branch}/{directory}"

    headers = {
        "Accept": "application/vnd.github+json",
        "X-GitHub-Api-Version": "2022-11-28",
        "User-Agent": "pbugni@uw.edu",
    }
    if False:
        # dysfunctional; may use in the future for dynamic lookup of available ndjson files
        response = requests.get(src_url, headers=headers)
        response.raise_for_status()
        for item in response.json():
            print(item['name'])

    # Need to control order of imports due to dependency graph.  manually deliver filelist for now
    items = ('Patient.ndjson', 'Encounter.ndjson')
    for i in items:
        yield f"{src_url}/{i}"


def build_request_body():
    """Build bulk import POST body from available import files"""
    body = {
        "resourceType": "Parameters",
        "parameter": 
            [
                {
                    "name": "inputFormat",
                    "valueCode": "application/fhir+ndjson",
                },
                {
                    "parameter": "storageDetail",
                    "part": [
                        {
                            "name": "type",
                            "valueCode": "https",
                        },
                        {
                            "name": "maxBatchResourceCount",
                            "valueString": "500",
                        }
                    ],
                }
            ]
        }

    for ndjson_file_url in obtain_filelist():
        response = requests.get(ndjson_file_url)
        response.raise_for_status()
        ndjson = json.loads(response.text.splitlines()[0])
        resourceType = ndjson['resourceType']
        body["parameter"].append({
            "name": "input",
            "part": [
                {
                    "name": "type",
                    "valueCode": resourceType,
                },
                {
                    "name": "url",
                    "valueUri": ndjson_file_url,
                }
            ]
        })

    return body


def fixup_url(url, base_url):
    """
    Replace FHIR base URL in given FHIR API call with different base_url
    Helpful when a FHIR server is configured with a server_name that does not match its public one
    No generalized solution when urls significantly different
    """

    # Hapi ignores server_name configuration
    if base_url.startswith("https://"):
        url = url.replace("http://", "https://")

    if url.startswith(base_url):
        return url

    second_last_path, last_path = url.split("/")[-2:]
    # FHIR operations
    if last_path.startswith("$"):
        return f"{base_url}/{last_path}"

    # known resources (Hapi FHIR uses Binary)
    if second_last_path in ("Binary"):
        return f"{base_url}/{second_last_path}/{last_path}"


def poll_status(status_poll_url, auth_token=None, max_rety_time=600):
    """Poll given status URL until ready (or timeout). Returns response JSON when ready to download"""

    headers = {}
    if auth_token is not None:
        headers["Authorization"] = f"Bearer {auth_token}"

    rety_time = 0
    while rety_time < max_rety_time:
        status_poll_response = requests.get(status_poll_url, headers=headers)
        status_poll_response.raise_for_status()

        retry_after = int(status_poll_response.headers.get("Retry-After", 0))
        if not retry_after:
            return status_poll_response

        progress = status_poll_response.headers.get("X-Progress")
        if progress:
            print("progress: ", progress)

        print(f"waiting {retry_after} seconds")
        rety_time += retry_after
        time.sleep(retry_after)
    print("timeout exceeded")
    exit(1)


def kickoff(base_url, auth_token=None):
    """Initate a Bulk Import, return endpoint to poll"""
    body = build_request_body()
    print(f"POSTing to {base_url}/$import:")
    print(json.dumps(body, indent=4))
    headers = {
        "Accept": "application/json",
        "Content-Type": "application/fhir+ndjson",
        "Prefer": "respond-async",
    }

    params = {}
    if auth_token is not None:
        headers["Authorization"] = f"Bearer {auth_token}"

    kickoff_response = requests.post(
        url=f"{base_url}/$import",
        headers=headers,
        params=params,
        json=body,
    )
    # raise exceptions when response status is not 2XX
    try:
        kickoff_response.raise_for_status()
    except requests.exceptions.HTTPError as e:
        print("recieved error from Hapi in kickoff request")
        print("response: ", kickoff_response.content)
        if kickoff_response.status_code == 400:
            print("recieved 400 in kickoff response; is Bulk Import enabled?")
        exit(1)

    return kickoff_response.headers["Content-Location"]


def main():
    parser = argparse.ArgumentParser(description="Download FHIR resources using Bulk Export")
    parser.add_argument("base_url", help="FHIR base URL")
    parser.add_argument("--directory", action="store", help="Save files to given directory", default="./")
    parser.add_argument("--no-cache", action="store_true", help="Disable server-side caching")
    parser.add_argument("--max-timeout", action="store", help="Max timeout in seconds before failing", type=int, default=60*10)
    parser.add_argument("--auth-token", action="store", help="Use given token to authenticate")

    args = parser.parse_args()

    status_poll_url = kickoff(base_url=args.base_url, auth_token=args.auth_token)
    complete_response = poll_status(
        fixup_url(url=status_poll_url, base_url=args.base_url),
        auth_token=args.auth_token,
        max_rety_time=args.max_timeout,
    )
    try:
        complete_json = complete_response.json()
    except json.decoder.JSONDecodeError:
        print("error: import completed successfully, but response is not JSON: ", complete_response.text)
        print("warning: the Bulk Import request (for Hapi) likely did not return any resources")
        exit(1)

    errors = complete_json.get("errors")
    if errors:
        print(errors)


if __name__ == "__main__":
    main()
