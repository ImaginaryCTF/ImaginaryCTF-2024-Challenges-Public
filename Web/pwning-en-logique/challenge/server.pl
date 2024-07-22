:- use_module(library(http/thread_httpd)).
:- use_module(library(http/http_dispatch)).
:- use_module(library(http/http_session)).
:- use_module(library(http/http_client)).
:- use_module(library(http/http_parameters)).
:- use_module(library(http/html_write)).

:- http_handler('/', index, []).
:- http_handler('/login', login, []).
:- http_handler('/greet', greet, []).
:- http_handler('/flag', flag, []).

server(Port) :-
    http_server(http_dispatch, [port(Port)]).

index(_Request) :-
    reply_html_page(
        title('Index | Pwning en Logique'),
        [
            form([action='/login'], [
                button([type=submit], 'Log in')
            ]),
            form([action='/greet'], [
                button([type=submit], 'Get greeted by the server')
            ]),
            form([action='/flag'], [
                button([type=submit], 'Get the flag')
            ])
        ]
    ).

login(Request) :-
    member(method(post), Request),
    http_read_data(Request, Data, []),
    ((
        member(username=Username, Data),
        member(password=Password, Data),
        users(Users),
        member(Username=Password, Users),
        http_session_retractall(_OldUsername),
        http_session_assert(username(Username)),
        http_redirect(see_other, '/greet', Request)
    ); reply_html_page(
        [title('Log in | Pwning en Logique')],
        [
            h2([], 'Invalid credentials'),
            form([action='/login', method='POST'], [
                label([for=userame], 'Username: '),
                input([type=text, name=username], []),
                label([for=password], 'Password: '),
                input([type=password, name=password], []),
                input([type=submit], [])
            ])
        ]
    )).

login(_Request) :-
    reply_html_page(
        [title('Log in | Pwning en Logique')],
        [
            form([action='/login', method='POST'], [
                label([for=userame], 'Username: '),
                input([type=text, name=username], []),
                label([for=password], 'Password: '),
                input([type=password, name=password], []),
                input([type=submit], [])
            ])
        ]
    ).

greet(Request) :-
    http_session_data(username(Username)),
    http_parameters(Request, [
        greeting(Greeting, [default('Hello')]),
        format(Format, [default('~w, ~w!')])
    ]),
    content_type,
    format(Format, [Greeting, Username]).

greet(Request) :-
    http_redirect(see_other, '/login', Request).

flag(_Request) :-
    content_type,
    (http_session_data(username(admin)), print_flag; print_access_denied).

content_type :- format('Content-Type: text/html~n~n').
print_flag :- format('ictf{f0rm4t_5tr1ng_vuln3r4b1l1ty_1n_Prolog_4nd_1t5_n0t_3v3n_4_pwn_ch4ll3ng3}').
print_access_denied :- format('<h1>Only the admin can access the flag!</h1>').

users([
    guest=guest,
    'AzureDiamond'=hunter2,
    admin=AdminPass
]) :- crypto_n_random_bytes(32, RB), hex_bytes(AdminPass, RB).
