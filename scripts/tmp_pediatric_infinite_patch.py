from pathlib import Path
import re

p = Path('review/pediatric-dentistry-v1.html')
text = p.read_text(encoding='utf-8')

replacements = [
    ('.pd-hero{position:relative;overflow:hidden;padding:28px 0 64px;background:radial-gradient(ellipse at 72% 100%,rgba(142,229,233,.28) 0%,rgba(142,229,233,.12) 26%,rgba(142,229,233,0) 58%),linear-gradient(180deg,#fff 0%,#f7fbfb 70%,#eef7f8 100%)}',
     '.pd-intro-gallery{overflow:hidden;background:radial-gradient(circle at 78% 36%,rgba(142,229,233,.24),rgba(142,229,233,0) 34%),linear-gradient(180deg,#fff 0%,#f8fbfb 44%,#eef7f8 74%,#fff 100%);border-bottom:1px solid rgba(8,56,71,.06)}\n    .pd-hero{padding:28px 0 34px;background:transparent}'),
    ('.pd-hero:after{content:"";position:absolute;left:50%;bottom:-54px;width:min(1180px,92vw);height:120px;transform:translateX(-50%);background:radial-gradient(ellipse at center,rgba(13,124,144,.08),rgba(13,124,144,0) 68%);pointer-events:none}\n', ''),
    ('.pd-hero__grid{display:block;max-width:920px}',
     '.pd-hero__grid{display:grid;grid-template-columns:minmax(0,1.12fr) minmax(340px,.88fr);gap:72px;align-items:end}\n    .pd-hero__title{min-width:0}\n    .pd-hero__details{max-width:560px;padding:0 0 7px}'),
    ('.pd-hero h1{margin:0;color:var(--pd-deep);font-size:clamp(54px,6.1vw,80px);line-height:.96;letter-spacing:-.06em;font-weight:690;max-width:12.4ch}',
     '.pd-hero h1{margin:0;color:var(--pd-deep);font-size:clamp(54px,5.7vw,78px);line-height:.95;letter-spacing:-.06em;font-weight:690;max-width:10.6ch}'),
    ('.pd-hero__lead{margin:24px 0 0;max-width:700px;color:var(--pd-muted);font-size:17px;line-height:1.7}',
     '.pd-hero__lead{margin:0;max-width:560px;color:var(--pd-muted);font-size:16px;line-height:1.72}'),
    ('.pd-clinic{position:relative;overflow:hidden;margin-top:-24px;background:radial-gradient(circle at 72% 0,rgba(142,229,233,.24),transparent 40%),linear-gradient(180deg,#eef7f8 0%,#f7fbfb 34%,#fff 100%);padding:52px 0 62px;border-bottom:1px solid rgba(8,56,71,.06)}',
     '.pd-clinic{position:relative;overflow:hidden;background:transparent;padding:14px 0 62px}'),
    ('.pd-clinic__head{display:flex;align-items:end;justify-content:space-between;gap:34px;margin-bottom:12px}\n    .pd-clinic__head h2{margin:0;color:var(--pd-deep);font-size:clamp(36px,4.3vw,58px);line-height:.98;letter-spacing:-.05em;font-weight:680}\n    .pd-clinic__head>p{margin:0 0 4px;color:var(--pd-muted);font-size:13px;line-height:1.65;max-width:430px}\n',
     '.pd-clinic__label{margin:0 0 8px;color:var(--pd-teal);font-size:10px;font-weight:850;letter-spacing:.16em;text-transform:uppercase}\n'),
    ('.pd-clinic-viewport{overflow-x:auto;overscroll-behavior-inline:contain;scroll-snap-type:x mandatory;scroll-behavior:smooth;scrollbar-width:none;-ms-overflow-style:none;padding:18px 0 28px}',
     '.pd-clinic-viewport{overflow-x:auto;overscroll-behavior-inline:contain;scroll-snap-type:x mandatory;scrollbar-width:none;-ms-overflow-style:none;padding:12px 0 28px}'),
    ('@media(max-width:1000px){.pd-review-nav{display:none}.pd-visit-shell,.pd-faq-wrap{grid-template-columns:1fr;gap:42px}.pd-visit-copy{position:static}.pd-specialist-card{grid-template-columns:300px 1fr}.pd-specialist-body{padding-left:46px}}',
     '@media(max-width:1000px){.pd-review-nav{display:none}.pd-hero__grid{grid-template-columns:1fr;gap:28px}.pd-hero__details{max-width:700px}.pd-visit-shell,.pd-faq-wrap{grid-template-columns:1fr;gap:42px}.pd-visit-copy{position:static}.pd-specialist-card{grid-template-columns:300px 1fr}.pd-specialist-body{padding-left:46px}}'),
    ('@media(max-width:760px){.pd-private .container span:last-child{display:none}.pd-review-header__inner{height:70px}.pd-review-actions .pd-btn--secondary{display:none}.pd-section{padding:72px 0}.pd-hero{padding:24px 0 50px}.pd-breadcrumb{margin-bottom:24px}.pd-hero h1{font-size:47px;max-width:10.8ch}.pd-hero__lead{font-size:15px}.pd-care-grid{grid-template-columns:1fr}.pd-care-card{min-height:auto;padding:27px 25px 29px}.pd-care-card__top{margin-bottom:27px}.pd-specialist-card{grid-template-columns:1fr}.pd-specialist-photo{height:470px;min-height:0}.pd-specialist-body{padding:42px 0}.pd-specialist-body h2{font-size:46px}.pd-consultation__box{padding:34px 28px;display:block}.pd-consultation__box .pd-btn{margin-top:24px}.pd-visit-step{grid-template-columns:58px 1fr;gap:15px}.pd-faq-wrap{gap:30px}}',
     '@media(max-width:760px){.pd-private .container span:last-child{display:none}.pd-review-header__inner{height:70px}.pd-review-actions .pd-btn--secondary{display:none}.pd-section{padding:72px 0}.pd-hero{padding:22px 0 26px}.pd-breadcrumb{margin-bottom:24px}.pd-hero__grid{gap:24px}.pd-hero h1{font-size:47px;max-width:10.8ch}.pd-hero__lead{font-size:15px}.pd-hero__details{padding-bottom:0}.pd-care-grid{grid-template-columns:1fr}.pd-care-card{min-height:auto;padding:27px 25px 29px}.pd-care-card__top{margin-bottom:27px}.pd-specialist-card{grid-template-columns:1fr}.pd-specialist-photo{height:470px;min-height:0}.pd-specialist-body{padding:42px 0}.pd-specialist-body h2{font-size:46px}.pd-consultation__box{padding:34px 28px;display:block}.pd-consultation__box .pd-btn{margin-top:24px}.pd-visit-step{grid-template-columns:58px 1fr;gap:15px}.pd-faq-wrap{gap:30px}}'),
    ('      .pd-clinic{margin-top:-18px;padding:38px 0 44px}\n      .pd-clinic__head{display:block;margin-bottom:8px}\n      .pd-clinic__head h2{font-size:41px}\n      .pd-clinic__head>p{margin-top:12px;max-width:330px}\n      .pd-clinic-viewport{padding:10px 0 20px}',
     '      .pd-clinic{padding:8px 0 44px}\n      .pd-clinic__label{margin-bottom:6px}\n      .pd-clinic-viewport{padding:8px 0 20px}')
]

