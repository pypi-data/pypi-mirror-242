#!/usr/bin/env python
# coding: utf-8

__author__  = "ChenyangGao <https://chenyanggao.github.io/>"
__all__ = [
    "fromstring", "to_xhtml", "elementpath_of", "xpath_of", "generalize_elementpath", 
    "generalize_xpath", "clean_nsmap", "find", "iterfind", "xpath", 
]

from functools import partial
from itertools import chain
from re import compile as re_compile, Match, Pattern
from typing import (
    cast, Any, Callable, Final, ItemsView, Iterable, Iterator, Mapping, NamedTuple, Optional
)

from lxml.etree import fromstring as xml_fromstring, tostring, _Element as Element, _ElementTree as ElementTree
from lxml.html import fromstring as html_fromstring


CRE_XML_ENCODING: Final = re_compile(r'(?<=\bencoding=")[^"]+|(?<=\bencoding=\')[^\']+')
MATCH_START_XML_DEC: Final = re_compile(r'<\?xml\b').match
MATCH_DEC: Final = re_compile(r'\s*((?s:<\?.+?\?>))').match
MATCH_DEC_B: Final = re_compile(br'\s*((?s:<\?.+?\?>))').match
MATCH_START_HTML_DTD: Final = re_compile(r'\s*(?i:<!DOCTYPE\s+html\b)').match
MATCH_START_HTML_DTD_B: Final = re_compile(br'\s*(?i:<!DOCTYPE\s+html\b)').match
XPATH_TOEKN_PATS: Final = [
    ("DSLASH", r"//"), 
    ("SLASH", r"/"), 
    ("LBRACKET", r"\["), 
    ("RBRACKET", r"\]"), 
    ("LPARAN", r"\("), 
    ("RPARAN", r"\)"), 
    ("DCOLON", r"::"), 
    ("COLON", r":"), 
    ("DDOT", r"\.\."), 
    ("DOT", r"\."), 
    ("AT", r"@"), 
    ("DOLLAR", "\$"), 
    ("COMMA", r","), 
    ("STAR", r"\*"), 
    ("VERTICAL_BAR", r"\|"), 
    ("QM", r"\?"), 
    ("COMP", r"!=|<=|>=|=|<|="), 
    ("NUMBER", r"\d+(?:\.\d*)?|\.\d+"), 
    ("NAME", r"\w[\w.-]*"), 
    ("STRING", r"'[^'\\]*(?:\\.[^'\\]*)*'|" + r'"[^"\\]*(?:\\.[^"\\]*)*"'),
    ("WHITESPACES", r"\s+"), 
    ("ANY", r"(?s:.)"), 
]
CRE_XPATH_TOKEN: Final = re_compile("|".join("(?P<%s>%s)" % pair for pair in XPATH_TOEKN_PATS))
ELEMENTPATH_TOEKN_PATS: Final = [
    ("DSLASH", r"//"), 
    ("SLASH", r"/"), 
    ("LBRACKET", r"\["), 
    ("RBRACKET", r"\]"), 
    ("LPARAN", r"\("), 
    ("RPARAN", r"\)"), 
    ("COLON", r":"), 
    ("DDOT", r"\.\."), 
    ("DOT", r"\."), 
    ("AT", r"@"), 
    ("STAR", r"\*"), 
    ("COMP", r"!=|="), 
    ("NUMBER", r"\d+"), 
    ("NAME", r"\w[\w.-]*"), 
    ("STRING", r"'[^'\\]*(?:\\.[^'\\]*)*'|" + r'"[^"\\]*(?:\\.[^"\\]*)*"'), 
    ("NSURI", r"\{[^}]*\}"), 
    ("WHITESPACES", r"\s+"), 
    ("ANY", r"(?s:.)"), 
]
CRE_ELEMENTPATH_TOKEN: Final = re_compile("|".join("(?P<%s>%s)" % pair for pair in ELEMENTPATH_TOEKN_PATS))


