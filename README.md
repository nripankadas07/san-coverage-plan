# san-coverage-plan

Map declared DNS/IP SANs to hosts and compute a bounded exact cost plan.

**Alpha, offline diagnostic.** Built for a platform engineer planning certificate name coverage from an exported SAN inventory.
Original implementation with AI assistance; no competitor code or prose copied.
No production impact, adoption or performance advantage is claimed.

## Install and get a useful result

Python 3.10+. Clone this repository, then:

```bash
python -m venv .venv
. .venv/bin/activate
python -m pip install .
san-coverage-plan example.json
```

The bundled fixture is synthetic. `example.py` only creates its own temporary
fixture when present. Exit 0 means a report was produced with no CLI-level failure;
exit 1 explicitly reports hazards/uncovered hosts; exit 2 reports invalid or unsupported input.
Read the report limits before taking action.

## Input

`san-coverage-plan inventory.json` accepts `hosts` and `certificates` arrays;
see [the fixture](example.json). Each certificate has unique `id`, optional
positive integer `cost` (default 1), and string arrays `dns` and `ip`. Copy SAN
identities from your trusted certificate inventory; this tool cannot authenticate
that declaration. `hosts[].covered_by` contains every matching certificate/SAN.
The plan covers all coverable hosts, and `uncovered` remains explicit; exit 1
means some hosts are uncovered. Declared cost is your planning weight, not price
or cryptographic quality.

## Capability and limits

Declared SAN inventory only: 1..64 unique normalized hosts, at most 16 certificates and 1,000 SANs per certificate. ASCII A-label DNS names only; case-insensitive with one trailing dot removed. Exact IP SAN matching after address normalization; DNS SANs containing an IP are rejected. Full leftmost wildcard matches one label and requires at least two suffix labels. No IDNA conversion or public-suffix policy. Exact enumeration minimizes positive declared integer cost, then certificate count, then IDs, covering all coverable hosts; uncovered hosts remain explicit. No PEM parsing, trust-chain/signature/expiry/revocation checks, TLS connection, issuance or deployment.

## Acceptance criteria

Wildcard apex and multilevel hosts stay uncovered; IPv6 equivalents match IP SANs; invalid wildcard/Unicode/numeric-IP inputs fail; an expensive broad certificate loses to the cheaper exact pair; ties and uncovered hosts are deterministic.

## Checks and evidence

```bash
python -m unittest -v
python -m compileall -q .
```

[Validation](VALIDATION.md) documents the prepared checks and failure cases.
[Research and alternatives](RESEARCH.md) records dated observations, competing
workflows and a bounded inferred need. The [CI workflow](.github/workflows/test.yml)
builds wheels and tests installed commands outside the checkout on Linux Python
3.10/3.12/3.14. Check the actual current Actions result before relying on it.

[Contributing](CONTRIBUTING.md) · [Support](SUPPORT.md) ·
[Security](SECURITY.md) · [MIT license](LICENSE)
