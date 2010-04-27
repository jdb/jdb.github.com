


   getPage( url ):
      
      create an HTTP factory object and append it to the TCP queue of the reactor:

      	    __init__( url ):
	          parses the url to get the fully qualified name 	       
		  format an HTTP get request

      	    on build protocol:
		  create an DNS factory object and append it to the TCP queue of the reactor
		  
            on connection made: 
	        writes the HTTP request

	    on data received:
	       parse the data and extract the html body
	       execute the callback with the html body

      create an DNS factory object and append it to the TCP queue of the reactor:
            on build protocol:
	        formats a DNS request for the FQDN
            on connection made: 
	        writes the request into the socket
	    on data received: 
	        parses the bytes and execute the callback with the ip address as the argument
	    returns a slot for the callback


    reactor.run():

           reactor.empty_queues:
           for each TCP, UDP, SSL queues:
	       for each factory in the queue:
		 call the build protocol method
		 protocol = instantiate an object of the class factory.protocol
	         protocol.transport = open a socket for the protocol requested
		 reactor.protocols.append(protocol)
		 call protocol.connectionMade()

	   monitoring = epoll_create( [p.transport for p in reactor.protocols] )

	   while True:
	       bytes_received = epoll_monitor(monitoring)
	       for b,p in enumerate(bytes_received):
	       	   data = reactor.protocols[p].transport.read(b)
	           reactor.protocols[p].dataReceived(data)

               reactor.empty_queues()
	       manage the protocole queue: 
	           put the transport from new protocol under supervision
		   remove closed connexion form the supervision

