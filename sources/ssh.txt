

Secure shell techniques
=======================


X11 forwarding
--------------

In Debian and Ubuntu, if there is a need to use a graphical
application on a server with no display, it is possible to run the
application there and the window showing on the local display.

With the default configuration on etch and lenny, the server is
already correctly configured with X11Forwarding set to 'yes'

#. install xbase-clients on the remote machine

#. connect using ssh -X to the remote machine and launch the
   application from there;

.. rubric:: forwarding without ssh


Note: it is a security risk since the input and output are not encrypted

#. get rid of the '-nolisten tcp' option on the local X server in the
   gdm configuration. In Gnome, it is in *System > Administration >
   Login Window*, in the security section.

#. On the local system, I set 'xhost +'.

#. Also on the local system, 'echo $DISPLAY' shows :0.0, so on the
   remote server: 'export DISPLAY=192.168.0.2:0.0' where 192.168.0.2
   is the local machine with the X server.
  
Client preferences
------------------

The preferences file it at ``~/.ssh/ssh_config``. These options take
precedence on the default options in  ``/etc/ssh/ssh_config``

A while ago point, the login to a server would take 5/10 secondes, and
commenting these two options would take care of the problem ::

  #    GSSAPIAuthentication yes

Passwordless ssh access
-----------------------

When you want a passwordless access to a remote ssh server::

  ssh-copy-id alice@remote_server

You will have to type your password one last time, and voila

What ``ssh-copy-id`` does is just append your public key to the remote
file ``/home/alice/.ssh/authorized_keys``:: .


The ssh client detects man-in-the-middle attacks
------------------------------------------------

When a server refuse the ssh connexion with a warning about a
*man-in-the-middle attack*, there are good chances that it is because
the server displays a server key different from the server key which
was displayed before for this host. ssh keeps the server keys in
``~/.ssh/known_hosts``. The problem arise when a virtual machine is
reinstalled a virtual machine with the same name.

The warning message says for example, ``Offending key
~/.ssh/known_hosts:27``. If you are sure that you want to connect,
just use ::

  sed -i 27d ~/.ssh/known_hosts

ssh asks to put new server keys in the known hosts lists, the ssh
client will do it automatically if the option
``StrictHostKeyChecking`` is set to no.

Il est aussi possible de changer les options de connexion du client
ssh pour eviter le "strict checking". Dans le fichier
{{{~/.ssh/config}}} mettre l'option {{{StrictHostKeyChecking no}}}. Le
plus propre, c'est encore d'utiliser la commande {{{HostKeyAlias}}}
dans le fichier d'option:

::
   Host mngmt
        Port            2222
        User            root
        Hostname        localhost
        HostKeyAlias    mngmt}}}

Note that, it is quite confusing for the ssh client, we tell him to
connect to localhost but when he receives a server key from that
connexion, it does not match the key called 'localhost' in
{{{.ssh/known_host}}}. As you may have guessed, the server public key
comes from the management server not from localhost. With the
{{{HostKeyAlias}}} command, we can tell the ssh client to look up the
key associated to the name "mngmt" in the known_hosts file instead of
looking up the key associated with the name "localhost".

From now on, you can tighten up security by getting rid of
{{{StrictHostKeyChecking no}}} because server public keys will be
correctly handled even with tunnels. You may have this message again
if you do change the public keys of the ssh server on this IP
address. Or you have a real man-in-the-middle attack going on.

Keepalive from the client
-------------------------

If you get disconnected from the remote server after an intervalle,
maybe it is a firewall which breaks the connexion because it decides
the connexion is inactive. In the preference file, you can add ::

   ServerAliveInterval 300 

Every 300 secondes, the client will request a short data to the
server, keeping the connexion active.


SSH port forwarding
-------------------

It is commonly called "ssh tunnel" but we prefer to call it "ssh port
forwarding" as it is more precise and it helps understanding what is
possible and what is not.

This technique is powerful: let's say you have web servers, SMTP
servers, LDAP servers etc waiting for you on some far away network BUT
there is a firewall that only lets ssh traffic going through between
you and one ssh server on the remote network. You will be able to use
your local email client and browser to access the remote servers
behind the firewall. 

SSH port forwarding will work fine with **TCP services toward
pre-defined servers on pre-defined tcp ports.**

You need :

* access to one ssh server on that remote network (openssh all the
  way, no VNC or remote desktop protocol!)

* your local client can choose the port on which to connect

You can't do : 

* ftp because the file transfer happen on new dynamic ports new
  servers

* H323 or SIP because the 'connect' packet tells the client to connect to new
  ports, sometime new server.

* HTTP redirect, your web client will not be able to follow them: use
  the final url directly not the shortcut

* UDP protocole : media, SNMP use port **udp**/161,162, ssh tunnel
  only works with TCP

Additional goodies :

 * under linux, you can declare a directory on the ssh server to be
   seen as a "share" or "network directory". For example, you can
   study remote traces with your local ethereal without having to
   download and store the traces.

 * in a slightly different config where the firewall only accepts
   outgoing ssh connexions and not incoming connexions on the remote
   network, it is still possible to connect to a webserver of the
   remote network from an outside local web client. (Example: I want
   to connect to the ncx intranet from my home without VPN).

Quick howto
~~~~~~~~~~~

Let's say you have a "hop server" called *bastion* running sshd on the
remote network, on which you can connect with the alice login. Only
from this server, you can connect with the bob login to the
*streamer01* and *streamer02* servers you are interested. This is two
hops for each server instead of one, this is inconvenient. You can use
the following for only executing one command to tget directly from
your laptop to *streamer01* or to *streamer02* ::

   # This command will not return
   ssh alice@bastion -N -L 2201:streamer01:22 -L 2202:streamer02:22 -L 8080:webserver:80 &

   ssh -p 2201 bob@localhost     # to get to streamer01
   ssh -p 2202 bob@localhost     # to get to streamer02
   wget http://localhost:8080    # to make an http get to webserver


It is a pain to remember the port on the bastion driving you to the
correct server, the preferences file ``~/.ssh/config`` is handy

::

   Host streamer01
        Port            2201
        User            bob
        Hostname        bastion

   Host streamer02
        Port            2202
        User            bob
        Hostname        bastion



Going beyond the limitations
~~~~~~~~~~~~~~~~~~~~~~~~~~~~


.. todo::

   SSh tunnels are a lot of configuration on the client side, plus
   SNMP, H323 and ftp won't work with this technique, what is possible
   when there is only an ssh access to one of the remote server?

   You can set up a PPP tunnel in an ssh tunnel and configure routes
   to this interface.

.. todo::

   What is this ``ssh -D`` "dynamic port" option and what can I do with it?


