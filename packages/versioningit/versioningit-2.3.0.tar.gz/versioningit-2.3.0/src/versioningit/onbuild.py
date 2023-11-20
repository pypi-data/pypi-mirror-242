from __future__ import annotations
from pathlib import Path
import re
from typing import Any
from .errors import ConfigError
from .logging import log, warn_extra_fields
from .util import bool_guard, ensure_terminated, optional_str_guard, str_guard


def replace_version_onbuild(
    *,
    build_dir: str | Path,
    is_source: bool,
    template_fields: dict[str, Any],
    params: dict[str, Any],
) -> None:
    """Implements the ``"replace-version"`` ``onbuild`` method"""

    DEFAULT_REGEX = r"^\s*__version__\s*=\s*(?P<version>.*)"
    DEFAULT_REPLACEMENT = '"{version}"'

    params = params.copy()
    source_file = str_guard(params.pop("source-file", None), "onbuild.source-file")
    build_file = str_guard(params.pop("build-file", None), "onbuild.build-file")
    encoding = str_guard(params.pop("encoding", "utf-8"), "onbuild.encoding")
    regex = str_guard(params.pop("regex", DEFAULT_REGEX), "onbuild.regex")
    try:
        rgx = re.compile(regex)
    except re.error as e:
        raise ConfigError(f"versioningit: onbuild.regex: Invalid regex: {e}")
    require_match = bool_guard(
        params.pop("require-match", False), "onbuild.require-match"
    )
    replacement = str_guard(
        params.pop("replacement", DEFAULT_REPLACEMENT),
        "onbuild.replacement",
    )
    append_line = optional_str_guard(
        params.pop("append-line", None), "onbuild.append-line"
    )
    warn_extra_fields(
        params,
        "onbuild",
        [
            "source-file",
            "build-file",
            "encoding",
            "regex",
            "require-match",
            "replacement",
            "append-line",
        ],
    )

    path = Path(build_dir, source_file if is_source else build_file)
    log.info("Updating version in file %s", path)
    lines = path.read_text(encoding=encoding).splitlines(keepends=True)
    for i, ln in enumerate(lines):
        m = rgx.search(ln)
        if m:
            log.debug("onbuild.regex matched file on line %d", i + 1)
            vgroup: str | int
            if "version" in m.groupdict():
                vgroup = "version"
            else:
                vgroup = 0
            if m[vgroup] is None:
                raise RuntimeError(
                    "'version' group in versioningit's onbuild.regex did"
                    " not participate in match"
                )
            newline = ensure_terminated(
                ln[: m.start(vgroup)]
                + m.expand(replacement.format_map(template_fields))
                + ln[m.end(vgroup) :]
            )
            log.debug("Replacing line %r with %r", ln, newline)
            lines[i] = newline
            break
    else:
        if require_match:
            raise RuntimeError(f"onbuild.regex did not match any lines in {path}")
        elif append_line is not None:
            log.info(
                "onbuild.regex did not match any lines in the file; appending line"
            )
            if lines:
                lines[-1] = ensure_terminated(lines[-1])
            lines.append(ensure_terminated(append_line.format_map(template_fields)))
        else:
            log.info(
                "onbuild.regex did not match any lines in the file; leaving unmodified"
            )
            return
    path.unlink()  # In case of hard links
    path.write_text("".join(lines), encoding=encoding)
