import fs from 'node:fs';
import vm from 'node:vm';
import assert from 'node:assert/strict';
const context={};
for(const p of ['ai/assets/clinic-text.js','ai/assets/booking.js'])vm.runInNewContext(fs.readFileSync(p,'utf8'),context);
const roster=JSON.parse(fs.readFileSync('ai/clinic-knowledge-v1.json','utf8')).doctors;
assert.equal(context.SilwadiBooking.doctors.length,roster.length,'Booking roster must match the reviewed doctor directory');
assert.ok(context.SilwadiBooking.doctors.some(([name])=>name==='Mithra Pothancheri'));
for(const [q,name] of [['I want to book an appointment with Dr Mithra','Mithra Pothancheri'],['ابغي احجز موعد مع دكتورة ميثرا','Mithra Pothancheri']]){
 assert.equal(context.SilwadiBooking.preferredDoctor(q),name,q);
 assert.ok(context.SilwadiBooking.intent(q),q);
}
assert.ok(context.SilwadiBooking.valid(2,{doctor:'Mithra Pothancheri',clinic:'Bani Yas Tower',treatment:'General Dentistry'}));
console.log('English/Arabic named-doctor booking and reviewed roster parity passed.');