def fromstring(
    doc: bytes | str, 
    /, 
    base_url=None, 
    parser=None, 
) -> Element:
    """
    Parse an XML or HTML document from a bytes or string input and return a `lxml.etree._Element` object.

    :param doc: The XML or HTML document to parse.
    :param base_url: Optional base URL for the document. Used for resolving relative URLs in the document.
    :param parser: Optional parser to use for parsing the document. If not provided, the default parser will be used.

    :return: The parsed XML or HTML document as a `lxml.etree._Element` object.
    """
    match_dec: Callable
    match_html_dtd: Callable
    fromstring: Callable
    if isinstance(doc, str):
        match_dec = MATCH_DEC
        match_html_dtd = MATCH_START_HTML_DTD
        flag_check_xml_dec = True
    else:
        match_dec = MATCH_DEC_B
        match_html_dtd = MATCH_START_HTML_DTD_B
        flag_check_xml_dec = False
    start = 0
    xml_dec_matches = []
    while (match := match_dec(doc, start)) is not None:
        if flag_check_xml_dec and MATCH_START_XML_DEC(match[1]) is not None:
            xml_dec_matches.append(match[1])
        start = match.end()
    if match_html_dtd(doc, start) is not None:
        fromstring = html_fromstring
    else:
        fromstring = xml_fromstring
    if isinstance(doc, str):
        for match in map(CRE_XML_ENCODING.search, xml_dec_matches):
            if match is not None:
                doc = bytes(doc, match[0])
                break
    return fromstring(doc, base_url=base_url, parser=parser)


def to_xhtml(
    etree: Element | ElementTree, 
    ensure_epub: bool = False, 
) -> Callable[..., bytes]:
    """Convert a HTML element node (with its descendants) or tree into XHTML format.

    :param etree: Element node or tree that to be converted.
    :param ensure_epub: Determine whether to add ePub namespaces to the root element, 
                        but it must itself be a root element or element tree.

    :return: A helper function (ignore if not needed), used to serialize the current 
             element node or element tree (depending on what is provided).
    """
    # NOTE: However, if XML or XHTML is converted to HTML, the element tags may lose the namespace prefix.
    if isinstance(etree, Element):
        root = etree.getroottree().getroot()
        is_root = etree is root
    else:
        root = etree.getroot()
        is_root = True
    # NOTE: Because in Sigil editor, double hyphen (--) within comment will 
    #       issue an error, so I just escape all the double hyphens 😂.
    comments: list[_Comment] = etree.xpath(".//comment()") # type: ignore
    if comments:
        for comment in comments:
            if comment.text and "--" in comment.text:
                comment.text = comment.text.replace("--", "&#45;&#45;")
    # NOTE: Because if you want to convert HTML to XHTML, you may need to use 
    #       `lxml.etree.tostring`. When encountering an element node without 
    #       children, it will form a self closing tag, but there is no such 
    #       thing in HTML. However there is a concept of void element in HTML:
    #
    #           - https://html.spec.whatwg.org/multipage/syntax.html#void-elements
    #           - https://developer.mozilla.org/en-US/docs/Glossary/Void_element
    #
    #       A void element is an element in HTML that cannot have any child nodes 
    #       (i.e., nested elements or text nodes). Void elements only have a start 
    #       tag; end tags must not be specified for void elements.
    #       To make sure that all non-void elements do not form self closing tags, 
    #       it is possible to replace the text node with "" by checking that their 
    #       text node is None.
    for el in etree.iter("*"):
        # NOTE: In the past, there were other elements that were void elements, such as 
        #       <param> and <keygen>, but they have all been deprecated and removed. 
        #       An obsoleted element is not occupied by the HTML standard and is not 
        #       considered as a void element. So they can be given new meanings by users, 
        #       and cannot be directly considered as void elements.
        #
        #           - https://developer.mozilla.org/en-US/docs/Web/HTML/Element/param
        #           - https://developer.mozilla.org/en-US/docs/Mozilla/Firefox/Releases/69
        if el.tag.lower() not in (
            "area", "base", "br", "col", "embed", "hr", "img", "input", "link", 
            "meta", "source", "track", "wbr", 
        ):
            if el.text is None:
                el.text = ""
    # NOTE: You need to use epub:type to perform `Expression Structural Semantics`, 
    #       so there are two namespaces that need to be defined.
    #
    #           - https://www.w3.org/TR/epub/#app-structural-semantics
    #           - https://www.w3.org/TR/xml-names/
    if is_root:
        if "xmlns" not in root.attrib:
            root.attrib["xmlns"] = "http://www.w3.org/1999/xhtml"
        if ensure_epub and "xmlns:epub" not in root.attrib:
            root.attrib["xmlns:epub"] = "http://www.idpf.org/2007/ops"
    # NOTE: Because UTF-8 is currently the most recommended encoding
    kwargs: dict[str, Any] = {"encoding": "utf-8"}
    if is_root:
        # NOTE: Specify the DOCTYPE as HTML5 (<!DOCTYPE html>), ignoring the original.
        kwargs["doctype"] = "<!DOCTYPE html>"
        kwargs["xml_declaration"] = True
    return partial(tostring, etree, **kwargs) # type: ignore


