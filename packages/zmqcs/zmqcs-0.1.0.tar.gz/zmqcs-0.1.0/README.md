# zmqcs

`zmqcs` is apython package that implements a client server infrastructure based on the zeromq library. To do so it fixes some properties:

 - There are 2 types of concurrent communications:
    - Request - response: Used to send commands from the client to the server. Server always answer when the command has finished. Is up to the developer to let the answer return before ending the comand in case the command is takes long to execute.
    - Pub - Sub: The server has the ability to send packages to the client with data. The client has to subscribe to the topics he wants to receive data and define a callback to be executed every time data is received for that topic
    
A full detailed example on how to use the library can be found at https://github.com/IFAEControl/zmqCSExample

All the packages are JSON formatted. 