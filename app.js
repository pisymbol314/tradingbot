// Application data
const appData = {
  currentMarket: {
    spxPrice: 5980,
    rsi: 32.4,
    timestamp: "2025-09-14T15:30:00Z",
    marketStatus: "OPEN"
  },
  historicalRSI: [
    {"date": "2025-08-15", "rsi": 65.2, "price": 5820},
    {"date": "2025-08-16", "rsi": 58.7, "price": 5835},
    {"date": "2025-08-17", "rsi": 52.1, "price": 5850},
    {"date": "2025-08-18", "rsi": 48.9, "price": 5865},
    {"date": "2025-08-19", "rsi": 45.3, "price": 5840},
    {"date": "2025-08-20", "rsi": 38.7, "price": 5795},
    {"date": "2025-08-21", "rsi": 34.2, "price": 5775},
    {"date": "2025-08-22", "rsi": 28.9, "price": 5750},
    {"date": "2025-08-23", "rsi": 31.5, "price": 5780},
    {"date": "2025-08-24", "rsi": 37.8, "price": 5820},
    {"date": "2025-08-25", "rsi": 44.2, "price": 5865},
    {"date": "2025-08-26", "rsi": 51.6, "price": 5890},
    {"date": "2025-08-27", "rsi": 57.3, "price": 5910},
    {"date": "2025-08-28", "rsi": 62.1, "price": 5935},
    {"date": "2025-08-29", "rsi": 68.4, "price": 5960},
    {"date": "2025-08-30", "rsi": 71.2, "price": 5975},
    {"date": "2025-08-31", "rsi": 69.8, "price": 5970},
    {"date": "2025-09-01", "rsi": 65.5, "price": 5955},
    {"date": "2025-09-02", "rsi": 61.2, "price": 5940},
    {"date": "2025-09-03", "rsi": 56.8, "price": 5925},
    {"date": "2025-09-04", "rsi": 52.4, "price": 5910},
    {"date": "2025-09-05", "rsi": 48.1, "price": 5895},
    {"date": "2025-09-06", "rsi": 43.7, "price": 5880},
    {"date": "2025-09-07", "rsi": 39.3, "price": 5865},
    {"date": "2025-09-08", "rsi": 34.9, "price": 5850},
    {"date": "2025-09-09", "rsi": 30.5, "price": 5825},
    {"date": "2025-09-10", "rsi": 28.7, "price": 5810},
    {"date": "2025-09-11", "rsi": 31.2, "price": 5835},
    {"date": "2025-09-12", "rsi": 33.8, "price": 5860},
    {"date": "2025-09-13", "rsi": 32.1, "price": 5955},
    {"date": "2025-09-14", "rsi": 32.4, "price": 5980}
  ],
  currentPositions: [
    {
      id: 1,
      entryDate: "2025-09-10",
      shortStrike: 5800,
      longStrike: 5790,
      expiry: "2025-09-24",
      quantity: 2,
      entryCredit: 4.70,
      currentValue: 2.35,
      pnl: 470,
      status: "OPEN",
      dte: 10
    },
    {
      id: 2,
      entryDate: "2025-09-02",
      shortStrike: 5900,
      longStrike: 5890,
      expiry: "2025-09-16",
      quantity: 1,
      entryCredit: 5.20,
      currentValue: 1.30,
      pnl: 390,
      status: "TARGET_HIT",
      dte: 2
    }
  ],
  performance: {
    totalTrades: 12,
    winningTrades: 11,
    winRate: 91.7,
    totalPnL: 8420,
    currentMonthPnL: 1250,
    avgDaysInTrade: 6.8,
    maxDrawdown: -530
  },
  signals: [
    {"date": "2025-09-10", "rsi": 28.7, "action": "ENTERED", "outcome": "OPEN"},
    {"date": "2025-09-02", "rsi": 30.1, "action": "ENTERED", "outcome": "WIN"},
    {"date": "2025-08-21", "rsi": 34.2, "action": "ENTERED", "outcome": "WIN"},
    {"date": "2025-08-05", "rsi": 29.8, "action": "ENTERED", "outcome": "WIN"},
    {"date": "2025-07-22", "rsi": 33.5, "action": "SKIPPED", "outcome": "N/A"},
    {"date": "2025-07-15", "rsi": 31.2, "action": "ENTERED", "outcome": "WIN"}
  ],
  platforms: [
    {
      name: "Interactive Brokers",
      rating: "Best",
      commission: "$0.65/contract",
      spxSupport: true,
      apiSupport: true,
      minBalance: "$0",
      signupUrl: "https://www.interactivebrokers.com"
    },
    {
      name: "TD Ameritrade/Schwab",
      rating: "Good",
      commission: "$0.65/contract", 
      spxSupport: true,
      apiSupport: "Limited",
      minBalance: "$0",
      signupUrl: "https://www.schwab.com"
    },
    {
      name: "Alpaca",
      rating: "OK",
      commission: "$0.50/contract",
      spxSupport: false,
      apiSupport: true,
      minBalance: "$0",
      signupUrl: "https://alpaca.markets"
    }
  ],
  strategyParams: {
    rsiThreshold: 35,
    daysToExpiry: 14,
    profitTarget: 50,
    positionSize: 1,
    maxPositions: 5,
    spreadWidth: 10
  }
};

