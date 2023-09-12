#!/usr/bin/env python3
"""Util to download all resources from the given FHIR server"""
import argparse, requests, sys, time


def download_file(url, filename=None):
    """Download given large file via streaming"""
    # https://stackoverflow.com/a/16696317
    if not filename:
        filename = url.split("/")[-1]
    with requests.get(url, stream=True) as r:
        r.raise_for_status()
        with open(filename, "wb") as f:
            for chunk in r.iter_content(chunk_size=8192):
                # If you have chunk encoded response uncomment if
                # and set chunk_size parameter to None.
                # if chunk:
                f.write(chunk)
    return filename


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


def poll_status(status_poll_url):
    """Poll given status URL until ready (or timeout). Returns response JSON when ready to download"""
    # TODO set via argparse
    # in seconds
    max_rety_time = 10 * 60
    rety_time = 0

    while rety_time < max_rety_time:
        status_poll_response = requests.get(status_poll_url)
        status_poll_response.raise_for_status()

        retry_after = int(status_poll_response.headers.get("Retry-After", 0))
        if not retry_after:
            return status_poll_response.json()

        progress = status_poll_response.headers.get("X-Progress")
        if progress:
            print("progress: ", progress)

        print(f"waiting {retry_after} seconds")
        rety_time += retry_after
        time.sleep(retry_after)


def kickoff(base_url, no_cache=False):
    """Initate a Bulk Export, return endpoint to poll"""
    headers = {
        "Accept": "application/fhir+json",
        "Prefer": "respond-async",
        # TODO set via argparse
        #'Authorization': 'Bearer <Auth Token>'
    }

    if no_cache:
        print("server-side caching disabled")
        headers["Cache-control"] = "no-cache"

    kickoff_response = requests.post(
        url=f"{base_url}/$export",
        headers=headers,
        # TODO allow passing querystring params via argparse
    )
    # raise exceptions when response status is not 2XX
    try:
        kickoff_response.raise_for_status()
    except requests.exceptions.HTTPError as e:
        print("recieved error from Hapi in kickoff request")
        print("response: ", kickoff_response)
        if kickoff_response.status_code == 400:
            print("recieved 400 in kickoff response; is Bulk Export enabled?")
        exit(1)

    return kickoff_response.headers["Content-Location"]


def main():
    parser = argparse.ArgumentParser(description="Download FHIR resources using Bulk Export")
    parser.add_argument("base_url", help="FHIR base URL")
    parser.add_argument("--no-cache", action="store_true", help="Disable server-side caching")

    args = parser.parse_args()

    status_poll_url = kickoff(base_url=args.base_url, no_cache=args.no_cache)
    complete_json = poll_status(fixup_url(url=status_poll_url, base_url=args.base_url))
    errors = complete_json.get("errors")
    if errors:
        print(errors)

    file_items = complete_json.get("output")
    if not file_items:
        print("warning: no files listed in Complete status response:")
        print(complete_json)
        exit(1)

    for file_item in file_items:
        url = fixup_url(url=file_item["url"], base_url=args.base_url)

        # TODO allow passing directory via argparse
        local_filename = ".".join((
            url.split("/")[-1],
            file_item["type"],
            "ndjson",
        ))
        print("downloading: ", url)
        download_file(url=url, filename=local_filename)
        print("saved to: ", local_filename)


if __name__ == "__main__":
    main()
