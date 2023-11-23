import re
from pathlib import Path

from sphinx.cmd.build import make_main

from sphinx_emoji_favicon import _get_twemoji_latest_version

_conf_original = """
emoji_favicon = ":unicorn:"
"""
_conf_with_cdn_1 = """
emoji_favicon = {
    "emoji": ":独角兽:",
    "twemoji_cdn": "https://twemoji.maxcdn.com/2/",
}
"""
_conf_with_cdn_2 = """
emoji_favicon = {
    "emoji": ":独角兽:",
    "twemoji_cdn": "https://cdnjs.cloudflare.com/ajax/libs/twemoji/13.1.0/svg/",
}
"""
_conf_with_svg_assets = """
emoji_favicon = {
    "emoji": ":unicorn:",
    "twemoji_assets_type": "svg",
}
"""
_conf_with_lang = """
emoji_favicon = {
    "emoji": ":lion:",
    "language": "fr",
}
"""


def test_build():
    """Test building the docs."""

    test_project_dir = Path(__file__).parent / "sample_project"
    src_dir = test_project_dir / "source"
    build_dir = test_project_dir / "build"

    conf_bak = (src_dir / "conf.py").read_text()

    alternative_emoji_favicons = [
        _conf_original,
        _conf_with_cdn_1,
        _conf_with_cdn_2,
        _conf_with_svg_assets,
        _conf_with_lang,
    ]

    for alternative_emoji_favicon in alternative_emoji_favicons:
        new_conf = conf_bak.replace(_conf_original, alternative_emoji_favicon)
        (src_dir / "conf.py").write_text(new_conf)

        # first, clean the build directory
        make_main(["-M", "clean", str(src_dir), str(build_dir)])

        # then, build the docs
        make_main(["-M", "html", str(src_dir), str(build_dir)])
        # check that the favicon is correctly added to the HTML pages
        pages = Path(build_dir / "html").glob("*.html")
        assert (build_dir / "html" / "index.html").exists()
        for page in pages:
            if page.name in ["search.html", "genindex.html"]:
                continue
            page_content = page.read_text()
            assert re.search(r'<link id="favicon" rel="icon" type="image/(png|svg\+xml)" href=".+">', page_content)
            if alternative_emoji_favicon == _conf_with_cdn_1:
                latest_version = _get_twemoji_latest_version()
                assert (
                    f'<link id="favicon" rel="icon" type="image/png" href="https://twemoji.maxcdn.com/2/{latest_version}/72x72/1f984.png">'
                    in page_content
                )
            elif alternative_emoji_favicon == _conf_with_cdn_2:
                assert (
                    '<link id="favicon" rel="icon" type="image/svg+xml" href="https://cdnjs.cloudflare.com/ajax/libs/twemoji/13.1.0/svg/1f984.svg">'
                    in page_content
                )

        # execute "make clean" to remove the build files
        make_main(["-M", "clean", str(src_dir), str(build_dir)])

    # restore the original conf.py
    (src_dir / "conf.py").write_text(conf_bak)
