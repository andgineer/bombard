from pygments import highlight
from pygments.lexers.markup import MarkdownLexer
from pygments.formatters.terminal import TerminalFormatter

def show_descr(descr: str) -> str:
    return highlight(descr, MarkdownLexer(), TerminalFormatter())
