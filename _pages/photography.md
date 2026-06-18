---
permalink: /photography/
title: "Photography"
author_profile: false
---
{% include base_path %}

No agenda here — I mostly just shoot for the vibe.

{% assign ordered = site.data.photo_order %}

<div class="photo-grid" id="photo-grid">
{% for name in ordered %}
  {% assign ar = site.data.photo_aspects[name] %}
  <a class="photo-grid__item" href="{{ base_path }}/images/photography/{{ name }}"{% if ar %} data-aspect="{{ ar }}"{% endif %}>
    <img src="{{ base_path }}/images/photography/{{ name }}" loading="lazy" alt="">
  </a>
{% endfor %}
{% comment %} fallback: photos added to the folder but not yet in the optimized order {% endcomment %}
{% assign photos = site.static_files | where_exp: "f", "f.path contains '/images/photography/'" %}
{% for photo in photos %}
  {% assign ext = photo.extname | downcase %}
  {% if ext == '.jpg' or ext == '.jpeg' or ext == '.png' or ext == '.webp' %}
    {% unless ordered contains photo.name %}
  <a class="photo-grid__item" href="{{ photo.path | prepend: base_path }}">
    <img src="{{ photo.path | prepend: base_path }}" loading="lazy" alt="">
  </a>
    {% endunless %}
  {% endif %}
{% endfor %}
</div>

<script>
(function () {
  var grid = document.getElementById('photo-grid');
  if (!grid) return;

  var GAP = 8;          // must match the CSS gap
  var TARGET = 300;     // target row height in px
  var MAX_LAST = 1.5;   // cap the last row's height (× TARGET) so it isn't huge
  var MAX_PER_ROW = 3;  // hard limit on photos per row

  var items = Array.prototype.slice.call(grid.children);

  function aspect(a) {
    var baked = parseFloat(a.getAttribute('data-aspect'));
    if (baked > 0) return baked;                 // known at build time — no crop, no reflow
    var img = a.querySelector('img');
    if (img.naturalWidth) return img.naturalWidth / img.naturalHeight;
    return 1.5;  // placeholder until a newly-added image loads
  }

  function size(a, w, h) {
    a.style.width = Math.floor(w) + 'px';
    a.style.height = Math.floor(h) + 'px';
  }

  // Flickr-style justified layout: fill each row to the full width,
  // letting the row height float around TARGET, capped at 3 photos per row.
  function layout() {
    var W = grid.clientWidth;
    if (!W) return;
    var row = [], sum = 0;

    for (var i = 0; i < items.length; i++) {
      var r = aspect(items[i]);
      row.push(items[i]); sum += r;
      var h = (W - (row.length - 1) * GAP) / sum;
      var filled = h <= TARGET;

      if (filled || row.length >= MAX_PER_ROW) {
        if (filled && row.length > 1) {
          var hPrev = (W - (row.length - 2) * GAP) / (sum - r);
          if (Math.abs(hPrev - TARGET) < Math.abs(h - TARGET)) {
            row.pop(); sum -= r;
            var hp = (W - (row.length - 1) * GAP) / sum;
            for (var k = 0; k < row.length; k++) size(row[k], aspect(row[k]) * hp, hp);
            row = [items[i]]; sum = r;
            continue;
          }
        }
        for (var m = 0; m < row.length; m++) size(row[m], aspect(row[m]) * h, h);
        row = []; sum = 0;
      }
    }
    if (row.length) {
      var hl = Math.min((W - (row.length - 1) * GAP) / sum, TARGET * MAX_LAST);
      for (var n = 0; n < row.length; n++) size(row[n], aspect(row[n]) * hl, hl);
    }
  }

  // Re-layout only if a not-yet-measured image loads, and on resize
  var raf;
  function schedule() { cancelAnimationFrame(raf); raf = requestAnimationFrame(layout); }
  items.forEach(function (a) {
    if (parseFloat(a.getAttribute('data-aspect')) > 0) return;
    var img = a.querySelector('img');
    if (!img.complete) {
      img.addEventListener('load', schedule);
      img.addEventListener('error', schedule);
    }
  });
  var t;
  window.addEventListener('resize', function () { clearTimeout(t); t = setTimeout(layout, 150); });
  layout();
})();
</script>
