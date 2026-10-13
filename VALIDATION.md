# Prepared validation — 13 October 2026

Acceptance contract: Wildcard apex and multilevel hosts stay uncovered; IPv6 equivalents match IP SANs; invalid wildcard/Unicode/numeric-IP inputs fail; an expensive broad certificate loses to the cheaper exact pair; ties and uncovered hosts are deterministic.

12 meaningful unit/integration tests pass in the cloud preparation environment.
The real compiler bytecode check passes. Wheel build, fresh virtual-environment install, installed example and malformed-input
failure checks passed outside the source tree. Preparation: Python 3.12.14, Linux
x86_64 glibc 2.39, Git 2.51.1 for Git fixtures. Remote Linux Python 3.10/3.12/3.14
CI remains required before LIVE; inspect current Actions and the portfolio ledger. Tests do not establish behavior outside the explicit README limits.
No runtime third-party dependencies. The setuptools build requirement is audited
separately in the portfolio dependency workflow. No technical performance benchmark
or comparator superiority is claimed.