// Global variables
let rsiChart;
let currentPositions = [...appData.currentPositions];

// Initialize the dashboard
document.addEventListener('DOMContentLoaded', function() {
  console.log('Dashboard initializing...');
  initializeDashboard();
  setupEventListeners();
  updateDateTime();
  setInterval(updateDateTime, 1000);
});

function initializeDashboard() {
  updateRSIDisplay();
  createRSIChart();
  updateMarketStatus();
  populatePositions();
  updatePerformanceMetrics();
  populateSignals();
  populatePlatforms();
  updateStrategyParams();
  updateRiskCalculations();
}

function updateDateTime() {
  const now = new Date();
  const options = {
    weekday: 'long',
    year: 'numeric',
    month: 'long',
    day: 'numeric',
    hour: '2-digit',
    minute: '2-digit',
    second: '2-digit',
    timeZoneName: 'short'
  };
  document.getElementById('current-datetime').textContent = now.toLocaleDateString('en-US', options);
}

function updateMarketStatus() {
  const marketStatus = document.getElementById('market-status');
  const now = new Date();
  const hour = now.getHours();
  const day = now.getDay();
  
  // Simple market hours check (9:30 AM - 4:00 PM ET, Mon-Fri)
  const isWeekday = day >= 1 && day <= 5;
  const isDuringMarketHours = hour >= 9 && hour < 16;
  const isOpen = isWeekday && isDuringMarketHours;
  
  marketStatus.textContent = isOpen ? 'MARKET OPEN' : 'MARKET CLOSED';
  marketStatus.className = isOpen ? 'status status--success' : 'status status--error';
}

function updateRSIDisplay() {
  const rsiValue = document.getElementById('rsi-value');
  const signalIndicator = document.getElementById('signal-indicator');
  const currentRSI = appData.currentMarket.rsi;
  
  rsiValue.textContent = currentRSI.toFixed(1);
  
  // Update signal indicator based on RSI threshold
  const threshold = parseFloat(document.getElementById('rsi-threshold').value);
  if (currentRSI < threshold) {
    signalIndicator.innerHTML = '<span class="status status--success">BUY SIGNAL</span>';
  } else {
    signalIndicator.innerHTML = '<span class="status status--info">NO SIGNAL</span>';
  }
}

function createRSIChart() {
  const ctx = document.getElementById('rsi-chart').getContext('2d');
  const threshold = parseFloat(document.getElementById('rsi-threshold').value);
  
  rsiChart = new Chart(ctx, {
    type: 'line',
    data: {
      labels: appData.historicalRSI.map(item => {
        const date = new Date(item.date);
        return date.toLocaleDateString('en-US', { month: 'short', day: 'numeric' });
      }),
      datasets: [{
        label: 'RSI',
        data: appData.historicalRSI.map(item => item.rsi),
        borderColor: '#1FB8CD',
        backgroundColor: 'rgba(31, 184, 205, 0.1)',
        fill: true,
        tension: 0.4
      }, {
        label: 'Signal Line',
        data: Array(appData.historicalRSI.length).fill(threshold),
        borderColor: '#DB4545',
        borderDash: [5, 5],
        fill: false,
        pointRadius: 0
      }]
    },
    options: {
      responsive: true,
      maintainAspectRatio: false,
      plugins: {
        legend: {
          display: true,
          position: 'top'
        }
      },
      scales: {
        y: {
          beginAtZero: false,
          min: 0,
          max: 100,
          grid: {
            color: 'rgba(255, 255, 255, 0.1)'
          }
        },
        x: {
          grid: {
            color: 'rgba(255, 255, 255, 0.1)'
          }
        }
      }
    }
  });
}

