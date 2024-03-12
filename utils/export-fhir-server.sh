#!/bin/sh -e
cmdname="$(basename "$0")"
bin_path="$(cd "$(dirname "$0")" && pwd)"
repo_path="$(readlink -f ${bin_path}/..)"

usage() {
    cat << USAGE >&2
Usage:
    $cmdname [--help|-h]


    TODO FILL DESC

USAGE
    exit 1
}

if [ "$1" = "-h" ] || [ "$1" = "--help" ]; then
    usage
    exit 0
fi

FHIR_BASE_URL="$1"
# set -x

FHIR_BASE_URL='https://hapi.128.208.230.197.nip.io/fhir'

export_poll_url=$(curl ${FHIR_BASE_URL}'/$export?_type=Measure,MeasureReport,QuestionnaireResponse' \
    -H 'Prefer: respond-async' \
    -H 'Accept: ndjson' -v \
    -o /dev/null 2>&1 | grep content-location | cut -d ' ' -f3)

export_poll_url=$(echo $export_poll_url | sed 's|http:|https:|g')
export_poll_url=$(echo $export_poll_url | sed 's|\r||g')

# export_poll_url=$(echo $export_poll_url | sed 's|\$|%24|g')
# export_poll_url=$(echo -n $export_poll_url | tr -d '\r')

# echo $export_poll_url > out.bar

echo $export_poll_url
sleep 1m

#temp_dir="$(mktemp --directory --suffix="$cmdname")"
curl "$export_poll_url" | grep url | cut -d'"' -f4 | xargs wget


exit 0
