// Stellar Compass - Frontend JavaScript with Lobstr Support
console.log('🚀 Stellar Compass Initializing...');

let connectedAccount = null;
let walletConnectSession = null;

// WalletConnect configuration
const WALLETCONNECT_PROJECT_ID = 'YOUR_PROJECT_ID'; // You'll need to get this from https://cloud.walletconnect.com

// Connect to Lobstr wallet via WalletConnect
async function connectWallet() {
    console.log('🔗 Connecting to Lobstr wallet...');
    
    try {
        // For Lobstr, we'll use a simpler approach with manual address input
        // Or you can integrate WalletConnect for full functionality
        
        // Show modal for wallet address input
        const modal = document.createElement('div');
        modal.className = 'fixed inset-0 bg-black bg-opacity-50 flex items-center justify-center z-50';
        modal.innerHTML = `
            <div class="bg-white rounded-lg p-8 max-w-md w-full mx-4">
                <h3 class="text-2xl font-bold mb-4">Connect Lobstr Wallet</h3>
                <p class="text-gray-600 mb-4">Enter your Stellar public address from Lobstr wallet:</p>
                <input 
                    type="text" 
                    id="wallet-address-input" 
                    placeholder="GXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX"
                    class="w-full border-2 border-gray-300 rounded-lg px-4 py-2 mb-4 font-mono text-sm"
                />
                <div class="text-xs text-gray-500 mb-4">
                    📱 Open Lobstr app → Settings → Account Details → Copy your Public Key
                </div>
                <div class="flex space-x-3">
                    <button 
                        onclick="cancelConnection()" 
                        class="flex-1 bg-gray-300 text-gray-700 py-2 rounded-lg hover:bg-gray-400 transition">
                        Cancel
                    </button>
                    <button 
                        onclick="confirmConnection()" 
                        class="flex-1 bg-purple-600 text-white py-2 rounded-lg hover:bg-purple-700 transition">
                        Connect
                    </button>
                </div>
            </div>
        `;
        
        document.body.appendChild(modal);
        
        // Focus on input
        setTimeout(() => {
            document.getElementById('wallet-address-input').focus();
        }, 100);
        
    } catch (error) {
        console.error('❌ Error connecting wallet:', error);
        showError('Failed to connect wallet.');
    }
}

// Confirm wallet connection
async function confirmConnection() {
    const input = document.getElementById('wallet-address-input');
    const publicKey = input.value.trim();
    
    // Validate Stellar address
    if (!publicKey || publicKey.length !== 56 || !publicKey.startsWith('G')) {
        showError('Invalid Stellar address. Please check and try again.');
        input.classList.add('border-red-500');
        return;
    }
    
    console.log('✅ Wallet address entered:', publicKey);
    
    connectedAccount = publicKey;
    
    // Remove modal
    const modal = document.querySelector('.fixed.inset-0');
    if (modal) modal.remove();
    
    // Update UI
    document.getElementById('wallet-address').textContent = 
        `${publicKey.substring(0, 8)}...${publicKey.substring(publicKey.length - 8)}`;
    document.getElementById('connect-btn').style.display = 'none';
    document.getElementById('wallet-info').classList.remove('hidden');
    document.getElementById('get-started').style.display = 'none';
    document.getElementById('dashboard').classList.remove('hidden');
    
    showSuccess('🎉 Lobstr wallet connected! Sending notification...');
    
    // Notify backend that wallet is connected (triggers email/SMS)
    try {
        const notifyResponse = await fetch('http://localhost:5000/api/wallet/connected', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({
                public_key: publicKey
            })
        });
        
        if (notifyResponse.ok) {
            console.log('✅ Notification sent');
            showSuccess('📧 Check your email for wallet connection confirmation!');
        }
    } catch (error) {
        console.warn('⚠️ Could not send notification:', error);
    }
    
    // Load portfolio and opportunities (also triggers notifications)
    await loadPortfolio();
    await loadOpportunities();
}

// Cancel connection
function cancelConnection() {
    const modal = document.querySelector('.fixed.inset-0');
    if (modal) modal.remove();
}

// Load portfolio data
async function loadPortfolio() {
    if (!connectedAccount) return;
    
    console.log('📊 Loading portfolio...');
    
    try {
        const response = await fetch(`http://localhost:5000/api/portfolio/${connectedAccount}`);
        const data = await response.json();
        
        console.log('✅ Portfolio loaded:', data);
        
        // Update portfolio display
        document.getElementById('total-value').textContent = 
            `$${data.total_value.toFixed(2)}`;
        document.getElementById('asset-count').textContent = data.assets.length;
        document.getElementById('idle-count').textContent = data.idle_assets.length;
        
        // Display assets
        const assetsList = document.getElementById('assets-list');
        assetsList.innerHTML = '';
        
        if (data.assets.length === 0) {
            assetsList.innerHTML = `
                <div class="text-center py-8">
                    <p class="text-2xl mb-2">🪙</p>
                    <p class="text-gray-500">No assets found.</p>
                    <p class="text-sm text-gray-400 mt-2">Fund your Lobstr wallet to get started!</p>
                </div>
            `;
        } else {
            data.assets.forEach(asset => {
                const assetDiv = document.createElement('div');
                assetDiv.className = 'p-4 bg-gray-50 rounded-lg hover:bg-gray-100 transition';
                assetDiv.innerHTML = `
                    <div class="flex justify-between items-center">
                        <div>
                            <span class="font-bold text-lg">${asset.asset}</span>
                            <p class="text-sm text-gray-600">${asset.balance.toFixed(4)}</p>
                        </div>
                        <div class="text-right">
                            <p class="font-semibold text-purple-600">$${asset.value.toFixed(2)}</p>
                        </div>
                    </div>
                `;
                assetsList.appendChild(assetDiv);
            });
        }
        
        showSuccess('📧 Portfolio analysis sent to your email!');
        
    } catch (error) {
        console.error('❌ Error loading portfolio:', error);
        showError('Failed to load portfolio data. Is the backend running?');
    }
}

