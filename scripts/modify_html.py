#!/usr/bin/env python3
"""
Script para modificar o HTML:
- Substitui o player de vídeo pelo novo VTurb
- Remove links de checkouts antigos
- Insere placeholder para novo checkout (quando disponível)
"""

import re
import sys

def modify_html(html: str) -> str:

    # ── 1. Adiciona preloads do VTurb no <head> ──────────────────────────────
    vturb_head = """  <script>!function(i,n){i._plt=i._plt||(n&&n.timeOrigin?n.timeOrigin+n.now():Date.now())}(window,performance);</script>
  <link rel="preload" href="https://scripts.converteai.net/1f606299-8601-495f-853a-fa04328be8e4/players/6a5e5bbd263a6954d36693a8/v4/player.js" as="script">
  <link rel="preload" href="https://scripts.converteai.net/lib/js/smartplayer-wc/v4/smartplayer.js" as="script">
  <link rel="preload" href="https://cdn.converteai.net/1f606299-8601-495f-853a-fa04328be8e4/6a5e5bb96b019bbab4b49883/main.m3u8" as="fetch">
  <link rel="dns-prefetch" href="https://cdn.converteai.net">
  <link rel="dns-prefetch" href="https://scripts.converteai.net">
  <link rel="dns-prefetch" href="https://images.converteai.net">
  <link rel="dns-prefetch" href="https://license.vturb.com">"""

    # Insere preloads antes do </head> se ainda não existirem
    if "converteai.net/1f606299-8601-495f-853a-fa04328be8e4/players/6a5e5bbd263a6954d36693a8" not in html:
        html = re.sub(r'(</head>)', vturb_head + r'\n\1', html, count=1, flags=re.IGNORECASE)

    # ── 2. Novo player VTurb ─────────────────────────────────────────────────
    new_player = """<vturb-smartplayer id="vid-6a5e5bbd263a6954d36693a8" style="display: block; margin: 0 auto; width: 100%; max-width: 400px;"><div class="vturb-player-placeholder" style="position: relative; width: 100%; padding: 178.21782178217822% 0 0; z-index: 0; background-color: black;"></div></vturb-smartplayer>
<script type="text/javascript">
  var s=document.createElement("script");
  s.src="https://scripts.converteai.net/1f606299-8601-495f-853a-fa04328be8e4/players/6a5e5bbd263a6954d36693a8/v4/player.js";
  s.async=!0;
  document.head.appendChild(s);
</script>"""

    # Remove qualquer player VTurb antigo (vturb-smartplayer)
    html = re.sub(
        r'<vturb-smartplayer[\s\S]*?</vturb-smartplayer>\s*(<script[\s\S]*?converteai\.net[\s\S]*?</script>)?',
        new_player,
        html,
        count=1,
        flags=re.IGNORECASE
    )

    # Remove iframe de vídeo (YouTube / Vimeo / genérico) se não houver vturb
    if '<vturb-smartplayer' not in html:
        html = re.sub(
            r'<iframe[^>]*(youtube\.com|youtu\.be|vimeo\.com|player\.vimeo|facebook\.com/plugins/video)[^>]*>[\s\S]*?</iframe>',
            new_player,
            html,
            count=1,
            flags=re.IGNORECASE
        )

    # ── 3. Remove links de checkout antigos ─────────────────────────────────
    # Padrões comuns de checkouts (Hotmart, Eduzz, Monetizze, PerfectPay, Kiwify, Pepper, etc.)
    checkout_patterns = [
        r'pay\.hotmart\.com',
        r'checkout\.hotmart\.com',
        r'hotmart\.com/product',
        r'eduzz\.com',
        r'monetizze\.com\.br',
        r'perfectpay\.com\.br',
        r'kiwify\.com\.br',
        r'pepper\.com\.br',
        r'payt\.com\.br',
        r'lastlink\.com',
        r'app\.cakto\.com\.br',
        r'clkdmg\.site',
        r'go\.hotmart\.com',
    ]

    combined = '|'.join(checkout_patterns)

    # Remove <a href="...checkout...">...</a> completamente
    html = re.sub(
        r'<a\s[^>]*href=["\'][^"\']*(?:' + combined + r')[^"\']*["\'][^>]*>[\s\S]*?</a>',
        '<!-- CHECKOUT_PLACEHOLDER -->',
        html,
        flags=re.IGNORECASE
    )

    return html


if __name__ == "__main__":
    input_file  = sys.argv[1] if len(sys.argv) > 1 else "index.html"
    output_file = sys.argv[2] if len(sys.argv) > 2 else input_file

    with open(input_file, "r", encoding="utf-8", errors="ignore") as f:
        content = f.read()

    modified = modify_html(content)

    with open(output_file, "w", encoding="utf-8") as f:
        f.write(modified)

    print(f"✓ HTML modificado salvo em: {output_file}")