function populatePositions() {
  const tbody = document.getElementById('positions-tbody');
  tbody.innerHTML = '';
  
  currentPositions.forEach(position => {
    const row = document.createElement('tr');
    const pnlClass = position.pnl >= 0 ? 'profit' : 'loss';
    const statusClass = position.status === 'OPEN' ? 'status--info' : 
                       position.status === 'TARGET_HIT' ? 'status--success' : 'status--error';
    
    row.innerHTML = `
      <td>${formatDate(position.entryDate)}</td>
      <td>${position.shortStrike}/${position.longStrike}</td>
      <td>${position.dte}</td>
      <td class="${pnlClass}">$${position.pnl}</td>
      <td><span class="status ${statusClass}">${position.status.replace('_', ' ')}</span></td>
    `;
    tbody.appendChild(row);
  });
}

function updatePerformanceMetrics() {
  document.getElementById('win-rate').textContent = `${appData.performance.winRate}%`;
  document.getElementById('total-pnl').textContent = `$${appData.performance.totalPnL.toLocaleString()}`;
  document.getElementById('avg-days').textContent = appData.performance.avgDaysInTrade;
  document.getElementById('month-pnl').textContent = `$${appData.performance.currentMonthPnL.toLocaleString()}`;
}

function populateSignals() {
  const signalsList = document.getElementById('signals-list');
  signalsList.innerHTML = '';
  
  appData.signals.forEach(signal => {
    const signalItem = document.createElement('div');
    signalItem.className = 'signal-item';
    
    const actionClass = signal.action === 'ENTERED' ? 'profit' : 'loss';
    const outcomeClass = signal.outcome === 'WIN' ? 'profit' : 
                        signal.outcome === 'LOSS' ? 'loss' : '';
    
    signalItem.innerHTML = `
      <div>
        <div class="signal-date">${formatDate(signal.date)}</div>
        <div class="signal-rsi">RSI: ${signal.rsi}</div>
      </div>
      <div>
        <div class="signal-action ${actionClass}">${signal.action}</div>
        <div class="signal-outcome ${outcomeClass}">${signal.outcome}</div>
      </div>
    `;
    signalsList.appendChild(signalItem);
  });
}

function populatePlatforms() {
  const platformsGrid = document.getElementById('platforms-grid');
  platformsGrid.innerHTML = '';
  
  appData.platforms.forEach(platform => {
    const platformItem = document.createElement('div');
    platformItem.className = 'platform-item';
    
    const ratingClass = platform.rating.toLowerCase().replace(' ', '-');
    
    platformItem.innerHTML = `
      <div class="platform-info">
        <div class="platform-name">${platform.name}</div>
        <div class="platform-details">
          Commission: ${platform.commission} | 
          SPX: ${platform.spxSupport ? 'Yes' : 'No'} | 
          API: ${platform.apiSupport}
        </div>
      </div>
      <div>
        <div class="platform-rating platform-rating--${ratingClass}">${platform.rating}</div>
        <a href="${platform.signupUrl}" target="_blank" class="btn btn--sm btn--outline" style="margin-top: 8px;">Sign Up</a>
      </div>
    `;
    platformsGrid.appendChild(platformItem);
  });
}

function updateStrategyParams() {
  document.getElementById('rsi-threshold').value = appData.strategyParams.rsiThreshold;
  document.getElementById('days-expiry').value = appData.strategyParams.daysToExpiry;
  document.getElementById('profit-target').value = appData.strategyParams.profitTarget;
  document.getElementById('position-size').value = appData.strategyParams.positionSize;
  document.getElementById('max-positions').value = appData.strategyParams.maxPositions;
}

function updateRiskCalculations() {
  const accountBalance = parseFloat(document.getElementById('account-balance').value);
  const riskPercent = parseFloat(document.getElementById('risk-percent').value);
  
  const maxRisk = (accountBalance * riskPercent) / 100;
  const portfolioRisk = currentPositions.reduce((total, pos) => {
    if (pos.status === 'OPEN') {
      return total + (pos.quantity * 10 * 100); // Assuming $10 spread width * 100 multiplier
    }
    return total;
  }, 0);
  
  document.getElementById('max-risk').textContent = `$${maxRisk.toLocaleString()}`;
  document.getElementById('portfolio-risk').textContent = `$${portfolioRisk.toLocaleString()}`;
}

