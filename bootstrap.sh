#!/bin/bash
sudo apt install python3-venv
python3 -m venv venv
source venv/bin/activate
pip3 install adafruit-circuitpython-tsl2591
