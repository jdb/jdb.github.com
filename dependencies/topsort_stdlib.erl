-module(topsort_stdlib).
-export([start/0,test/0]).
-import(lists,[map/2,foreach/2,flatmap/2,usort/1]).

prepare() ->

    {ok,[L]}=file:consult("projects.term"),

    Edges=flatmap(fun({C,G}) -> [ {P,C} || P<-G] end,D),
    Vertices=usort(flatmap(fun tuple_to_list/1, Edges)),

    G=digraph:new(),

    foreach(
      fun(Vertex) -> digraph:add_vertex(G,Vertex) end,
      Vertices),

    foreach(
      fun({Parent,Child}) -> digraph:add_edge(G,Parent,Child) end,
      Edges),

    G.


start() ->
    G = ,
    io:format("Here are the projects, sorted by their dependences~n"
	      "~p~n",[digraph_utils:topsort(prepare())]).


test()-> eunit:test(
	   [
	    fun() -> 
		    [3,2,1,4,5,6,8,7,9,11,10,12]
			= topsort_from_deps(load_deps()) end
	    ]).

    
