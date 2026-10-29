// Idempotent repair for pages regenerated outside the public bundle workflow.
import fs from 'node:fs';
import path from 'node:path';
import {fileURLToPath} from 'node:url';
const root=path.resolve(path.dirname(fileURLToPath(import.meta.url)),'..');
export function integrate(html){
 const ar=/<html[^>]*lang="ar"/i.test(html);
 const link=`<a data-faq-link href="${ar?'/ai/?lang=ar':'/ai/'}">${ar?'الأسئلة الشائعة':'FAQ'}</a>`;
 html=html.replace(/<nav\b[^>]*class="(?:site-nav|mobile-nav__panel|global-nav|nav)"[^>]*>[\s\S]*?<\/nav>/g,nav=>nav.includes('/ai/')?nav:nav.replace('</nav>',link+'</nav>'));
 html=html.replace(/<footer\b[^>]*>[\s\S]*?<\/footer>/g,footer=>{
  if(footer.includes('/ai/'))return footer;
  if(/<h3>\s*(?:Centre|المركز)\s*<\/h3>/i.test(footer))return footer.replace(/(<h3>\s*(?:Centre|المركز)\s*<\/h3>)/i,'$1'+link);
  return footer.replace('</footer>','<div class="container footer-bottom">'+link+'</div></footer>');
 });
 if(!html.includes('silwadi-ai-widget.js'))html=html.replace('</body>',['clinic-text','booking','silwadi-ai-widget'].map(a=>`<script src="/ai/assets/${a}.js?v=20261029-restore1" defer></script>`).join('\n')+'\n</body>');
 return html;
}
let count=0;
for(const match of fs.readFileSync(path.join(root,'sitemap.xml'),'utf8').matchAll(/<loc>(.*?)<\/loc>/g)){
 let p=new URL(match[1]).pathname.replace(/^\//,'')||'index.html';if(p.startsWith('ai/'))continue;if(p.endsWith('/'))p+='index.html';
 const file=path.join(root,p),old=fs.readFileSync(file,'utf8'),next=integrate(old);
 if(integrate(next)!==next)throw new Error('Not idempotent: '+p);
 if(next!==old){fs.writeFileSync(file,next);count++;}
}
console.log(`Updated ${count} public pages.`);
