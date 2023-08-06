"""Nginx Language Server.

Creates the language server constant and wraps "features" with it.

Official language server spec:
    https://microsoft.github.io/language-server-protocol/specification
"""

from typing import Optional

from pygls.features import COMPLETION, HOVER
from pygls.server import LanguageServer
from pygls.types import (
    CompletionItem,
    CompletionList,
    CompletionParams,
    Hover,
    InsertTextFormat,
    MarkupContent,
    MarkupKind,
    SymbolKind,
    TextDocumentPositionParams,
)

from . import pygls_utils
from .parser import nginxconf
from .parser.directives import directives

# pylint: disable=line-too-long


SERVER = LanguageServer()


# Server capabilities


@SERVER.feature(COMPLETION, trigger_characters=[".", "'", '"'])
def completion(
    server: LanguageServer, params: CompletionParams
) -> Optional[CompletionList]:
    """Returns completion items."""
    document = server.workspace.get_document(params.textDocument.uri)
    parsed = nginxconf.convert(document.source)
    line = nginxconf.find(parsed, params.position.line)
    contexts = line["contexts"] if line["contexts"] else ["main"]
    possibilities = directives.get(contexts[-1], {})
    completion_items = [
        CompletionItem(
            label=directive["name"],
            filter_text=directive["name"],
            detail=directive["desc"],
            kind=SymbolKind.Property,
            insert_text=directive["name"],
            insert_text_format=InsertTextFormat.PlainText,
        )
        for directive in possibilities.values()
    ]
    return (
        CompletionList(is_incomplete=False, items=completion_items)
        if completion_items
        else None
    )


@SERVER.feature(HOVER)
def hover(
    server: LanguageServer, params: TextDocumentPositionParams
) -> Optional[Hover]:
    """Support Hover."""
    document = server.workspace.get_document(params.textDocument.uri)
    parsed = nginxconf.convert(document.source)
    word = document.word_at_position(params.position)
    line = nginxconf.find(parsed, params.position.line)
    contexts = line["contexts"] if line["contexts"] else ["main"]
    possibilities = directives.get(contexts[-1], {})
    directive = possibilities.get(word)
    if directive:
        contents = MarkupContent(
            kind=MarkupKind.PlainText,
            value=directive["desc"],
        )
        _range = pygls_utils.current_word_range(document, params.position)
        return Hover(contents=contents, range=_range)
    return None
