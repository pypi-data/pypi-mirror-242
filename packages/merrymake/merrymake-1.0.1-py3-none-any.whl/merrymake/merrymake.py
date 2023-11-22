import json
import os
import pathlib
import requests
import sys

from merrymake.streamhelper import read_to_end
from merrymake.nullmerrymake import NullMerrymake
from merrymake.imerrymake import IMerrymake
from merrymake.merrymimetypes import MerryMimetypes

class Merrymake(IMerrymake):
    def service(args):
        return Merrymake(args)

    def __init__(self, args):

        try:
            self.action = args[-2]
            self.envelope = json.loads(args[-1])
            self.payloadBytes = read_to_end(sys.stdin.buffer)
        except ValueError:  # includes simplejson.decoder.JSONDecodeError
            print('Decoding JSON has failed')
            raise Exception("Decoding JSON has failed")
        except:
            print("Could not read from stdin")
            raise Exception("Could not read from stdin")

    # string action, Action<byte[], JsonObject> handler
    def handle(self, action, handler):

        if self.action == action:
            handler(self.payloadBytes, self.envelope)
            return NullMerrymake()
        else:
            return self

    def initialize(self, f):
        f()

    # string pEvent
    def post_event_to_rapids(pEvent):
        uri = f"{os.getenv('RAPIDS')}/{pEvent}"
        requests.post(uri)

    # string pEvent, string body, MimeType content_type
    def post_to_rapids(pEvent, body, content_type):
        headers = {'Content-Type': content_type.__str__()}
        uri = f"{os.getenv('RAPIDS')}/{pEvent}"

        requests.post(uri, data=body, headers=headers)

    def reply_to_origin(body, content_type):

        Merrymake.post_to_rapids("$reply", body, content_type)

    def reply_file_to_origin(path):
        # get the extension, skip the dot
        extension = pathlib.Path(path).suffix[1:]

        mime = MerryMimetypes.getMimeType(extension)

        Merrymake.reply_file_to_origin_with_content_type(path, mime)

    def reply_file_to_origin_with_content_type(path, content_type):
        with open(path, 'r') as file:
            body = file.read()
            Merrymake.post_to_rapids("$reply", body, content_type)