def elementpath_of(
    el: Element, 
    with_name: bool = True, 
) -> str:
    """
    Gets the ElementPath of a given XML (HTML, XHTML, SGML, ...) element relative to its root.

    :param el: The element for which the ElementPath needs to be determined.
    :param with_name: A flag to determine if the tag names should be displayed in the ElementPath.

    :return: The ElementPath of the given element.
    """
    pel = el.getparent()
    if pel is None:
        return "."
    ls: list[str] = []
    add = ls.append
    if with_name:
        # NOTE: You can use `el.getroottree().getelementpath(el)` instead.
        while pel is not None:
            tag = el.tag
            add(f"/{tag}")
            if any(sel is not el for sel in pel.iterchildren(tag)):
                for i, sel in enumerate(pel.iterchildren(tag), 1):
                    if sel is el:
                        break
                ls[-1] += f"[{i}]"
            el, pel = pel, pel.getparent()
    else:
        while pel is not None:
            for i, sel in enumerate(pel.iterchildren("*"), 1):
                if sel is el:
                    break
            add(f"/*[{i}]")
            el, pel = pel, pel.getparent()
    return "".join(reversed(ls))


def xpath_of(
    el: Element, 
    with_name: bool = True, 
) -> str:
    """Gets the XPath of a given XML (HTML, XHTML, SGML, ...) element in the document tree. 

    :param el: The element for which the XPath needs to be determined.
    :param with_name: A flag to determine if the tag names should be displayed in the XPath. 

    :return: The XPath of the given element.
    """
    ls: list[str] = []
    add = ls.append
    if with_name:
        get_basetag = lambda tag: tag[tag.find("}")+1:]
        while True:
            tag = el.tag
            basetag = get_basetag(tag)
            if tag == basetag:
                add(f"/{tag}")
                epath = "{}%s" % basetag
            else:
                add(f'/*[local-name()="{basetag}"]')
                epath = "{*}%s" % basetag
            pel = el.getparent()
            if pel is None:
                break
            if any(sel is not el for sel in pel.iterchildren(epath)):
                for i, sel in enumerate(pel.iterchildren(epath), 1):
                    if sel is el:
                        break
                ls[-1] += f"[{i}]"
            el = pel
    else:
        # NOTE: You can use `el.getroottree().getpath(el)` instead.
        pel = el.getparent()
        while pel is not None:
            for i, sel in enumerate(pel.iterchildren("*"), 1):
                if el is sel:
                    break
            add(f"/*[{i}]")
            el, pel = pel, pel.getparent()
        add("/*")
    return "".join(reversed(ls))


class Token(NamedTuple):
    type: str
    value: str
    start: int
    stop: int
    match: Match


