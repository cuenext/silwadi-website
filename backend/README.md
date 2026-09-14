# Silwadi booking email backend

This folder contains the server-side endpoint for the website appointment popup.

The public website is served by GitHub Pages, so PHP cannot run on `silwadi.ae` itself. The endpoint is intended to run on the clinic's existing cPanel hosting at:

`https://booking.silwadi.ae/booking-submit.php`

## One-time deployment

1. In cPanel, create the subdomain `booking.silwadi.ae` with its own document root.
2. Confirm SSL/AutoSSL is active for the subdomain.
3. Upload `booking-submit.php` from this folder into that document root as `booking-submit.php`.
4. Confirm the subdomain resolves over HTTPS.
5. Test an appointment request from `https://silwadi.ae` and confirm it reaches `appointment@silwadidentalcenter.ae`.
6. Only after the endpoint test succeeds, merge the matching `booking-modal.js` change into the live website.

## Security notes

- The endpoint only accepts browser requests from `https://silwadi.ae` and `https://www.silwadi.ae`.
- It validates required fields and email format.
- It includes a honeypot and lightweight per-IP rate limiting.
- The visitor's email address is used only as `Reply-To`; the message itself is sent server-side.
- No SMTP password or API key is stored in the public website JavaScript or this repository.
