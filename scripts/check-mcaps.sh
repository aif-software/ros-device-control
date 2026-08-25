#!/usr/bin/env bash
set -euo pipefail

input="${1:-./wasa_nauhoitus_1}"
output="${2:-results.out}"

: > "$output"

if [[ -f "$input" ]]; then
    files=("$input")
elif [[ -d "$input" ]]; then
    files=("$input"/*.mcap)
else
    echo "Error: '$input' is not a file or directory" >&2
    exit 1
fi

for file in "${files[@]}"; do
    [[ -f "$file" ]] || continue

    {
        echo "========================================"
        echo "$file"
        echo "========================================"
        mcap info "$file"
        echo
    } >> "$output"
done
