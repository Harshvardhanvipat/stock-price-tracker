const stockList = document.getElementById('stock-list');
const addStockForm = document.getElementById('add-stock-form');
const stockSymbolInput = document.getElementById('stock-symbol');
const lastUpdatedSpan = document.getElementById('last-updated');

// Fetch stocks from API
async function fetchStocks() {
    try {
        const response = await fetch('/api/stocks');
        const stocks = await response.json();
        renderStocks(stocks);
        updateLastUpdated();
    } catch (error) {
        console.error('Error fetching stocks:', error);
    }
}

// Render stocks to DOM
function renderStocks(stocks) {
    stockList.innerHTML = ''; // Clear current list

    // Sort: Starred first, then alphabetical
    stocks.sort((a, b) => {
        if (a.starred === b.starred) {
            return a.symbol.localeCompare(b.symbol);
        }
        return b.starred ? 1 : -1;
    });

    stocks.forEach(stock => {
        const card = document.createElement('div');
        card.className = 'stock-card';

        const isPositive = stock.change >= 0;
        const changeClass = isPositive ? 'positive' : 'negative';
        const changeSign = isPositive ? '+' : '';
        const starClass = stock.starred ? 'starred' : '';
        const starIcon = stock.starred ? '★' : '☆';

        card.innerHTML = `
            <div class="card-header">
                <div class="symbol">${stock.symbol}</div>
                <button class="star-btn ${starClass}" onclick="toggleStar('${stock.symbol}')">
                    ${starIcon}
                </button>
            </div>
            <div class="price-container">
                <span class="price">$${stock.price.toFixed(2)}</span>
                <span class="change ${changeClass}">${changeSign}${stock.change.toFixed(2)}%</span>
            </div>
        `;
        stockList.appendChild(card);
    });
}

// Add new stock
addStockForm.addEventListener('submit', async (e) => {
    e.preventDefault();
    const symbol = stockSymbolInput.value.trim();
    if (!symbol) return;

    try {
        const response = await fetch('/api/stocks', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ symbol })
        });

        if (response.ok) {
            stockSymbolInput.value = '';
            fetchStocks(); // Refresh list
        } else {
            const data = await response.json();
            alert(data.error || 'Failed to add stock');
        }
    } catch (error) {
        console.error('Error adding stock:', error);
    }
});

// Toggle star
window.toggleStar = async (symbol) => {
    try {
        await fetch(`/api/stocks/${symbol}/star`, { method: 'POST' });
        fetchStocks(); // Refresh list
    } catch (error) {
        console.error('Error toggling star:', error);
    }
};

function updateLastUpdated() {
    const now = new Date();
    lastUpdatedSpan.textContent = `Last updated: ${now.toLocaleTimeString()}`;
}

// Initial load
fetchStocks();

// Auto-refresh every 30 seconds (matching backend update interval for demo)
setInterval(fetchStocks, 30000);
