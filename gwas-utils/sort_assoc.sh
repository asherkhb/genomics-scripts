#!/bin/bash
awk '$12!="NA"' $1 | sed 's/^[[:space:]]*//g' | sed 's/[[:space:]]*$//g' | tr -s ' ' '\t' > ${1}.pruned;
sort -k 12,12 -g ${1}.pruned > ${1}.sorted;
