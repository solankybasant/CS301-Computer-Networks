#!/bin/bash

# Specify the range of packet sizes
for size in {64..100..64}; do
    # Run ping with the specified packet size and count
    ping -c 5 -s $size google.com | grep "round-trip" | awk '{print $4}' | cut -d '/' -f 2 >> rtt_results.txt
done

