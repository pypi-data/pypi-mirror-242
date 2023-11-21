#!/usr/bin/env python
# coding: utf-8

__author__  = "ChenyangGao <https://chenyanggao.github.io/>"
__all__ = ["resolve_prefix", "el_find", "el_iterfind", "el_xpath", "el_add", "el_del", "el_set"]

from re import compile as re_compile
from typing import cast, Callable, ItemsView, Iterable, Iterator, Mapping, Optional
try:
    # https://lxml.de
    from lxml.etree import _Element as Element, SubElement # type: ignore
except ModuleNotFoundError:
    # https://docs.python.org/3/library/xml.etree.elementtree.html
    from xml.etree.ElementTree import Element, SubElement # type: ignore


def resolve_prefix(
    name, 
    nsmap: Optional[Mapping] = None, 
    optional_nsmap: Optional[Mapping] = None, 
    inherit: bool = False, 
    _match=re_compile(r"\w(?<!\d)[\w.-]*:").match, 
):
    if not nsmap and not optional_nsmap or not isinstance(name, str):
        return name
    if name.startswith(":"):
        return name.lstrip(":")
    elif name.startswith("{*}"):
        name = name.removeprefix("{*}")
    elif name.startswith("{"):
        return name
    prefix = _match(name)
    if prefix is None:
        if not inherit:
            return name
        name0 = name
    else:
        index = prefix.end()
        prefix, name0 = name[:index-1], name[index:]
    if nsmap and prefix in nsmap:
        uri = nsmap[prefix]
    elif prefix and optional_nsmap and prefix in optional_nsmap:
        uri = optional_nsmap[prefix]
    else:
        return name
    if not uri:
        name
    return f"{{{uri}}}{name0}"


def _items(m, /):
    if isinstance(m, Mapping):
        try:
            m = m.items()
        except Exception:
            m = ItemsView(m)
    return m


def _el_set(
    el: Element, 
    /, 
    attrib: None | Mapping | Iterable = None, 
    text=None, 
    tail=None, 
    nsmap: Optional[Mapping] = None, 
    optional_nsmap: Optional[Mapping] = None, 
):
    """
    """
    if attrib:
        attrib = cast(Iterable, _items(attrib))
        el_attrib = el.attrib
        for key, val in attrib:
            if key == "":
                el.text = val if val is None else str(val)
            elif key is None:
                el.tail = val if val is None else str(val)
            elif isinstance(key, str) and key != "xmlns" and not key.startswith("xmlns:"):
                key = resolve_prefix(key, nsmap, optional_nsmap)
                if val is None:
                    el_attrib.pop(key, "")
                el_attrib[key] = str(val)
    if callable(text):
        text = text()
        if text is None:
            el.text = None
    if text is not None:
        el.text = str(text)
    if callable(tail):
        tail = tail()
        if tail is None:
            el.tail = None
    if tail is not None:
        el.tail = str(tail)


def _el_setmerge(
    el: Element, 
    /, 
    attrib: None | Mapping | Iterable = None, 
    text=None, 
    tail=None, 
    nsmap: Optional[Mapping] = None, 
    optional_nsmap: Optional[Mapping] = None, 
):
    """
    """
    if attrib:
        attrib = cast(Iterable, _items(attrib))
        el_attrib = el.attrib
        for key, val in attrib:
            if val is None:
                continue
            if key == "":
                if el.text is None:
                    el.text = str(val)
            elif key is None:
                if el.tail is None:
                    el.tail = str(val)
            elif isinstance(key, str) and key != "xmlns" and not key.startswith("xmlns:"):
                key = resolve_prefix(key, nsmap, optional_nsmap)
                if key not in el_attrib:
                    el_attrib[key] = val
    if el.text is None:
        if callable(text):
            text = text()
            if text is None:
                pass
        if text is not None:
            el.text = str(text)
    if el.tail is None:
        if callable(tail):
            tail = tail()
            if tail is None:
                pass
        if tail is not None:
            el.tail = str(tail)


def el_find(
    el: Element, 
    path: Optional[str] = None, 
    /, 
    namespaces: Optional[Mapping] = None, 
) -> Optional[Element]:
    """
    """
    return next(el_iterfind(el, path, namespaces), None)


