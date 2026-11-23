---
layout: home
title: Documentation OpenMandriva
nav_order: 1
page_id: home
lang: fr
source_lang: en
permalink: /
card_columns: 2
---
Bienvenue dans la documentation d'OpenMandriva !

<div class="home-cards cols-{{ page.card_columns }}">
  {% for card in site.data.home_cards %}
  <div class="home-card">
    <h3>
      {% if card.base_url %}
      <a href="{{ card.base_url | append: '/' | relative_url }}">{{ card.title }}</a>
      {% else %}
      {{ card.title }}
      {% endif %}
    </h3>
    <div class="description">{{ card.description }}</div>
    <ul>
      {% for link in card.links %}
      {% if link.url %}
        <li><a href="{{ link.url | relative_url }}">{{ link.name }}</a></li>
      {% elsif link.base_url %}
        <li><a href="{{ link.base_url | append: '/' | relative_url }}">{{ link.name }}</a></li>
      {% endif %}
      {% endfor %}
    </ul>
  </div>
  {% endfor %}
</div>
