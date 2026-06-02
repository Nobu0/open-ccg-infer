
run(Content) :-
    writeln(Content),
    %ccg_parse(Content, Pattern),
    test,
    writeln("Pattern").

test :-
    writeln('TEST OK').    
