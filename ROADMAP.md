* create twisited server http://twistedmatrix.com/trac/ (most likely ssh)
  * data will be handled by the ssh server, and have a constant
    connection to each client.  Vs the way it is now (pull every 60 
    seconds)
  * improve security
* update php code to connect to ssh server, send/receive config, message.
* convert all gui clients to connect twisted to ssh server
* create a way for clients to send each other messages.
* create an admin client for parents to send/receive messages.

