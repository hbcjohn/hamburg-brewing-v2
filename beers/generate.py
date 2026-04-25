#!/usr/bin/env python3
"""Generate beer detail pages for Hamburg Brewing v2"""

import os

# Beer data
beers = [
    {
        "id": "louie-ipa",
        "name": "Louie IPA",
        "style": "India Pale Ale",
        "tagline": "Bold. Bright. Unmistakable.",
        "abv": "6.9%",
        "ibu": "55",
        "srm": "Golden Amber",
        "availability": "Year-Round",
        "packaging": "12oz 6-Pack Cans",
        "description": "This IPA features a soft mouthfeel, a hint of bitterness, and a burst of fruity aromas from Mosaic and Amarillo hops. Louie is our flagship beer—the one that started it all. Named after a legend, brewed for the bold.",
        "icon": "🍺",
        "tasting_notes": ["Tropical Fruit", "Citrus", "Pine", "Floral", "Biscuit Malt"],
        "pairings": [
            {"icon": "🍔", "name": "Burgers"},
            {"icon": "🌮", "name": "Tacos"},
            {"icon": "🍕", "name": "Pizza"},
            {"icon": "🧀", "name": "Sharp Cheddar"},
            {"icon": "🌶️", "name": "Spicy Wings"},
            {"icon": "🥗", "name": "Citrus Salad"},
        ],
        "seasonal": False,
        "type": "Beer"
    },
    {
        "id": "lake-view-lager",
        "name": "Lake View Lager",
        "style": "Lager",
        "tagline": "Crisp. Clean. Classic.",
        "abv": "5.2%",
        "ibu": "18",
        "srm": "Pale Gold",
        "availability": "Year-Round",
        "packaging": "12oz 6-Pack & 12-Pack Cans",
        "description": "A crisp, refreshing lager created for everyday life. Whether you're on the boat, at the game, or on your porch—Lake View is the perfect companion. Clean malt flavor with a subtle hop finish.",
        "icon": "🍺",
        "tasting_notes": ["Cracker Malt", "Light Honey", "Noble Hops", "Clean Finish", "Crisp"],
        "pairings": [
            {"icon": "🐟", "name": "Fish Fry"},
            {"icon": "🍗", "name": "Chicken"},
            {"icon": "🌭", "name": "Brats"},
            {"icon": "🥨", "name": "Pretzels"},
            {"icon": "🥗", "name": "Garden Salad"},
            {"icon": "🍋", "name": "Lemon Chicken"},
        ],
        "seasonal": False,
        "type": "Beer"
    },
    {
        "id": "berry-sneaky",
        "name": "Berry Sneaky",
        "style": "Fruited Sour Ale",
        "tagline": "Sweet. Tart. Sneaky Good.",
        "abv": "7.2%",
        "ibu": "8",
        "srm": "Deep Purple",
        "availability": "Year-Round",
        "packaging": "12oz 6-Pack Cans",
        "description": "This sour is packed with Blackberry, Blueberry, Raspberry, Strawberry and Milk Sugar. Berry Sneaky hides its 7.2% ABV behind a wall of fruity sweetness and tart punch. Don't let the pretty color fool you.",
        "icon": "🫐",
        "tasting_notes": ["Blackberry", "Blueberry", "Raspberry", "Strawberry", "Lactose Sweetness", "Tart Finish"],
        "pairings": [
            {"icon": "🍰", "name": "Cheesecake"},
            {"icon": "🍫", "name": "Dark Chocolate"},
            {"icon": "🧀", "name": "Goat Cheese"},
            {"icon": "🍦", "name": "Vanilla Ice Cream"},
            {"icon": "🥗", "name": "Arugula Salad"},
            {"icon": "🍑", "name": "Stone Fruit"},
        ],
        "seasonal": False,
        "type": "Beer"
    },
    {
        "id": "big-lou",
        "name": "Big Lou",
        "style": "Double India Pale Ale",
        "tagline": "Double the Lou. Double the Flavor.",
        "abv": "9.0%",
        "ibu": "80",
        "srm": "Deep Gold",
        "availability": "Year-Round",
        "packaging": "19.2oz Single Cans",
        "description": "If you're a fan of our Louie IPA, you'll be an even bigger fan of Big Lou! We've doubled down on the flavor, mouthfeel and aroma of our flagship IPA. Massive hop presence meets big malt backbone in this bold double IPA.",
        "icon": "🍺",
        "tasting_notes": ["Resinous Pine", "Tropical Fruit", "Grapefruit", "Caramel Malt", "Dank", "Bitter Finish"],
        "pairings": [
            {"icon": "🥩", "name": "Steak"},
            {"icon": "🍔", "name": "Double Burger"},
            {"icon": "🌶️", "name": "Hot Wings"},
            {"icon": "🧀", "name": "Blue Cheese"},
            {"icon": "🍕", "name": "Meat Lovers Pizza"},
            {"icon": "🍖", "name": "BBQ Ribs"},
        ],
        "seasonal": False,
        "type": "Beer"
    },
    {
        "id": "irish-red",
        "name": "Irish Red",
        "style": "Irish Style Red Ale",
        "tagline": "Across the Pond. Down the Street.",
        "abv": "4.8%",
        "ibu": "22",
        "srm": "Ruby Red",
        "availability": "Seasonal (Spring)",
        "packaging": "12oz 6-Pack Cans",
        "description": "A smooth malty ale backed by a good dusting of roasted barley, just like the ones across the pond. Irish Red delivers caramel and toffee notes with a dry, clean finish that keeps you coming back.",
        "icon": "🍺",
        "tasting_notes": ["Caramel", "Toffee", "Roasted Barley", "Biscuit", "Malty Sweetness", "Dry Finish"],
        "pairings": [
            {"icon": "🌽", "name": "Corned Beef"},
            {"icon": "🥔", "name": "Shepherd's Pie"},
            {"icon": "🧀", "name": "Irish Cheddar"},
            {"icon": "🍖", "name": "Roast Pork"},
            {"icon": "🍞", "name": "Soda Bread"},
            {"icon": "🥩", "name": "Beef Stew"},
        ],
        "seasonal": True,
        "type": "Beer"
    },
    {
        "id": "summer-lager",
        "name": "Summer Lager",
        "style": "Lager with a Kiss of Lime",
        "tagline": "Sunshine in a Can.",
        "abv": "4.2%",
        "ibu": "12",
        "srm": "Pale Straw",
        "availability": "Seasonal (Summer)",
        "packaging": "12oz 6-Pack Cans",
        "description": "A simple and easy-drinking beer with a kiss of lime. Summer Lager is your dockside companion, your beach buddy, your porch-sittin' partner. Crack one open and let the sunshine in.",
        "icon": "🍺",
        "tasting_notes": ["Lime Zest", "Crisp Malt", "Light Citrus", "Refreshing", "Clean", "Bright"],
        "pairings": [
            {"icon": "🌮", "name": "Fish Tacos"},
            {"icon": "🍤", "name": "Shrimp"},
            {"icon": "🍉", "name": "Watermelon"},
            {"icon": "🥗", "name": "Ceviche"},
            {"icon": "🍋", "name": "Lemon Herb Chicken"},
            {"icon": "🧀", "name": "Queso Fresco"},
        ],
        "seasonal": True,
        "type": "Beer"
    },
    {
        "id": "oktoberfest",
        "name": "Oktoberfest",
        "style": "Märzen Lager",
        "tagline": "Prost!",
        "abv": "5.7%",
        "ibu": "24",
        "srm": "Copper Amber",
        "availability": "Seasonal (Fall)",
        "packaging": "12oz 6-Pack Cans",
        "description": "Big malty flavor from Vienna style malts fades away to a clean bitterness from Perle hops for a full-flavored and balanced experience. Our Oktoberfest pays homage to tradition while keeping things distinctly Hamburg.",
        "icon": "🍺",
        "tasting_notes": ["Toasted Malt", "Caramel", "Noble Hops", "Clean Bitterness", "Bready", "Smooth"],
        "pairings": [
            {"icon": "🌭", "name": "Bratwurst"},
            {"icon": "🥨", "name": "Pretzels"},
            {"icon": "🧀", "name": "Beer Cheese"},
            {"icon": "🍗", "name": "Roast Chicken"},
            {"icon": "🥔", "name": "Potato Pancakes"},
            {"icon": "🍎", "name": "Apple Strudel"},
        ],
        "seasonal": True,
        "type": "Beer"
    },
    {
        "id": "frosty-the-ipa",
        "name": "Frosty the IPA",
        "style": "India Pale Ale",
        "tagline": "This Ain't No Fairy Tale.",
        "abv": "5.5%",
        "ibu": "50",
        "srm": "Golden Orange",
        "availability": "Seasonal (Winter)",
        "packaging": "12oz 6-Pack Cans",
        "description": "This is no fairytale, our remarkably crushable winter IPA is loaded with bright citrusy Mosaic and Simcoe hops to get you through the cold. Frosty brings the warmth when you need it most.",
        "icon": "❄️",
        "tasting_notes": ["Citrus", "Pine", "Tropical Fruit", "Mosaic Hops", "Simcoe Hops", "Crushable"],
        "pairings": [
            {"icon": "🍗", "name": "Turkey"},
            {"icon": "🥩", "name": "Prime Rib"},
            {"icon": "🧀", "name": "Aged Gouda"},
            {"icon": "🥣", "name": "Butternut Squash Soup"},
            {"icon": "🍯", "name": "Honey Glazed Ham"},
            {"icon": "🥧", "name": "Pot Pie"},
        ],
        "seasonal": True,
        "type": "Beer"
    },
    {
        "id": "lil-guy",
        "name": "Lil Guy",
        "style": "Little IPA",
        "tagline": "Fat Flavor. Little Can.",
        "abv": "3.9%",
        "ibu": "35",
        "srm": "Pale Gold",
        "availability": "Year-Round",
        "packaging": "12oz Can 12-Pack",
        "description": "That's it, it's go time for fat flavor in a little can with this highly drinkable 3.9% IPA. Ya we caught a niner in there. All the hop flavor you love, without the heavy ABV. Sessionable and satisfying.",
        "icon": "🍺",
        "tasting_notes": ["Light Citrus", "Floral Hops", "Crisp Malt", "Sessionable", "Refreshing", "Easy Drinking"],
        "pairings": [
            {"icon": "🌭", "name": "Hot Dogs"},
            {"icon": "🍟", "name": "Fries"},
            {"icon": "🥗", "name": "Caesar Salad"},
            {"icon": "🍕", "name": "Flatbread"},
            {"icon": "🧀", "name": "Mozzarella"},
            {"icon": "🍿", "name": "Popcorn"},
        ],
        "seasonal": False,
        "type": "Beer"
    },
    {
        "id": "steel-city-red",
        "name": "Steel City Red",
        "style": "Red Ale",
        "tagline": "Forged in Erie. Enjoyed Everywhere.",
        "abv": "4.8%",
        "ibu": "20",
        "srm": "Ruby Copper",
        "availability": "Year-Round",
        "packaging": "12oz Can 12-Pack",
        "description": "A smooth red ale brewed with roasted barley and the spirit of the Steel City. This easy-drinking ale honors our neighbors in Erie, PA with every sip. Malty, smooth, and made for good times.",
        "icon": "🍺",
        "tasting_notes": ["Roasted Barley", "Caramel", "Toffee", "Smooth", "Malty", "Clean Finish"],
        "pairings": [
            {"icon": "🍔", "name": "Burgers"},
            {"icon": "🍗", "name": "Fried Chicken"},
            {"icon": "🧀", "name": "Smoked Gouda"},
            {"icon": "🍕", "name": "Pizza"},
            {"icon": "🥩", "name": "Meatloaf"},
            {"icon": "🌭", "name": "Kielbasa"},
        ],
        "seasonal": False,
        "type": "Beer"
    },
    {
        "id": "steel-city-pils",
        "name": "Steel City Pils",
        "style": "Pilsner Lager",
        "tagline": "Bright. Crisp. Steel Strong.",
        "abv": "4.5%",
        "ibu": "30",
        "srm": "Pale Straw",
        "availability": "Year-Round",
        "packaging": "12oz Can 12-Pack",
        "description": "Crafted with a harmonious blend of American malt and European hops, this beer delivers a bright, crisp flavor profile that's both refreshing and invigorating. It's perfect for enjoying no matter the season. Drink with pride.",
        "icon": "🍺",
        "tasting_notes": ["Crisp", "Clean", "Noble Hops", "Light Malt", "Refreshing", "Bright"],
        "pairings": [
            {"icon": "🐟", "name": "Perch Fry"},
            {"icon": "🌭", "name": "Dogs"},
            {"icon": "🥨", "name": "Pretzels"},
            {"icon": "🧀", "name": "Swiss Cheese"},
            {"icon": "🥗", "name": "Cucumber Salad"},
            {"icon": "🍤", "name": "Calamari"},
        ],
        "seasonal": False,
        "type": "Beer"
    },
]

