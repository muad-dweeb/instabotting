#!/usr/bin/env python
# coding=utf-8

import json
import os
import random
import time
import traceback
from argparse import ArgumentParser
from datetime import datetime

from instapy import InstaPy
from InstaBotException import InstaBotException


def read_config_file(config_file_path):
    """
    {
        "creds": {
            "email": "user@email.com",
            "password": "*****"
        },
        "tags": {
            "whitelist": [
                "#blancoynegro",
                "#モノクロ"
            ],
            "blacklist": [
                "#porn",
                "politics"
            ]
        }
    }
    :param config_file_path:
    :return:
    """
    try:
        with open(config_file_path, 'r') as config:
            config_dict = json.load(config)
        return config_dict
    except IOError:
        raise InstaBotException('File \'{}\' is inaccessible or does not exist!'.format(config_file_path))


def run_session(session, tags):

    print('These tags will be run: {}'.format(tags['whitelist']))

    # set up all the settings
    session.set_relationship_bounds(enabled=False)
    session.set_do_comment(False)
    # session.set_comments(['aMEIzing!', 'So much fun!!', 'Nicey!'])
    # session.set_dont_include(['friend1', 'friend2', 'friend3'])
    session.set_dont_like(tags['blacklist'])

    session.set_quota_supervisor(enabled=True,
                                 peak_likes=(300, 1500),
                                 peak_server_calls=(500, 3000),
                                 sleepyhead=True,
                                 notify_me=True,
                                 sleep_after=["likes", "comments", "follows", "unfollows", "server_calls"])

    session.set_user_interact(amount=3, randomize=True, percentage=66, media='Photo')

    # do the actual liking
    like_amount = random.randrange(50, 100)
    session.like_by_tags(tags['whitelist'], amount=like_amount)


if __name__ == '__main__':
    try:
        parser = ArgumentParser(description='Like some shit')
        parser.add_argument('--config_file_path', '-c', help='path to config file', required=True)
        # parser.add_argument('--tags', '-t', help='comma-delimited list of tags to search',
        #                     required=False)
        args = parser.parse_args()
        config_file_path = os.path.expanduser(args.config_file_path)
        # tags = args.tags

        config_dict = read_config_file(config_file_path)
        creds = config_dict['creds']
        tags = config_dict['tags']

        session = InstaPy(username=creds['email'], password=creds['password'],
                          headless_browser=True, nogui=True)
        session.login()

        hour = datetime.now().hour
        session_count = 0
        while hour < 23:
            if session_count > 0:
                wait_minutes = random.randrange(1, 60)
                wait_seconds = wait_minutes * 60 + random.randrange(1, 60)
                print('\nWaiting {} seconds'.format(wait_seconds))
                # TODO: Print next session run time
                time.sleep(wait_seconds)

            session_count += 1
            print('\nRunning Session #{}'.format(session_count))
            run_session(session, tags)

            hour = datetime.now().hour

            # TODO: Start a new session if Liked/AleadyLiked ratio is too high?

        # end the bot session
        session.end()
    except InstaBotException as e:
        print('Botting failed. Error: {}'.format(e))
        traceback.print_exc()
    except KeyboardInterrupt:
        session.end()
