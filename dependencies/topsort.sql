-- create temporary table  deps (p int, d int[]);

-- insert into deps values ( 1 , array[2,3]);
-- insert into deps values ( 5 , array[4]);
-- insert into deps values ( 6 , array[1]);
-- insert into deps values ( 7 , array[6, 5, 4]);
-- insert into deps values ( 8 , array[6, 4]);
-- insert into deps values ( 9 , array[6, 5, 8, 7]);
-- insert into deps values ( 11, array[6, 5, 4, 7]);
-- insert into deps values ( 10, array[4, 6, 7]);
-- insert into deps values ( 12, array[6, 7, 11, 10, 8, 1, 9]);
-- insert into deps values ( 2 , array[]::integer[]);
-- insert into deps values ( 3 , array[]::integer[]);
-- insert into deps values ( 4 , array[]::integer[]);

with recursive topsort(p,d,path) as (
     select null::integer, null::integer[], array[]::integer[]
UNION ALL
     select deps.p, deps.d, path || deps.p
     from topsort, deps
     where (deps.d <@ path and not deps.p = any(path)))
select path from topsort where array_length(path, 1) = (select count(*) from deps);

-- # if not redirected, 'more' is spawn and interactively blocks
-- psql -f topsort.sql > toto && cat toto     # is easier to use