def tokenize(
    xpath: str, 
    tokenspec: Pattern = CRE_XPATH_TOKEN, 
) -> Iterator[Token]:
    """
    """
    # Reference:
    #   - https://www.python.org/community/sigs/retired/parser-sig/towards-standard/
    #   - https://www.w3.org/TR/xpath/
    #   - https://github.com/antlr/antlr4
    #   - https://www.gnu.org/software/bison/
    #   - https://www.antlr3.org/grammar/list.html
    #   - https://github.com/antlr/grammars-v4/tree/master/xpath
    #   - https://github.com/lark-parser/lark
    #   - https://github.com/dabeaz/ply
    for match in tokenspec.finditer(xpath):
        token_type = cast(str, match.lastgroup)
        token_value = match.group(token_type)
        yield Token(token_type, token_value, *match.span(), match)


def name_token_iter(
    path: str, 
    /, 
    tokenspec: Pattern = CRE_XPATH_TOKEN, 
) -> Iterator[Token]:
    """
    """
    step_begin = True
    pred_level = 0
    #para_level = 0
    cache_token = None
    for token in tokenize(path, tokenspec):
        type = token.type
        value = token.value
        if type == "WHITESPACES":
            continue
        if step_begin:
            if type == "NAME":
                cache_token = token
                continue
            # NOTE: axes end
            elif type == "DCOLON":
                if cache_token:
                    cache_token = None
                else:
                    step_begin = False
                continue
        if not pred_level and type in ("SLASH", "DSLASH", "VERTICAL_BAR"):
            if cache_token:
                yield cache_token
                cache_token = None
            step_begin = True
            continue
        if cache_token:
            if not pred_level and type == "LBRACKET":
                yield cache_token
            cache_token = None
        if type == "LBRACKET":
            pred_level += 1
        elif type == "RBRACKET" and pred_level:
            pred_level -= 1
        step_begin = False
    if cache_token:
        yield cache_token


def generalize_elementpath(
    epath: str, 
    /, 
    prefix: Optional[str] = None, 
    uri: Optional[str] = None, 
) -> str:
    """Generalizes a given ElementPath expression, so that namespaces can be disregarded or determined. 

    :param epath: The original ElementPath to be generalized.
    :param prefix: An optional prefix for the generalized version.
    :param uri: An optional URI for the generalized version.

    :return: The generalized ElementPath.

    :NOTE:

        - The `prefix` takes precedence over the `uri`.
        - `prefix` takes effect when `prefix` is a non-empty string.
        - `uri` takes effect when `prefix` is None and `uri` is a string.

    :EXAMPLE:

        >>> generalize_elementpath("title")
        '{*}title'
        >>> generalize_elementpath("title", "dc")
        'dc:title'
        >>> generalize_elementpath("title", uri="http://purl.org/dc/elements/1.1/")
        '{http://purl.org/dc/elements/1.1/}title'
        >>> generalize_elementpath("title", uri="")
        '{}title'
    """
    tokens = tuple(name_token_iter(epath, CRE_ELEMENTPATH_TOKEN))
    if not tokens:
        return epath
    parts: list[str] = []
    add_part = parts.append
    if prefix:
        expand = f"{prefix}:%s".__mod__
    elif uri is not None:
        expand = f"{{{uri}}}%s".__mod__
    else:
        expand = '{*}%s'.__mod__
    start = 0
    for token in tokens:
        add_part(epath[start:token.start])
        add_part(expand(token.value))
        start = token.stop
    add_part(epath[start:])
    return "".join(parts)


def generalize_xpath(
    xpath: str, 
    /, 
    prefix: Optional[str] = None, 
) -> str:
    """Generalizes a given XPath expression, so that namespaces can be disregarded or determined. 

    :param xpath: The XPath expression to be generalized.
    :param prefix: An optional namespace prefix to be used in the generalized XPath.
                   If provided, the prefix is added before the tag names in the XPath.
                   If not provided, the 'local-name()' function is used to match the tag names in the XPath.

    :return: The generalized XPath.

    :EXAMPLE:

        >>> generalize_xpath("element")
        '*[local-name()="element"]'
        >>> generalize_elementpath("element", "xml")
        'xml:element'
    """
    # TODO: Research is ongoing for XPath of more complex nested structures, even XSLT.
    tokens = tuple(name_token_iter(xpath, CRE_XPATH_TOKEN))
    if not tokens:
        return xpath
    parts: list[str] = []
    add_part = parts.append
    if prefix:
        expand = f"{prefix}:%s".__mod__
    else:
        expand = '*[local-name()="%s"]'.__mod__
    start = 0
    for token in tokens:
        add_part(xpath[start:token.start])
        add_part(expand(token.value))
        start = token.stop
    add_part(xpath[start:])
    return "".join(parts)


