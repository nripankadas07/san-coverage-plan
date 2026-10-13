import unittest
from san_coverage_plan import analyze, dns, matches


def c(name,names,cost=1,ips=None):return {'id':name,'dns':names,'ip':ips or [],'cost':cost}
def run(hosts,certs):return analyze({'hosts':hosts,'certificates':certs})


class Tests(unittest.TestCase):
    def test_exact_case_and_trailing_dot(self):
        self.assertEqual(run(['API.Example.com.'],[c('one',['api.example.com'])])['uncovered'],[])
    def test_wildcard_one_label_only(self):
        r=run(['api.example.com','example.com','a.api.example.com'],[c('one',['*.example.com'])]);self.assertEqual(r['uncovered'],['example.com','a.api.example.com'])
    def test_ip_requires_ip_san_and_normalizes_ipv6(self):
        r=run(['2001:db8::1','192.0.2.1'],[c('one',[],ips=['2001:0db8::1'])]);self.assertEqual(r['uncovered'],['192.0.2.1'])
        with self.assertRaises(ValueError):run(['192.0.2.1'],[c('bad',['192.0.2.1'])])
    def test_partial_wildcards_and_unicode_rejected(self):
        for x in ['a*.example.com','*.*.example.com','é.example.com','-bad.example.com']:
            with self.subTest(x=x),self.assertRaises(ValueError):dns(x,True)
    def test_exact_weighted_plan_beats_single_greedy_choice(self):
        r=run(['a.example.com','b.example.com','c.example.com'],[c('broad',['*.example.com'],8),c('ab',['a.example.com','b.example.com'],2),c('bc',['b.example.com','c.example.com'],2)])
        self.assertEqual(r['plan']['certificate_ids'],['ab','bc']);self.assertEqual(r['plan']['cost'],4)
    def test_equal_cost_prefers_fewer_then_ids(self):
        r=run(['a.example.com','b.example.com'],[c('a',['*.example.com'],2),c('b',['*.example.com'],2),c('c',['a.example.com']),c('d',['b.example.com'])]);self.assertEqual(r['plan']['certificate_ids'],['a'])
    def test_uncovered_not_hidden_by_partial_plan(self):
        r=run(['a.example.com','other.example.net'],[c('x',['a.example.com'])]);self.assertEqual(r['plan']['certificate_ids'],['x']);self.assertEqual(r['uncovered'],['other.example.net'])
    def test_empty_certificates(self):
        r=run(['a.example.com'],[]);self.assertEqual(r['plan']['cost'],0);self.assertEqual(r['uncovered'],['a.example.com'])
    def test_duplicate_hosts_ids_and_invalid_cost(self):
        with self.assertRaises(ValueError):run(['a.example.com','A.example.com'],[])
        with self.assertRaises(ValueError):run(['a.example.com'],[c('same',[]),c('same',[])])
        for cost in [0,-1,True,1.5]:
            with self.subTest(cost=cost),self.assertRaises(ValueError):run(['a.example.com'],[c('x',[],cost)])
    def test_nonstring_ip_no_numeric_coercion(self):
        with self.assertRaises(ValueError):run(['a.example.com'],[c('x',[],ips=[1])])
    def test_limits(self):
        with self.assertRaises(ValueError):run([],[])
        with self.assertRaises(ValueError):run(['a.example.com'],[c(str(i),[]) for i in range(17)])
    def test_all_matching_sans_exposed(self):
        r=run(['api.example.com'],[c('x',['*.example.com','api.example.com'])]);self.assertEqual(r['hosts'][0]['covered_by'][0]['sans'],['*.example.com','api.example.com'])


if __name__=='__main__':unittest.main()
