import ply.lex as lex;
import sys

tokens = ('ID', 'BOLD', 'ITALIC', 'UNDERLINE', 'MONOSPACED')

# t_BOLD = r'[*]{2}'
t_ITALIC = r'[/]{2}'
t_UNDERLINE = r'[_]{2}'
t_MONOSPACED = r'[\']{2}'

def t_BOLD(t):
    r'[*]{2}'
    lexer.level += 1;
    if (lexer.level == 2):
        print('bold found')
    return t

def t_newline(t):
    r'\n+'
    t.lexer.lineno += len(t.value)

# Error handling rule
def t_error(t):
    print("Illegal character '%s'" % t.value[0])
    t.lexer.skip(1)

t_ignore = '  \t'

lexer = lex.lex()
lexer.level = 0
fh = open(sys.argv[1], "r")
lexer.input(fh.read())

for token in lexer:
    print("line %d: %s(%s)" %(token.lineno, token.type, token.value))


# if __name__ == '__main__':
#     lex.runmain()