for old, new in replacements:
    if old not in text:
        raise SystemExit(f'Expected source fragment not found: {old[:110]}')
    text = text.replace(old, new, 1)

old_hero = '''        <div class="pd-hero__grid">
          <div>
            <p class="pd-eyebrow">Pediatric Dentistry · Pedodontics</p>
            <h1>Pediatric Dentistry in <span>Abu&nbsp;Dhabi</span></h1>
            <p class="pd-hero__lead">Specialist dental care for children at Al Raha Mall — focused on prevention, comfort and the right treatment for each stage of a growing smile.</p>
            <div class="pd-hero__actions"><a class="pd-btn pd-btn--primary" href="#consultation">Book an Appointment</a><a class="pd-btn pd-btn--secondary" href="#specialist">Meet Dr. Kashmira</a></div>
            <div class="pd-hero__micro"><span>Al Raha Mall</span><span>Children's dental care</span><span>Specialist pediatric dentist</span></div>
          </div>
        </div>'''
new_hero = '''        <div class="pd-hero__grid">
          <div class="pd-hero__title">
            <p class="pd-eyebrow">Pediatric Dentistry · Pedodontics</p>
            <h1>Pediatric Dentistry in <span>Abu&nbsp;Dhabi</span></h1>
          </div>
          <div class="pd-hero__details">
            <p class="pd-hero__lead">Specialist dental care for children at Al Raha Mall — focused on prevention, comfort and the right treatment for each stage of a growing smile.</p>
            <div class="pd-hero__actions"><a class="pd-btn pd-btn--primary" href="#consultation">Book an Appointment</a><a class="pd-btn pd-btn--secondary" href="#specialist">Meet Dr. Kashmira</a></div>
            <div class="pd-hero__micro"><span>Al Raha Mall</span><span>Children's dental care</span><span>Specialist pediatric dentist</span></div>
          </div>
        </div>'''
