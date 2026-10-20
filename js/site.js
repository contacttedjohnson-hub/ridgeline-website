/* Ridgeline Realty site behavior. Small on purpose.
   1. Phone menu open/close.
   2. Marks the current page in the menu.
   3. Time-slot buttons on the schedule form.
   4. Forms: if no form service is wired up yet, opens the visitor's
      email app with the answers filled in, so the form works on day one. */

(function () {
  // 1. Phone menu
  var toggle = document.querySelector('.nav-toggle');
  var nav = document.querySelector('header nav');
  if (toggle && nav) {
    toggle.addEventListener('click', function () {
      var open = nav.classList.toggle('open');
      toggle.setAttribute('aria-expanded', open ? 'true' : 'false');
    });
  }

  // 2. Current page highlight
  var here = location.pathname.split('/').pop() || 'index.html';
  document.querySelectorAll('header nav a').forEach(function (a) {
    var target = a.getAttribute('href').split('#')[0] || 'index.html';
    if (target === here && !a.classList.contains('cta')) a.classList.add('current');
  });

  // 3. Time slots
  document.querySelectorAll('.slots').forEach(function (group) {
    var hidden = group.parentNode.querySelector('input[name="time"]');
    group.querySelectorAll('.slot').forEach(function (btn) {
      btn.addEventListener('click', function (e) {
        e.preventDefault();
        group.querySelectorAll('.slot').forEach(function (b) { b.classList.remove('on'); });
        btn.classList.add('on');
        if (hidden) hidden.value = btn.textContent.trim();
      });
    });
  });

  // 4. Forms
  document.querySelectorAll('form[data-email]').forEach(function (form) {
    form.addEventListener('submit', function (e) {
      var action = form.getAttribute('action') || '';
      if (action.indexOf('YOUR_FORM_ID') === -1 && action !== '') return; // a real service is wired up, let it post
      e.preventDefault();
      var lines = [];
      form.querySelectorAll('input, select, textarea').forEach(function (el) {
        if (!el.name || el.type === 'submit') return;
        var label = el.name.replace(/_/g, ' ');
        lines.push(label + ': ' + (el.value || ''));
      });
      var subject = form.getAttribute('data-subject') || 'Website request';
      var mailto = 'mailto:' + form.getAttribute('data-email') +
        '?subject=' + encodeURIComponent(subject) +
        '&body=' + encodeURIComponent(lines.join('\n'));
      window.location.href = mailto;
      var sent = form.querySelector('.sent');
      if (sent) sent.style.display = 'block';
    });
  });
})();
