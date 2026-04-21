#!/usr/bin/env node
/**
 * Hamburg Brewing Site Audit Script
 * Uses Playwright to crawl and document the entire Shopify site
 */

const { chromium } = require('playwright');
const fs = require('fs');
const path = require('path');

const BASE_URL = 'https://www.hamburgbrewing.com';
const OUTPUT_DIR = path.join(__dirname, '..', 'audit');

// Ensure output directories exist
const dirs = ['screenshots', 'html', 'data'];
dirs.forEach(d => {
  const dir = path.join(OUTPUT_DIR, d);
  if (!fs.existsSync(dir)) fs.mkdirSync(dir, { recursive: true });
});

const discoveredUrls = new Set();
const visitedUrls = new Set();
const pageData = [];

// URL patterns to crawl
const crawlPatterns = [
  /^\/$/,                              // homepage
  /^\/pages\/.+/,                      // pages
  /^\/collections\/.+/,               // collections
  /^\/products\/.+/,                  // products
  /^\/blogs\/.+/,                     // blog posts
  /^\/cart/,                          // cart
];

// URLs to skip
const skipPatterns = [
  /\/account/,
  /\/challenge/,
  /\/password/,
  /^mailto:/,
  /^tel:/,
];

async function shouldCrawl(url) {
  const parsed = new URL(url);
  if (parsed.hostname !== 'www.hamburgbrewing.com') return false;
  if (skipPatterns.some(p => p.test(parsed.pathname))) return false;
  return crawlPatterns.some(p => p.test(parsed.pathname));
}

async function extractLinks(page) {
  const links = await page.evaluate(() => {
    return Array.from(document.querySelectorAll('a[href]'))
      .map(a => a.href)
      .filter(href => href.startsWith('http'));
  });
  return [...new Set(links)];
}

async function analyzePageFeatures(page, url) {
  const features = await page.evaluate(() => {
    const data = {
      hasAgeGate: !!document.querySelector('[id*="age"], [class*="age"], [id*="21"], [class*="age-gate"]'),
      hasNewsletterPopup: !!document.querySelector('[class*="popup"], [class*="newsletter"]'),
      hasShoppingCart: !!document.querySelector('[class*="cart"], [id*="cart"]'),
      hasSearch: !!document.querySelector('form[action*="/search"], input[type="search"]'),
      hasVideo: document.querySelectorAll('video').length,
      hasCarousel: !!document.querySelector('[class*="carousel"], [class*="slider"], [class*="splide"]'),
      hasToastIntegration: document.body.innerHTML.toLowerCase().includes('toast') || 
                            !!document.querySelector('script[src*="toast"]'),
      forms: Array.from(document.querySelectorAll('form')).map(f => ({
        action: f.action,
        method: f.method,
        hasFileUpload: !!f.querySelector('input[type="file"]'),
        fields: Array.from(f.querySelectorAll('input, select, textarea')).map(i => ({
          type: i.type,
          name: i.name,
          required: i.required
        }))
      })),
      scripts: Array.from(document.querySelectorAll('script[src]')).map(s => s.src).filter(s => s.includes('shopify') || s.includes('stripe') || s.includes('toast')),
      sections: Array.from(document.querySelectorAll('[class*="section"], section')).map(s => s.className).filter(Boolean),
      images: Array.from(document.querySelectorAll('img')).map(img => ({
        src: img.src,
        alt: img.alt,
        isProduct: img.closest('[class*="product"]') !== null
      })),
      products: Array.from(document.querySelectorAll('[class*="product"]')).length,
      buttons: Array.from(document.querySelectorAll('button, .button, [class*="btn"]')).map(b => b.textContent?.trim()).filter(Boolean),
      meta: {
        title: document.title,
        description: document.querySelector('meta[name="description"]')?.content,
        ogImage: document.querySelector('meta[property="og:image"]')?.content
      }
    };
    return data;
  });
  return features;
}

async function capturePage(page, url) {
  const slug = url.replace(BASE_URL, '').replace(/[^a-zA-Z0-9]/g, '_') || 'home';
  const timestamp = new Date().toISOString().replace(/[:.]/g, '-');
  
  // Full page screenshot
  await page.screenshot({ 
    path: path.join(OUTPUT_DIR, 'screenshots', `${slug}_${timestamp}.png`),
    fullPage: true 
  });
  
  // Desktop viewport
  await page.setViewportSize({ width: 1920, height: 1080 });
  await page.screenshot({ 
    path: path.join(OUTPUT_DIR, 'screenshots', `${slug}_desktop.png`)
  });
  
  // Mobile viewport
  await page.setViewportSize({ width: 375, height: 812 });
  await page.screenshot({ 
    path: path.join(OUTPUT_DIR, 'screenshots', `${slug}_mobile.png`)
  });
  
  // Save HTML
  const html = await page.content();
  fs.writeFileSync(path.join(OUTPUT_DIR, 'html', `${slug}.html`), html);
  
  return { slug, timestamp };
}

