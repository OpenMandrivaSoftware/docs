---
title: Home
layout: home
card_columns: 2
nav_order: 1
lang: en
lang-exclusive: [en]
---
Welcome to the OpenMandriva documentation!

<div class="home-cards cols-{{ page.card_columns }}">
  {% for card in site.data.home_cards %}
  <div class="home-card">
    <h3>
      {% if card.base_url %}
      <a href="{{ card.base_url }}/index.en.html">{{ card.title }}</a>
      {% else %}
      {{ card.title }}
      {% endif %}
    </h3>
    <div class="description">{{ card.description }}</div>
    <ul>
      {% for link in card.links %}
      {% if link.url %}
        <li><a href="{{ link.url }}">{{ link.name }}</a></li>
      {% elsif link.base_url %}
        <li><a href="{{ link.base_url }}.en.html">{{ link.name }}</a></li>
      {% endif %}
      {% endfor %}
    </ul>
  </div>
  {% endfor %}
</div>