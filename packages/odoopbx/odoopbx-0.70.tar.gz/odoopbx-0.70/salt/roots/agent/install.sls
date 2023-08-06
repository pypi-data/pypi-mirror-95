{% from "agent/map.jinja" import agent with context %}

agent-pip-upgrade:
  cmd.run:
    - name: pip3 install --upgrade pip
    - reload_modules: true
    - onfail:
      - pip: agent-install

agent-install:
  pkg.installed:
    - pkgs: {{ agent.pkgs }}
    - refresh: true
  pip.installed:
    - pkgs:
      - jsonrpcserver
      - aiorun
      - ipsetpy
      - odoopbx
      - OdooRPC
      - https://github.com/litnimax/panoramisk/archive/master.zip
      - pastebin
      - setproctitle
      - terminado
      - tornado-httpclient-session
    - require:
      - pkg: agent-install
    - retry: True
    - reload_modules: True

agent-locale:
  locale.present:
    - name: en_US.UTF-8