# Hard ciders
ciders = [
    {
        "id": "original-hard-cider",
        "name": "Original Hard Cider",
        "style": "Hard Cider",
        "tagline": "Crisp. Clean. Classic.",
        "abv": "6.0%",
        "ibu": "N/A",
        "srm": "Pale Gold",
        "availability": "Year-Round",
        "packaging": "12oz 6-Pack Cans",
        "description": "Crisp, clean, and refreshing flavor with just enough sweetness to remind you that it was born from fruit. Our original hard cider is the perfect introduction to the Hamburg Brewing cider family.",
        "icon": "🍎",
        "tasting_notes": ["Apple", "Crisp", "Clean", "Subtle Sweetness", "Refreshing", "Bright"],
        "pairings": [
            {"icon": "🧀", "name": "Brie"},
            {"icon": "🍖", "name": "Pork Chops"},
            {"icon": "🥗", "name": "Waldorf Salad"},
            {"icon": "🍰", "name": "Apple Pie"},
            {"icon": "🍗", "name": "Turkey"},
            {"icon": "🥜", "name": "Peanuts"},
        ],
        "seasonal": False,
        "type": "Hard Cider"
    },
    {
        "id": "blueberry-peach-cider",
        "name": "Blueberry Peach Hard Cider",
        "style": "Hard Cider",
        "tagline": "Juicy. Fruity. Unforgettable.",
        "abv": "6.0%",
        "ibu": "N/A",
        "srm": "Rose Gold",
        "availability": "Year-Round",
        "packaging": "12oz 6-Pack & 19.2oz Cans",
        "description": "Bursting with juicy notes of blueberries and a bouquet of sweet peach aroma. This cider is summer in a can—fruity, refreshing, and downright delightful.",
        "icon": "🫐",
        "tasting_notes": ["Blueberry", "Peach", "Juicy", "Fruity", "Sweet", "Refreshing"],
        "pairings": [
            {"icon": "🧀", "name": "Cream Cheese"},
            {"icon": "🍰", "name": "Peach Cobbler"},
            {"icon": "🥗", "name": "Spinach Salad"},
            {"icon": "🍗", "name": "BBQ Chicken"},
            {"icon": "🍫", "name": "White Chocolate"},
            {"icon": "🥞", "name": "Pancakes"},
        ],
        "seasonal": False,
        "type": "Hard Cider"
    },
    {
        "id": "nice-and-dry-cider",
        "name": "Nice and Dry Hard Cider",
        "style": "Hard Cider",
        "tagline": "Dry. Sophisticated. Smooth.",
        "abv": "6.0%",
        "ibu": "N/A",
        "srm": "Pale Yellow",
        "availability": "Year-Round",
        "packaging": "12oz 6-Pack Cans",
        "description": "You'll experience a pleasant balance between acidity and sourness with a hidden touch of sweetness. Nice and Dry is for those who appreciate the finer things—complex, nuanced, and never too sweet.",
        "icon": "🍏",
        "tasting_notes": ["Tart Apple", "Acidity", "Dry", "Subtle Sweetness", "Crisp", "Complex"],
        "pairings": [
            {"icon": "🧀", "name": "Aged Cheddar"},
            {"icon": "🐟", "name": "Salmon"},
            {"icon": "🥗", "name": "Arugula Salad"},
            {"icon": "🍖", "name": "Roast Pork"},
            {"icon": "🥜", "name": "Almonds"},
            {"icon": "🍋", "name": "Lemon Tart"},
        ],
        "seasonal": False,
        "type": "Hard Cider"
    },
    {
        "id": "pear-cider",
        "name": "Pear Hard Cider",
        "style": "Hard Cider",
        "tagline": "Velvety. Bright. Refined.",
        "abv": "6.0%",
        "ibu": "N/A",
        "srm": "Pale Green-Gold",
        "availability": "Year-Round",
        "packaging": "12oz 6-Pack Cans",
        "description": "Velvety essence of ripe pears, perfectly blended with the bright, clean taste of orchard-fresh fruit. Pear Hard Cider is elegant, smooth, and surprisingly refreshing.",
        "icon": "🍐",
        "tasting_notes": ["Pear", "Orchard Fresh", "Velvety", "Smooth", "Clean", "Bright"],
        "pairings": [
            {"icon": "🧀", "name": "Gorgonzola"},
            {"icon": "🍖", "name": "Prosciutto"},
            {"icon": "🥗", "name": "Endive Salad"},
            {"icon": "🍰", "name": "Pear Tart"},
            {"icon": "🍗", "name": "Roast Duck"},
            {"icon": "🥜", "name": "Walnuts"},
        ],
        "seasonal": False,
        "type": "Hard Cider"
    },
    {
        "id": "strawberry-cider",
        "name": "Strawberry Hard Cider",
        "style": "Hard Cider",
        "tagline": "Sweet. Aromatic. Summery.",
        "abv": "6.0%",
        "ibu": "N/A",
        "srm": "Rose Pink",
        "availability": "Seasonal (Summer)",
        "packaging": "12oz 6-Pack Cans",
        "description": "Each sip envelops your senses with the sweet aromatic flavors of ripe strawberries and fresh apples. Strawberry Hard Cider is summer romance in liquid form.",
        "icon": "🍓",
        "tasting_notes": ["Strawberry", "Sweet", "Aromatic", "Fresh Apple", "Fruity", "Smooth"],
        "pairings": [
            {"icon": "🧀", "name": "Mascarpone"},
            {"icon": "🍰", "name": "Shortcake"},
            {"icon": "🥗", "name": "Spinach Salad"},
            {"icon": "🍫", "name": "Dark Chocolate"},
            {"icon": "🍦", "name": "Ice Cream"},
            {"icon": "🥞", "name": "Waffles"},
        ],
        "seasonal": True,
        "type": "Hard Cider"
    },
    {
        "id": "pomegranate-cider",
        "name": "Pomegranate Hard Cider",
        "style": "Hard Cider",
        "tagline": "Rich. Tangy. Unique.",
        "abv": "6.0%",
        "ibu": "N/A",
        "srm": "Deep Ruby",
        "availability": "Seasonal (Fall/Winter)",
        "packaging": "12oz 6-Pack Cans",
        "description": "A crisp and refreshing blend of rich sweetness with a subtle tang. Pomegranate Hard Cider brings something special to the table—complex, vibrant, and totally unique.",
        "icon": "🫐",
        "tasting_notes": ["Pomegranate", "Rich Sweetness", "Subtle Tang", "Crisp", "Refreshing", "Vibrant"],
        "pairings": [
            {"icon": "🧀", "name": "Feta"},
            {"icon": "🥗", "name": "Mediterranean Salad"},
            {"icon": "🍖", "name": "Lamb"},
            {"icon": "🍰", "name": "Cheesecake"},
            {"icon": "🥜", "name": "Pistachios"},
            {"icon": "🍫", "name": "Milk Chocolate"},
        ],
        "seasonal": True,
        "type": "Hard Cider"
    },
]

