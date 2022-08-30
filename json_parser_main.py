#!/usr/bin/env python3
import os
import sys


######################################################################
# Define make_parser() function for stand-alone or dependent parser.
######################################################################

LARK_DEMO_MODE = os.getenv('LARK_DEMO_MODE') or 'dependency'

if LARK_DEMO_MODE == 'standalone':
    from standalone_module import Lark_StandAlone, Transformer, v_args

    def make_parser(make_transformer):
        """Helper function to create parser instance."""
        transformer = make_transformer()
        return Lark_StandAlone(transformer=transformer)

elif LARK_DEMO_MODE == 'dependency':
    from lark import Lark, Transformer, v_args

    def make_parser(make_transformer):
        """Helper function to create parser instance."""
        with open('json.lark') as f:
            grammar = f.read()  # Get entire file as a string.
        transformer = make_transformer()
        return Lark(grammar, parser='lalr', transformer=transformer)

else:
    raise EnvironmentError(f'unknown LARK_DEMO_MODE: {LARK_DEMO_MODE!r}')


######################################################################
# Define Transformer class.
######################################################################

inline_args = v_args(inline=True)

class TreeToJson(Transformer):
    @inline_args
    def string(self, s):
        return s[1:-1].replace('\\"', '"')

    def array(self, args):
        return list(args)

    def pair(self, args):
        return tuple(args)

    def object(self, args):
        return dict(args)

    @inline_args
    def number(self, n):
        return float(n)

    def null(self, _):
        return None

    def true(self, _):
        return True

    def false(self, _):
        return False


######################################################################
# Create a parser instance.
######################################################################

parser = make_parser(TreeToJson)


if __name__ == '__main__':
    with open(sys.argv[1]) as f:
        print(parser.parse(f.read()))

