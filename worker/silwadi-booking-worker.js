const DEFAULT_ORIGIN = 'https://silwadi.ae';
const RESEND_API_URL = 'https://api.resend.com/emails';
const DEFAULT_RECIPIENT = 'appointment@silwadidentalcenter.ae';
const DEFAULT_FROM = 'Silwadi Website <booking@silwadi.ae>';
const RATE_WINDOW_MS = 10 * 60 * 1000;
const RATE_WINDOW_MAX = 5;

const rateBuckets = new Map();

function responseJson(payload, status, origin, allowedOrigin) {
  const headers = {
    'Content-Type': 'application/json; charset=utf-8',
    'Cache-Control': 'no-store',
    'Vary': 'Origin',
    'X-Content-Type-Options': 'nosniff',
    'Referrer-Policy': 'no-referrer',
  };

  if (origin === allowedOrigin) {
    headers['Access-Control-Allow-Origin'] = origin;
    headers['Access-Control-Allow-Methods'] = 'POST, OPTIONS';
    headers['Access-Control-Allow-Headers'] = 'Content-Type';
    headers['Access-Control-Max-Age'] = '86400';
  }

  return new Response(JSON.stringify(payload), { status, headers });
}

function rateLimited(request) {
  const key = request.headers.get('CF-Connecting-IP') || 'anonymous';
  const now = Date.now();
  const bucket = rateBuckets.get(key);

  if (!bucket || now - bucket.startedAt >= RATE_WINDOW_MS) {
    rateBuckets.set(key, { startedAt: now, count: 1 });
    return false;
  }

  bucket.count += 1;
  return bucket.count > RATE_WINDOW_MAX;
}

function clean(value, maxLength) {
  return typeof value === 'string' ? value.trim().slice(0, maxLength) : '';
}

function isValidEmail(value) {
  return /^[^\s@]+@[^\s@]+\.[^\s@]+$/.test(value);
}

function buildMessage(payload) {
  const lines = [
    'New appointment request from silwadi.ae',
    '',
    `Name: ${payload.name}`,
    `Email: ${payload.email}`,
    `Phone: ${payload.phone}`,
    `Treatment: ${payload.treatment}`,
    `Preferred date: ${payload.date || 'Not specified'}`,
    `Preferred time: ${payload.time}`,
    `Preferred clinic: ${payload.clinic}`,
    `Language: ${payload.language === 'ar' ? 'Arabic' : 'English'}`,
    '',
    `Notes: ${payload.notes || 'None'}`,
    '',
    'Submitted through the Silwadi Dental Center website booking form.',
  ];

  return lines.join('\n');
}

async function handleBooking(request, env, origin, allowedOrigin) {
  if (request.method !== 'POST') {
    return responseJson({ ok: false, error: 'method_not_allowed' }, 405, origin, allowedOrigin);
  }

  if (!env.RESEND_API_KEY) {
    return responseJson({ ok: false, error: 'email_service_not_configured' }, 503, origin, allowedOrigin);
  }

  if (rateLimited(request)) {
    return responseJson({ ok: false, error: 'too_many_requests' }, 429, origin, allowedOrigin);
  }

  const contentLength = Number(request.headers.get('Content-Length') || 0);
  if (contentLength > 12000) {
    return responseJson({ ok: false, error: 'request_too_large' }, 413, origin, allowedOrigin);
  }

  let body;
  try {
    body = await request.json();
  } catch {
    return responseJson({ ok: false, error: 'invalid_json' }, 400, origin, allowedOrigin);
  }

  const payload = {
    name: clean(body?.name, 120),
    email: clean(body?.email, 180),
    phone: clean(body?.phone, 60),
    treatment: clean(body?.treatment, 120),
    date: clean(body?.date, 30),
    time: clean(body?.time, 30),
    clinic: clean(body?.clinic, 160),
    notes: clean(body?.notes, 1500),
    language: body?.language === 'ar' ? 'ar' : 'en',
  };

  if (!payload.name || !payload.email || !payload.phone || !payload.treatment || !payload.time || !payload.clinic) {
    return responseJson({ ok: false, error: 'missing_required_fields' }, 400, origin, allowedOrigin);
  }

  if (!isValidEmail(payload.email)) {
    return responseJson({ ok: false, error: 'invalid_email' }, 400, origin, allowedOrigin);
  }

  const subject = `Appointment request - ${payload.treatment}`;
  const providerResponse = await fetch(RESEND_API_URL, {
    method: 'POST',
    headers: {
      'Authorization': `Bearer ${env.RESEND_API_KEY}`,
      'Content-Type': 'application/json',
    },
    body: JSON.stringify({
      from: env.BOOKING_FROM || DEFAULT_FROM,
      to: [env.BOOKING_RECIPIENT || DEFAULT_RECIPIENT],
      reply_to: payload.email,
      subject,
      text: buildMessage(payload),
    }),
  });

  if (!providerResponse.ok) {
    return responseJson({ ok: false, error: 'email_delivery_failed' }, 502, origin, allowedOrigin);
  }

  return responseJson({ ok: true }, 200, origin, allowedOrigin);
}

export default {
  async fetch(request, env) {
    const url = new URL(request.url);
    const origin = request.headers.get('Origin') || '';
    const allowedOrigin = env.ALLOWED_ORIGIN || DEFAULT_ORIGIN;

    if (request.method === 'OPTIONS') {
      if (origin !== allowedOrigin) {
        return responseJson({ ok: false, error: 'origin_not_allowed' }, 403, origin, allowedOrigin);
      }
      return new Response(null, {
        status: 204,
        headers: {
          'Access-Control-Allow-Origin': origin,
          'Access-Control-Allow-Methods': 'POST, OPTIONS',
          'Access-Control-Allow-Headers': 'Content-Type',
          'Access-Control-Max-Age': '86400',
          'Vary': 'Origin',
        },
      });
    }

    if (origin !== allowedOrigin) {
      return responseJson({ ok: false, error: 'origin_not_allowed' }, 403, origin, allowedOrigin);
    }

    if (url.pathname !== '/request') {
      return responseJson({ ok: false, error: 'not_found' }, 404, origin, allowedOrigin);
    }

    return handleBooking(request, env, origin, allowedOrigin);
  },
};
