#!/usr/bin/env python3
"""Fix all Hamburg Brewing pages - standardize nav and footer"""
import os, re

BASE = "/home/walt/.openclaw/workspace/projects/hamburg-brewing"

# Read template
with open(f"{BASE}/.template.html") as f:
    TEMPLATE = f.read()

# Standard nav HTML
NAV_HTML = """      <li><a href="index.html">Home</a></li>
      <li><a href="about.html">About Us</a></li>
      <li><a href="book-your-event.html">Book Your Event</a></li>
      <li><a href="menu.html">Taproom Menu</a></li>
      <li><a href="beer.html">Beer + Hard Cider</a></li>
      <li><a href="merch.html">Shop</a></li>
      <li><a href="faqs.html">FAQs</a></li>
      <li><a href="contact.html">Contact</a></li>
      <li><a href="join-team.html">Join Our Team</a></li>
      <li><a href="donations.html">Donations</a></li>
      <li><a href="bus-policy.html">Bus &amp; Limo Policy</a></li>
      <li><a href="new-account.html">New Account Inquiry</a></li>
      <li><a href="live-music.html">Live Music</a></li>
      <li><a href="events.html">Upcoming Events</a></li>
      <li><a href="branding.html">Branding</a></li>
      <li><a href="holiday-parties.html">Holiday Parties</a></li>
      <li><a href="https://order.toasttab.com/online/hamburgbrewing" target="_blank" rel="noopener">Take Out</a></li>
      <li><a href="https://www.toasttab.com/catering/hamburgbrewing/" target="_blank" rel="noopener">Large Party + Catering</a></li>"""

