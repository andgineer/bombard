from pygments import highlight
from pygments.formatters.terminal import TerminalFormatter
from pygments.lexers.markup import MarkdownLexer


def markdown_for_terminal(descr: str) -> str:
    return str(highlight(descr, MarkdownLexer(), TerminalFormatter()))
