load('@aspect_rules_js//js:defs.bzl', 'js_binary')
load(':defs.bzl', 'get_env')

get_env(name='get_env')

js_binary(
    name = 'run',
    env = {
        'NAME': '$(NAME)',
    },
    toolchains = [
        ':get_env',
    ],
    entry_point = 'hello.js',
)