async function crawlPage(browser, url) {
  if (visitedUrls.has(url)) return;
  visitedUrls.add(url);
  
  console.log(`Crawling: ${url}`);
  
  const page = await browser.newPage();
  try {
    await page.goto(url, { waitUntil: 'networkidle', timeout: 30000 });
    
    // Wait for age gate if present
    await page.waitForTimeout(2000);
    
    // Try to dismiss age gate
    const ageButton = await page.$('button:has-text("Enter"), button:has-text("Yes"), [class*="age-gate"] button');
    if (ageButton) {
      await ageButton.click();
      await page.waitForTimeout(1000);
    }
    
    // Capture page data
    const features = await analyzePageFeatures(page, url);
    const capture = await capturePage(page, url);
    
    const pageInfo = {
      url,
      slug: capture.slug,
      timestamp: capture.timestamp,
      features
    };
    pageData.push(pageInfo);
    
    // Extract and queue new links
    const links = await extractLinks(page);
    for (const link of links) {
      if (await shouldCrawl(link)) {
        discoveredUrls.add(link);
      }
    }
    
  } catch (error) {
    console.error(`Error crawling ${url}:`, error.message);
  } finally {
    await page.close();
  }
}

async function discoverCollections(browser) {
  const page = await browser.newPage();
  await page.goto(`${BASE_URL}/collections`, { waitUntil: 'networkidle' });
  
  const collections = await page.evaluate(() => {
    return Array.from(document.querySelectorAll('a[href^="/collections/"]'))
      .map(a => a.href)
      .filter((v, i, a) => a.indexOf(v) === i);
  });
  
  await page.close();
  return collections;
}

async function main() {
  console.log('Starting Hamburg Brewing site audit...');
  console.log(`Output directory: ${OUTPUT_DIR}`);
  
  const browser = await chromium.launch({ headless: true });
  
  // Start with homepage
  discoveredUrls.add(BASE_URL);
  
  // Discover collections
  console.log('Discovering collections...');
  const collections = await discoverCollections(browser);
  collections.forEach(c => discoveredUrls.add(c));
  
  // Known important pages
  const knownPages = [
    '/pages/about-us',
    '/pages/contact-us',
    '/pages/faqs',
    '/pages/join-our-team',
    '/pages/book-your-event',
    '/pages/donations',
    '/pages/bus-and-limo-policy',
    '/pages/new-account-inquiry',
    '/cart',
    '/search',
  ];
  knownPages.forEach(p => discoveredUrls.add(`${BASE_URL}${p}`));
  
  // Crawl all discovered URLs
  const urlsToCrawl = [...discoveredUrls];
  for (const url of urlsToCrawl) {
    if (!visitedUrls.has(url)) {
      await crawlPage(browser, url);
    }
  }
  
  // Generate audit report
  const report = {
    auditDate: new Date().toISOString(),
    baseUrl: BASE_URL,
    totalPages: pageData.length,
    pages: pageData,
    summary: {
      hasEcommerce: pageData.some(p => p.features.hasShoppingCart),
      hasAgeGate: pageData.some(p => p.features.hasAgeGate),
      hasNewsletter: pageData.some(p => p.features.hasNewsletterPopup),
      hasSearch: pageData.some(p => p.features.hasSearch),
      productCount: pageData.reduce((sum, p) => sum + (p.features.products || 0), 0),
      totalImages: pageData.reduce((sum, p) => sum + (p.features.images?.length || 0), 0),
      formsFound: pageData.flatMap(p => p.features.forms || [])
    }
  };
  
  fs.writeFileSync(
    path.join(OUTPUT_DIR, 'data', 'site-audit.json'),
    JSON.stringify(report, null, 2)
  );
  
  // Generate markdown report
  const mdReport = `# Hamburg Brewing Site Audit
Generated: ${new Date().toLocaleString()}

## Summary
- **Total Pages Crawled:** ${report.totalPages}
- **Has E-commerce:** ${report.summary.hasEcommerce ? 'Yes' : 'No'}
- **Has Age Gate:** ${report.summary.hasAgeGate ? 'Yes' : 'No'}
- **Has Newsletter:** ${report.summary.hasNewsletter ? 'Yes' : 'No'}
- **Product Elements Found:** ${report.summary.productCount}
- **Total Images:** ${report.summary.totalImages}

## Pages Discovered
${pageData.map(p => `- [${p.url}](${p.url})`).join('\n')}

## Features to Replicate
${pageData.map(p => `
### ${p.url}
- Age Gate: ${p.features.hasAgeGate ? '✓' : '✗'}
- Shopping Cart: ${p.features.hasShoppingCart ? '✓' : '✗'}
- Newsletter Popup: ${p.features.hasNewsletterPopup ? '✓' : '✗'}
- Products: ${p.features.products}
- Scripts: ${p.features.scripts?.join(', ') || 'None'}
`).join('')}

## Technical Requirements
1. **Shopping Cart** - Full e-commerce functionality needed
2. **Age Verification** - 21+ gate required
3. **Newsletter Signup** - Email capture popup
4. **Search** - Product/content search
5. **Forms** - Multiple contact/booking forms
6. **Toast Integration** - ${pageData.some(p => p.features.hasToastIntegration) ? 'Already detected' : 'Need to add'}
7. **Stripe Payments** - For payment processing
`;

  fs.writeFileSync(
    path.join(OUTPUT_DIR, 'SITE_AUDIT_REPORT.md'),
    mdReport
  );
  
  await browser.close();
  
  console.log(`\n✓ Audit complete!`);
  console.log(`  - Pages crawled: ${pageData.length}`);
  console.log(`  - Screenshots saved to: ${path.join(OUTPUT_DIR, 'screenshots')}`);
  console.log(`  - HTML saved to: ${path.join(OUTPUT_DIR, 'html')}`);
  console.log(`  - Report saved to: ${path.join(OUTPUT_DIR, 'SITE_AUDIT_REPORT.md')}`);
}

main().catch(console.error);
