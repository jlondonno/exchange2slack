 #!/usr/bin/env python

import time
import imaplib
from email.parser import Parser
from slacker import Slacker
import argparse
import traceback
import ConfigParser

config_file = ConfigParser.ConfigParser()
config_file.read('config.ini')

class Exchange2Slack():
    def __init__(self, user, app, slack):
        self.slack = slack
        self.slack_user_id = user
        self.slack_app = app

    def read_exchange(self):

        url = config_file.get("config_exchange", "url_exchange")
        port = int(config_file.get("config_exchange", "port_exchange"))
        user = config_file.get("config_exchange", "user_exchange")
        password = config_file.get("config_exchange", "pass_exchange")

        conn = imaplib.IMAP4_SSL(url, port)
        conn.login(user, password)
        conn.select('INBOX')

        results, data = conn.search(None,'(UNSEEN)')

        for index in range(len(data)):
            msg_ids = data[index]
            msg_id_list = msg_ids.split()

            try:
                latest_email_id = msg_id_list[-1]
                result,data = conn.fetch(latest_email_id,"(RFC822)")
                raw_email = data[index][1]

                p = Parser()
                msg = p.parsestr(raw_email)

                print msg.get('From')
                print msg.get('Subject')

                from_date = msg.get('Date')
                say = "New Email\n>From: %s\n>Date: %s\n>Subject: %s\n>\n>" % \
                      (msg.get('From'), from_date, msg.get('Subject'))
                self.slack.direct_message(say, self.slack_user_id, self.slack_app)
            except IndexError:
                print "No mensajes recientes"
                return


class Slack():
    def __init__(self, apikey):
        self.slack = Slacker(apikey)

    def get_name_id(self, name):
        users = self.slack.users.list()
        for member in users.body['members']:
            if member['name'] == name:
                return member['id']
        return None

    def direct_message(self, message, user_id, slack_from):
        print user_id, slack_from
        self.slack.chat.post_message(user_id, message, username=slack_from)


def main():
    parser = argparse.ArgumentParser()

    parser.add_argument("-l", "--loop", help="loop every per seconds", action="store", default=0)
    args = parser.parse_args()

    slack_user = config_file.get("config_slack", "slack_user")
    slack_app = config_file.get("config_slack", "slack_from")
    slack_api_key = config_file.get("config_slack", "slack_apikey")

    slack = Slack(slack_api_key)
    slack_user_id  = slack.get_name_id(slack_user)

    g2s = Exchange2Slack(slack_user_id, slack_app, slack)
    if int(args.loop) > 0:
        delay = int(args.loop)
    else:
        delay = 0
    while True:
        try:
            g2s.read_exchange()
        except:
            traceback.print_exc()
        if delay:
            time.sleep(delay)
        else:
            break


if __name__ == "__main__":
    main()
