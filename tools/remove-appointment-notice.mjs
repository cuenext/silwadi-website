import fs from 'node:fs';
import path from 'node:path';

const root = process.cwd();
const contactPath = path.join(root, 'contact.html');
const contactCssPath = path.join(root, 'contact-pages.css');

let html = fs.readFileSync(contactPath, 'utf8');
const noticePattern = /<div class="appointment-disclaimer">[\s\S]*?<\/div><\/div>(?=<h2 class="appointment-form-heading">)/g;
html = html.replace(noticePattern, '');

if (html.includes('appointment-disclaimer') || html.includes('Important notice') || html.includes('false online offers promising free treatments')) {
  throw new Error('Appointment notice cleanup did not fully remove the notice from contact.html');
}
fs.writeFileSync(contactPath, html);

let css = fs.readFileSync(contactCssPath, 'utf8');
css = css.replace(/\n?\s*\.appointment-disclaimer(?:__icon)?(?:\s+(?:strong|p))?\{[^}]*\}/g, '');
if (css.includes('.appointment-disclaimer')) {
  throw new Error('Appointment notice cleanup did not fully remove its CSS');
}
fs.writeFileSync(contactCssPath, css);

console.log('Removed the obsolete appointment notice and its styling.');