def el_iterfind(
    el: Element, 
    path: Optional[str] = None, 
    /, 
    namespaces: Optional[Mapping] = None, 
) -> Iterator[Element]:
    """
    """
    if not path or path in (".", "*..", "*...", "./."):
        return iter((el,))
    nsmap: Optional[Mapping]
    try:
        nsmap = el.nsmap
    except:
        nsmap = namespaces
    else:
        if namespaces:
            nsmap.update(namespaces)
    return el.iterfind(path, nsmap) # type: ignore


def el_xpath(
    el: Element, 
    path: Optional[str] = None, 
    /, 
    namespaces: Optional[Mapping] = None, 
    **kwargs, 
) -> list:
    """
    """
    if not path or path == ".":
        return [el]
    nsmap: Optional[Mapping]
    try:
        nsmap = el.nsmap # type: ignore
    except:
        nsmap = namespaces
    else:
        if nsmap:
            nsmap = {k: v for k, v in nsmap.items() if k and v}
        if namespaces:
            nsmap.update(namespaces)
    return el.xpath(path, namespaces=nsmap, **kwargs) # type: ignore


def el_add(
    el: Element, 
    /, 
    name: str, 
    attrib: None | Mapping | Iterable = None, 
    text=None, 
    tail=None, 
    namespaces: Optional[Mapping] = None, 
) -> Element:
    """
    """
    try:
        nsmap = el.nsmap # type: ignore
    except:
        nsmap = {}
    if attrib:
        attrib0 = _items(attrib)
        attrib = {}
        for key, val in attrib0:
            if key is None:
                attrib[key] = val
            elif isinstance(key, str):
                if key == "xmlns":
                    if val:
                        nsmap[None] = val
                    else:
                        nsmap.pop(None, None)
                elif key.startswith("xmlns:"):
                    if val:
                        nsmap[key[6:]] = val
                    else:
                        nsmap.pop(key[6:], None)
                else:
                    attrib[key] = val
    name = resolve_prefix(name, nsmap, namespaces, inherit=True)
    sel = SubElement(el, name.removeprefix("{*}").removeprefix("{}"), nsmap=cast(dict[str, str], nsmap))
    _el_set(sel, attrib, text, tail, nsmap, namespaces)
    return sel


def el_del(
    el: Element, 
    path: Optional[str] = None, 
    /, 
    namespaces: Optional[Mapping] = None, 
) -> Optional[Element]:
    """
    """
    sel = el_find(el, path, namespaces) if path else el
    if sel is not None:
        try:
            pel = sel.getparent() # type: ignore
        except AttributeError:
            pel = el
        if pel is None or pel is sel:
            raise LookupError(f"can't get parent element: {sel!r}")
        pel.remove(sel)
    return sel


def el_set(
    el: Element, 
    path: Optional[str] = None, 
    /, 
    name: Optional[str] = None, 
    attrib: None | Mapping | Iterable = None, 
    text=None, 
    tail=None, 
    namespaces: Optional[Mapping] = None, 
    merge: bool = False, 
) -> Element:
    """
    """
    sel = el_find(el, path, namespaces) if path else el
    if sel is not None:
        if text is None and tail is None and not attrib:
            return sel
        try:
            nsmap = sel.nsmap # type: ignore
        except:
            nsmap = None
        (_el_setmerge if merge else _el_set)(sel, attrib, text, tail, nsmap, namespaces)
    elif name is not None:
        if name == "":
            name = path
        sel = el_add(el, cast(str, name), attrib=attrib, text=text, tail=tail, namespaces=namespaces)
    else:
        raise LookupError(f"element not found: {el!r}.find({path!r}) is None")
    return sel


# TODO: 
# el_map：对查找到的元素，运用map操作
# el_move：移动
# el_move_before
# el_move_after
# el_move_up：作为父元素的prev或next
# el_swap：交换位置
# el_sort：对子元素排序
# el_copy：copy.deepcopy(el)
# el_wrap：把查找到的一堆元素，插入作为某个元素的子元素，例如footnote的移动和集中。可能需要对查找到的元素进行二次map、过滤和排序
# el_split：删除某个元素，它的所有子元素替换它原来位置
# el_add_before
# el_add_after

