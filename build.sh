#!/bin/bash

python3 src/btl2025.py
npx @tailwindcss/cli -i css/input.css -o output/site.css
tsc src/*.ts --lib es2015,dom --outDir output
cp -vR img output
