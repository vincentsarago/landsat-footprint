#!/usr/bin/env bash

function run() {
    [ "$#" -lt 3 ] && echo "Usage: main <sceneid> <band> <ovr_level>" && exit 1
    sceneid=$1
    band=$2
    ovr_level=$3

    echo "${sceneid} | band: ${band} | overview: ${ovr_level}"
    output_file="${sceneid}_ovr${ovr_level}_B${band}.geojson"

    log_file="/tmp/landsat_footprint.log"
    CPL_CURL_VERBOSE=YES l8foot data-footprint $sceneid --band $band --overview-level $ovr_level 2>$log_file 1>$output_file

    log=$(cat $log_file | grep "< Content-Length:")
    nbytes=$(echo "$log" | awk '{print $3}' | awk '{n += $1}; END {print n}')

    log=$(cat $log_file | grep "> GET")
    nget=$(echo "$log" | wc -l)
    echo "Bytes transfered: "$nbytes
    echo "GET requests: "$nget

    echo
    exit 0
}

[ "$0" = "$BASH_SOURCE" ] && run "$@"
