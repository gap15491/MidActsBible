# Serve the reordered KJV as a static site with Caddy.
FROM caddy:2-alpine
COPY Caddyfile /etc/caddy/Caddyfile
COPY index.html chart.html /usr/share/caddy/
