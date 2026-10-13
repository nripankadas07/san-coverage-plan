"""Explain declared DNS/IP SAN coverage and a bounded exact certificate plan."""
import argparse
import hashlib
import ipaddress
import json
import re
import sys


def dns(value, wildcard=False):
    if not isinstance(value, str) or not value.isascii():
        raise ValueError('DNS names must be ASCII A-labels')
    value = value.lower().removesuffix('.')
    labels = value.split('.')
    if wildcard and labels[0] == '*':
        if len(labels) < 3:
            raise ValueError('wildcard must have at least two suffix labels')
        check = labels[1:]
    else:
        check = labels
    if not value or len(value) > 253 or any(not re.fullmatch(r'[a-z0-9](?:[a-z0-9-]{0,61}[a-z0-9])?', l) for l in check):
        raise ValueError('invalid DNS name or wildcard')
    try:
        ipaddress.ip_address(value)
    except ValueError:
        return value
    raise ValueError('IP addresses require IP SANs, not DNS SANs')


def host(value):
    if not isinstance(value, str):
        raise ValueError('host must be a string')
    try:
        return ('ip', str(ipaddress.ip_address(value)))
    except ValueError:
        return ('dns', dns(value))


def matches(pattern, name):
    if pattern.startswith('*.'):
        return len(name.split('.')) == len(pattern.split('.')) and name.split('.', 1)[1] == pattern[2:]
    return pattern == name


def analyze(data):
    if not isinstance(data, dict) or not isinstance(data.get('hosts'), list) or not isinstance(data.get('certificates'), list):
        raise ValueError('hosts and certificates arrays required')
    if not 1 <= len(data['hosts']) <= 64 or len(data['certificates']) > 16:
        raise ValueError('limit: 1..64 hosts, at most 16 certificates')
    normalized = [host(x) for x in data['hosts']]
    if len(set(normalized)) != len(normalized):
        raise ValueError('duplicate normalized host')
    certificates, seen = [], set()
    for c in data['certificates']:
        if not isinstance(c, dict) or not isinstance(c.get('id'), str) or not c['id'] or c['id'] in seen:
            raise ValueError('certificate ids must be unique nonempty strings')
        seen.add(c['id'])
        cost = c.get('cost', 1)
        if type(cost) is not int or cost < 1:
            raise ValueError('cost must be a positive integer')
        names, ips = c.get('dns', []), c.get('ip', [])
        if not isinstance(names, list) or not isinstance(ips, list) or len(names) + len(ips) > 1000:
            raise ValueError('SAN arrays required; at most 1000 entries')
        patterns = sorted({dns(n, wildcard=True) for n in names})
        if any(not isinstance(n, str) for n in ips):
            raise ValueError('IP SANs must be address strings')
        addresses = sorted({str(ipaddress.ip_address(n)) for n in ips})
        evidence, mask = [], 0
        for index, (kind, name) in enumerate(normalized):
            witnesses = [p for p in patterns if matches(p, name)] if kind == 'dns' else ([name] if name in addresses else [])
            if witnesses:
                mask |= 1 << index
            evidence.append(witnesses)
        certificates.append({'id': c['id'], 'cost': cost, 'mask': mask, 'evidence': evidence})
    certificates.sort(key=lambda x: x['id'])
    union = 0
    for c in certificates:
        union |= c['mask']
    best = None
    for subset in range(1 << len(certificates)):
        coverage, cost, ids = 0, 0, []
        for i, c in enumerate(certificates):
            if subset & (1 << i):
                coverage |= c['mask']
                cost += c['cost']
                ids.append(c['id'])
        if coverage == union:
            score = (cost, len(ids), ids)
            if best is None or score < best:
                best = score
    rows = []
    for i, (kind, name) in enumerate(normalized):
        rows.append({'host': name, 'kind': kind, 'covered_by': [{'certificate': c['id'], 'sans': c['evidence'][i]} for c in certificates if c['evidence'][i]]})
    digest = hashlib.sha256(json.dumps(data, sort_keys=True).encode()).hexdigest()
    return {'schema': 'san-coverage-plan/v1', 'input_sha256': digest, 'hosts': rows, 'uncovered': [r['host'] for r in rows if not r['covered_by']],
            'plan': {'certificate_ids': best[2], 'cost': best[0], 'objective': 'minimum declared cost, then count, then lexicographic ids, covering all coverable hosts'},
            'limits': 'Declared SAN inventory only; no PEM parsing, signature/chain/expiry/revocation/TLS checks or issuance. ASCII names, exact IP SAN, full leftmost wildcard only. No IDNA conversion or public-suffix policy.'}


def main():
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument('input')
    args = p.parse_args()
    try:
        with open(args.input, encoding='utf-8') as f:
            result = analyze(json.load(f))
        print(json.dumps(result, indent=2, sort_keys=True))
        return 1 if result['uncovered'] else 0
    except (ValueError, TypeError, KeyError, OSError) as error:
        print('error: ' + str(error), file=sys.stderr)
        return 2


if __name__ == '__main__':
    raise SystemExit(main())
