/**
 * Hamburg Brewing - Main JavaScript
 * Handles: Age gate, navigation, cart, Toast integration
 */

// ========================
// Age Gate
// ========================
class AgeGate {
  constructor() {
    this.modal = document.getElementById('age-gate');
    this.storageKey = 'hbc_age_verified';
    this.init();
  }

  init() {
    if (localStorage.getItem(this.storageKey) !== 'true') {
      this.show();
    } else {
      this.hide();
    }
  }

  show() {
    document.body.style.overflow = 'hidden';
    this.modal.classList.remove('hidden');
  }

  hide() {
    document.body.style.overflow = '';
    this.modal.classList.add('hidden');
  }

  verify() {
    localStorage.setItem(this.storageKey, 'true');
    this.hide();
  }

  deny() {
    window.location.href = 'https://www.google.com';
  }
}

// ========================
// Mobile Navigation
// ========================
class MobileNav {
  constructor() {
    this.toggle = document.getElementById('menu-toggle');
    this.nav = document.getElementById('main-nav');
    this.overlay = document.getElementById('nav-overlay');
    this.closeBtn = document.getElementById('nav-close');
    this.init();
  }

  init() {
    this.toggle?.addEventListener('click', () => this.open());
    this.closeBtn?.addEventListener('click', () => this.close());
    this.overlay?.addEventListener('click', () => this.close());
    
    // Close on escape
    document.addEventListener('keydown', (e) => {
      if (e.key === 'Escape') this.close();
    });
  }

  open() {
    this.nav?.classList.add('open');
    this.overlay?.classList.add('open');
    document.body.style.overflow = 'hidden';
  }

  close() {
    this.nav?.classList.remove('open');
    this.overlay?.classList.remove('open');
    document.body.style.overflow = '';
  }
}

// ========================
// Shopping Cart
// ========================
class ShoppingCart {
  constructor() {
    this.items = [];
    this.drawer = document.getElementById('cart-drawer');
    this.overlay = document.getElementById('cart-overlay');
    this.itemsContainer = document.getElementById('cart-items');
    this.subtotalEl = document.getElementById('cart-subtotal');
    this.countEl = document.getElementById('cart-count');
    this.storageKey = 'hbc_cart';
    this.init();
  }

  init() {
    // Load from storage
    const saved = localStorage.getItem(this.storageKey);
    if (saved) {
      try {
        this.items = JSON.parse(saved);
      } catch(e) { this.items = []; }
    }
    
    this.updateUI();
    
    // Event listeners
    document.getElementById('cart-toggle')?.addEventListener('click', () => this.open());
    document.getElementById('cart-close')?.addEventListener('click', () => this.close());
    this.overlay?.addEventListener('click', () => this.close());
    
    // Add to cart buttons
    document.querySelectorAll('[data-add-to-cart]').forEach(btn => {
      btn.addEventListener('click', (e) => {
        const id = e.currentTarget.dataset.productId;
        const name = e.currentTarget.dataset.productName;
        const price = parseFloat(e.currentTarget.dataset.productPrice);
        const image = e.currentTarget.dataset.productImage;
        this.add({ id, name, price, image, qty: 1 });
      });
    });
  }

  add(product) {
    const existing = this.items.find(i => i.id === product.id);
    if (existing) {
      existing.qty += product.qty;
    } else {
      this.items.push(product);
    }
    this.save();
    this.updateUI();
    this.open();
  }

  remove(id) {
    this.items = this.items.filter(i => i.id !== id);
    this.save();
    this.updateUI();
  }

  updateQty(id, qty) {
    const item = this.items.find(i => i.id === id);
    if (item) {
      item.qty = Math.max(1, qty);
      this.save();
      this.updateUI();
    }
  }

  getSubtotal() {
    return this.items.reduce((sum, i) => sum + (i.price * i.qty), 0);
  }

  save() {
    localStorage.setItem(this.storageKey, JSON.stringify(this.items));
  }

  updateUI() {
    const count = this.items.reduce((sum, i) => sum + i.qty, 0);
    if (this.countEl) {
      this.countEl.textContent = count;
      this.countEl.style.display = count > 0 ? 'flex' : 'none';
    }
    
    if (this.itemsContainer) {
      if (this.items.length === 0) {
        this.itemsContainer.innerHTML = `
          <div class="cart-empty">
            <svg width="48" height="48" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.5">
              <path d="M6 6h15l-1.5 9h-12z"/>
              <circle cx="9" cy="20" r="1"/>
              <circle cx="18" cy="20" r="1"/>
              <path d="M6 6L5 3H2"/>
            </svg>
            <p style="margin-top: 16px;">Your cart is currently empty.</p>
          </div>
        `;
      } else {
        this.itemsContainer.innerHTML = this.items.map(item => `
          <div class="cart-item">
            <div class="cart-item-image">
              <img src="${item.image}" alt="${item.name}">
            </div>
            <div class="cart-item-details">
              <h4>${item.name}</h4>
              <p>$${item.price.toFixed(2)}</p>
              <div class="cart-item-qty">
                <button onclick="cart.updateQty('${item.id}', ${item.qty - 1})">-</button>
                <span>${item.qty}</span>
                <button onclick="cart.updateQty('${item.id}', ${item.qty + 1})">+</button>
              </div>
            </div>
            <button onclick="cart.remove('${item.id}')" style="background:none;border:none;cursor:pointer;color:var(--color-text-lighter);">
              <svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                <line x1="18" y1="6" x2="6" y2="18"/>
                <line x1="6" y1="6" x2="18" y2="18"/>
              </svg>
            </button>
          </div>
        `).join('');
      }
    }
    
    if (this.subtotalEl) {
      this.subtotalEl.textContent = `$${this.getSubtotal().toFixed(2)}`;
    }
  }

