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
access_token=""
bearer_token=""
client_secret=""
client_credentials=""
authority=""
tests=()
test_size="partial"

# Usage function
usage() {
    echo "Usage: $0 -u <server_url> [-f] [-n <num_threads>] [-t <access_token>] [-a <signing_authority>] [-i <client_id>] [-s <client_secret] [<test1> .. <testN>]"
    exit 1
}
[ $# -eq 0 ] && usage

# Parse options and their values
while getopts "u:n::t::a::i::s::f" opt; do
    case $opt in
        u)
            url="${OPTARG}"
            echo "url is ${url}"
            ;;
        n)
            threads="${OPTARG}"
            echo "threads is $threads"
            ;;
        t)
            token="${OPTARG}"
            access_token="--access-token $token"
            bearer_token="--header 'Authorization: Bearer $token'"
            echo "token is $token"
            ;;
        a)
            authority="--authority ${OPTARG}"
            echo "signing authority is $authority"
            ;;
        i)
            client_id="--client-id ${OPTARG}"
            echo "client id is $client_id"
            ;;
        s)
            client_secret="--client-secret ${OPTARG}"
            echo "client secret is $client_secret"
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

        echo $url >> $output_prefix.saner.txt
        echo "Start time:" >> $output_prefix.saner.txt
        date +"%Y.%m.%d.%H%M%S" >> $output_prefix.saner.txt

        echo "Loading files from ${folder}"
        # Iterate through each file in the folder
        for file in "$folder"/*; do
            # Check if the item is a file (not a directory)
            if [ -f "$file" ]; then
                echo "{ time dotnet run -- --fhir-server-url $url --max-degree-of-parallelism $threads --buffer-file-name $file --force-post $access_token $client_secret $client_id $authority >> $output_prefix.saner.txt 2>&1 ; } 2>&1 | grep real >> $output_prefix.saner.txt"
                { time dotnet run -- --fhir-server-url $url --max-degree-of-parallelism $threads --buffer-file-name $file --force-post $access_token $client_secret $client_id $authority >> $output_prefix.saner.txt 2>&1 ; } 2>&1 | grep real >> $output_prefix.saner.txt
            fi
        done
        echo "End time:" >> $output_prefix.saner.txt
        date +"%Y.%m.%d.%H%M%S" >> $output_prefix.saner.txt 
    done
}

load_synthea() {
    # load patient data
    echo "Loading Synthea patients"

    echo $url >> $output_prefix.synthea.txt
    echo "Start time:" >> $output_prefix.synthea.txt
    date +"%Y.%m.%d.%H%M%S" >> $output_prefix.synthea.txt

    synthea_subdir=(
        "preload"
        "fhir"
    )
    for subdir in ${synthea_subdir[@]}; do
        # folder="$test_directory/data/patients/20230929.synthea.$test_size/$subdir"
        folder="$test_directory/data/patients/20240122.synthea.$test_size/$subdir"
            # Check if the folder exists
        if [ ! -d "$folder" ]; then
            echo "Folder not found: $folder"
            exit 1
        fi
        start_time=$(date +%s)
        for file in "$folder"/*; do
            if [ -f "$file" ]; then
                curl_command="curl -s -o /dev/null -w '%{http_code}' --header 'Content-Type: application/json' $bearer_token --data @'$file' $url"
                echo "$curl_command"
                http_status_code=$(eval "$curl_command")
                echo "$http_status_code" >> "$output_prefix.synthea.txt"
                # Check if the curl command was successful (HTTP status code 2xx)
                if [ "$http_status_code" -ge 200 ] && [ "$http_status_code" -lt 300 ]; then
                    echo "Request successful (HTTP status code: $http_status_code)"
                else
                    # Output the response if not successful
                    echo "Request failed with HTTP status code: $http_status_code"
                    # You might want to include additional error handling or logging here
                    sleep 1
                    curl_command_verbose="curl -H 'Content-Type: application/json' $bearer_token --data @'$file' $url"
                    output=$(eval "$curl_command_verbose")
                    echo "$output" >> "$output_prefix.synthea.txt"
                fi
            fi
        done
        end_time=$(date +%s)
        execution_time=$(($end_time - $start_time))
        echo "Execution time: $execution_time seconds" >> $output_prefix.synthea.txt
    done

    echo "End time:" >> $output_prefix.synthea.txt
    date +"%Y.%m.%d.%H%M%S" >> $output_prefix.synthea.txt
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