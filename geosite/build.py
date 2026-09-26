"""Assemble the geosite data directory for the v2fly builder.

Base: every category of hydraponique/roscomvpn-geosite (keeps client configs compatible).
Refresh: categories below get the flattened content of the same (or listed) v2fly
domain-list-community files appended. Whitelist gets hxehex mobile-whitelist domains.
Our own additions live in geosite/extra/<category>.

usage: build.py <roscom-data-dir> <v2fly-data-dir> <hxehex-whitelist.txt> <extra-dir> <out-dir>
"""
import os, re, sys, shutil

# our category -> v2fly files merged into it
FROM_V2FLY = {
    "category-ru": ["category-ru", "category-gov-ru", "category-bank-ru"],
    "youtube": ["youtube"],
    "telegram": ["telegram"],
    "github": ["github"],
    "google-play": ["google-play"],
    "microsoft": ["microsoft"],
    "apple": ["apple"],
    "steam": ["steam"],
    "epicgames": ["epicgames"],
    "riot": ["riot"],
    "twitch": ["twitch"],
    "pinterest": ["pinterest"],
    "origin": ["ea"],
    "faceit": ["faceit"],
    "escapefromtarkov": ["escapefromtarkov"],
    "private": ["private"],
    # category-ads is referenced by block rules in every client config; v2fly's
    # flattened list is ~10k domains, too heavy for the iOS network extension.
}

INCLUDE = re.compile(r"^include:([A-Za-z0-9!\-_.]+)")


def read_lines(path):
    with open(path, encoding="utf-8") as f:
        for raw in f:
            line = raw.split("#", 1)[0].strip()
            if line:
                yield line


def flatten(v2dir, name, seen=None):
    """Return v2fly rules of `name` with include: resolved recursively (attribute filters on include are ignored)."""
    seen = seen if seen is not None else set()
    if name in seen:
        return []
    seen.add(name)
    path = os.path.join(v2dir, name)
    if not os.path.isfile(path):
        print(f"  ! v2fly has no '{name}'", file=sys.stderr)
        return []
    out = []
    for line in read_lines(path):
        m = INCLUDE.match(line)
        if m:
            out.extend(flatten(v2dir, m.group(1), seen))
        else:
            out.append(line)
    return out


def append_unique(path, lines):
    have = set(read_lines(path)) if os.path.isfile(path) else set()
    new = [l for l in lines if l not in have and not have.add(l)]
    if new:
        with open(path, "a", encoding="utf-8") as f:
            f.write("\n" + "\n".join(new) + "\n")
    return len(new)


def main():
    roscom, v2fly, hxehex, extra, out = sys.argv[1:6]
    shutil.rmtree(out, ignore_errors=True)
    shutil.copytree(roscom, out)
    print(f"base: {len(os.listdir(out))} roscomvpn categories")

    for cat, sources in FROM_V2FLY.items():
        lines = []
        for src in sources:
            lines.extend(flatten(v2fly, src))
        n = append_unique(os.path.join(out, cat), lines)
        print(f"  {cat:18} +{n} from v2fly {sources}")

    wl = [l for l in read_lines(hxehex) if re.match(r"^[A-Za-z0-9.\-_*]+$", l)]
    wl = [l.lstrip("*.") for l in wl]
    print(f"  {'whitelist':18} +{append_unique(os.path.join(out, 'whitelist'), wl)} from hxehex")

    if os.path.isdir(extra):
        for cat in sorted(c for c in os.listdir(extra) if not c.startswith(".")):
            n =append_unique(os.path.join(out, cat), list(read_lines(os.path.join(extra, cat))))
            print(f"  {cat:18} +{n} from extra/")

    for cat in sorted(os.listdir(out)):
        print(f"  = {cat:18} {sum(1 for _ in read_lines(os.path.join(out, cat)))} rules")


if __name__ == "__main__":
    main()
