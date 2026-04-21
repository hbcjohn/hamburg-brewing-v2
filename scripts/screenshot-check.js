const { chromium } = require('playwright');

(async () => {
  const browser = await chromium.launch({ headless: true });
  const page = await browser.newPage();
  await page.goto('http://localhost:8090');
  await page.waitForTimeout(2000);
  
  // Click YES on age gate
  const yesBtn = await page.$('.btn-primary');
  if (yesBtn) await yesBtn.click();
  await page.waitForTimeout(1000);
  
  await page.screenshot({ path: '/home/walt/.openclaw/workspace/projects/hamburg-brewing/audit/preview-home-no-gate.png', fullPage: false });
  
  // Scroll down to see content
  await page.evaluate(() => window.scrollTo(0, 800));
  await page.waitForTimeout(500);
  await page.screenshot({ path: '/home/walt/.openclaw/workspace/projects/hamburg-brewing/audit/preview-home-scrolled.png', fullPage: false });
  
  // Merch page
  await page.goto('http://localhost:8090/merch.html');
  await page.waitForTimeout(2000);
  const yesBtn2 = await page.$('.btn-primary');
  if (yesBtn2) await yesBtn2.click();
  await page.waitForTimeout(1000);
  await page.screenshot({ path: '/home/walt/.openclaw/workspace/projects/hamburg-brewing/audit/preview-merch.png', fullPage: false });
  
  await browser.close();
  console.log('Screenshots saved');
})();