# Combine all drinks
all_drinks = beers + ciders

# Read template
template_path = os.path.join(os.path.dirname(__file__), "template.html")
with open(template_path, "r") as f:
    template = f.read()

def get_related_beers(current_id, current_type):
    """Get 3 related drinks of the same type"""
    same_type = [d for d in all_drinks if d["type"] == current_type and d["id"] != current_id]
    related = same_type[:3]
    if len(related) < 3:
        other_type = [d for d in all_drinks if d["type"] != current_type and d["id"] != current_id]
        related.extend(other_type[:3 - len(related)])
    return related[:3]

def generate_page(drink):
    html = template
    
    # Basic replacements
    html = html.replace("{{BEER_NAME}}", drink["name"])
    html = html.replace("{{BEER_STYLE}}", drink["style"])
    html = html.replace("{{BEER_TAGLINE}}", drink["tagline"])
    html = html.replace("{{ABV}}", drink["abv"])
    html = html.replace("{{IBU}}", drink["ibu"])
    html = html.replace("{{SRM}}", drink["srm"])
    html = html.replace("{{AVAILABILITY}}", drink["availability"])
    html = html.replace("{{PACKAGING}}", drink["packaging"])
    html = html.replace("{{DESCRIPTION}}", drink["description"])
    html = html.replace("{{BEER_ICON}}", drink["icon"])
    html = html.replace("{{TYPE}}", drink["type"])
    
    # Seasonal badge
    if drink["seasonal"]:
        seasonal_html = f'\n        \u003cdiv class="seasonal-badge"\u003e\n          \u003csvg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" style="margin-right: 4px;"\u003e\n            \u003cpath d="M12 2v4M12 18v4M4.93 4.93l2.83 2.83M16.24 16.24l2.83 2.83M2 12h4M18 12h4M4.93 19.07l2.83-2.83M16.24 7.76l2.83-2.83"/\u003e\n          \u003c/svg\u003e\n          {drink["availability"]}\n        \u003c/div\u003e'
        html = html.replace("{{SEASONAL_BADGE}}", seasonal_html)
    else:
        html = html.replace("{{SEASONAL_BADGE}}", "")
    
    # Tasting notes
    tasting_html = "\n".join([f'            \u003cspan class="tasting-note"\u003e{note}\u003c/span\u003e' for note in drink["tasting_notes"]])
    html = html.replace("{{TASTING_NOTES}}", tasting_html)
    
    # Food pairings
    pairings_html = "\n".join([
        f'            \u003cdiv class="food-pairing"\u003e\n              \u003cspan class="food-pairing-icon"\u003e{p["icon"]}\u003c/span\u003e\n              \u003cspan class="food-pairing-name"\u003e{p["name"]}\u003c/span\u003e\n            \u003c/div\u003e'
        for p in drink["pairings"]
    ])
    html = html.replace("{{FOOD_PAIRINGS}}", pairings_html)
    
    # Related beers
    related = get_related_beers(drink["id"], drink["type"])
    related_html = "\n".join([
        f'        \u003ca href="{r["id"]}.html" class="related-beer-card"\u003e\n          \u003cdiv class="related-beer-card-image"\u003e\n            \u003cspan style="position: relative; z-index: 1;"\u003e{r["icon"]}\u003c/span\u003e\n          \u003c/div\u003e\n          \u003cdiv class="related-beer-card-info"\u003e\n            \u003ch3\u003e{r["name"]}\u003c/h3\u003e\n            \u003cp\u003e{r["style"]} • {r["abv"]} ABV\u003c/p\u003e\n          \u003c/div\u003e\n        \u003c/a\u003e'
        for r in related
    ])
    html = html.replace("{{RELATED_BEERS}}", related_html)
    
    # Hero image (placeholder gradient based on beer type)
    if "IPA" in drink["style"]:
        gradient = "linear-gradient(135deg, #d4a017, #8B6914)"
    elif "Lager" in drink["style"] or "Pils" in drink["style"]:
        gradient = "linear-gradient(135deg, #f0e68c, #daa520)"
    elif "Sour" in drink["style"]:
        gradient = "linear-gradient(135deg, #9370db, #4b0082)"
    elif "Red" in drink["style"]:
        gradient = "linear-gradient(135deg, #cd5c5c, #8b0000)"
    elif "Cider" in drink["type"]:
        gradient = "linear-gradient(135deg, #f4a460, #d2691e)"
    else:
        gradient = "linear-gradient(135deg, #b19460, #6b5b3e)"
    
    # Use real product image from media kit
    image_path = f"../images/beers/{drink['id']}.jpg"
    image_exists = os.path.exists(f"/home/walt/.openclaw/workspace/projects/hamburg-brewing-v2/images/beers/{drink['id']}.jpg")
    if image_exists:
        # Hero background
        html = html.replace('style="background-image: url(\'{{HERO_IMAGE}}\');"', f'style="background-image: url(\'{image_path}\'); background-size: contain; background-repeat: no-repeat; background-position: center; opacity: 0.15;"')
        # Main beer image section
        image_html = f'''<div class="beer-art-placeholder" style="background: none; padding: 0;">
            <img src="{image_path}" alt="{drink['name']}" style="width: 100%; height: 100%; object-fit: contain; border-radius: 12px;">
          </div>'''
        html = html.replace("{{BEER_IMAGE}}", image_html)
    else:
        # Fallback gradient
        if "IPA" in drink["style"]:
            gradient = "linear-gradient(135deg, #d4a017, #8B6914)"
        elif "Lager" in drink["style"] or "Pils" in drink["style"]:
            gradient = "linear-gradient(135deg, #f0e68c, #daa520)"
        elif "Sour" in drink["style"]:
            gradient = "linear-gradient(135deg, #9370db, #4b0082)"
        elif "Red" in drink["style"]:
            gradient = "linear-gradient(135deg, #cd5c5c, #8b0000)"
        elif "Cider" in drink["type"]:
            gradient = "linear-gradient(135deg, #f4a460, #d2691e)"
        else:
            gradient = "linear-gradient(135deg, #b19460, #6b5b3e)"
        html = html.replace('style="background-image: url(\'{{HERO_IMAGE}}\');"', f'style="background: {gradient};"')
        # Fallback image placeholder
        placeholder_html = f'''<div class="beer-art-placeholder">
            <span class="beer-art-icon">{drink['icon']}</span>
            <span class="beer-art-label">Artwork Coming Soon</span>
          </div>'''
        html = html.replace("{{BEER_IMAGE}}", placeholder_html)
    
    return html

# Generate all pages
output_dir = os.path.dirname(__file__)
for drink in all_drinks:
    filename = os.path.join(output_dir, f"{drink['id']}.html")
    html = generate_page(drink)
    with open(filename, "w") as f:
        f.write(html)
    print(f"Generated: {filename}")

print(f"\nGenerated {len(all_drinks)} beer/cider detail pages!")