  open() {
    this.drawer?.classList.add('open');
    this.overlay?.classList.add('open');
    document.body.style.overflow = 'hidden';
  }

  close() {
    this.drawer?.classList.remove('open');
    this.overlay?.classList.remove('open');
    document.body.style.overflow = '';
  }
}

// ========================
// Toast Integration
// ========================
class ToastIntegration {
  constructor() {
    this.restaurantGuid = null; // Set this when you get your Toast restaurant GUID
    this.baseUrl = 'https://www.toasttab.com';
  }

  getOrderUrl() {
    // Example: https://www.toasttab.com/hamburg-brewing-company/v3
    // You'll need to update this with your actual Toast URL
    return 'https://www.toasttab.com/hamburg-brewing-company/v3';
  }

  embedMenu(containerId) {
    // Toast doesn't have a simple embed API, but we can:
    // 1. Link out to Toast ordering
    // 2. Use Toast's iframe embed if available
    // 3. Use Toast's API to fetch menu items (requires API key)
    
    const container = document.getElementById(containerId);
    if (!container) return;
    
    container.innerHTML = `
      <div class="toast-menu-embed">
        <h3>Order Online for Pickup</h3>
        <p>Browse our full menu and order directly through Toast for quick pickup at the brewery.</p>
        <a href="${this.getOrderUrl()}" target="_blank" rel="noopener" class="btn btn-primary">
          View Menu & Order
        </a>
      </div>
    `;
  }

  // Toast API integration (requires API credentials)
  async fetchMenu() {
    // This requires Toast API access
    // Endpoint: GET /menus/v2/menus
    // Headers: Authorization: Bearer {api_key}
    console.log('Toast menu fetch - requires API setup');
  }
}

// ========================
// Stripe Checkout
// ========================
class StripeCheckout {
  constructor() {
    this.publishableKey = null; // Set your Stripe publishable key
    this.stripe = null;
  }

  init(key) {
    this.publishableKey = key;
    if (window.Stripe) {
      this.stripe = Stripe(key);
    }
  }

  async createCheckoutSession(items) {
    // This would normally call your backend to create a checkout session
    // For now, we'll redirect to a simple checkout page
    console.log('Creating checkout for:', items);
    
    // In production:
    // 1. Call your backend API
    // 2. Backend creates Stripe Checkout Session
    // 3. Return session ID
    // 4. Redirect to Stripe Checkout
  }
}

// ========================
// Scroll Animations
// ========================
class ScrollAnimations {
  constructor() {
    this.observer = new IntersectionObserver((entries) => {
      entries.forEach(entry => {
        if (entry.isIntersecting) {
          entry.target.classList.add('fade-in-up');
        }
      });
    }, { threshold: 0.1 });
    
    this.init();
  }

  init() {
    document.querySelectorAll('.animate-on-scroll').forEach(el => {
      el.style.opacity = '0';
      this.observer.observe(el);
    });
  }
}

// ========================
// Search
// ========================
class SiteSearch {
  constructor() {
    this.toggle = document.getElementById('search-toggle');
    this.modal = document.getElementById('search-modal');
    this.input = document.getElementById('search-input');
    this.results = document.getElementById('search-results');
    this.closeBtn = document.getElementById('search-close');
    this.init();
  }

  init() {
    this.toggle?.addEventListener('click', () => this.open());
    this.closeBtn?.addEventListener('click', () => this.close());
    this.input?.addEventListener('input', (e) => this.search(e.target.value));
    
    document.addEventListener('keydown', (e) => {
      if (e.key === 'Escape') this.close();
      if ((e.metaKey || e.ctrlKey) && e.key === 'k') {
        e.preventDefault();
        this.open();
      }
    });
  }

  open() {
    this.modal?.classList.add('open');
    this.input?.focus();
    document.body.style.overflow = 'hidden';
  }

  close() {
    this.modal?.classList.remove('open');
    document.body.style.overflow = '';
  }

  search(query) {
    if (!query || query.length < 2) {
      this.results.innerHTML = '';
      return;
    }
    
    // Simple client-side search
    const pages = [
      { title: 'Home', url: '/', desc: 'Welcome to Hamburg Brewing Company' },
      { title: 'About Us', url: '/about.html', desc: 'Our story and mission' },
      { title: 'Contact', url: '/contact.html', desc: 'Get in touch with us' },
      { title: 'Merch', url: '/merch.html', desc: 'HBC merchandise and gift cards' },
      { title: 'FAQs', url: '/faqs.html', desc: 'Frequently asked questions' },
    ];
    
    const matches = pages.filter(p => 
      p.title.toLowerCase().includes(query.toLowerCase()) ||
      p.desc.toLowerCase().includes(query.toLowerCase())
    );
    
    this.results.innerHTML = matches.map(m => `
      <a href="${m.url}" class="search-result">
        <h4>${m.title}</h4>
        <p>${m.desc}</p>
      </a>
    `).join('');
  }
}

// ========================
// Initialize Everything
// ========================
document.addEventListener('DOMContentLoaded', () => {
  window.ageGate = new AgeGate();
  window.mobileNav = new MobileNav();
  window.cart = new ShoppingCart();
  window.toast = new ToastIntegration();
  window.stripeCheckout = new StripeCheckout();
  window.scrollAnim = new ScrollAnimations();
  window.siteSearch = new SiteSearch();
  
  // Header scroll effect
  const header = document.querySelector('.site-header');
  let lastScroll = 0;
  
  window.addEventListener('scroll', () => {
    const currentScroll = window.pageYOffset;
    
    if (currentScroll > 100) {
      header?.classList.add('scrolled');
    } else {
      header?.classList.remove('scrolled');
    }
    
    lastScroll = currentScroll;
  });
});
