# Нумерация страниц

Оригинал статьи: http://flask.pocoo.org/snippets/44/

## Flask

```Python
from flask import redirect

PER_PAGE = 20

@app.route('/users/', defaults={'page': 1})
@app.route('/users/page/<int:page>')
def show_users(page):
    count = count_all_users()
    users = get_users_for_page(page, PER_PAGE, count)
    if not users and page != 1:
        abort(404)
    pagination = Pagination(page, PER_PAGE, count)
    return render_template('users.html',
        pagination=pagination,
        users=users
    )
```

## Рендеринг

```html
{% macro render_pagination(pagination) %}
  <div class=pagination>
  {%- for page in pagination.iter_pages() %}
    {% if page %}
      {% if page != pagination.page %}
        <a href="{{ url_for_other_page(page) }}">{{ page }}</a>
      {% else %}
        <strong>{{ page }}</strong>
      {% endif %}
    {% else %}
      <span class=ellipsis>…</span>
    {% endif %}
  {%- endfor %}
  {% if pagination.has_next %}
    <a href="{{ url_for_other_page(pagination.page + 1)
      }}">Next &raquo;</a>
  {% endif %}
  </div>
{% endmacro %}
```
