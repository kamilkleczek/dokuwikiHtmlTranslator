import ply.lex as lex;
import ply.yacc as yacc;


class Parser:

    def __init__(self):
        self.lexer = lex.lex(module=self)
        self.yacc = yacc.yacc(module=self)

    def read(self, file):
        self.lexer.input(file.read())
        for self.tokens in self.lexer:
            print("line %d: %s(%s)" % (self.tokens.lineno, self.tokens.type, self.tokens.value))

    tokens = (
        'STRONG',
        'UNDERLINE',
        'ITALIC',
        'LINK_BEGIN',
        'LINK_END',
        'LINK_SEPARATOR',
        'LISTITEM',
        'DEL_BEGIN',
        'DEL_END',
        'SUB_BEGIN',
        'SUB_END',
        'HEADING1',
        'HEADING2',
        'HEADING3',
        'TEXT',
        'newline',
    )

    def t_STRONG(self, t):
        r'\*\*'
        return t

    def t_ITALIC(self, t):
        r'\/\/'
        return t

    def t_UNDERLINE(self, t):
        r'__'
        return t

    def t_LINK_BEGIN(self, t):
        r'\[\['
        return t

    def t_LINK_END(self, t):
        r'\]\]'
        return t

    def t_LINK_SEPARATOR(self, t):
        r'\|'
        return t

    def t_LISTITEM(self, t):
        r'\ \ \*'
        return t

    def t_DEL_BEGIN(self, t):
        r'<del>'
        return t

    def t_DEL_END(self, t):
        r'</del>'
        return t

    def t_SUB_BEGIN(self, t):
        r'<sub>'
        return t

    def t_SUB_END(self, t):
        r'</sub>'
        return t

    def t_HEADING1(self, t):
        r'===='
        return t

    def t_HEADING2(self, t):
        r'==='
        return t

    def t_HEADING3(self, t):
        r'=='
        return t

    def t_TEXT(self, t):
        r'[^]%<_\/\*\|\[@=\n\#\^~\-]+'
        return t

    def t_error(self, t):
        print("Illegal character '%s' (line %s)" % (t.value[0], t.lineno))
        self.lexer.skip(1)

    def t_newline(self, t):
        r'\n'
        t.lexer.lineno += len(t.value)
        return t

    def p_markdown(self, p):
        '''markdown : block'''
        p[0] = p[1]

    def p_markdown_block(self, p):
        '''markdown : markdown block'''
        p[0] = p[1] + p[2]

    def p_block_markdown(self, p):
        '''markdown : block markdown'''
        p[0] = p[1] + p[2]

    def p_text(self, p):
        '''block : TEXT'''
        p[0] = Node().TextNode(value=p[1])

    def p_block(self, p):
        '''block : block TEXT'''
        p[0] = p[1] + p[2]

    def p_newline(self, p):
        '''block : newline'''
        p[0] = Node().NewlineNode()

    def p_link(self, p):
        '''block : LINK_BEGIN TEXT LINK_SEPARATOR TEXT LINK_END'''
        p[0] = Node().LinkNode(p[2], p[4])

    def p_strong(self, p):
        '''block : STRONG block STRONG'''
        p[0] = Node().StrongNode(p[2])

    def p_italic(self, p):
        '''block : ITALIC block ITALIC'''
        p[0] = Node().ItalicNode(p[2])

    def p_underline(self, p):
        '''block : UNDERLINE block UNDERLINE'''
        p[0] = Node().UnderlineNode(p[2])

    def p_del(self, p):
        '''block : DEL_BEGIN block DEL_END'''
        p[0] = Node().DelNode(p[2])

    def p_SUB(self, p):
        '''block : SUB_BEGIN block SUB_END'''
        p[0] = Node().SubNode(p[2])

    def p_HEADING1(self, p):
        '''block : HEADING1 block HEADING1'''
        p[0] = Node().Heading1Node(p[2])

    def p_HEADING2(self, p):
        '''block : HEADING2 block HEADING2'''
        p[0] = Node().Heading2Node(p[2])

    def p_HEADING3(self, p):
        '''block : HEADING3 block HEADING3'''
        p[0] = Node().Heading3Node(p[2])

    def p_LISTITEM(self, p):
        '''listblock : LISTITEM block newline'''
        p[0] = Node().ListItem(p[2])

    def p_LISTBLOCK(self, p):
        '''listblocks : listblock listblock
                        | listblocks listblock
                        | listblock'''
        if len(p) > 2:
            p[0] = p[1] + p[2]
        else:
            p[0] = p[1]

    def p_LISTBLOCKS(self, p):
        '''block : listblocks'''
        p[0] = Node().List(p[1])

    def p_error(self, p):
        pass


class Node:

    def TextNode(self, value):
        return '{}'.format(value)

    def NewlineNode(self):
        return '\n'

    def LinkNode(self, value, text):
        return '<a href="{}">{}</a>'.format(value, text)

    def StrongNode(self, value):
        return '<strong> {} </strong>'.format(value)

    def UnderlineNode(self, value):
        return '<u> {} </u>'.format(value)

    def ItalicNode(self, value):
        return '<i> {} </i>'.format(value)

    def DelNode(self, value):
        return '<del> {} </del>'.format(value)

    def SubNode(self, value):
        return '<sub> {} </sub>'.format(value)

    def Heading1Node(self, value):
        return '<h1> {} </h1>'.format(value)

    def Heading2Node(self, value):
        return '<h2> {} </h2>'.format(value)

    def Heading3Node(self, value):
        return '<h3> {} </h3>'.format(value)

    def ListItem(self, value):
        return '<li>{}</li>\n'.format(value)

    def List(self, value):
        return '<ul>\n{}</ul>\n'.format(value)


fh = open('sample.dokuwiki', "r")
output = Parser().yacc.parse(fh.read(), debug=False, tracking=True)
print(output)