if old_hero not in text:
    raise SystemExit('Expected hero markup not found')
text = text.replace(old_hero, new_hero, 1)

old_clinic_head = '''    <section class="pd-clinic" id="clinic" aria-labelledby="pd-clinic-title">
      <div class="container">
        <div class="pd-clinic__head">
          <div><p class="pd-eyebrow">Al Raha Mall · Pediatric Clinic</p><h2 id="pd-clinic-title">Explore Our Pediatric Clinic</h2></div>
          <p>A closer look at the child-focused treatment environment at our Al Raha Mall branch.</p>
        </div>
      </div>'''
new_clinic_head = '''    <section class="pd-clinic" id="clinic" aria-label="Pediatric clinic photo gallery">
      <div class="container"><p class="pd-clinic__label">Al Raha Mall · Pediatric Clinic</p></div>'''
if old_clinic_head not in text:
    raise SystemExit('Expected clinic heading block not found')
text = text.replace(old_clinic_head, new_clinic_head, 1)

text = text.replace('  <main>\n    <section class="pd-hero" id="hero">', '  <main>\n    <div class="pd-intro-gallery">\n    <section class="pd-hero" id="hero">', 1)
marker = '    </section>\n\n    <section class="pd-section" id="care">'
if marker not in text:
    raise SystemExit('Expected clinic/care boundary not found')
text = text.replace(marker, '    </section>\n    </div>\n\n    <section class="pd-section" id="care">', 1)

