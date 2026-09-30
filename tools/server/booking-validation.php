<?php
declare(strict_types=1);

/** Pure validation; does not send email, log patient data, or access storage. */
function booking_validation_error(array $body): ?string
{
    $limits = ['name'=>120, 'email'=>180, 'phone'=>60, 'treatment'=>120,
        'date'=>30, 'time'=>30, 'clinic'=>160, 'notes'=>1500, 'website'=>200];
    foreach ($limits as $field => $max) {
        if (!array_key_exists($field, $body)) { continue; }
        $value = $body[$field];
        if (!is_string($value) || preg_match('//u', $value) !== 1) { return 'invalid_fields'; }
        $length = preg_match_all('/./us', $value);
        if ($length === false || $length > $max) { return 'invalid_fields'; }
        $controls = $field === 'notes' ? '/[\x00-\x08\x0B\x0C\x0E-\x1F\x7F]/' : '/[\x00-\x1F\x7F]/';
        if (preg_match($controls, $value) === 1) { return 'invalid_fields'; }
    }
    foreach (['name','email','phone','treatment','time','clinic'] as $field) {
        if (!isset($body[$field]) || trim($body[$field]) === '') { return 'missing_required_fields'; }
    }
    if (($body['consent'] ?? null) !== true) { return 'consent_required'; }
    if (filter_var(trim($body['email']), FILTER_VALIDATE_EMAIL) === false) { return 'invalid_email'; }
    $phone = trim($body['phone']);
    if (preg_match('/^\+?[0-9 () .-]+$/D', $phone) !== 1) { return 'invalid_phone'; }
    $digits = preg_replace('/\D/', '', $phone);
    if (strlen($digits) < 7 || strlen($digits) > 15) { return 'invalid_phone'; }
    $treatments = ['General Dentistry','Preventive Dentistry','Prosthodontics','Cosmetic Dentistry',
        'Dental Implants','Orthodontics','Periodontics','Endodontics','Paediatric Dentistry',
        'People of Determination Dental Care','Other / Not sure',
        'طب الأسنان العام','طب الأسنان الوقائي','تركيبات الأسنان','طب الأسنان التجميلي',
        'زراعة الأسنان','تقويم الأسنان','أمراض اللثة','علاج اللثة','علاج جذور الأسنان',
        'طب أسنان الأطفال','رعاية أسنان لأصحاب الهمم','أخرى / لست متأكداً'];
    if (!in_array(trim($body['treatment']), $treatments, true)) { return 'invalid_treatment'; }
    $clinics = ['Bani Yas Tower','Bani Yas Tower - Corniche Street','Al Raha Mall',
        'برج بني ياس','برج بني ياس - شارع الكورنيش','الراحة مول'];
    if (!in_array(trim($body['clinic']), $clinics, true)) { return 'invalid_clinic'; }
    if (preg_match('/^(?:09|1[0-9]|20):00$/D', trim($body['time'])) !== 1) { return 'invalid_time'; }
    $date = trim($body['date'] ?? '');
    if ($date !== '') {
        if (preg_match('/^(\d{4})-(\d{2})-(\d{2})$/D', $date, $parts) !== 1
            || !checkdate((int)$parts[2], (int)$parts[3], (int)$parts[1])) { return 'invalid_date'; }
    }
    return null;
}
