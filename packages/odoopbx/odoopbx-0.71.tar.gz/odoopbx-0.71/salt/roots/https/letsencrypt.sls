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

letsencrypt-activate-cert:
  file.symlink:
    - onlyif:
        fun: x509.read_certificate
        certificate: /etc/letsencrypt/live/odoopbx/cert.pem
    - name: /etc/odoopbx/pki/current
    - target: /etc/letsencrypt/live/odoopbx
