-module(tut).
-export([double/1]).
-export([fac/1, mult/2, convert/2]).
-export([convert_length/1]).
-export([list_length/1]).

double(X) ->
    2 * X.

fac(1) ->
    1;
fac(N) ->
    N * fac(N - 1).

mult(X, Y) ->
    X * Y.

convert(M, inch) ->
    M / 2.54;
convert(M, cm) ->
    M * 2.54.

convert_length({cm, X}) ->
    {inch, X / 2.54};
convert_length({inch, Y}) ->
    {cm, Y * 2.54}.

list_length([]) ->
    0;
list_length([First | Remainder]) ->
    1 + list_length(Remainder).
