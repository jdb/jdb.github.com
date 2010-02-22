
========================
 Backward compatibility
========================

Softwares and specifications must be corrected or evolve to support
new needs. This paragraph addresses the difficulty for protocol or a
library to evolve while making it possible for impacted subsystems to
be updated at a different pace. We identified three steps in a
deprecation process:

#. before the implementation of the evolution,endpoints are compatible, 

#. a transitory state where one of the endpoint implements the new
   feature but also supports the old behavior, and provides the other
   endpoint with what it expects. During this phase, communication
   about the changes and about the end of support of the old feature
   is required.

   .. todo::

   this is a pretty empty paragraph, some smarter dudes must have
   written something more complete. Maybe monkey patching in Plone, or
   Erlangs 
 
#. unsupported where one of the endpoints does not support the old
   behavior. This third step may not be required as both solution, th
   old and the new can coexist indefinitely for various reason

When the changes concerns clarifications, new figures, fixed typos,
packaging the minor number should be augmented. It is also possible to
specify workarounds for keeping backward compatibility.

Whenever compatibility is broken, there should be a bump in the major
number. Incompatibilities varies they can be at the wire level when
message format is impacted, configuration: when a new binary cannot be
used with an old configuration file, API, when an application expects
some functions or some signatures to be presented.



Example 1: *fragment-duration* is renamed *duration*
----------------------------------------------------

The *fragment-duration* parameter of the the *setup* command is a
misnomer and is misleading and should be renamed *duration*. Client
and servers are distributed independently to give mandatory
flexibility to the integration team. Client (resp. server) version x+1
can handle server (resp. client) version x.

**problem**: If the manager is recent and sends the new parameter
*duration* parameter to an old streaming server, the parameter is
unknown, hence ignored. The duration of the contents are
systematically the default duration whatever the client requests.

**Solution 1**: The manager maintains and branches on runtime or
through the configuration on differing implementations of the
protocol. As the protocol version is stated by the streaming server on
login, the manager sends *fragment-duration* when the streaming server
is implementing the old protocol version. The client sends *duration*
when connected to a recent streaming server.

**Solution 2**: The manager handles the transition period by sending
both *fragment-duration* and *duration*, set to the same
value. Because ALLP servers must ignore unknown parameters, old
versions will ignore the old parameter, and new versions will ignore
old parameters. Streaming servers should log unknown parameters. The
*manager should log on connect the protocol differences between two
versions of the protocol, for the streaming server information.

**Solution 3**: The streaming server handles the transition period and
knows how to interpret both *fragment-duration* and *duration*. The
streaming server can answer a "201 Ok-but-deprecated-element".

Whether it is the streaming server of the manager using the old
version of the protocol or using a workaround, the server log should
state that the protocol in deprecated in favor of an more recent
version and the **date** when the server will stop supporting the old
version of the protocol.

The release note of both ends of the protocol must state which version
of the protocol they implement so the integration knows which versions
of client and servers incompatible.


.. In any case, here the deal is one of the two element handles
   **both** versions and the corresponding element is faked.

.. What about a calendar server or a mailing list with scheduled mails
   to schedule the deprecation APIs. Leading to time based release.


Example 2: *stream-id* is unneeded
----------------------------------

*stream-id* is a parameter in the ALLP VODRTP and ALLP VOD2, it is not
part of RTSP, unnecessary to the manager, unknown to the RTP streaming
server and mis-used by the TS streaming server. In the TS streaming
server, the current use of the *stream-id* is overlapping with the
*session* in some case and with *filename* in other case.

The *stream-id* parameter comes from the VLS streaming server, is
meant to control multiple streams in the same session [#]_ but is not
adapted to the TS context where multiple streams would supposedly be
multiplexed at the SPTS level.

.. [#] Note that the concept of multiple stream is quite powerful:

       * a content whose video is streamed in several codecs or resolution,
         one multicast address each. This is called adaptative streaming.
 
       * a physical conference presentation composed of two video
         streams one shows the speaker at the microphone, while the
         second video shows its slides.

Concerning the RTP streaming server, the request from the developer
team is to suppress every mention of *stream-id* from the
specification since they do not need and support it. Their approach to
multi stream per session uses other parameters: *track-id* and *pt*
(for *payload type*). The *stream-id* parameter was stripped from the
RTP streaming server specification and the manager team is kept up to
date, via synchrone media, asynchrone media and via the specification
changelog for archive.

Concerning the ALLP TS, the stream-id is an optional parameter of some
requests and an unneeded column of some events. The streaming server
must ignore *stream-id* in requests (and log deprecation warning) and
must strip the stream-id parameter from the events. 


.. todo::

   Make three packages from the spec-{build,quickstart} and templates
   and a dummy package which pulls them all.


.. todo::

   Implement a script *spec-release* similar to spec-build which
   interactively helps with the different steps of a release.

   Use canonical's Quickly ...


.. when I put in a changelog a "working on: #nnn", then I can launch a
.. script which puts the bug into analysis

.. when I commit and there are "closes: #nnn" in the last version


.. todo::

   Put examples for every interesting command and every
   response. Clarify between commands and requests, between reply and
   response (stick to RTSP naming)


.. todo::

   the ``:term:`` role does not seem to work. inline reference to
   title does not seem to work either but it looks like the inline
   reference bug. The latex output of a definition list is a bit
   weird.  

.. todolist::

