include:
  - ..letsencrypt

letsencrypt-webroot-dir:
  file.directory:
    - name: /var/spool/letsencrypt
    - require_in:
        - letsencrypt-config

letsencrypt-grains-update:
  grains.present:
    - name: letsencrypt:domainsets:odoopbx
    - value:
        - '{{ salt['config.get']('fqdn') }}'
    - force: yes

letsencrypt-grains-refresh:
  module.run:
    - name: saltutil.refresh_grains
    - reload_grains: true
    - require:
      - letsencrypt-grains-update
    - require_in:
      - letsencrypt-config

letsencrypt-activate-cert:
  file.symlink:
    - onlyif:
        fun: x509.read_certificate
        certificate: /etc/letsencrypt/live/odoopbx/cert.pem
    - name: /etc/odoopbx/pki/current
    - target: /etc/letsencrypt/live/odoopbx