# Standard footer HTML
FOOTER_HTML = """  <footer class="site-footer">
    <div class="container">
      <div class="footer-grid">
        <div class="footer-col">
          <h4>Menu</h4>
          <ul class="footer-links">
            <li><a href="about.html">About</a></li>
            <li><a href="contact.html">Contact Us</a></li>
            <li><a href="menu.html">Taproom Menu</a></li>
            <li><a href="https://order.toasttab.com/online/hamburgbrewing" target="_blank" rel="noopener">Take Out</a></li>
            <li><a href="https://www.toasttab.com/catering/hamburgbrewing/" target="_blank" rel="noopener">Large Party + Catering</a></li>
            <li><a href="book-your-event.html">Book Your Event</a></li>
            <li><a href="join-team.html">Join Our Team</a></li>
            <li><a href="live-music.html">Live Music</a></li>
            <li><a href="events.html">Upcoming Events</a></li>
            <li><a href="branding.html">Branding</a></li>
            <li><a href="donations.html">Donations</a></li>
            <li><a href="bus-policy.html">Bus + Limo Policy</a></li>
            <li><a href="faqs.html">FAQs</a></li>
            <li><a href="merch.html">Shop</a></li>
            <li><a href="#" onclick="document.getElementById('search-toggle').click();return false;">Search</a></li>
          </ul>
        </div>
        <div class="footer-col">
          <h4>Current Taproom Hours</h4>
          <p><em>Updated 4/8/26</em></p>
          <p>Monday – Tuesday: 4:00PM–10:00PM<br>Wednesday – Saturday: 12:00PM – 10:00PM<br>Sunday: 10:00AM – 8:00PM (Brunch 10am–12pm, Kitchen closed from 12–12:30pm)</p>
          <p><strong>Sun. May 10 – Mother's Day Breakfast 9am–11am – Reservations Required. Open for regular service 12:30pm–8pm</strong></p>
          <p>We do not take reservations, all seating first come first served.</p>
        </div>
        <div class="footer-col">
          <h4>Contact</h4>
          <p><a href="tel:7166493249">(716) 649-3249</a></p>
          <p>6553 Boston State Rd<br>Hamburg, NY 14075</p>
        </div>
        <div class="footer-col">
          <h4>Social</h4>
          <div class="social-links">
            <a href="https://facebook.com/hamburgbrewingcompany" target="_blank" rel="noopener" aria-label="Facebook"><svg width="20" height="20" viewBox="0 0 24 24" fill="currentColor"><path d="M24 12.073c0-6.627-5.373-12-12-12s-12 5.373-12 12c0 5.99 4.388 10.954 10.125 11.854v-8.385H7.078v-3.47h3.047V9.43c0-3.007 1.792-4.669 4.533-4.669 1.312 0 2.686.235 2.686.235v2.953H15.83c-1.491 0-1.956.925-1.956 1.874v2.25h3.328l-.532 3.47h-2.796v8.385C19.612 23.027 24 18.062 24 12.073z"/></svg></a>
            <a href="https://instagram.com/hamburgbrewing" target="_blank" rel="noopener" aria-label="Instagram"><svg width="20" height="20" viewBox="0 0 24 24" fill="currentColor"><path d="M12 2.163c3.204 0 3.584.012 4.85.07 3.252.148 4.771 1.691 4.919 4.919.058 1.265.069 1.645.069 4.849 0 3.205-.012 3.584-.069 4.849-.149 3.225-1.664 4.771-4.919 4.919-1.266.058-1.644.07-4.85.07-3.204 0-3.584-.012-4.849-.07-3.26-.149-4.771-1.699-4.919-4.92-.058-1.265-.07-1.644-.07-4.849 0-3.204.013-3.583.07-4.849.149-3.227 1.664-4.771 4.919-4.919 1.266-.057 1.645-.069 4.849-.069zM12 0C8.741 0 8.333.014 7.053.072 2.695.272.273 2.69.073 7.052.014 8.333 0 8.741 0 12c0 3.259.014 3.668.072 4.948.2 4.358 2.618 6.78 6.98 6.98C8.333 23.986 8.741 24 12 24c3.259 0 3.668-.014 4.948-.072 4.354-.2 6.782-2.618 6.979-6.98.059-1.28.073-1.689.073-4.948 0-3.259-.014-3.667-.072-4.947-.196-4.354-2.617-6.78-6.979-6.98C15.668.014 15.259 0 12 0zm0 5.838a6.162 6.162 0 100 12.324 6.162 6.162 0 000-12.324zM12 16a4 4 0 110-8 4 4 0 010 8zm6.406-11.845a1.44 1.44 0 100 2.881 1.44 1.44 0 000-2.881z"/></svg></a>
            <a href="https://twitter.com/HamburgBrewing" target="_blank" rel="noopener" aria-label="Twitter"><svg width="20" height="20" viewBox="0 0 24 24" fill="currentColor"><path d="M18.244 2.25h3.308l-7.227 8.26 8.502 11.24H16.17l-5.214-6.817L4.99 21.75H1.68l7.73-8.835L1.254 2.25H8.08l4.713 6.231zm-1.161 17.52h1.833L7.084 4.126H5.117z"/></svg></a>
          </div>
        </div>
      </div>
      <div class="footer-bottom">
        <p>© 2026 Hamburg Brewing Company. All rights reserved.</p>
      </div>
    </div>
  </footer>"""

# Find all HTML files
for fname in os.listdir(BASE):
    if not fname.endswith('.html') or fname.startswith('.'):
        continue
    fpath = os.path.join(BASE, fname)
    with open(fpath) as f:
        content = f.read()
    
    # Replace nav section
    nav_start = content.find('<nav id="main-nav"')
    nav_end = content.find('</nav>') + len('</nav>')
    if nav_start >= 0:
        old_nav = content[nav_start:nav_end]
        content = content.replace(old_nav, f'<nav id="main-nav" class="main-nav">\n    <ul>\n{NAV_HTML}\n    </ul>\n  </nav>')
    
    # Replace footer section
    footer_start = content.find('<footer class="site-footer"')
    if footer_start >= 0:
        # Find where footer ends (before closing </body> or before cart/search overlays)
        remaining = content[footer_start:]
        footer_end_rel = remaining.find('  </footer>') + len('  </footer>')
        old_footer = content[footer_start:footer_start+footer_end_rel]
        content = content.replace(old_footer, FOOTER_HTML)
    
    with open(fpath, 'w') as f:
        f.write(content)
    print(f"Updated {fname}")

print("\nDone! All pages standardized.")
