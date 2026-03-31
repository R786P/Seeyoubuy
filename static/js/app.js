// Load and display products
async function loadProducts(category = 'all') {
    const grid = document.getElementById('productsGrid');
    grid.innerHTML = '<div class="loading">Loading deals... 🛍️</div>';
    
    try {
        const url = category === 'all' ? '/api/products' : `/api/products?category=${category}`;
        const res = await fetch(url);
        const products = await res.json();
        
        if (products.length === 0) {
            grid.innerHTML = '<p style="text-align:center; grid-column:1/-1;">No products found. Check back soon! 😊</p>';
            return;
        }
        
        // Show Deal of the Day if available
        showDealOfTheDay(products);
        
        // Render products
        grid.innerHTML = products.map(product => createProductCard(product)).join('');
        
    } catch (error) {
        console.error('Error loading products:', error);
        grid.innerHTML = '<p style="text-align:center; grid-column:1/-1; color:#e74c3c;">Failed to load products. Please refresh. 🔄</p>';
    }
}

// Create product card HTML
function createProductCard(p) {
    const discount = p.original_price ? calculateDiscount(p.price, p.original_price) : null;
    const dealBadge = p.deal_type === 'lightning' ? '⚡ Lightning' : 
                      p.deal_type === 'hot' ? '🔥 Hot' : null;
    
    return `
        <article class="product-card">
            ${dealBadge ? `<span class="deal-badge">${dealBadge}</span>` : ''}
            <img src="${p.image}" alt="${p.name}" class="product-image" 
                 onerror="this.src='https://via.placeholder.com/300x200?text=No+Image'">
            <div class="product-info">
                <span class="category">${p.category}</span>
                <h3>${p.name}</h3>
                <div class="price-section">
                    <span class="price">${p.price}</span>
                    ${p.original_price ? `<span class="original-price">${p.original_price}</span>` : ''}
                    ${discount ? `<span class="discount">(${discount}% OFF)</span>` : ''}
                </div>
                ${p.description ? `<p class="description">${p.description}</p>` : ''}
                <a href="/go/${p.id}" target="_blank" rel="noopener noreferrer" class="buy-btn">
                    🛒 Buy Now →
                </a>
            </div>
        </article>
    `;
}

// Calculate discount percentage
function calculateDiscount(current, original) {
    const curr = parseFloat(current.replace(/[^0-9.]/g, ''));
    const orig = parseFloat(original.replace(/[^0-9.]/g, ''));
    if (curr && orig && orig > curr) {
        return Math.round((1 - curr/orig) * 100);
    }
    return null;
}

// Show Deal of the Day
function showDealOfTheDay(products) {
    const deals = products.filter(p => p.deal_type !== 'normal');
    const banner = document.getElementById('dealBanner');
    
    if (deals.length > 0) {
        // Pick one based on date for consistency
        const today = new Date().toDateString();
        const index = Math.abs(hashCode(today)) % deals.length;
        const deal = deals[index];
        
        document.getElementById('dealContent').innerHTML = `
            <h4>${deal.name}</h4>
            <div class="price">${deal.price} 
                ${deal.original_price ? `<s style="font-size:0.9rem">${deal.original_price}</s>` : ''}
            </div>
            <a href="/go/${deal.id}" target="_blank" class="buy-btn" style="padding:0.4rem 1rem; font-size:0.9rem; margin-top:0.5rem; display:inline-block; width:auto;">
                Grab Deal →
            </a>
        `;
        banner.style.display = 'flex';
    } else {
        banner.style.display = 'none';
    }
}

// Simple hash function for consistent daily selection
function hashCode(str) {
    let hash = 0;
    for (let i = 0; i < str.length; i++) {
        hash = ((hash << 5) - hash) + str.charCodeAt(i);
        hash |= 0;
    }
    return hash;
}

// Filter buttons
document.querySelectorAll('.filter-btn').forEach(btn => {
    btn.addEventListener('click', (e) => {
        document.querySelectorAll('.filter-btn').forEach(b => b.classList.remove('active'));
        e.target.classList.add('active');
        loadProducts(e.target.dataset.category);
    });
});

// Initialize
document.addEventListener('DOMContentLoaded', () => {
    loadProducts();
});
