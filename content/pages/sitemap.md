---
title: Sitemap
permalink: /sitemap/
---

## Pages

{% for link in site.data.navigation.main %}
- [{{ link.title }}]({{ link.url | relative_url }})
{% endfor %}

## Research

{% assign published_papers = site.papers | where_exp: 'paper', 'paper.published != false' %}
{% for paper in published_papers %}
{% assign paper_href = paper.paper_url %}
{% assign paper_url_start = paper_href | slice: 0, 1 %}
{% if paper_url_start == '/' %}{% assign paper_href = paper_href | relative_url %}{% endif %}
- {% if paper_href %}[{{ paper.title }}]({{ paper_href }}){% else %}{{ paper.title }}{% endif %}
{% endfor %}
