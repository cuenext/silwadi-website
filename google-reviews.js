/* Render the verified review dataset before language and app initialization. */
(function () {
  'use strict';

  const labels = {
    en: {
      review: 'Google review', open: (reviewer, branch) => `Open patient review by ${reviewer} at the ${branch} branch`,
      stars: '5 out of 5 stars', hint: 'Tap to read',
      branches: {corniche: 'Corniche', 'al-raha': 'Al Raha'}
    },
    ar: {
      review: 'تقييم على Google', open: (reviewer, branch) => `فتح تقييم ${reviewer} عن فرع ${branch}`,
      stars: '٥ من ٥ نجوم', hint: 'اضغط للقراءة',
      branches: {corniche: 'الكورنيش', 'al-raha': 'الراحة'}
    }
  };

  function escapeHtml(value) {
    return String(value).replace(/[&<>"']/g, character => ({
      '&': '&amp;', '<': '&lt;', '>': '&gt;', '"': '&quot;', "'": '&#39;'
    })[character]);
  }

  function renderCard(review, language, interactive) {
    const copy = labels[language];
    const words = review.reviewer.trim().split(/\s+/);
    const initials = words.slice(0, 2).map(word => Array.from(word)[0]).join('').toUpperCase();
    const action = interactive
      ? ` data-review-expand tabindex="0" role="button" aria-haspopup="dialog" aria-label="${escapeHtml(copy.open(review.reviewer, copy.branches[review.branch]))}"`
      : '';
    return `<article class="google-review-card" data-review-id="${escapeHtml(review.id)}" data-review-url="${escapeHtml(review.sourceUrl)}"${action}>` +
      `<div class="google-review-card__top"><span class="review-avatar">${escapeHtml(initials)}</span>` +
      `<div><strong>${escapeHtml(review.reviewer)}</strong><span>${copy.review} · ${copy.branches[review.branch]}</span>` +
      `<span class="review-stars" aria-label="${copy.stars}">★★★★★</span></div></div>` +
      `<p>${escapeHtml(review.summary[language])}</p><span class="review-card__hint">${copy.hint}</span></article>`;
  }

  window.renderSilwadiGoogleReviews = function (language) {
    language = language === 'ar' ? 'ar' : 'en';
    const track = document.querySelector('.google-reviews-track');
    const groups = track?.querySelectorAll('.google-reviews-group');
    if (!groups || groups.length < 2) return 0;

    const reviews = window.SILWADI_GOOGLE_REVIEWS || [];
    groups[0].innerHTML = reviews.map(review => renderCard(review, language, true)).join('');
    // Keep every visual, including the hint, identical for a seamless loop.
    // The duplicate has no focus targets or dialog triggers.
    groups[1].innerHTML = reviews.map(review => renderCard(review, language, false)).join('');
    groups[1].setAttribute('aria-hidden', 'true');
    track.style.setProperty('--reviews-duration', `${Math.max(46, reviews.length * 46 / 5)}s`);
    document.dispatchEvent(new CustomEvent('silwadi:reviews-rendered', {
      detail: {count: reviews.length, language}
    }));
    return reviews.length;
  };

  window.renderSilwadiGoogleReviews(document.documentElement.lang);
}());