// Load DeFi opportunities
async function loadOpportunities() {
    if (!connectedAccount) return;
    
    console.log('🔍 Loading opportunities...');
    
    try {
        const response = await fetch(`http://localhost:5000/api/opportunities/${connectedAccount}`);
        const opportunities = await response.json();
        
        console.log('✅ Opportunities loaded:', opportunities);
        
        const oppList = document.getElementById('opportunities-list');
        oppList.innerHTML = '';
        
        if (opportunities.length === 0) {
            oppList.innerHTML = `
                <div class="text-center py-8">
                    <p class="text-2xl mb-2">🚀</p>
                    <p class="text-gray-500">No opportunities available.</p>
                    <p class="text-sm text-gray-400 mt-2">Add assets to your wallet first!</p>
                </div>
            `;
        } else {
            opportunities.forEach(opp => {
                const oppDiv = document.createElement('div');
                oppDiv.className = 'p-4 border-2 border-gray-200 rounded-lg hover:border-purple-400 transition cursor-pointer';
                oppDiv.innerHTML = `
                    <div class="flex justify-between items-start mb-3">
                        <div>
                            <h4 class="font-bold text-lg">${opp.protocol}</h4>
                            <p class="text-sm text-gray-600">${opp.type}</p>
                        </div>
                        <span class="px-3 py-1 rounded-full text-xs font-semibold ${
                            opp.risk === 'Low' ? 'bg-green-100 text-green-800' :
                            opp.risk === 'Medium' ? 'bg-yellow-100 text-yellow-800' :
                            'bg-red-100 text-red-800'
                        }">${opp.risk} Risk</span>
                    </div>
                    <div class="grid grid-cols-2 gap-2 mb-3 text-sm">
                        <div>
                            <span class="text-gray-500">APY:</span>
                            <span class="font-bold text-green-600 ml-1">${opp.apy}</span>
                        </div>
                        <div>
                            <span class="text-gray-500">TVL:</span>
                            <span class="font-bold ml-1">${opp.tvl}</span>
                        </div>
                    </div>
                    <p class="text-sm text-gray-600 mb-3">${opp.description}</p>
                    <button class="w-full bg-gradient-to-r from-purple-600 to-blue-600 text-white py-2 rounded-lg font-semibold hover:from-purple-700 hover:to-blue-700 transition">
                        ${opp.action}
                    </button>
                `;
                oppList.appendChild(oppDiv);
            });
            
            if (opportunities.length > 0) {
                showSuccess(`📧 ${opportunities.length} opportunities found! Check your email for details.`);
            }
        }
        
    } catch (error) {
        console.error('❌ Error loading opportunities:', error);
        showError('Failed to load opportunities.');
    }
}

// Disconnect wallet
function disconnectWallet() {
    console.log('🔌 Disconnecting wallet...');
    
    connectedAccount = null;
    document.getElementById('connect-btn').style.display = 'block';
    document.getElementById('wallet-info').classList.add('hidden');
    document.getElementById('get-started').style.display = 'block';
    document.getElementById('dashboard').classList.add('hidden');
    document.getElementById('assets-list').innerHTML = '';
    document.getElementById('opportunities-list').innerHTML = '';
    document.getElementById('total-value').textContent = '$0.00';
    document.getElementById('asset-count').textContent = '0';
    document.getElementById('idle-count').textContent = '0';
    
    showSuccess('Wallet disconnected.');
}

// Utility functions
function showSuccess(message) {
    showNotification(message, 'success');
}

function showError(message) {
    showNotification(message, 'error');
}

function showNotification(message, type) {
    const notification = document.createElement('div');
    notification.className = `fixed top-4 right-4 px-6 py-4 rounded-lg shadow-2xl z-50 max-w-md animate-fade-in ${
        type === 'success' ? 'bg-green-500' : 'bg-red-500'
    } text-white`;
    notification.innerHTML = `
        <div class="flex items-center space-x-3">
            <span class="text-2xl">${type === 'success' ? '✅' : '❌'}</span>
            <p>${message}</p>
        </div>
    `;
    
    document.body.appendChild(notification);
    
    setTimeout(() => {
        notification.style.opacity = '0';
        notification.style.transform = 'translateX(100%)';
        notification.style.transition = 'all 0.5s';
        setTimeout(() => notification.remove(), 500);
    }, 5000);
}

// Initialize on page load
window.addEventListener('load', async () => {
    console.log('🌟 Stellar Compass loaded with Lobstr support!');
    
    // Check backend connection
    try {
        const response = await fetch('http://localhost:5000/api/health');
        const data = await response.json();
        console.log('✅ Backend connected:', data.message);
    } catch (error) {
        console.error('❌ Backend not reachable');
        showError('Backend server not running. Please start the backend on port 5000.');
    }
});