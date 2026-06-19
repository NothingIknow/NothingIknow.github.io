---
permalink: /
title: "About me"
author_profile: false
redirect_from: 
  - /about/
  - /about.html
---
<img src="/images/IMG_2979.png" alt="Shuwei Li" class="about-photo">

<div class="about-intro" markdown="1">

My name is Shuwei Li (李书伟). I received my Ph.D. from the [National University of Singapore](https://www.nus.edu.sg/), where I was advised by Prof. [Robby T. Tan](https://tanrobby.github.io/). Prior to that, I received my bachelor’s degree from [Southeast University](https://www.seu.edu.cn/english/) and my master’s degree from [Boston University](https://www.bu.edu/).

My doctoral research focused on color constancy via deep learning. I find color fascinating because it lies at the boundary between the world as it is and the world as we perceive it.

Outside of research, I find my peace and freedom in driving alone at nightfall.

</div>

<p class="about-links">
  <a href="mailto:shuwei@u.nus.edu"><i class="fas fa-envelope" aria-hidden="true"></i> Email</a>
  <a href="https://scholar.google.com/citations?user=qOiTDoIAAAAJ&hl=en"><i class="ai ai-google-scholar" aria-hidden="true"></i> Google Scholar</a>
  <a href="https://github.com/NothingIknow"><i class="fab fa-github" aria-hidden="true"></i> GitHub</a>
</p>

## Publications

{% include base_path %}

{% for post in site.publications reversed %}
  {% unless post.hidden %}
    {% include archive-single.html %}
  {% endunless %}
{% endfor %}

## Photography

When I'm not working, I shoot [photos]({{ base_path }}/photography/) sometimes.