---
title: Documentation OpenMandriva
layout: home
card_columns: 2
lang: fr
lang-exclusive: [fr]
permalink: /index.html
---
Bienvenue dans la documentation d'OpenMandriva !

<div class="home-cards cols-{{ page.card_columns }}">
  {% for card in site.data.home_cards %}
  <div class="home-card">
    <h3>
      {% if card.base_url %}
        {% assign fr_section_url = card.base_url | append: '/index.fr.html' %}
        {% assign fr_section = site.pages | where: "url", fr_section_url | first %}
        {% if fr_section %}
          <a href="{{ fr_section_url }}">{{ card.title }}</a>
        {% else %}
          <a href="{{ card.base_url }}/index.en.html">{{ card.title }}</a>
        {% endif %}
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
        {% assign fr_link_url = link.base_url | append: '.fr.html' %}
        {% assign fr_page = site.pages | where: "url", fr_link_url | first %}
        {% if fr_page %}
          <li><a href="{{ fr_link_url }}">{{ link.name }}</a></li>
        {% else %}
          <li><a href="{{ link.base_url }}.en.html">{{ link.name }}</a></li>
        {% endif %}
      {% endif %}
      {% endfor %}
    </ul>
  </div>
  {% endfor %}
</div>