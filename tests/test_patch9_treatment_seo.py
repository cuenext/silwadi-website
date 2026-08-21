from pathlib import Path
import json
import re
import unittest
import xml.etree.ElementTree as ET

ROOT = Path(__file__).resolve().parents[1]

PRIMARY = {
    'treatments/dental-implants.html': {'title_term': 'Dental Implants in Abu Dhabi','h1': 'Dental Implants in Abu Dhabi','service_term': 'implant'},
    'treatments/orthodontics.html': {'title_term': 'Orthodontist & Braces in Abu Dhabi','h1': 'Orthodontics in Abu Dhabi','service_term': 'orthodont'},
    'treatments/cosmetic-dentistry.html': {'title_term': 'Cosmetic Dentistry in Abu Dhabi','h1': 'Cosmetic Dentistry in Abu Dhabi','service_term': 'cosmetic'},
    'treatments/general-dentistry.html': {'title_term': 'General Dentist in Abu Dhabi','h1': 'General Dentistry in Abu Dhabi','service_term': 'general'},
    'treatments/emergency-dentist.html': {'title_term': 'Emergency Dentist in Abu Dhabi','h1': 'Emergency Dentist in Abu Dhabi','service_term': 'emergency'},
}
BANNED = ['best dentist', 'world-class', 'cutting-edge', 'state-of-the-art', 'guaranteed', 'pain-free']

def read(rel): return (ROOT / rel).read_text(encoding='utf-8')
def jsonld_nodes(rel):
    html=read(rel); blocks=re.findall(r'<script\s+type="application/ld\+json"[^>]*>(.*?)</script>',html,re.I|re.S); nodes=[]
    for block in blocks:
        parsed=json.loads(block); nodes.extend(parsed['@graph'] if isinstance(parsed,dict) and isinstance(parsed.get('@graph'),list) else [parsed])
    return nodes

class PatchNineTreatmentSEO(unittest.TestCase):
    def test_primary_pages_exist_with_unique_search_metadata(self):
        titles=[]; descriptions=[]
        for rel,cfg in PRIMARY.items():
            path=ROOT/rel; self.assertTrue(path.is_file(),rel); html=path.read_text(encoding='utf-8'); title=re.search(r'<title>(.*?)</title>',html,re.I|re.S); desc=re.search(r'<meta\s+name="description"\s+content="([^"]+)"',html,re.I); h1s=re.findall(r'<h1[^>]*>(.*?)</h1>',html,re.I|re.S)
            self.assertIsNotNone(title,rel); self.assertIsNotNone(desc,rel); self.assertIn(cfg['title_term'],title.group(1),rel); self.assertEqual(len(h1s),1,rel); self.assertEqual(re.sub(r'<[^>]+>','',h1s[0]).strip(),cfg['h1'],rel); canonical=f"https://silwadi.ae/{rel}"; self.assertIn(f'<link rel="canonical" href="{canonical}">',html,rel); self.assertIn(f'<meta property="og:url" content="{canonical}">',html,rel); self.assertIn('Abu Dhabi',html,rel); self.assertIn('Bani Yas Tower',html,rel); self.assertIn('tel:+97126262042',html,rel); self.assertRegex(html,r'href="\.\./contact\.html#consultation|href="contact\.html#consultation',rel)
            for phrase in BANNED: self.assertNotIn(phrase,html.lower(),(rel,phrase))
            titles.append(title.group(1).strip()); descriptions.append(desc.group(1).strip())
        self.assertEqual(len(titles),len(set(titles))); self.assertEqual(len(descriptions),len(set(descriptions)))
    def test_pages_have_breadcrumb_and_service_schema(self):
        for rel,cfg in PRIMARY.items():
            nodes=jsonld_nodes(rel); crumbs=[n for n in nodes if n.get('@type')=='BreadcrumbList']; services=[n for n in nodes if n.get('@type')=='Service']; self.assertEqual(len(crumbs),1,rel); self.assertEqual(len(services),1,rel); items=crumbs[0]['itemListElement']; self.assertEqual(len(items),3,rel); self.assertEqual([i['position'] for i in items],[1,2,3],rel); self.assertEqual(items[0]['item'],'https://silwadi.ae/',rel); self.assertEqual(items[1]['item'],'https://silwadi.ae/treatments.html',rel); self.assertEqual(items[2]['item'],f'https://silwadi.ae/{rel}',rel); service=services[0]; self.assertIn(cfg['service_term'],service['serviceType'].lower(),rel); self.assertEqual(service['url'],f'https://silwadi.ae/{rel}',rel); self.assertEqual(service['provider']['@id'],'https://silwadi.ae/#dentist',rel); self.assertEqual(service['areaServed']['name'],'Abu Dhabi',rel); serialized=json.dumps(service).lower(); self.assertNotIn('aggregaterating',serialized,rel); self.assertNotIn('review',serialized,rel)
    def test_faq_content_is_compact(self):
        for rel in PRIMARY:
            count=read(rel).count('data-faq-item'); self.assertGreaterEqual(count,2,rel); self.assertLessEqual(count,4,rel)
    def test_orthodontics_has_braces_clear_aligners_and_verified_team(self):
        html=read('treatments/orthodontics.html'); lower=html.lower(); self.assertIn('braces',lower); self.assertIn('clear aligners',lower)
        for name in ['Dr. Hani Hasbini','Dr. Moammer Rifai','Dr. Krishnamurthy Katta Balajee']: self.assertIn(name,html)
        self.assertIn('../doctors.html',html)
    def test_implants_routes_to_munir_profile(self):
        html=read('treatments/dental-implants.html'); self.assertIn('../doctors/dr-munir-silwadi.html',html); self.assertIn('Dr. Munir Silwadi',html)
    def test_emergency_page_has_safe_escalation_and_no_24_7_promise(self):
        html=read('treatments/emergency-dentist.html'); lower=html.lower()
        for cue in ['breathing','swallowing','uncontrolled bleeding','major facial trauma','emergency medical care']: self.assertIn(cue,lower)
        self.assertNotIn('24/7',lower); self.assertIn('clinic hours',lower); self.assertGreaterEqual(html.count('tel:+97126262042'),2)
    def test_directory_and_home_link_primary_pages(self):
        directory=read('treatments.html')
        for rel in PRIMARY: self.assertIn(f"treatments/{rel.split('/')[-1]}",directory,rel)
        home=read('index.html')
        for filename in ['dental-implants.html','orthodontics.html','cosmetic-dentistry.html','general-dentistry.html']: self.assertIn(f'treatments/{filename}',home,filename)
        self.assertIn('treatments/emergency-dentist.html',home)
    def test_sitemap_contains_all_primary_treatment_urls_once(self):
        root=ET.fromstring(read('sitemap.xml')); ns={'sm':'http://www.sitemaps.org/schemas/sitemap/0.9'}; locs=[el.text for el in root.findall('sm:url/sm:loc',ns)]
        for rel in PRIMARY: self.assertEqual(locs.count(f'https://silwadi.ae/{rel}'),1,rel)
        self.assertEqual(len(locs),24)

if __name__=='__main__': unittest.main()
