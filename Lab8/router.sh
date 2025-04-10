#!/bin/bash

MY_X=85


for i in $(seq 71 90); do
  if [ "$i" -ne "$MY_X" ]; then
    sudo ip route add 10.192.$i.0/30 via 192.168.48.$i
  fi
done
