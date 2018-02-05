#!/bin/bash
PYV=`python -c "import sys; print(sys.version_info[:])"`
PRETTY_PYV=`python -c "import sys; print('.'.join(map(str, sys.version_info[:3])))"`

echo "Checking Python version >= 3.5..."
echo "Using $PRETTY_PYV"

if [ ${PRETTY_PYV:0:1} -eq "3" ] && [ ${PRETTY_PYV:2:1} -ge "5" ]
then
   echo "Valid Python version! Starting bot..."
   echo "------"
   python -u run.py
else
   echo "Unsupported version of Python. Please upgrade to at least 3.5."
fi
