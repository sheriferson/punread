#!/bin/bash
# <bitbar.title>punread</bitbar.title>
# <bitbar.version>v1.0</bitbar.version>
# <bitbar.author>Sherif Soliman</bitbar.author>
# <bitbar.author.github>sheriferson</bitbar.author.github>
# <bitbar.desc>Show pinboard unread count</bitbar.desc>
# <bitbar.dependencies>python</bitbar.dependencies>
# <bitbar.abouturl>https://github.com/sheriferson/punread</bitbar.abouturl>

links=$(/usr/local/bin/python3 /Users/sherif/projects/punread/punread.py 5)
echo "$links"

echo "---"
echo "📌 Random article | href=https://pinboard.in/random/?type=unread"
