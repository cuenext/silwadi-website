<?php
declare(strict_types=1);
require $argv[1] ?? __DIR__ . '/../../tools/server/booking-validation.php';
$valid=['name'=>'عبدالله O\'Brien','email'=>'test@example.com','phone'=>'+971 50 123 4567',
    'treatment'=>'General Dentistry','date'=>'2026-10-06','time'=>'09:00',
    'clinic'=>'Bani Yas Tower','notes'=>"Question\nSecond line",'website'=>'','consent'=>true];
$cases=[[$valid,null], [array_replace($valid,['treatment'=>'طب الأسنان العام','clinic'=>'برج بني ياس']),null]];
foreach ([['name',str_repeat('ا',121),'invalid_fields'],['email',"a@example.com\r\nBcc:x@example.com",'invalid_fields'],
    ['phone','abc','invalid_phone'],['phone','123','invalid_phone'],['phone',str_repeat('1',16),'invalid_phone'],
    ['name',['nested'],'invalid_fields'],['name',"bad\0value",'invalid_fields'],['name',"\xFF",'invalid_fields'],
    ['notes',str_repeat('x',1501),'invalid_fields'],['treatment','Unlisted','invalid_treatment'],
    ['clinic','Unlisted','invalid_clinic'],['time','23:00','invalid_time'],['date','2026-02-30','invalid_date'],
    ['consent',false,'consent_required'],['consent','true','consent_required'],['email','bad','invalid_email'],
    ['name','','missing_required_fields']] as [$key,$value,$error]) {
    $cases[]=[array_replace($valid,[$key=>$value]),$error];
}
$missing=$valid;unset($missing['consent']);$cases[]=[$missing,'consent_required'];
foreach($cases as $n=>[$input,$expected]) {
    $actual=booking_validation_error($input);
    if($actual!==$expected){fwrite(STDERR,"Case $n failed: expected ".($expected??'valid').", got ".($actual??'valid')."\n");exit(1);}
}
echo count($cases)." booking validation cases passed; no email sent\n";
