"""Sphinx extension to add emoji favicons.
"""

import posixpath
import re
from typing import Any, Dict, Optional

import docutils.nodes as nodes
import requests
from emoji.unicode_codes.data_dict import EMOJI_DATA, LANGUAGES
from sphinx.application import Sphinx
from sphinx.util import logging

logger = logging.getLogger(__name__)


version = "0.2"


# constants
_defalut_twemoji_latest_version = "14.0.2"
_str2emoji = {}
_str2emoji_lang = {lang: {} for lang in LANGUAGES}
for k, v in EMOJI_DATA.items():
    if "status" in v and v["status"] > 2:
        # https://carpedm20.github.io/emoji/docs/api.html#emoji-status
        # 1: component, 2: fully-qualified, 3: minimally-qualified, 4: unqualified
        continue
    if "E" in v and str(v["E"]) > _defalut_twemoji_latest_version:
        # skip emoji with newer version than twemoji latest version
        continue
    # limit to unicode emoji with length <= 2
    # longer emoji strings are usually composed of multiple unicode emoji
    if len(k) > 2:
        continue
    for key, s in v.items():
        if key in ["status", "E", "variant"]:
            # "E" for Emoji version: https://carpedm20.github.io/emoji/docs/api.html#emoji-version
            continue
        if key == "alias":
            for alias in s:
                if alias not in _str2emoji:
                    # alias might coincide with other emoji strings,
                    # e.g. ":Japanese_post_office:" has alias ":post_office:",
                    # but ":post_office:" is itself an emoji string in "en" language
                    _str2emoji[alias] = k
        else:
            _str2emoji[s] = k
            _str2emoji_lang[key][s] = k
emoji_strs = set(_str2emoji.keys())
emoji_unicodes = set(_str2emoji.values())


def _url_is_reachable(url: str, timeout: float = 0.8) -> bool:
    """Check if a URL is reachable.

    Parameters
    ----------
    url : str
        The URL.
    timeout : float, optional
        The timeout in seconds, by default 0.8.

    Returns
    -------
    bool
        Whether the URL is reachable.

    """
    try:
        r = requests.head(url, timeout=timeout)
        return r.status_code == 200
    except Exception:
        return False


def _get_twemoji_latest_version() -> str:
    """Get the latest twemoji version.

    Returns
    -------
    str
        The latest twemoji version.

    """
    url = "https://unpkg.com/twemoji@latest/dist/twemoji.min.js"
    try:
        r = requests.get(url, timeout=3)
        if r.status_code == 200:
            # search for the version number in r.url
            # which will be redirected to the latest version with version number
            # e.g. https://unpkg.com/twemoji@14.0.2/dist/twemoji.min.js
            return re.search("twemoji@([\\w\\.\\-]+)", r.url).group(1)
        else:
            return _defalut_twemoji_latest_version
    except Exception:
        return _defalut_twemoji_latest_version


def _get_twemoji_config(twemoji_assets_type: str = "72x72", twemoji_cdn: Optional[str] = None, **kwargs: Any) -> Dict[str, Any]:
    """Get the twemoji configuration.

    Parameters
    ----------
    twemoji_assets_type : {"svg", "72x72"}, optional
        The twemoji assets type, by default "72x72".
    twemoji_cdn : Optional[str], optional
        The twemoji cdn, by default None.
    **kwargs : Any
        Other keyword arguments.

    Returns
    -------
    Dict[str, Any]
        The twemoji configuration.

    """
    # twemoji_version = "14.0.2"
    twemoji_version = _get_twemoji_latest_version()
    twemoji_assets_ext = {"svg": "svg", "72x72": "png"}[twemoji_assets_type]
    twemoji_image_type = {"svg": "image/svg+xml", "72x72": "image/png"}[twemoji_assets_type]
    twemoji_cdn_cadidates = [
        f"https://cdnjs.cloudflare.com/ajax/libs/twemoji/{twemoji_version}/{twemoji_assets_type}/",  # cdnjs
        f"https://cdn.jsdelivr.net/gh/twitter/twemoji@{twemoji_version}/assets/{twemoji_assets_type}/",  # jsdelivr
        f"https://cdn.staticfile.org/twemoji/{twemoji_version}/{twemoji_assets_type}/",  # 七牛云
        f"https://cdn.bootcdn.net/ajax/libs/twemoji/{twemoji_version}/{twemoji_assets_type}/",  # bootcdn
    ]
    if twemoji_cdn is not None:
        # twemoji_cdn_cadidates.insert(0, twemoji_cdn)
        twemoji_base_url = twemoji_cdn
        if not re.search("(\\d+\\.\\d+\\.\\d+)|latest", twemoji_base_url):
            twemoji_base_url = posixpath.join(twemoji_base_url, twemoji_version)
        if not re.search("svg|72x72", twemoji_base_url):
            twemoji_base_url = posixpath.join(twemoji_base_url, twemoji_assets_type)
        else:
            # override default twemoji_assets_type and twemoji_assets_ext
            twemoji_assets_type = re.search("svg|72x72", twemoji_base_url).group(0)
            twemoji_assets_ext = {"svg": "svg", "72x72": "png"}[twemoji_assets_type]
            twemoji_image_type = {"svg": "image/svg+xml", "72x72": "image/png"}[twemoji_assets_type]
    else:
        test_emoji_code_point = "1f40d"  # snake
        twemoji_base_url = twemoji_cdn_cadidates[0]  # by default, use cdnjs
        for _twemoji_cdn in twemoji_cdn_cadidates[1:]:
            if _url_is_reachable(f"{_twemoji_cdn}{test_emoji_code_point}.{twemoji_assets_ext}", timeout=0.8):
                twemoji_base_url = _twemoji_cdn
                break

    twemoji_config = {
        "version": twemoji_version,
        "assets_type": twemoji_assets_type,
        "assets_ext": twemoji_assets_ext,
        "image_type": twemoji_image_type,
        "base_url": twemoji_base_url,
    }
    twemoji_config.update(kwargs)

    return twemoji_config


