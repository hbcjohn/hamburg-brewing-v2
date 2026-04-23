#!/usr/bin/env python3
"""
Batch-add Snipcart integration to all Hamburg Brewing HTML pages.
Usage: python3 add-snipcart.py [--api-key KEY]
"""
import os, re, sys, glob

PROJECT_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
API_KEY = sys.argv[2] if len(sys.argv) > 2 and sys.argv[1] == '--api-key' else 'YOUR_SNIPCART_PUBLIC_API_KEY'

def add_snipcart_to_head(content):
    """Add Snipcart CSS before closing </head>"""
    snipcart_css = '  <link rel="stylesheet" href="https://cdn.snipcart.com/themes/v3.0.31/default/snipcart.css" />\n'
    if 'snipcart.css' in content:
        return content
    content = content.replace('</head>', snipcart_css + '</head>')
    return content

def replace_cart_button(content):
    """Replace custom cart button with Snipcart checkout trigger"""
    old_cart = re.compile(
        r'<button id="cart-toggle" class="header-icon" aria-label="Cart">\s*'
        r'<svg[^>]*>.*?</svg>\s*'
        r'<span id="cart-count" class="cart-count" style="display:none">0</span>\s*'
        r'</button>',
        re.DOTALL
    )
    new_cart = '''<button class="header-icon snipcart-checkout" aria-label="Cart">
          <svg width="22" height="22" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
            <path d="M6 6h15l-1.5 9h-12z"/>
            <circle cx="9" cy="20" r="1"/>
            <circle cx="18" cy="20" r="1"/>
            <path d="M6 6L5 3H2"/>
          </svg>
          <span class="snipcart-items-count cart-count">0</span>
        </button>'''
    content = old_cart.sub(new_cart, content)
    return content

def remove_cart_drawer(content):
    """Remove custom cart drawer markup"""
    drawer_pattern = re.compile(
        r'<!-- Cart Drawer -->\s*'
        r'<div id="cart-overlay"[^>]*></div>\s*'
        r'<div id="cart-drawer"[^>]*>.*?</div>\s*'
        r'</div>',
        re.DOTALL
    )
    content = drawer_pattern.sub('', content)
    return content

def add_snipcart_scripts(content):
    """Add Snipcart JS and config div before closing </body>"""
    if 'snipcart.js' in content:
        return content
    
    snipcart_scripts = f'''  <script async src="https://cdn.snipcart.com/themes/v3.0.31/default/snipcart.js"></script>
  <div hidden id="snipcart" data-api-key="{API_KEY}" data-config-modal-style="side"></div>
'''
    
    content = content.replace('</body>', snipcart_scripts + '</body>')
    return content

def process_file(filepath):
    """Process a single HTML file"""
    with open(filepath, 'r') as f:
        content = f.read()
    
    original = content
    
    content = add_snipcart_to_head(content)
    content = replace_cart_button(content)
    content = remove_cart_drawer(content)
    content = add_snipcart_scripts(content)
    
    if content != original:
        with open(filepath, 'w') as f:
            f.write(content)
        print(f"  Updated: {os.path.basename(filepath)}")
        return True
    else:
        print(f"  Skipped: {os.path.basename(filepath)}")
        return False

def main():
    print(f"Adding Snipcart to Hamburg Brewing v2...")
    print(f"API Key: {'*' * 10 if API_KEY != 'YOUR_SNIPCART_PUBLIC_API_KEY' else API_KEY}")
    print()
    
    html_files = glob.glob(os.path.join(PROJECT_DIR, '*.html'))
    updated = 0
    
    for filepath in sorted(html_files):
        if process_file(filepath):
            updated += 1
    
    print(f"\nDone! Updated {updated} files.")
    print(f"\nTo use your real API key, run:")
    print(f"  python3 scripts/add-snipcart.py --api-key YOUR_KEY")

if __name__ == '__main__':
    main()
