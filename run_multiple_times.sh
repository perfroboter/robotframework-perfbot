#!/bin/bash
python3 example/sut/server.py & 
# whatever code here, as long as it doesn't change the pid variable
for run in {1..20}; do
   python3 -m robot --prerebotmodifier perfbot.perfbot example/tests 
   sleep 10
done