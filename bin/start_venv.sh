#!/bin/bash
#Note: this must be run under $HOME/finance dir
VENT_NAME=venv

if [[ "$OSTYPE" == "msys" ]]; then
   .\%VENT_NAME%\Scripts/activate.bat
else
    source ./$VENT_NAME/bin/activate
fi
