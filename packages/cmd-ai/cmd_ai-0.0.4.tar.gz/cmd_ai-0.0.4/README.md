Project cmd~ai~
===============

*Another ChatGPT project implemented in a shell command*

README for version `0.0.3`

Installation
------------

It should work with `pip install`, not tested.

Needs `API_KEY` for OpenAI in `~/.openai.token`

Features
--------

-   conversation in terminal with gpt4
-   incremental saving conversation to `conversations.org`
-   *pythonista* mode
-   *sheller* mode (both with a simple system prompt)
-   show spent money
-   save code to `/tmp` and execute with `.e`

Help
----

``` {.example}
.h      help
.q      quit
.r      run code
.l      show tokens
.l number ... change limit tokens
________________ ROLES
.a   assistent
.t   NO translator
.p   python coder
.s   shell expert
.d   NO dalle
________________ MODEL
.i   NO use dalle
.v   NO use vision
```
