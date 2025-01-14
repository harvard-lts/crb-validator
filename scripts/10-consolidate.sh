#!/bin/bash

# Define the source and target directories
#source_dir="/Volumes/crb/staging/nlc/images/all"
#target_root="/Volumes/crb/data/nlc/images/"
source_dir="/Volumes/crb/staging/nlc/checksums/all"
target_root="/Volumes/crb/data/nlc/checksums/"

# Ensure the target root exists
mkdir -p "$target_root"

# Initialize variables
batch_size=1000
batch_number=1
counter=0

# Sort and iterate through the subdirectories
find "$source_dir" -mindepth 1 -maxdepth 1 -type d | sort | while read -r subdir; do
    # Determine the batch directory
    batch_dir=$(printf "%s/%02d" "$target_root" "$batch_number")
    
    # Create the batch directory if it doesn't exist
    mkdir -p "$batch_dir"
    
    # Move the subdirectory to the batch
    mv "$subdir" "$batch_dir/"
    
    # Increment the counter
    ((counter++))
    
    # If the counter reaches the batch size, move to the next batch
    if ((counter >= batch_size)); then
        counter=0
        ((batch_number++))
    fi
done

echo "Directories sorted and moved successfully!"
