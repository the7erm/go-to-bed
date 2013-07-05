#!/usr/bin/env python
from twisted.internet import reactor, defer
from twisted.internet.protocol import ClientCreator
from twisted.protocols import amp
from ampserver import JsonCmd
import json


def doMath():
    creator = ClientCreator(reactor, amp.AMP)
    jsonDeferred = creator.connectTCP('127.0.0.1', 1234)
    def connected(ampProto):
        return ampProto.callRemote(JsonCmd, json_string='{"something":true}')
    jsonDeferred.addCallback(connected)
    
    def response(result):
        print "result:",result
        return result['response']
    jsonDeferred.addCallback(response)

    def trapTypeError(result):
        result.trap(TypeError)
        print "Json Error"
        return "{}"
    
    jsonDeferred.addErrback(trapTypeError)

    def done(result):
        print 'Done with math:', result
        reactor.stop()
    defer.DeferredList([jsonDeferred]).addCallback(done)

if __name__ == '__main__':
    doMath()
    reactor.run()