# ru-routing-geo

Compact `geoip.dat` / `geosite.dat` for Xray clients in Russia, rebuilt daily.

Download (latest):

- `https://cdn.jsdelivr.net/gh/kesevone/ru-routing-geo@release/geoip.dat`
- `https://cdn.jsdelivr.net/gh/kesevone/ru-routing-geo@release/geosite.dat`

SHA-256 next to each file (`*.sha256`). Every build is also a GitHub Release.

## Categories

**geoip**

| code | content |
|---|---|
| `ru` | Russian address space (RIR data via ipverse), IPv4 and IPv6 |
| `direct` | `ru` + roscomvpn `DIRECT` + `geoip/extra/direct.txt`, minus Re:filter ipsum |
| `whitelist` | Russian mobile whitelist: roscomvpn `WHITELIST` + hxehex + escapingworm |
| `private` | private and reserved ranges |

**geosite** — every roscomvpn-geosite category, with the ones listed in
`geosite/build.py` refreshed from v2fly/domain-list-community (includes flattened)
and `whitelist` extended with hxehex mobile-whitelist domains. Local additions go to
`geosite/extra/<category>`.

A build fails and nothing is published if any category from `required.txt` is missing,
empty or not upper-case, or if Xray cannot load a config that references all of them.

## Sources

- [hydraponique/roscomvpn-geoip](https://github.com/hydraponique/roscomvpn-geoip), [roscomvpn-geosite](https://github.com/hydraponique/roscomvpn-geosite)
- [ipverse/country-ip-blocks](https://github.com/ipverse/country-ip-blocks) (CC0)
- [v2fly/domain-list-community](https://github.com/v2fly/domain-list-community) (MIT)
- [hxehex/russia-mobile-internet-whitelist](https://github.com/hxehex/russia-mobile-internet-whitelist) (MIT)
- [escapingworm/russia-whitelist](https://github.com/escapingworm/russia-whitelist) (MIT)
- [1andrevich/Re-filter-lists](https://github.com/1andrevich/Re-filter-lists) (MIT)

Built with [Loyalsoldier/geoip](https://github.com/Loyalsoldier/geoip) and the
v2fly domain-list-community builder.
