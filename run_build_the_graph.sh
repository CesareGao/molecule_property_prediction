#!/bin/bash

# Run the graphframes code

# Set names of files for input and output.
# Paths must be absolute paths.
# $PWD is bash shell variable for the current directory
#INPUT_MANAGER="$PWD/../lab4/Lab4Data/Managers.csv"

# Delete any old copies output directory on linux filesystem
#rm -rf "$OUTPUT_DIR"

# Run the job passing command line parameters for the input/output directories
# if HDFS is configured on the system, that is the default for spark
# Override with prefix "file://" when passing to python/spark
spark-submit \
    --master "local[*]" \
    --deploy-mode "client" \
    --packages graphframes:graphframes:0.7.0-spark2.4-s_2.11 \
    graph_processing.py

exit $?
