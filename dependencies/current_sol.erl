
-module  ( current_sol ).
-compile ( export_all )
.
-import(lists,[member/2, foreach/2, all/2, filter/2,fold/2]).


start() ->
    {ok, [Data]} = file:consult("projects.term"),
    Projects = lists:usort(
		 lists:flatten(
		   [ [P|D] || {P,D} <- Data ])),

    Deps = lists:foldl(fun({K,V}, Dict) -> dict:append_list(K,V,Dict) end, 
		       dict:from_list([{E,[]} || E <- Projects]), 
		       Data),
    foreach(fun(P)-> sons(P,[],Deps,length(Projects)) end, 
	    appropriate([],Deps)).

appropriate(Path,Deps)->
    filter(
      fun(X) -> not member(X,Path) 
		and all(fun(D) -> member(D,Path) end, dict:fetch(X, Deps))
      end, 
      [K ||{K,_} <- dict:to_list(Deps)]).

sons(Parent,Path, Deps,Lenpath) ->
    Newpath=[Parent|Path],
    if 
	length(Newpath)=:=Lenpath -> io:format("~p~n",[Newpath]),true; 
	true -> true
    end,
    foreach(fun(S) -> 
    sons(S, Newpath, Deps, Lenpath) end, 
	    appropriate(Newpath,Deps)).
    



    
