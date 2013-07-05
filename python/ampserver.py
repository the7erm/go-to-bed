#!/usr/bin/env python
import json
import pprint
from twisted.protocols import amp
pp = pprint.PrettyPrinter(indent=4)

class JsonCmd(amp.Command):
    arguments = [('json_string', amp.String())]
    response = [('response', amp.String())]
    errors = {TypeError: 'TYPE_ERROR',
              ValueError: "VALUE_ERROR"}

class Math(amp.AMP):

    def on_json(self, json_string):
        print "ON_JSON"
        print "json_string:'%s'" % json_string
        obj = json.loads(json_string)
        if 'something' in obj:
            print "something:%s" % obj['something']
        pp.pprint(obj)
        return {"response": ""}

    JsonCmd.responder(on_json)


def main():
    from twisted.internet import reactor
    from twisted.internet.protocol import Factory
    pf = Factory()
    pf.protocol = Math
    reactor.listenTCP(1234, pf)
    print 'started'
    reactor.run()

if __name__ == '__main__':
    main()