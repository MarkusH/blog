# -*- coding: utf-8 -*-

"""
Taken from the Pygments C lexer
"""

from pygments.lexer import RegexLexer, include, bygroups, using, this
from pygments.util import get_bool_opt
from pygments.token import (
    Comment, Error, Keyword, Name, Number, Operator, Punctuation, String, Text,
)

__all__ = ['JNILexer']


class JNILexer(RegexLexer):
    """
    For JNI source code with preprocessor directives.
    """
    name = 'JNI'
    aliases = ['jni']
    filenames = ['*.c', '*.h']
    mimetypes = ['text/x-chdr', 'text/x-csrc']

    #: optional Comment or Whitespace
    _ws = r'(?:\s|//.*?\n|/[*].*?[*]/)+'

    tokens = {
        'whitespace': [
            # preprocessor directives: without whitespace
            ('^#if\s+0', Comment.Preproc, 'if0'),
            ('^#', Comment.Preproc, 'macro'),
            # or with whitespace
            ('^(' + _ws + r')(#if\s+0)',
             bygroups(using(this), Comment.Preproc), 'if0'),
            ('^(' + _ws + ')(#)',
             bygroups(using(this), Comment.Preproc), 'macro'),
            (r'^(\s*)([a-zA-Z_][a-zA-Z0-9_]*:(?!:))',
             bygroups(Text, Name.Label)),
            (r'\n', Text),
            (r'\s+', Text),
            (r'\\\n', Text),  # line continuation
            (r'//(\n|(.|\n)*?[^\\]\n)', Comment.Single),
            (r'/(\\\n)?[*](.|\n)*?[*](\\\n)?/', Comment.Multiline),
        ],
        'statements': [
            (r'L?"', String, 'string'),
            (r"L?'(\\.|\\[0-7]{1,3}|\\x[a-fA-F0-9]{1,2}|[^\\\'\n])'", String.Char),
            (r'(\d+\.\d*|\.\d+|\d+)[eE][+-]?\d+[LlUu]*', Number.Float),
            (r'(\d+\.\d*|\.\d+|\d+[fF])[fF]?', Number.Float),
            (r'0x[0-9a-fA-F]+[LlUu]*', Number.Hex),
            (r'0[0-7]+[LlUu]*', Number.Oct),
            (r'\d+[LlUu]*', Number.Integer),
            (r'\*/', Error),
            (r'[~!%^&*+=|?:<>/-]', Operator),
            (r'[()\[\],.]', Punctuation),
            (r'\b(case)(.+?)(:)', bygroups(Keyword, using(this), Text)),
            (r'(auto|break|case|const|continue|default|do|else|enum|extern|'
             r'for|goto|if|register|restricted|return|sizeof|static|struct|'
             r'switch|typedef|union|volatile|virtual|while)\b', Keyword),
            (r'(int|long|float|short|double|char|unsigned|signed|void|jint|jstring|jclass|JNIEnv)\b',
             Keyword.Type),
            (r'(_{0,2}inline|naked|restrict|thread|typename)\b', Keyword.Reserved),
            (r'__(asm|int8|based|except|int16|stdcall|cdecl|fastcall|int32|'
             r'declspec|finally|int64|try|leave)\b', Keyword.Reserved),
            (r'(true|false|NULL)\b', Name.Builtin),
            (r'(JNIEXPORT|JNICALL)\b', Comment.Preproc),
            ('[a-zA-Z_][a-zA-Z0-9_]*', Name),
        ],
        'root': [
            include('whitespace'),
            # functions
            (r'(JNIEXPORT)'
             r'((?:[a-zA-Z0-9_*\s])+?(?:\s|[*]))'    # return arguments
             r'(JNICALL)'
             r'([a-zA-Z_][a-zA-Z0-9_\\]*)'             # method name
             r'(\s*\([^;]*?\))'                      # signature
             r'(' + _ws + r')({)',
             bygroups(Comment.Preproc, using(this), Comment.Preproc, Name.Function, using(this), using(this),
                      Punctuation),
             'function'),
            # function declarations
            (r'(JNIEXPORT)?'
             r'((?:[a-zA-Z0-9_*\s])+?(?:\s|[*]))'    # return arguments
             r'(JNICALL)'
             r'([a-zA-Z_][a-zA-Z0-9_\\]*)'             # method name
             r'(\s*\([^;]*?\))'                      # signature
             r'(' + _ws + r')(;)',
             bygroups(using(this), using(this), using(this), Name.Function, using(this), using(this),
                      Punctuation)),
            ('', Text, 'statement'),
        ],
        'statement': [
            include('whitespace'),
            include('statements'),
            ('[{}]', Punctuation),
            (';', Punctuation, '#pop'),
        ],
        'function': [
            include('whitespace'),
            include('statements'),
            (';', Punctuation),
            ('{', Punctuation, '#push'),
            ('}', Punctuation, '#pop'),
        ],
        'string': [
            (r'"', String, '#pop'),
            (r'\\([\\abfnrtv"\']|x[a-fA-F0-9]{2,4}|[0-7]{1,3})', String.Escape),
            (r'[^\\"\n]+', String),  # all other characters
            (r'\\\n', String),  # line continuation
            (r'\\', String),  # stray backslash
        ],
        'macro': [
            (r'[^/\n]+', Comment.Preproc),
            (r'/[*](.|\n)*?[*]/', Comment.Multiline),
            (r'//.*?\n', Comment.Single, '#pop'),
            (r'/', Comment.Preproc),
            (r'(?<=\\)\n', Comment.Preproc),
            (r'\n', Comment.Preproc, '#pop'),
        ],
        'if0': [
            (r'^\s*#if.*?(?<!\\)\n', Comment.Preproc, '#push'),
            (r'^\s*#el(?:se|if).*\n', Comment.Preproc, '#pop'),
            (r'^\s*#endif.*?(?<!\\)\n', Comment.Preproc, '#pop'),
            (r'.*?\n', Comment),
        ]
    }

    stdlib_types = ['size_t', 'ssize_t', 'off_t', 'wchar_t', 'ptrdiff_t',
            'sig_atomic_t', 'fpos_t', 'clock_t', 'time_t', 'va_list',
            'jmp_buf', 'FILE', 'DIR', 'div_t', 'ldiv_t', 'mbstate_t',
            'wctrans_t', 'wint_t', 'wctype_t']
    c99_types = ['_Bool', '_Complex', 'int8_t', 'int16_t', 'int32_t', 'int64_t',
            'uint8_t', 'uint16_t', 'uint32_t', 'uint64_t', 'int_least8_t',
            'int_least16_t', 'int_least32_t', 'int_least64_t',
            'uint_least8_t', 'uint_least16_t', 'uint_least32_t',
            'uint_least64_t', 'int_fast8_t', 'int_fast16_t', 'int_fast32_t',
            'int_fast64_t', 'uint_fast8_t', 'uint_fast16_t', 'uint_fast32_t',
            'uint_fast64_t', 'intptr_t', 'uintptr_t', 'intmax_t', 'uintmax_t']

    def __init__(self, **options):
        self.stdlibhighlighting = get_bool_opt(options,
                'stdlibhighlighting', True)
        self.c99highlighting = get_bool_opt(options,
                'c99highlighting', True)
        RegexLexer.__init__(self, **options)

    def get_tokens_unprocessed(self, text):
        for index, token, value in \
                RegexLexer.get_tokens_unprocessed(self, text):
            if token is Name:
                if self.stdlibhighlighting and value in self.stdlib_types:
                    token = Keyword.Type
                elif self.c99highlighting and value in self.c99_types:
                    token = Keyword.Type
            yield index, token, value
