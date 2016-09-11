#!/bin/bash
count=$(/usr/local/bin/python3 /Users/sherif/projects/punread/punread.py)
icon="📖"
echo "$icon $count"

echo "---"
echo "📌 Random article | href=https://pinboard.in/random/?type=unread"
