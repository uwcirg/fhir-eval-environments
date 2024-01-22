#!/bin/bash
# url="https://firely.fl.dlorigan.dev.cirg.uw.edu/"
# url="https://hapi.fhir-eval.demo.cirg.uw.edu/fhir/"
# url="https://aidbox.fhir-eval.demo.cirg.uw.edu/fhir/"
timestamp=`date +"%Y.%m.%d.%H%M%S"`
cd ..
test_directory=$(pwd)
fhirLoaderProjectPath="$test_directory/FhirLoader"
output_prefix="$test_directory/tests/results/$timestamp"
# Initialize variables with default values
url=""
threads=1
token=""
tests=()
test_size="partial"

# Usage function
usage() {
    echo "Usage: $0 -u <server_url> -f [-t <num_threads>] [-a <access_token>] [<test1> ...]"
    exit 1
}
[ $# -eq 0 ] && usage

# Parse options and their values
while getopts "u:t::a::f" opt; do
    case $opt in
        u)
            url="${OPTARG}"
            echo "url is ${url}"
            ;;
        t)
            threads="${OPTARG}"
            echo "threads is $threads"
            ;;
        a)
            token="--access-token ${OPTARG}"
            echo "token is $token"
            ;;
        f)
            test_size="full"
            echo "size is $test_size"
            ;;
        \?)
            echo "Invalid option: -$OPTARG"
            usage
            ;;
    esac
done

# Shift the processed options out of the argument list
shift $((OPTIND-1))
tests=$@

# Check for mandatory arguments
if [[ -z $url ]]; then
    echo "Url is required"
    usage
fi

load_saner() {
    # load saner data
    echo "Loading SANER MeasureReports"

    saner_folders=(
        "clinics"
        "hospitals"
    )

    for dir in ${saner_folders[@]}; do
        folder="$test_directory/data/saner/20230721.MeasureReports.$test_size/$dir/fhir"
        # Check if the folder exists
        if [ ! -d "$folder" ]; then
            echo "Folder not found: $folder"
            exit 1
        fi

        echo "Loading files from ${folder}"
        # Iterate through each file in the folder
        for file in "$folder"/*; do
            # Check if the item is a file (not a directory)
            if [ -f "$file" ]; then
                echo "{ time dotnet run -- --fhir-server-url $url --max-degree-of-parallelism $threads --buffer-file-name $file $accessToken >>$output_prefix.saner.txt 2>&1 ; } 2>&1 | grep real >>$output_prefix.saner.txt"
                { time dotnet run -- --fhir-server-url $url --max-degree-of-parallelism $threads --buffer-file-name $file $accessToken >>$output_prefix.saner.txt 2>&1 ; } 2>&1 | grep real >>$output_prefix.saner.txt
            fi
        done
    done
}

load_synthea() {
    # load patient data
    echo "Loading Synthea patients"

    synthea_subdir=(
        "preload"
        "fhir"
    )
    for subdir in ${synthea_subdir[@]}; do
        folder="$test_directory/data/patients/20230929.synthea.$test_size/$subdir"
            # Check if the folder exists
        if [ ! -d "$folder" ]; then
            echo "Folder not found: $folder"
            exit 1
        fi
        echo "{ time  dotnet run -- --fhir-server-url $url --max-degree-of-parallelism $threads --input-folder $folder --buffer-file-name "./20230929.synthea.$subdir.json" $accessToken >>$output_prefix.synthea.txt 2>&1 ; } 2>&1 | grep real >>$output_prefix.synthea.txt"
        { time  dotnet run -- --fhir-server-url $url --max-degree-of-parallelism $threads --input-folder $folder --buffer-file-name "./20230929.synthea.$subdir.json" $accessToken >>$output_prefix.synthea.txt 2>&1 ; } 2>&1 | grep real >>$output_prefix.synthea.txt
    done
}

# Check if the folder exists
if [ ! -d "$fhirLoaderProjectPath" ]; then
    echo "Folder not found: $fhirLoaderProjectPath"
    exit 1
fi

cd $fhirLoaderProjectPath

available_tests=(
    "load_saner"
    "load_synthea"
)

if [ ${#tests[@]} -gt 0 ]; then
    for test in ${tests[@]}; do
        if [ "$test" = "load_saner" ] || [ "$test" = "load_synthea" ]; then
            eval "$test"
        fi
    done
    exit 0
fi

for test in ${available_tests[@]}; do
    eval "$test"
done