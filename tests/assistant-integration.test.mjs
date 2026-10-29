import assert from 'node:assert/strict';
import fs from 'node:fs';
import path from 'node:path';
import {fileURLToPath} from 'node:url';
const root=path.resolve(path.dirname(fileURLToPath(import.meta.url)),'..');
const urls=[...fs.readFileSync(path.join(root,'sitemap.xml'),'utf8').matchAll(/<loc>(.*?)<\/loc>/g)].map(m=>new URL(m[1]));
let count=0;
for(const url of urls){
 if(url.pathname.startsWith('/ai/'))continue;
 let relative=url.pathname.replace(/^\//,'')||'index.html';
 if(relative.endsWith('/'))relative+='index.html';
 const html=fs.readFileSync(path.join(root,relative),'utf8');
 for(const asset of ['clinic-text','booking','silwadi-ai-widget'])assert.ok(html.includes('/ai/assets/'+asset+'.js'),`${relative}: missing ${asset}`);
 const navs=[...html.matchAll(/<nav\b[^>]*class="(?:site-nav|mobile-nav__panel|global-nav|nav)"[^>]*>[\s\S]*?<\/nav>/g)];
 assert.ok(navs.length,`${relative}: missing navigation`);
 for(const [nav] of navs)assert.ok(nav.includes('/ai/'),`${relative}: missing FAQ link`);
 assert.match(html,/<footer\b[^>]*>[\s\S]*?\/ai\/[\s\S]*?<\/footer>/,`${relative}: missing footer FAQ`);
 if(relative.startsWith('ar/'))assert.ok(html.includes('/ai/?lang=ar'),`${relative}: Arabic FAQ target`);
 count++;
}
for(const file of ['index.html','privacy.html','site-shell.js','site-shell.css','silwadi-ai-page.css','assets/assistant.svg','assets/faq.js','assets/clinic-text.js','assets/booking.js','assets/silwadi-ai-widget.js','assets/silwadi-ai-widget.css'])assert.ok(fs.existsSync(path.join(root,'ai',file)),`Missing public assistant file: ${file}`);
console.log(`Assistant scripts and FAQ navigation verified on ${count} published English/Arabic pages.`);
