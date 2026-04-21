# Hamburg Brewing - Migration Plan

## Current Site Analysis
**URL:** https://www.hamburgbrewing.com  
**Platform:** Shopify (hamburg-brewery.myshopify.com)  
**Theme:** Dark navy/charcoal + gold/tan accents  

### Pages Discovered (11)
1. **Homepage** - Hero slider, taproom hours, event promos (Playoffs, Mother's Day)
2. **About Us** - Brewery story, fireplace photo, mission statement
3. **Contact Us** - FAQ link, hours, party booking form
4. **FAQs** - Accordion categories (Taproom, Donations, The Beer) + live search
5. **Join Our Team** - Employment form
6. **Donations** - Donation request form
7. **Bus & Limo Policy** - Policy text
8. **New Account Inquiry** - Wholesale/distribution form
9. **Merch Collection** - Products (Gift Cards, Flannels, Hats)
10. **Cart** - Shopify cart
11. **Search** - Shopify search

### Features to Preserve
- [x] Age verification gate (21+)
- [x] Shopping cart + checkout (Stripe)
- [x] Product catalog (merch)
- [x] Newsletter signup (Mailchimp)
- [x] Taproom hours display
- [x] Event promotions (homepage slider)
- [x] FAQ accordion with search
- [x] Contact/booking forms
- [x] Dark theme + gold accents

### New Features to Add
- [ ] **Toast Integration** - Online food ordering
- [ ] **Stripe Payments** - Payment processing (already have account)
- [ ] **Gift Card Sales** - Digital gift cards
- [ ] **Improved SEO** - Structured data, meta tags
- [ ] **Performance** - Static site, CDN, image optimization
- [ ] **Accessibility** - WCAG 2.1 AA compliance

## Architecture

```
hamburg-brewing/
├── index.html              # Homepage
├── about.html              # About Us
├── contact.html            # Contact
├── faqs.html               # FAQs
├── join-team.html          # Join Our Team
├── donations.html          # Donations
├── bus-policy.html         # Bus & Limo Policy
├── new-account.html        # New Account Inquiry
├── merch.html              # Merch Collection
├── cart.html               # Shopping Cart
├── search.html             # Search
├── css/
│   └── styles.css          # Custom theme
├── js/
│   ├── main.js             # Core functionality
│   ├── cart.js             # Shopping cart (Stripe)
│   ├── age-gate.js         # Age verification
│   ├── toast-integration.js # Toast API
│   └── search.js           # Search functionality
├── images/                 # Downloaded assets
└── data/
    ├── products.json       # Product catalog
    └── faqs.json          # FAQ content
```

## Color Palette
- **Primary Dark:** #1a1a2e (navy/black)
- **Primary Gold:** #c9a227 (gold/tan)
- **Secondary Gold:** #d4af37 (lighter gold)
- **Text Light:** #f5f5f5 (off-white)
- **Text Muted:** #a0a0a0 (gray)
- **Accent:** #8b0000 (dark red for CTAs)
- **Background:** #0f0f0f (near black)

## Typography
- **Headings:** Oswald or similar bold sans-serif
- **Body:** Inter or similar clean sans-serif
- **Logo:** Custom/script font

## Shopping Cart Flow (Stripe)
1. Browse products → Add to cart
2. Cart sidebar/drawer
3. Checkout page
4. Stripe Elements for payment
5. Order confirmation

## Toast Integration Plan
- Toast Takeout API for online ordering
- Display food menu from Toast
- Integrate with cart/checkout
- Real-time availability

## Next Steps
1. [ ] Download all images/assets
2. [ ] Build HTML structure for all pages
3. [ ] Implement CSS theme
4. [ ] Add JavaScript functionality
5. [ ] Set up Stripe checkout
6. [ ] Integrate Toast API
7. [ ] Test all flows
8. [ ] Deploy to Cloudflare Pages
