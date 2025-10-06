#!/bin/bash


#####################################################################
# Simple URL Health Check Script
#
# Author: Arief
# Version: v0.0.1
#
# Usage: ./check_url.sh <URL_TO_CHECK>
# Example: ./check_url.sh https://example.com
#
# Description:
#   This script checks the HTTP status code of the given URL using curl.
#   If the response status code is in the 2xx range, it prints that the
#   application is UP. Otherwise, it prints that the application is DOWN.
#
# Exit Codes:
#   0 - Application is UP (2xx)
#   1 - Application is DOWN (non-2xx)
#####################################################################

if [ -z "$1" ]; then
    echo "Usage: $0 <URL_TO_CHECK>"
    exit 1
fi

URL_TO_CHECK="$1"

HTTP_STATUS=$(curl -s -o /dev/null -w "%{http_code}" "$URL_TO_CHECK")

# Check if the status code is in the 2xx range
if [[ "$HTTP_STATUS" -ge 200 && "$HTTP_STATUS" -lt 300 ]]; then
  echo "Application is UP. Status code: $HTTP_STATUS"
  exit 0
else
  echo "Application is DOWN. Status code: $HTTP_STATUS"
  exit 1
fi

