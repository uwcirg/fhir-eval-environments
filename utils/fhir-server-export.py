#!/usr/bin/env python3
"""Util to upload all given, or available FHIR resources to the given FHIR server"""
import requests, sys, time


def poll_status(status_poll_url):
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


def download_file(url, filename=None):
    if not filename:
        filename = url.split("/")[-1]
    # NOTE the stream=True parameter below
    with requests.get(url, stream=True) as r:
        r.raise_for_status()
        with open(filename, "wb") as f:
            for chunk in r.iter_content(chunk_size=8192):
                # If you have chunk encoded response uncomment if
                # and set chunk_size parameter to None.
                # if chunk:
                f.write(chunk)
    return filename


def main():
    base_url = sys.argv.pop()

    headers = {
        "Accept": "ndjson",
        "Prefer": "respond-async",
        #'Authorization': 'Bearer <Auth Token>'
    }

    kickoff_response = requests.post(
        url=f"{base_url}/$export",
        headers=headers,
    )

    # raise exceptions when response status is not 2XX
    kickoff_response.raise_for_status()

    status_poll_url = kickoff_response.headers["Content-Location"]
    # Hapi ignores server_name configuration
    if base_url.startswith("https://"):
        status_poll_url = status_poll_url.replace("http://", "https://")
    print(status_poll_url)

    complete_json = poll_status(status_poll_url)

    for file_item in complete_json.get("output"):
        local_filename = ".".join((
            file_item["url"].split("/")[-1],
            file_item["type"],
            "ndjson",
        ))
        print("downloading: ", file_item["url"])
        download_file(url=file_item["url"], filename=local_filename)

    errors = complete_json.get("errors")
    if errors:
        print(errors)

if __name__ == "__main__":
    main()

# FHIR_BASE_URL='https://hapi.128.208.230.197.nip.io/fhir'

# export_poll_url=$(curl ${FHIR_BASE_URL}'/$export?_type=Measure,MeasureReport,QuestionnaireResponse' \
    # -H 'Prefer: respond-async' \
    # -H 'Accept: ndjson' -v \
    # -o /dev/null 2>&1 | grep content-location | cut -d ' ' -f3)

# export_poll_url=$(echo $export_poll_url | sed 's|http:|https:|g')
# export_poll_url=$(echo $export_poll_url | sed 's|\r||g')

# export_poll_url=$(echo $export_poll_url | sed 's|\$|%24|g')
# export_poll_url=$(echo -n $export_poll_url | tr -d '\r')

# echo $export_poll_url > out.bar

# echo $export_poll_url
# sleep 1m

#temp_dir="$(mktemp --directory --suffix="$cmdname")"
# curl "$export_poll_url" | grep url | cut -d'"' -f4 | xargs wget
