# Research — san-coverage-plan

Observed 13 October 2026 on live GitHub. Demand is inferred from documented workflows and public issues, not a verified request for this product. Only the first page of each star-sorted problem search was reviewed; this is not an exhaustive global ranking. Broad unrelated results were excluded. Stars are discovery signals, not technical performance evidence.

## User and acceptance

A platform engineer planning certificate name coverage from an exported SAN inventory.

Pain: Map declared DNS/IP SANs to hosts and compute a bounded exact cost plan.

Smallest useful capability and acceptance: Wildcard apex and multilevel hosts stay uncovered; IPv6 equivalents match IP SANs; invalid wildcard/Unicode/numeric-IP inputs fail; an expensive broad certificate loses to the cheaper exact pair; ties and uncovered hosts are deterministic.

## Observed alternatives

| Repository | Stars | Last push (UTC) | Status / detected license |
| --- | ---: | --- | --- |
| [FiloSottile/mkcert](https://github.com/FiloSottile/mkcert) | 59737 | 2024-08-13T13:37:46Z | active repository / BSD-3-Clause |
| [certbot/certbot](https://github.com/certbot/certbot) | 33268 | 2026-10-10T02:14:52Z | active repository / NOASSERTION |
| [go-acme/lego](https://github.com/go-acme/lego) | 9931 | 2026-10-11T11:56:39Z | active repository / MIT |

Query: `certificate`; [GitHub search, Most stars](https://github.com/search?q=certificate&type=repositories&s=stars&o=desc). Exact observed queries, stars and push dates are recorded above. Highest-star relevant result on that page: FiloSottile/mkcert. Other established workflow alternatives were reviewed even if they were not on that first page.

Mkcert creates development certificates and installs a local CA; its cert.go distinguishes DNS and IP SANs. Certbot and Lego obtain ACME certificates and configure or integrate with servers. This tool uses a declared SAN inventory to expose name matches and an exact small cost plan. It performs none of the trust, issuance, expiration or deployment work supplied by those mature tools.

## Differentiation and discovery

Existing DNS/mail tools explain DNS topology, not certificate SAN-to-host set coverage or a bounded exact cost plan. Discover through synthetic certificate rotation inventories and a weighted-plan counterexample.

## Fair comparison boundary

Docs, relevant source and accessible issue collections were inspected. No comparator was installed or timed on equivalent workloads; therefore no install-speed, reliability or performance superiority is claimed. A passing example proves our documented behavior only. No external code was reused; comparator licenses above are API-detected labels, not a legal determination. Support and licensing follow each upstream repository; this alpha offers MIT source and best-effort issue support.
