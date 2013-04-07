#!/bin/sh
while [ true ]
do
    latex -interaction nonstopmode $1
    sleep 10
done
