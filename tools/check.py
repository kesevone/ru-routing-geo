"""Verify built geoip.dat / geosite.dat: every required category present, upper-case code, non-empty.

usage: check.py <geoip.dat> <geosite.dat> <required.txt>
Also prints per-category entry counts and file sizes.
"""
import os, sys


def varint(b, i):
    r = s = 0
    while True:
        x = b[i]; i += 1
        r |= (x & 0x7F) << s; s += 7
        if x < 0x80:
            return r, i


def fields(b):
    i = 0
    while i < len(b):
        key, i = varint(b, i)
        f, wire = key >> 3, key & 7
        if wire == 0:
            v, i = varint(b, i)
        elif wire == 2:
            n, i = varint(b, i); v = b[i:i + n]; i += n
        elif wire == 5:
            v = b[i:i + 4]; i += 4
        elif wire == 1:
            v = b[i:i + 8]; i += 8
        else:
            raise ValueError(f"wire type {wire}")
        yield f, v


def categories(path):
    """Both GeoIPList and GeoSiteList: field 1 = entry; entry field 1 = code, field 2 = repeated items."""
    out = {}
    for f, entry in fields(open(path, "rb").read()):
        if f != 1:
            continue
        code, n = None, 0
        for f2, v in fields(entry):
            if f2 == 1:
                code = v.decode()
            elif f2 == 2:
                n += 1
        out[code] = n
    return out


def main():
    geoip, geosite, req = sys.argv[1:4]
    cats = {"geoip": categories(geoip), "geosite": categories(geosite)}
    for kind, path in (("geoip", geoip), ("geosite", geosite)):
        print(f"{kind}: {os.path.getsize(path)} bytes, {len(cats[kind])} categories")
    bad = []
    for line in open(req, encoding="utf-8"):
        line = line.split("#", 1)[0].strip()
        if not line:
            continue
        kind, name = line.split(":", 1)
        code = name.upper()
        n = cats[kind].get(code)
        lower = name.lower() in cats[kind]
        status = "ok" if n else ("LOWERCASE" if lower else "MISSING") if not n else "ok"
        if not n:
            bad.append(line)
        print(f"  {kind}:{name:18} {status:9} {n or 0}")
    stray = [c for k in cats for c in cats[k] if c != c.upper()]
    if stray:
        print("non-uppercase codes:", stray)
        bad.extend(stray)
    if bad:
        print("FAILED:", bad)
        sys.exit(1)
    print("all required categories present")


if __name__ == "__main__":
    main()