_twemoji_config = _get_twemoji_config()


def _to_code_point(unicode_surrogates: str, sep: str = "-") -> str:
    """Convert a unicode surrogate to a code point to be used in a twemoji url.

    Converted from the following JavaScript code:

    https://github.com/streamlit/streamlit/blob/develop/frontend/lib/src/vendor/twemoji.ts#L7-L24

    https://unpkg.com/twemoji@14.0.2/dist/twemoji.min.js

    Parameters
    ----------
    unicode_surrogates : str
        A unicode surrogate.
    sep : str, optional
        The separator between code points, by default "-".

    Returns
    -------
    str
        The code point.

    """
    r = []
    c, p, i = 0, 0, 0
    while i < len(unicode_surrogates):
        c = ord(unicode_surrogates[i])
        i += 1
        if p:
            r.append(hex(0x10000 + ((p - 0xD800) << 10) + (c - 0xDC00))[2:])
            p = 0
        elif 0xD800 <= c <= 0xDBFF:
            p = c
        else:
            r.append(hex(c)[2:])
    return sep.join(r)


def _to_twemoji_url(unicode_surrogates: str) -> str:
    """Convert a unicode surrogate to a twemoji url.

    Parameters
    ----------
    unicode_surrogates : str
        A unicode surrogate.

    Returns
    -------
    str
        The twemoji url.

    """
    code_point = _to_code_point(unicode_surrogates)
    filename = f"""{code_point}.{_twemoji_config["assets_ext"]}"""
    return posixpath.join(_twemoji_config["base_url"], filename)


def create_emoji_favicon_meta(emoji_str_or_unicode: str, emoji_language: Optional[str] = None) -> str:
    """Create a favicon meta tag for a given emoji string.

    Parameters
    ----------
    emoji_str_or_unicode : str
        The emoji string or unicode surrogate.
        For example, ":snake:", ":蛇:", ":serpent:" or "🐍" or "\U0001f40d".

    Returns
    -------
    str
        The favicon meta tag.

    """
    emoji_str_or_unicode = emoji_str_or_unicode.replace("\U0000FE0F", "")
    if emoji_language is not None:
        emoji_unicode_surrogates = _str2emoji_lang[emoji_language].get(emoji_str_or_unicode, emoji_str_or_unicode)
    else:
        emoji_unicode_surrogates = _str2emoji.get(emoji_str_or_unicode, emoji_str_or_unicode)
    emoji_unicode_surrogates = emoji_unicode_surrogates.replace("\U0000FE0F", "")
    image_type = _twemoji_config["image_type"]
    twemoji_url = _to_twemoji_url(emoji_unicode_surrogates)
    return f"""<link id="favicon" rel="icon" type="{image_type}" href="{twemoji_url}">"""


def html_page_context(
    app: Sphinx,
    pagename: str,
    templatename: str,
    context: Dict[str, Any],
    doctree: nodes.document,
) -> None:
    """Update the html page context by adding the emoji favicons.

    Parameters
    ----------
    app : Sphinx
        The Sphinx application.
    pagename : str
        The name of the page.
    templatename : str
        The name of the template.
    context : Dict[str, Any]
        The context of the html page.
    doctree : nodes.document
        The document tree.

    Returns
    -------
    None
        The context is updated in-place.

    """
    global _twemoji_config
    # extract parameters from app
    emoji_favicon = app.config["emoji_favicon"]  # str or dict or None

    # if "favicons" from sphinx_favicon is set, raise warning and abort
    if hasattr(app.config, "favicons") and app.config["favicons"] is not None:
        logger.warning(
            "sphinx_emoji_favicon is incompatible with sphinx_favicon. "
            "To avoid conflict, sphinx_emoji_favicon will not be used. "
            "Or one can remove sphinx_favicon from conf.py to use sphinx_emoji_favicon."
        )
        return

    if not (doctree and emoji_favicon):
        return

    if isinstance(emoji_favicon, dict):
        if "emoji" not in emoji_favicon:
            logger.error(f"Invalid emoji config: {emoji_favicon}")
            return
        # update twemoji config
        _twemoji_config = _get_twemoji_config(
            twemoji_assets_type=emoji_favicon.get("twemoji_assets_type", "72x72"),
            twemoji_cdn=emoji_favicon.get("twemoji_cdn", None),
            language=emoji_favicon.get("language", None),
        )
        emoji_favicon = emoji_favicon["emoji"]

    emoji_favicon_meta = create_emoji_favicon_meta(emoji_favicon, emoji_language=_twemoji_config.get("language", None))
    if emoji_favicon_meta != "":
        if "metatags" not in context:
            context["metatags"] = ""
        context["metatags"] += emoji_favicon_meta


def setup(app: Sphinx) -> Dict[str, Any]:
    """Add custom configuration to sphinx app.

    Parameters
    ----------
    app : Sphinx
        The Sphinx application.

    Returns
    -------
    Dict[str, Any]
        The custom configuration.

    """
    app.add_config_value("emoji_favicon", None, "html")
    app.connect("html-page-context", html_page_context)

    return {
        "parallel_read_safe": True,
        "parallel_write_safe": True,
    }
