import os
import re

project_dir = '/home/walt/.openclaw/workspace/projects/hamburg-brewing'

old_nav = '''  <nav id="main-nav" class="main-nav">
    <ul>
      <li><a href="index.html">Home</a></li>
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
      <li><a href="https://www.toasttab.com/catering/hamburgbrewing/" target="_blank" rel="noopener">Large Party + Catering</a></li>
    </ul>
  </nav>'''

new_nav = '''  <nav id="main-nav" class="main-nav">
    <ul>
      <li><a href="index.html">Home</a></li>
      <li class="has-submenu">
        <a href="#" class="submenu-toggle">About</a>
        <ul class="submenu">
          <li><a href="about.html">About Us</a></li>
          <li><a href="join-team.html">Join Our Team</a></li>
          <li><a href="contact.html">Contact Us</a></li>
          <li><a href="live-music.html">Live Music</a></li>
          <li><a href="events.html">Upcoming Events</a></li>
        </ul>
      </li>
      <li class="has-submenu">
        <a href="#" class="submenu-toggle">Book Your Event</a>
        <ul class="submenu">
          <li><a href="book-your-event.html">Book Your Event</a></li>
          <li><a href="holiday-parties.html">Holiday Parties</a></li>
        </ul>
      </li>
      <li><a href="menu.html">Taproom Menu</a></li>
      <li><a href="https://order.toasttab.com/online/hamburgbrewing" target="_blank" rel="noopener">Take Out</a></li>
      <li><a href="https://www.toasttab.com/catering/hamburgbrewing/" target="_blank" rel="noopener">Large Party + Catering</a></li>
      <li><a href="beer.html">Beer + Hard Cider</a></li>
      <li><a href="merch.html">Shop</a></li>
    </ul>
  </nav>'''

count = 0
for filename in os.listdir(project_dir):
    if filename.endswith('.html'):
        filepath = os.path.join(project_dir, filename)
        with open(filepath, 'r') as f:
            content = f.read()
        
        if old_nav in content:
            content = content.replace(old_nav, new_nav)
            with open(filepath, 'w') as f:
                f.write(content)
            count += 1
            print(f"Updated: {filename}")
        else:
            # Check if it already has the new nav
            if 'has-submenu' in content and 'submenu-toggle' in content:
                print(f"Already updated: {filename}")
            else:
                print(f"Pattern not found in: {filename}")

print(f"\nTotal files updated: {count}")
