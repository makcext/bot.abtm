#!/bin/bash

# Имя файла JSON
FILE="./result.json"

# Извлекаем ссылки и подсчитываем их частоту
# grep -o '"href": "https://www[^"]*\.gr/' "$FILE" | \
#     sed 's/"href": "https:\/\/www\.\([^.]*\)\.gr\/.*/\1/' | \
#     sort | \
#     uniq -c | \
#     sort -rn | \
#     head -n 20 | \
#     while read count domain; do
#         echo "https://www.$domain.gr/ - $count occurrences"
#     done


grep -o '"href": "https://www[^"]*\.gr/' "$FILE" | \
    sed 's/"href": "https:\/\/www\.\([^.]*\)\.gr\/.*/\1/' | \
    sort | \
    uniq -c | \
    awk '{if ($1 % 2 == 0) print $1/2, $2; else print int($1/2), $2}' | \
    sort -rn | \
    head -n 30 | \
    while read count domain; do
        echo "https://www.$domain.gr/ - $count unique occurrences"
    done