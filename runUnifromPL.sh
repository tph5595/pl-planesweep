#!/bin/zsh


for i in `seq 100 100 10000`;
do
      for j in {0..30};
      do
            echo "$i $j" >> uniformPL.savetime.k10
            {time python3.8 newBarcode.py ../bdgen/uniform-$i-$j.barcodes 1} >> uniformPL.savetime.exactraw.k10 2>> uniformPL.savetime.k10
      done
done