def clean_nsmap(
    nsmap: Mapping[str, str] | Mapping[Optional[str], str] | Iterable[tuple[str, str]] | Iterable[tuple[Optional[str], str]], 
    extra_nsmap: None | Mapping[str, str] | Mapping[Optional[str], str] | Iterable[tuple[str, str]] | Iterable[tuple[Optional[str], str]] = None, 
    predicate_key: Optional[Callable] = None, 
    predicate_value: Callable = bool, 
) -> dict[str, str] | dict[Optional[str], str]:
    """Build a clean dictionary from a given `nsmap` and an optional `extra_nsmap`.

    :param nsmap: The namespace map object to be cleaned. It can be a mapping object or 
                  an iterable of key-value pairs representing namespaces.
    :param extra_nsmap: An additional namespace map object to be merged with the nsmap.
    :param predicate_key: 
        A callable that takes a key as input and returns a boolean value. 
        If provided, only entries with keys that satisfy the predicate will be included in the cleaned dictionary.
    :param predicate_value: 
        A callable that takes a value as input and returns a boolean value. 
        If provided, only entries with values that satisfy the predicate will be included in the cleaned dictionary.

    :return: A cleaned namespace map as a dictionary.
    """
    def items(m: Mapping, /) -> ItemsView:
        try:
            return m.items()
        except Exception:
            return ItemsView(m)
    if isinstance(nsmap, Mapping):
        nsmap = items(nsmap)
    if extra_nsmap:
        if isinstance(extra_nsmap, Mapping):
            extra_nsmap = items(extra_nsmap)
        nsmap = chain(extra_nsmap, nsmap)
    nsmap = cast(Iterable[tuple[Optional[str], str]], nsmap)
    if predicate_key is None:
        return {k: v for k, v in nsmap if predicate_value(v)}
    return {k: v for k, v in nsmap if predicate_key(k) and predicate_value(v)}


def find(
    el: Element | ElementTree, 
    path: str, 
    /, 
    generalize: bool = False, 
    namespaces: None | Mapping[str, str] | Mapping[Optional[str], str] = None, 
) -> Optional[Element]:
    return next(iterfind(el, path, generalize=generalize, namespaces=namespaces), None)


def iterfind(
    el: Element | ElementTree, 
    path: str, 
    /, 
    generalize: bool = False, 
    namespaces: None | Mapping[str, str] | Mapping[Optional[str], str] = None, 
) -> Iterator[Element]:
    if isinstance(el, Element):
        nsmap = el.nsmap
        if path.startswith("/"):
            el = el.getroottree()
    else:
        nsmap = el.getroot().nsmap
    if nsmap:
        namespaces = clean_nsmap(nsmap, namespaces)
    if generalize:
        path = generalize_elementpath(path)
    return el.iterfind(path, namespaces) # type: ignore


def xpath(
    el: Element | ElementTree, 
    path: str, 
    /, 
    generalize: bool = False, 
    namespaces: Optional[Mapping[str, str]] = None, 
    **kwargs, 
):
    if isinstance(el, Element):
        nsmap = el.nsmap
        if path.startswith("/"):
            el = el.getroottree()
    else:
        nsmap = el.getroot().nsmap
    if nsmap:
        namespaces = cast(dict[str, str], clean_nsmap(nsmap, namespaces, predicate_key=bool))
    if generalize:
        path = generalize_xpath(path)
    return el.xpath(path, namespaces=namespaces, **kwargs)

