#!/bin/bash

# Clean up any previous combined.json and temp directory
rm -f combined.json
rm -f temp.json
rm -rf temp_json

# Get the current directory name (year)
YEAR=$(basename "$(pwd)")

# Create directory for processed files
mkdir -p temp_json

# Create the initial JSON with the year from directory
echo '{
    "Año": '"$YEAR"',
    "datos": [' > combined.json

# Process each JSON file
process_json() {
    local file="$1"
    local is_first="$2"
    local base_name="${file%.json}.pdf" # Replace the .json extension to .pdf
    local temp_file="temp_json/$(basename "$file")"
    
    # Find the position of the first and last braces
    first_brace=$(grep -n "{" "$file" | head -n 1 | cut -d: -f1)
    last_brace=$(grep -n "}" "$file" | tail -n 1 | cut -d: -f1)
    
    # Create temporary file with the PDF field added after the first brace
    {
        head -n $((first_brace)) "$file"
        echo "    \"PDF\": \"$base_name\","
        tail -n +$((first_brace + 1)) "$file" | head -n $((last_brace - first_brace))
    } > "$temp_file"
    
    # Add comma if it's not the first file
    if [ "$is_first" != "true" ]; then
        echo "," >> combined.json
    fi
    
    # Append the processed content
    cat "$temp_file" >> combined.json
}

# Process all JSON files in the current directory
first_file=true
for file in *.json; do
    # Skip the combined.json file
    if [ "$file" != "combined.json" ]; then
        process_json "$file" "$first_file"
        first_file=false
    fi
done

# Close the JSON array and object
echo '
    ]
}' >> combined.json

# Clean up temporary files
rm -rf temp_json

# Optional: Format the final JSON (if jq is installed)
if command -v jq &> /dev/null; then
    jq '.' combined.json > temp.json && mv temp.json combined.json
fi

echo "JSON files have been combined into combined.json"