script_pattern = re.compile(r'''  <script>\n    \(\(\) => \{.*?\n    \}\)\(\);\n  </script>''', re.S)
new_script = '''  <script>
    (() => {
      const carousel = document.querySelector('[data-pd-carousel]');
      if (!carousel) return;
      const viewport = carousel.querySelector('[data-pd-viewport]');
      const track = carousel.querySelector('.pd-clinic-track');
      const originalSlides = [...carousel.querySelectorAll('[data-pd-slide]')];
      const previous = carousel.querySelector('[data-pd-prev]');
      const next = carousel.querySelector('[data-pd-next]');
      const current = carousel.querySelector('[data-pd-current]');
      if (!viewport || !track || originalSlides.length < 2) return;

      const ANIMATION_MS = 280;
      const SWIPE_THRESHOLD = 42;
      const reduceMotion = window.matchMedia('(prefers-reduced-motion: reduce)').matches;
      const total = originalSlides.length;
      const lastClone = originalSlides[total - 1].cloneNode(true);
      const firstClone = originalSlides[0].cloneNode(true);
      lastClone.dataset.pdClone = 'last';
      firstClone.dataset.pdClone = 'first';
      [lastClone, firstClone].forEach(clone => {
        clone.classList.remove('is-active');
        clone.setAttribute('aria-hidden', 'true');
        const image = clone.querySelector('img');
        if (image) image.setAttribute('loading', 'lazy');
      });
      track.insertBefore(lastClone, originalSlides[0]);
      track.appendChild(firstClone);

      const slides = [...track.querySelectorAll('[data-pd-slide]')];
      let trackIndex = 1;
      let logicalIndex = 0;
      let animating = false;
      let settleTimer = null;
      let pointerStartX = null;

      const logicalFromTrack = index => index === 0 ? total - 1 : index === total + 1 ? 0 : index - 1;
      const targetLeft = index => {
        const slide = slides[index];
        return slide.offsetLeft - (viewport.clientWidth - slide.clientWidth) / 2;
      };
      const updateActive = () => {
        slides.forEach((slide, index) => {
          const active = index === trackIndex;
          slide.classList.toggle('is-active', active);
          slide.setAttribute('aria-hidden', active ? 'false' : 'true');
        });
        logicalIndex = logicalFromTrack(trackIndex);
        current.textContent = String(logicalIndex + 1).padStart(2, '0');
      };
      const jumpTo = index => viewport.scrollTo({left: targetLeft(index), behavior: 'auto'});
      const normalizeLoopPosition = () => {
        if (trackIndex === 0) {
          trackIndex = total;
          jumpTo(trackIndex);
          updateActive();
        } else if (trackIndex === total + 1) {
          trackIndex = 1;
          jumpTo(trackIndex);
          updateActive();
        }
      };
      const animateTo = targetIndex => {
        if (animating) return;
        const boundedTarget = Math.max(0, Math.min(total + 1, targetIndex));
        if (reduceMotion) {
          trackIndex = boundedTarget;
          jumpTo(trackIndex);
          updateActive();
          normalizeLoopPosition();
          return;
        }
        const start = viewport.scrollLeft;
        const end = targetLeft(boundedTarget);
        const distance = end - start;
        let startedAt = null;
        animating = true;
        viewport.style.scrollSnapType = 'none';
        const step = timestamp => {
          if (startedAt === null) startedAt = timestamp;
          const progress = Math.min(1, (timestamp - startedAt) / ANIMATION_MS);
          const eased = 1 - Math.pow(1 - progress, 3);
          viewport.scrollLeft = start + distance * eased;
          if (progress < 1) {
            requestAnimationFrame(step);
            return;
          }
          viewport.scrollLeft = end;
          viewport.style.scrollSnapType = '';
          trackIndex = boundedTarget;
          updateActive();
          animating = false;
          normalizeLoopPosition();
        };
        requestAnimationFrame(step);
      };
      const go = delta => animateTo(trackIndex + delta);

      previous.addEventListener('click', () => go(-1));
      next.addEventListener('click', () => go(1));
      carousel.addEventListener('keydown', event => {
        if (event.key === 'ArrowLeft') { event.preventDefault(); go(-1); }
        if (event.key === 'ArrowRight') { event.preventDefault(); go(1); }
      });
      slides.forEach((slide, index) => slide.addEventListener('click', () => {
        if (index !== trackIndex) animateTo(index);
      }));
      carousel.addEventListener('pointerdown', event => {
        if (event.pointerType === 'mouse') return;
        pointerStartX = event.clientX;
      });
      carousel.addEventListener('pointerup', event => {
        if (pointerStartX === null) return;
        const distance = event.clientX - pointerStartX;
        pointerStartX = null;
        if (Math.abs(distance) >= SWIPE_THRESHOLD) go(distance < 0 ? 1 : -1);
      });
      carousel.addEventListener('pointercancel', () => { pointerStartX = null; });
      viewport.addEventListener('scroll', () => {
        if (animating) return;
        clearTimeout(settleTimer);
        settleTimer = setTimeout(() => {
          const viewportCenter = viewport.scrollLeft + viewport.clientWidth / 2;
          let nearest = trackIndex;
          let nearestDistance = Infinity;
          slides.forEach((slide, index) => {
            const slideCenter = slide.offsetLeft + slide.clientWidth / 2;
            const distance = Math.abs(slideCenter - viewportCenter);
            if (distance < nearestDistance) {
              nearest = index;
              nearestDistance = distance;
            }
          });
          trackIndex = nearest;
          updateActive();
          normalizeLoopPosition();
        }, 80);
      }, {passive:true});
      window.addEventListener('resize', () => jumpTo(trackIndex), {passive:true});
      requestAnimationFrame(() => {
        jumpTo(trackIndex);
        updateActive();
      });
    })();
  </script>'''
text, count = script_pattern.subn(new_script, text, count=1)
if count != 1:
    raise SystemExit(f'Expected one carousel script, replaced {count}')

p.write_text(text, encoding='utf-8')
