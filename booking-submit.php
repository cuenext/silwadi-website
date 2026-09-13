<?php
declare(strict_types=1);

header('Content-Type: application/json; charset=utf-8');
header('Cache-Control: no-store');
header('X-Content-Type-Options: nosniff');
header('Referrer-Policy: no-referrer');

const BOOKING_RECIPIENT = 'appointment@silwadidentalcenter.ae';
const BOOKING_FROM = 'Silwadi Website <website@silwadi.ae>';
const RATE_WINDOW_SECONDS = 600;
const RATE_WINDOW_MAX = 5;

function json_response(array $payload, int $status): never
{
    http_response_code($status);
    echo json_encode($payload, JSON_UNESCAPED_UNICODE | JSON_UNESCAPED_SLASHES);
    exit;
}

function clean_text(mixed $value, int $maxLength): string
{
    if (!is_string($value)) {
        return '';
    }

    $value = trim(str_replace("\0", '', $value));
    if (function_exists('mb_substr')) {
        return mb_substr($value, 0, $maxLength, 'UTF-8');
    }

    return substr($value, 0, $maxLength);
}

function rate_limit(string $ip): bool
{
    $key = hash('sha256', $ip !== '' ? $ip : 'unknown');
    $path = rtrim(sys_get_temp_dir(), DIRECTORY_SEPARATOR) . DIRECTORY_SEPARATOR . 'silwadi-booking-' . $key . '.json';
    $handle = @fopen($path, 'c+');

    if ($handle === false || !flock($handle, LOCK_EX)) {
        if (is_resource($handle)) {
            fclose($handle);
        }
        return false;
    }

    $now = time();
    $raw = stream_get_contents($handle);
    $bucket = is_string($raw) && $raw !== '' ? json_decode($raw, true) : null;

    if (!is_array($bucket) || !isset($bucket['started_at'], $bucket['count']) || ($now - (int) $bucket['started_at']) >= RATE_WINDOW_SECONDS) {
        $bucket = ['started_at' => $now, 'count' => 1];
    } else {
        $bucket['count'] = (int) $bucket['count'] + 1;
    }

    rewind($handle);
    ftruncate($handle, 0);
    fwrite($handle, json_encode($bucket));
    fflush($handle);
    flock($handle, LOCK_UN);
    fclose($handle);

    return (int) $bucket['count'] > RATE_WINDOW_MAX;
}

if (($_SERVER['REQUEST_METHOD'] ?? '') !== 'POST') {
    header('Allow: POST');
    json_response(['ok' => false, 'error' => 'method_not_allowed'], 405);
}

$origin = $_SERVER['HTTP_ORIGIN'] ?? '';
$allowedOrigins = ['https://silwadi.ae', 'https://www.silwadi.ae'];
if ($origin !== '' && !in_array($origin, $allowedOrigins, true)) {
    json_response(['ok' => false, 'error' => 'origin_not_allowed'], 403);
}

$contentType = strtolower((string) ($_SERVER['CONTENT_TYPE'] ?? ''));
if (!str_starts_with($contentType, 'application/json')) {
    json_response(['ok' => false, 'error' => 'unsupported_media_type'], 415);
}

$raw = file_get_contents('php://input');
if (!is_string($raw) || $raw === '' || strlen($raw) > 12000) {
    json_response(['ok' => false, 'error' => 'invalid_request'], 400);
}

$body = json_decode($raw, true);
if (!is_array($body)) {
    json_response(['ok' => false, 'error' => 'invalid_json'], 400);
}

$honeypot = clean_text($body['website'] ?? '', 200);
if ($honeypot !== '') {
    json_response(['ok' => true], 200);
}

$ip = (string) ($_SERVER['REMOTE_ADDR'] ?? '');
if (rate_limit($ip)) {
    json_response(['ok' => false, 'error' => 'too_many_requests'], 429);
}

$name = clean_text($body['name'] ?? '', 120);
$email = clean_text($body['email'] ?? '', 180);
$phone = clean_text($body['phone'] ?? '', 60);
$treatment = clean_text($body['treatment'] ?? '', 120);
$date = clean_text($body['date'] ?? '', 30);
$time = clean_text($body['time'] ?? '', 30);
$clinic = clean_text($body['clinic'] ?? '', 160);
$notes = clean_text($body['notes'] ?? '', 1500);
$language = ($body['language'] ?? '') === 'ar' ? 'Arabic' : 'English';

if ($name === '' || $email === '' || $phone === '' || $treatment === '' || $time === '' || $clinic === '') {
    json_response(['ok' => false, 'error' => 'missing_required_fields'], 400);
}

if (filter_var($email, FILTER_VALIDATE_EMAIL) === false) {
    json_response(['ok' => false, 'error' => 'invalid_email'], 400);
}

$treatmentForSubject = str_replace(["\r", "\n"], ' ', $treatment);
$subject = 'Appointment request - ' . $treatmentForSubject;
if (function_exists('mb_encode_mimeheader')) {
    $subject = mb_encode_mimeheader($subject, 'UTF-8', 'B');
}

$message = implode("\n", [
    'New appointment request from silwadi.ae',
    '',
    'Name: ' . $name,
    'Email: ' . $email,
    'Phone: ' . $phone,
    'Treatment: ' . $treatment,
    'Preferred date: ' . ($date !== '' ? $date : 'Not specified'),
    'Preferred time: ' . $time,
    'Preferred clinic: ' . $clinic,
    'Language: ' . $language,
    '',
    'Notes: ' . ($notes !== '' ? $notes : 'None'),
    '',
    'Submitted through the Silwadi Dental Center website booking form.',
]);

$headers = implode("\r\n", [
    'MIME-Version: 1.0',
    'Content-Type: text/plain; charset=UTF-8',
    'From: ' . BOOKING_FROM,
    'Reply-To: ' . $email,
]);

$sent = mail(BOOKING_RECIPIENT, $subject, $message, $headers);
if (!$sent) {
    error_log('Silwadi booking form: PHP mail() failed.');
    json_response(['ok' => false, 'error' => 'email_delivery_failed'], 502);
}

json_response(['ok' => true], 200);
