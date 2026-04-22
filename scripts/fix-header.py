import os

project_dir = '/home/walt/.openclaw/workspace/projects/hamburg-brewing'

old_header = '''      <div class="header-links" style="display:none;">
        <a href="index.html">Home</a>
        <a href="about.html">About</a>
        <a href="book-your-event.html">Book Your Event</a>
        <a href="beer.html">Beer + Hard Cider</a>
        <a href="merch.html">Shop</a>
      </div>
      <div class="header-right">'''

new_header = '''      <div class="header-right">'''

count = 0
for filename in os.listdir(project_dir):
    if filename.endswith('.html'):
        filepath = os.path.join(project_dir, filename)
        with open(filepath, 'r') as f:
            content = f.read()
        
        if old_header in content:
            content = content.replace(old_header, new_header)
            with open(filepath, 'w') as f:
                f.write(content)
            count += 1
            print(f"Updated: {filename}")

print(f"\nTotal files updated: {count}")
