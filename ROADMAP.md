* create twisited AMP protocal server http://twistedmatrix.com/trac/
  * data will be handled by the amp server, and have a constant
    connection to each client.  Vs the way it is now (pull every 60 
    seconds)
* update php code to connect to AMP server, send/receive config, message.
* convert all gui clients to connect twisted AMP server
* create a way for clients to send each other messages.
* create an admin client for parents to send/receive messages.