function setupEventListeners() {
  console.log('Setting up event listeners...');
  
  // Strategy form submission
  const strategyForm = document.getElementById('strategy-form');
  if (strategyForm) {
    strategyForm.addEventListener('submit', function(e) {
      e.preventDefault();
      
      appData.strategyParams.rsiThreshold = parseFloat(document.getElementById('rsi-threshold').value);
      appData.strategyParams.daysToExpiry = parseInt(document.getElementById('days-expiry').value);
      appData.strategyParams.profitTarget = parseFloat(document.getElementById('profit-target').value);
      appData.strategyParams.positionSize = parseInt(document.getElementById('position-size').value);
      appData.strategyParams.maxPositions = parseInt(document.getElementById('max-positions').value);
      
      updateRSIDisplay();
      updateRSIChart();
      alert('Strategy parameters updated successfully!');
    });
  }
  
  // Risk calculator updates
  const accountBalanceInput = document.getElementById('account-balance');
  const riskPercentInput = document.getElementById('risk-percent');
  
  if (accountBalanceInput) {
    accountBalanceInput.addEventListener('input', updateRiskCalculations);
  }
  if (riskPercentInput) {
    riskPercentInput.addEventListener('input', updateRiskCalculations);
  }
  
  // Add position modal handlers
  const addPositionBtn = document.getElementById('add-position-btn');
  const addPositionModal = document.getElementById('add-position-modal');
  const closeModalBtn = document.getElementById('close-modal');
  const cancelModalBtn = document.getElementById('cancel-modal');
  const addPositionForm = document.getElementById('add-position-form');
  
  if (addPositionBtn && addPositionModal) {
    addPositionBtn.addEventListener('click', function(e) {
      e.preventDefault();
      console.log('Add position button clicked');
      showModal();
    });
  }
  
  if (closeModalBtn) {
    closeModalBtn.addEventListener('click', function(e) {
      e.preventDefault();
      closeModal();
    });
  }
  
  if (cancelModalBtn) {
    cancelModalBtn.addEventListener('click', function(e) {
      e.preventDefault();
      closeModal();
    });
  }
  
  // Add position form submission
  if (addPositionForm) {
    addPositionForm.addEventListener('submit', function(e) {
      e.preventDefault();
      
      const newPosition = {
        id: Date.now(),
        entryDate: document.getElementById('entry-date').value,
        shortStrike: parseFloat(document.getElementById('short-strike').value),
        longStrike: parseFloat(document.getElementById('long-strike').value),
        expiry: document.getElementById('expiry-date').value,
        quantity: parseInt(document.getElementById('quantity').value),
        entryCredit: parseFloat(document.getElementById('entry-credit').value),
        currentValue: parseFloat(document.getElementById('entry-credit').value) * 0.5,
        pnl: parseFloat(document.getElementById('entry-credit').value) * parseInt(document.getElementById('quantity').value) * 100 * 0.5,
        status: 'OPEN',
        dte: calculateDTE(document.getElementById('expiry-date').value)
      };
      
      currentPositions.push(newPosition);
      populatePositions();
      updateRiskCalculations();
      closeModal();
      
      // Reset form
      addPositionForm.reset();
      
      alert('Position added successfully!');
    });
  }
  
  // Close modal when clicking outside
  if (addPositionModal) {
    addPositionModal.addEventListener('click', function(e) {
      if (e.target === addPositionModal) {
        closeModal();
      }
    });
  }
}

function showModal() {
  const modal = document.getElementById('add-position-modal');
  const entryDateInput = document.getElementById('entry-date');
  
  if (modal) {
    modal.classList.remove('hidden');
    modal.style.display = 'flex';
    console.log('Modal should be visible now');
  }
  
  if (entryDateInput) {
    entryDateInput.value = new Date().toISOString().split('T')[0];
  }
}

function closeModal() {
  const modal = document.getElementById('add-position-modal');
  if (modal) {
    modal.classList.add('hidden');
    modal.style.display = 'none';
  }
}

function updateRSIChart() {
  if (rsiChart) {
    const threshold = parseFloat(document.getElementById('rsi-threshold').value);
    rsiChart.data.datasets[1].data = Array(appData.historicalRSI.length).fill(threshold);
    rsiChart.update();
  }
}

function formatDate(dateString) {
  const date = new Date(dateString);
  return date.toLocaleDateString('en-US', { 
    month: 'short', 
    day: 'numeric',
    year: 'numeric'
  });
}

function calculateDTE(expiryDate) {
  const today = new Date();
  const expiry = new Date(expiryDate);
  const diffTime = expiry - today;
  const diffDays = Math.ceil(diffTime / (1000 * 60 * 60 * 24));
  return Math.max(0, diffDays);
}

// Simulate real-time RSI updates (for demo purposes)
function simulateRSIUpdates() {
  setInterval(() => {
    // Small random fluctuation in RSI
    const fluctuation = (Math.random() - 0.5) * 2;
    appData.currentMarket.rsi = Math.max(0, Math.min(100, appData.currentMarket.rsi + fluctuation));
    updateRSIDisplay();
  }, 30000); // Update every 30 seconds
}

// Start simulation after dashboard is loaded
setTimeout(simulateRSIUpdates, 5000);