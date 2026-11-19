// Kestrel Aviation Solutions website. Page animations and the hero carousel. The pages work without this file.
const reduce = matchMedia('(prefers-reduced-motion: reduce)').matches;

// Parts of each page rise in as they come into view.
const seen = new IntersectionObserver(es => es.forEach(e => { if (e.isIntersecting) { e.target.classList.add('in'); seen.unobserve(e.target); } }), { rootMargin: '0px 0px -6% 0px' });
document.querySelectorAll('[data-rise]').forEach(el => seen.observe(el));

// Hero carousel: moves on every 5 seconds, stops while you point at it, use it or switch tabs.
const box = document.querySelector('.carousel');
if (box) {
  const track = box.querySelector('.track'), slides = [...box.querySelectorAll('.slide')], dots = [...box.querySelectorAll('.dot')];
  const pauseBtn = box.querySelector('.pause');
  let at = 0, timer = null, stopped = reduce, hover = false;
  const show = i => {
    at = (i + slides.length) % slides.length;
    track.scrollTo({ left: at * track.clientWidth, behavior: reduce ? 'auto' : 'smooth' });
    mark();
  };
  const mark = () => {
    slides.forEach((s, k) => s.classList.toggle('on', k === at));
    dots.forEach((d, k) => d.setAttribute('aria-current', k === at ? 'true' : 'false'));
  };
  const tick = () => { clearTimeout(timer); if (!stopped && !hover && !document.hidden) timer = setTimeout(() => { show(at + 1); tick(); }, 5000); };
  const setStopped = v => { stopped = v; pauseBtn.textContent = v ? 'Play' : 'Pause'; pauseBtn.setAttribute('aria-label', v ? 'Play' : 'Pause'); tick(); };
  // Keep the dots right when someone swipes or scrolls the row by hand.
  let raf = 0;
  track.addEventListener('scroll', () => { cancelAnimationFrame(raf); raf = requestAnimationFrame(() => { const i = Math.round(track.scrollLeft / track.clientWidth); if (i !== at) { at = i; mark(); } }); }, { passive: true });
  box.querySelector('.prev').onclick = () => { show(at - 1); tick(); };
  box.querySelector('.next').onclick = () => { show(at + 1); tick(); };
  dots.forEach((d, k) => d.onclick = () => { show(k); tick(); });
  pauseBtn.onclick = () => setStopped(!stopped);
  box.addEventListener('pointerenter', () => { hover = true; tick(); });
  box.addEventListener('pointerleave', () => { hover = false; tick(); });
  box.addEventListener('focusin', () => { hover = true; tick(); });
  box.addEventListener('focusout', () => { hover = false; tick(); });
  track.addEventListener('keydown', e => { if (e.key === 'ArrowRight') { e.preventDefault(); show(at + 1); } if (e.key === 'ArrowLeft') { e.preventDefault(); show(at - 1); } });
  document.addEventListener('visibilitychange', tick);
  addEventListener('resize', () => track.scrollTo({ left: at * track.clientWidth, behavior: 'auto' }));
  mark(); setStopped(stopped);
}
