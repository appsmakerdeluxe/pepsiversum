import { story } from './content.js';

const $ = (selector, scope = document) => scope.querySelector(selector);
const $all = (selector, scope = document) => [...scope.querySelectorAll(selector)];
const reduceMotion = window.matchMedia('(prefers-reduced-motion: reduce)').matches;

function populateContent() {
  $('#traits-list').innerHTML = story.traits.map(([title, copy], index) => `<article class="trait reveal"><span>${String(index + 1).padStart(2, '0')}</span><h3>${title}</h3><p>${copy}</p></article>`).join('');
  $('#moments-list').innerHTML = story.moments.map(([date, text, quote], index) => `<article class="moment reveal"><span class="moment-index">${String(index + 1).padStart(2, '0')}</span><div><p class="moment-date">${date}</p><h3>${text}</h3><blockquote>${quote}</blockquote></div></article>`).join('');
  $('#affirmations').innerHTML = story.affirmations.map(word => `<p class="affirmation reveal">${word}</p>`).join('');
}

function revealOnScroll() {
  const observer = new IntersectionObserver(entries => entries.forEach(entry => {
    if (entry.isIntersecting) { entry.target.classList.add('is-visible'); observer.unobserve(entry.target); }
  }), { threshold: 0.14, rootMargin: '0px 0px -6% 0px' });
  $all('.reveal').forEach(el => observer.observe(el));
}

function openLetter() {
  const intro = $('#intro'); const storyEl = $('#story'); const button = $('#open-letter');
  const gate = $('#code-gate'); const form = $('#code-form'); const input = $('#access-code'); const error = $('#code-error');
  const startOpening = () => {
    gate.hidden = true;
    intro.classList.add('is-opening'); button.disabled = true;
    window.setTimeout(() => intro.classList.add('is-card'), reduceMotion ? 250 : 1300);
    window.setTimeout(() => { intro.classList.add('is-finished'); storyEl.removeAttribute('aria-hidden'); window.scrollTo(0, 0); }, reduceMotion ? 400 : 2600);
  };
  button.addEventListener('click', () => {
    if (intro.classList.contains('is-opening')) return;
    if (window.__serverUnlocked) { startOpening(); return; }
    gate.hidden = false; input.value = ''; error.textContent = ''; window.setTimeout(() => input.focus(), 20);
  });
  form.addEventListener('submit', event => {
    event.preventDefault();
    if (window.__serverUnlocked) startOpening();
    else { error.textContent = 'Bitte öffne den Brief über die sichere Startseite.'; }
  });
  if (window.__serverUnlocked) { gate.hidden = true; }
}

function interactions() {
  $all('.cat-card').forEach(card => card.addEventListener('click', () => { $('#cat-message').textContent = card.dataset.cat; }));
  $('#brunhilde').addEventListener('click', () => { $('#brunhilde-message').innerHTML = '<p>Brunhilde, mein Gemüt verlangt nach dem Anblick Eures holden Antlitzes.</p><small>Ja. Wir sind manchmal komplett bescheuert. 😂</small>'; });
  $('#final-button').addEventListener('click', () => { $('#last-message').innerHTML = '<h2>Du bist mein Lieblingsmensch. <em>♥</em></h2><p>Ende. Wirklich jetzt.<br>… wahrscheinlich.</p><small>Schnecke.</small>'; $('#last-message').classList.add('is-open'); });
  if (!reduceMotion && matchMedia('(pointer:fine)').matches) {
    document.addEventListener('pointermove', ({ clientX, clientY }) => { document.documentElement.style.setProperty('--mx', `${clientX / innerWidth * 100}%`); document.documentElement.style.setProperty('--my', `${clientY / innerHeight * 100}%`); });
  }
}

populateContent(); openLetter(); revealOnScroll(); interactions();
