# zable
**Category**: Misc
**Difficulty**: Easy/Medium
**Author**: puzzler7

# Description

There are two types of build systems - the ones people complain about, and the ones nobody uses.

# Distributions
- nc connection
- `zable.dist.zip` - generated with `gen_dist.sh`

# Solution

`js_binary` generates a bash script that sets up the environment where `hello.js` runs. Part of this involves putting the environment variables in a snippet that looks like the following:

```sh
EXPORT NAME="<env var here>"
```

Thus, putting double quotes in your name escapes this, allowing for RCE. The name `";cat /app/flag.txt;echo "` prints the flag.

