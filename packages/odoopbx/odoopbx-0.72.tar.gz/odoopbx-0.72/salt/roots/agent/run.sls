{% if grains.get('virtual') != "container" and grains.get('virtual_subtype') != "Docker" %}
agent-service:
  file:
    - managed
    - name: /etc/systemd/system/odoopbx-agent.service
    - source: salt://agent/agent.service
    - template: jinja
    - unless: file.exists /etc/systemd/system/odoopbx-agent.service
  service:
    - running
    - name: odoopbx-agent
    - enable: True
    - require:
      - pip: agent-install
      - pkg: agent-install
      - file: agent-service
{% endif %}
