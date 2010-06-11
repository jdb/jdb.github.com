

Diffs
=====

- defining function with /arity: more precise, less flexible: more
  functions in the namespace. For sets, python has ten methods while
  erlang has twice more. Arity does not help much with documentation
  sometime.

- xor exists, true and false are not capitalized

- langage seems a bit less extended than python -> smaller brain
  footprint, less idioms

- function, TCPserver and processes are similar: both receives data
  that they match to execute code. When clauses are not matched ->
  crash, when packets/messages are not matched, they stack.

- subpackages are not possible, imports are not required, they are
  meant for a shortcut to mymod:myfun

- tail recursive is optimised and do not leak memory by adding the
  calling arguments to the stack

- "Do not worry, it is safe, it will crash...": fast, and loudly from
  the end of your network

Pros
====

- concept of an application (better than just main)

- remote crash dumps sent to remote linked process

- trees and algo and graphs in the stdlib

- sending messages with !, marshalled, unmarshalled automatically
  accross the network

- hot code swap

- structured processmon and restart strategies built in the design

- stricter simpler, no objects -> no function/metho micmac -> no hair
  split about object modelling

- extends and append are destructive, l + [e] is an expression but it
  is slow. Fast expressions are in itertools, and usually need
  list(). This is quite unclear compared to no side effe

- compilation warns about unreachable code,

- good sctp server support

- the register is always correct, died process are unregistered
  automatically,

- processs do not die sillently

- tree structured startup of application, and restart strategies


Questions
=========

- how to refactor an fsm into a gen_fsm: by testing it regularly.

- how to do generator and backtracking?

- how to do an operator?

- how to store graph? how to update

- how to update

- what is a virtual node?

- Can a ~p representation for my records be registered?

- riak search, porter stamping? concerning lucene, bloom filters

Faq
===

- simply put, are there technical advantages for the gen_server or it
  is more about engineering methods: reusing tested code, sharing
  conventions, etc? *Resolved* They took care of race conditions.

- How can we allocate, prioritize, and monitor ressources (CPU,
  memory) supervision, quotas, QoS? *Resolved* "Do not
  try... processes can have priority but some processes wil starve."

- how to sort the startup, by associating each child spec to a
  supervisor? or leaving the child manage the restart... *Resolved*
  the child list is sorted.

- is a tree a supervisors starts also synchronously? *Resolved* yes

- the gen_server expects callback functions and signatures and
  specific replies too. What is the most convenient way to check user
  code and callback code to see what's wrong? *Resolved*: there is no
  really a way, use the doc and the tempo template.

- When to return an answer, and when to also return a reason?
  *Resolved* Use a reason when there are good reason that the function
  will fail due to an external cause.

- Can a function returning a tuple {cmd, Data} be wrapped in a call to
  a function whose signature is function(cmd, Data). Almost Resolved:
  easily by pattern matching the tuple (can a record be used?).

- the standard way to start a gen_server callback module 'mymod' is to
  call mymod:init()? *Resolved*: No, it is the gen_server module which
  calls init.  mymod:mystart() will call gen_server:start_link boiler
  plate which will expected to call init which is expected to return
  State.

- How to inspect the process of a mail box? *Resolved* flush()

- io:format does not work? *Resolved*: do not forget to wrap the
  elements in a list

- Compilation error! *Resolved*: modules can not contain statement and
  expressions, only function definition, use -define to declare
  macros.

- Can't define function clauses in the erl console! *Resolved*: no you
  can't. You can define funs and bind them to names.

- why can't I use lists:member to check the existence in db_list?
  instead of doing my recursive clauses? *Resolved*: because there is
  only a restricted set of BIF allowed in guards.

- Why can't I use a function in a flatmap() call. *Resolved*: affix with
  fun, suffix with arity

- help() does not show anything in the console and seems to
  hang. *Resolved*: do not forget the dot.

- How to quickly extract the key of a record returned by a function?
  *Resolved* (my_fun())#account.no.

- How to directly import functions in

Common traps
============

- badarg in register: either it is not an atom, or it is already
  registered. Custom init & start_link can register a name, gen_* init
  & start_link should not do it, as gen:start_link does it.


Misc
====

tons of process: use spawn_link to help the garbage collector

Given an instance of a 'blabi' record bound to R, which has a key
'number', how do I request the value of the record? 

(where is this documented in the docs?).

-module(titi).

-record(blabi, {key,no=3,val=yes}).

23> rr("titi.erl").
[blabi]
24> #blabi{key=5}.
#blabi{key = 5,no = 3,val = yes}
25> A=#blabi{key=5}.
#blabi{key = 5,no = 3,val = yes}
26> A#blabi.key.
5


Supervisor restarts childs which are expected to register


Generic server
=============

- the standard way to stop a server is mymod:mystop which
  gen_server:calls {stop} which does not need a handle_Call({stop})
  but needs a terminate.

 
Turn the code into a gen_server: 

- put behaviors at the top, 

- implement the standard callback

- differentiate the gecallback and the API

account, pin_valid, change_pin, withdraz, transfer, alance, transactions


FSM
===

- How does the fsm holds the current state, when you send an event E,
  then CurrentState(E) is called (be prepared to handle a CurrentState(E))

what are the generic :

- start_link use gen_fsm:start_link

- get_pin(card_inserted)

start it, stop it, add state

what is the signature in and out of states:

- evaluation.erlang-consulting.com oe0610

TDD
===


can you expect an exception

what is the -test(exports) directive? how to compile from emacs?
shortcut for export?
csp? (csp vs threads)

how to find out what to code, wihtout impeding refactor, 
how can you not throw away your tests when refactoring? it is part o fit


tdd and xp are a bit different
agile method + agile language -> agile2

tdd has a say about your how you use a scm
call unit test developer test instead
links with design and documentation (pair programming share info, tests are docs too)
fit.c2.com: executable specs
"free standing functions"

static typing is not safer since unexpected null can arise in any
types. static typing is for doc or perf, not security
do not forget the corner case for developer tests (language with patmatch and clauses map some tests explicitly)
"extrem forge" is a tdd product as eunit is
thread are impossible to tdd, especially race conditions (no control on the scheduler, it is kernel)
tdd and xp comes from smalltalk (dynamicly type, closures and duck typing)
what is triangulation?
try to avoid named processes since they are global variables

dominic williams
michael campbell

McErlang
========


testing all possible scheduling of the process of your application (re-implemented a scheduler)

produce another souce code, with mcerlang primitives

spawn(register(toto)), toto ! there was a bug buggy 

what iss the output with OTP, gen_server and gen_fsm

model checking is chacking every code path (do not revisit state and save a lots of computations)

Riak search
===========

query through keys, keys and instruction, key + JS.
what is sharded?
riak search is a bit a remplacement of Lucene
how do you store a graph on riak?
