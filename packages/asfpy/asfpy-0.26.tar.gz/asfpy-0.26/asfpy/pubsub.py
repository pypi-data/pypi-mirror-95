#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Licensed to the Apache Software Foundation (ASF) under one or more
# contributor license agreements.  See the NOTICE file distributed with
# this work for additional information regarding copyright ownership.
# The ASF licenses this file to You under the Apache License, Version 2.0
# (the "License"); you may not use this file except in compliance with
# the License.  You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
""" PyPubSub listener class. """

import requests
import requests.exceptions
import json
import time
import sys


class Listener:
    """ Generic listener for pubsubs. Grabs each payload and runs process() on them. """

    def __init__(self, url):
        self.url = url
        self.connection = None

    def attach(self, func, **kwargs):
        raw = kwargs.get('raw', False)
        debug = kwargs.get('debug', False)
        since = kwargs.get('since', -1)
        auth = kwargs.get('auth', None)
        while True:
            if debug:
                print("[INFO] Subscribing to stream at %s" % self.url)
            self.connection = None
            while not self.connection:
                try:
                    headers = {
                        'User-Agent': 'python/asfpy'
                    }
                    if since != -1:
                        headers['X-Fetch-Since'] = str(since)
                    self.connection = requests.get(self.url, headers=headers, auth=auth, timeout=30, stream=True)
                    if debug:
                        print("[INFO] Subscribed, reading stream")
                except requests.exceptions.RequestException as e:
                    sys.stderr.write("[WARNING] Could not connect to pubsub service at %s, retrying in 10s...\n" % self.url)
                    time.sleep(10)
                    continue
                if not self.connection:
                    if debug:
                        sys.stderr.write("[WARNING] %s did not respond with a streamable connection, reconnecting in 10 seconds\n" % self.url)
                        sys.stderr.flush()
                        time.sleep(10)
            try:
                body = ""
                for chunk in self.connection.iter_content(chunk_size=None):
                    body += chunk.decode('utf-8', errors='ignore')
                    # pypubsub/gitpubsub payloads end in \n, svnpubsub payloads end in \0:
                    if body[-1] in ["\n", "\x00"]:
                        try:
                            payload = json.loads(body.rstrip("\r\n\x00"))
                        except ValueError as detail:
                            if debug:
                                sys.stderr.write("[WARNING] Bad JSON or something: %s\n" % detail)
                        if not raw and isinstance(payload, dict):
                            payload = payload.get('payload')
                        if payload:
                            func(payload)
                        body = ""
            except requests.exceptions.RequestException as e:
                if debug:
                    sys.stderr.write("[WARNING] Disconnected from %s, reconnecting\n" % self.url)
                    sys.stderr.flush()
                    time.sleep(2)
                    continue
            if debug:
                sys.stderr.write("Connection to %s was closed, reconnecting in 10 seconds\n" % self.url)
                sys.stderr.flush()
                time.sleep(10)
