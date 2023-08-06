{% if grains.os_family == "Debian" %}
include:
  - https
  - asterisk
  - postgres
  - odoo
  - nginx
  - agent
{% else %}
not-yet-supported:
  test.show_notification:
    - text: Sorry, {{ grains.os_family }} is not supported yet
{% endif %}
