include:
  - ..letsencrypt

letsencrypt-webroot-dir:
  file.directory:
    - name: /var/spool/letsencrypt
    - require_in:
        - letsencrypt-config

letsencrypt-set-domain:
  grains.present:
    - name: letsencrypt:domainsets:odoopbx
    - value:
        - '{{ salt['config.get']('fqdn') }}'
    - force: yes
    - require_in:
        - letsencrypt-config

