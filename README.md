# CLOWNR

This is just a fun little bot that uses twython to handle annoying people who you don't want to keep talking to, but also don't want to get the last word. 

## HOW TO USE

- Step 1: Verify your twitter account in the [twitter developer portal](https://developer.twitter.com/en) and request access to their API. You are going to need API Key and Secret and Oauth (1.0) Access Token and Secre, with read and write permissions. You will need to tell twitter what it's for and be specific, but you know, not too specific. Don't tell them you are going to spam assholes, they might not like that. Just tell them you are setting up a fun little twitter bot that will reply to accounts interacting with your own as a private project or something like that.
- Step 2: When you have everything you need from twitter, download the repo and install all the dependencies, mainly python3 and twython. There are some other things you need as well, but you will find out when you run the script.
- Step 3: Fill in the necessary variables in clownr.py. This is your tokens, keys and secrets, as well as your own twitter handle and the handles of your targets (in quotes, comma separated). There are also a few paths you might want to add the full path to, in case you want to run the script with a cronjob, which is kinda the point.
- Step 4: Set up the cronjob and enjoy!
