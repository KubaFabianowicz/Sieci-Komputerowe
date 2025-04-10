#!/bin/bash

MY_X=85

sudo ip route add 192.168.48.0/24 via 10.192.$MY_X.1
