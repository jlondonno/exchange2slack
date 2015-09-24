# exchange2slack
This app is usefil to read the exchange inbox and send a direct message to Slack for each new email (unseen messages)

Get a Slack API Key and the client secret


    Visit https://api.slack.com/web
    Sign in if you need to
    Click Get Token
    This value must be replaced in the config.ini file in the slack_apikey entry
    
    Visit https://api.slack.com/applications
    There you must create the app with a name equal to exchange2slack.
    When you create the app, Slack will provide to you the client secret.  This
    Value must be replaced in the config.ini file in the slack_apikey client_secret entry 


# Run Once

If you are using the config.ini then just run

python exchange2slack

It will check your inbox, send any slack notifications and exit. This should be good for running fron cron, etc.

# Run Forever

If you want to have it loop forever and sleep in between checks, run it with the -l command with an argument of the number of seconds to sleep. For example

python exchange2slack -l 60
