#!/usr/bin/env python3
"""Util to download all resources from the given FHIR server"""
import requests, sys, time


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
    """
    if not url.startswith(base_url):
        second_last_path, last_path = url.split("/")[-2:]
        # FHIR operations
        if last_path.startswith("$"):
            return f"{base_url}/{last_path}"

        # known resources (Hapi FHIR uses Binary)
        if second_last_path in ("Binary"):
            return f"{base_url}/{second_last_path}/{last_path}"

    return url


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


def main():
    # TODO replace with argparse
    if len(sys.argv) == 1:
        print("FHIR base URL missing; pass as first argument")
        exit(1)
    base_url = sys.argv.pop()

    headers = {
        "Accept": "ndjson",
        "Prefer": "respond-async",
        # TODO set via argparse
        #'Authorization': 'Bearer <Auth Token>'
    }

    kickoff_response = requests.post(
        url=f"{base_url}/$export",
        headers=headers,
        # TODO allow passing querystring params via argparse
    )
    # raise exceptions when response status is not 2XX
    kickoff_response.raise_for_status()

    status_poll_url = kickoff_response.headers["Content-Location"]
    # Hapi ignores server_name configuration
    if base_url.startswith("https://"):
        status_poll_url = status_poll_url.replace("http://", "https://")

    complete_json = poll_status(fixup_url(url=status_poll_url, base_url=base_url))
    for file_item in complete_json.get("output"):
        url = fixup_url(url=file_item["url"], base_url=base_url)

        # TODO allow passing directory via argparse
        local_filename = ".".join((
            url.split("/")[-1],
            file_item["type"],
            "ndjson",
        ))
        print("downloading: ", url)
        download_file(url=url, filename=local_filename)
        print("saved to: ", local_filename)

    errors = complete_json.get("errors")
    if errors:
        print(errors)


if __name__ == "__main__":
    main()
