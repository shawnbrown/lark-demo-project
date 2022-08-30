# Lark Parser Usage Demo

This repository demonstrates how the Lark parser toolkit can be used in a project.

- Implements **stand-alone** and **dependent** versions of the same grammar.
- A single ``lark.Transformer`` is shared by both implementations.
- The ``tox.ini`` file includes a pre-testing step that rebuilds the
  stand-alone parser module before each test.
- The environment settings define an environment variable (``LARK_DEMO_MODE``)
  to determine which parser is checked (either ``standalone`` or ``dependency``).
- The test suite runs the same tests for each mode.

You can learn more about Lark on [PyPI](https://pypi.org/project/lark/) or
[GitHub](https://github.com/lark-parser/lark).


### The ``tox.ini`` file

We want to build the stand-alone module *before* we begin testing. We do this
by adding the ``build_standalone`` environment to the top of the list (tox
builds environments and runs tests in the order given). We also use the
``skipsdist = True`` setting because this demo is not a proper Python
package:

```ini
[tox]
envlist =
    build_standalone  # <- Pre-testing build step.
    py3-standalone
    py3-dependency
recreate = False
skipsdist = True

...
```

The ``testenv:build_standalone`` section requires
[Lark](https://github.com/lark-parser/lark) as a dependency. The
``commands`` setting runs Lark's stand-alone tool taking a grammar
file as input (``json.lark``) and generating a stand-alone parser
module as output (``standalone_module.py``):

```ini
...

[testenv:build_standalone]
description =
    Generate stand-alone parser module (pre-test build step).
deps =
    lark
commands =
    python -m lark.tools.standalone --out="standalone_module.py" json.lark

...
```

The other testing environments set the environment variable that
determines which version is loaded (see the *Define make_parser()
function* section of ``json_parser_main.py`` to see how this is
implemented):

```ini
...

[testenv:py3-standalone]
description =
    Run tests for stand-alone parser (no dependencies).
setenv =
    LARK_DEMO_MODE = standalone
deps =
    # None (Once built, no dependencies are required.)


[testenv:py3-dependency]
description =
    Run tests for parser with dependency (requires `lark`).
setenv =
    LARK_DEMO_MODE = dependency
deps =
    lark
```


### Sources

This demo project was adapted from pieces of code given in the Lark
documentation and Erez Shinan's blog post linked below:

- Create a stand-alone LALR(1) parser in Python:
  - http://blog.erezsh.com/create-a-stand-alone-lalr1-parser-in-python/
- Standalone Parser (from Docs » Examples for Lark):
  - https://lark-parser.readthedocs.io/en/latest/examples/standalone/json_parser_main.html


### MIT License

The code in this project builds on work form the Lark project which uses
the [MIT License](https://github.com/lark-parser/lark/blob/master/LICENSE).
All code presented here is presented using this same license and is copyright
by all contributing authors.

