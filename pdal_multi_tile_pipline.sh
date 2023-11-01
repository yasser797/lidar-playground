#!/bin/bash

function process_tile() {
    tile_index="$1"
    
    output_directory="./data/santa_monica_col_scans"
    tiles_directory="./data/tiles"

    # Hard-coded input file
    input_file="./SaMo_topo.laz"
    file_name=$(basename "$input_file")
    echo "Processing: $file_name"

    # Base name without extension
    base_name="${file_name%.las}"
    echo "Processing tile index: $tile_index"
    
    tile_file="$tiles_directory/santa_monica_2016_$tile_index.tif"

    # Check if tile file exists
    if [ ! -f "$tile_file" ]; then
        echo "Tile file does not exist: $tile_file"
        return  # Exit the function
    fi

    output_file="$output_directory/${base_name}_${tile_index}.las"

    # Construct and run PDAL pipeline
    pdal_pipeline=$(cat <<EOF
{
    "pipeline": [
        {
            "type": "readers.las",
            "filename": "$input_file"
        },
        {
            "type": "filters.colorization",
            "raster": "$tile_file"
        },
        {
            "type": "filters.range",
            "limits": "Red[1:]"
        },
        {
            "type": "writers.las",
            "minor_version": "2",
            "dataformat_id": "3",
            "filename": "$output_file"
        }
    ]
}
EOF
    )

    echo "$pdal_pipeline" | pdal pipeline -i /dev/stdin
    if [ $? -ne 0 ]; then
        echo "PDAL pipeline failed for tile index $tile_index"
    fi
}

export -f process_tile

output_directory="./data/santa_monica_col_scans"
tiles_directory="./data/tiles"

# Check if required directories exist
if [ ! -d "$output_directory" ] || [ ! -d "$tiles_directory" ]; then
    echo "Required directories are missing!"
    exit 1
fi

# Run the function process_tile in parallel for each index from 0 to 91
parallel process_tile ::: {0..91}