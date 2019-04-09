from pygments import highlight
from pygments.lexers.markup import MarkdownLexer
from pygments.formatters.terminal import TerminalFormatter


def markdown_for_terminal(descr: str) -> str:
    return highlight(descr, MarkdownLexer(), TerminalFormatter())
