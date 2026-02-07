"""
Stellar Horizon API Client
Handles all interactions with the Stellar blockchain
"""

import requests
from datetime import datetime, timedelta
from typing import List, Dict, Optional


class StellarHorizonClient:
    """Client for interacting with Stellar Horizon API"""
    
    def __init__(self, network='testnet'):
        """
        Initialize Horizon client
        
        Args:
            network: 'testnet' or 'mainnet'
        """
        if network == 'testnet':
            self.horizon_url = 'https://horizon-testnet.stellar.org'
        else:
            self.horizon_url = 'https://horizon.stellar.org'
        
        self.session = requests.Session()
        self.session.headers.update({
            'Content-Type': 'application/json'
        })
    
    def get_account_balances(self, public_key: str) -> List[Dict]:
        """
        Get all balances for an account
        
        Args:
            public_key: Stellar public key
            
        Returns:
            List of balance objects with asset, balance, and value
        """
        try:
            response = self.session.get(f"{self.horizon_url}/accounts/{public_key}")
            response.raise_for_status()
            
            account_data = response.json()
            balances = []
            
            for balance in account_data.get('balances', []):
                asset_code = balance.get('asset_code', 'XLM')
                asset_balance = float(balance.get('balance', 0))
                
                # Get USD value (mock for now, in production use price oracle)
                usd_value = self._get_asset_price(asset_code) * asset_balance
                
                balances.append({
                    'asset': asset_code,
                    'balance': asset_balance,
                    'value_usd': usd_value,
                    'asset_type': balance.get('asset_type', 'native')
                })
            
            return balances
            
        except requests.exceptions.RequestException as e:
            print(f"Error fetching balances: {e}")
            return self._get_mock_balances()
    
    def get_account_transactions(self, public_key: str, limit: int = 200) -> List[Dict]:
        """
        Get recent transactions for an account
        
        Args:
            public_key: Stellar public key
            limit: Number of transactions to fetch
            
        Returns:
            List of transaction objects
        """
        try:
            response = self.session.get(
                f"{self.horizon_url}/accounts/{public_key}/transactions",
                params={'limit': limit, 'order': 'desc'}
            )
            response.raise_for_status()
            
            data = response.json()
            transactions = []
            
            for tx in data.get('_embedded', {}).get('records', []):
                transactions.append({
                    'id': tx.get('id'),
                    'created_at': tx.get('created_at'),
                    'source_account': tx.get('source_account'),
                    'successful': tx.get('successful')
                })
            
            return transactions
            
        except requests.exceptions.RequestException as e:
            print(f"Error fetching transactions: {e}")
            return []
    
    def get_last_transaction_date(self, public_key: str, asset: str = None) -> Optional[datetime]:
        """
        Get the date of the last transaction for an account or specific asset
        
        Args:
            public_key: Stellar public key
            asset: Optional asset code to filter by
            
        Returns:
            Datetime of last transaction or None
        """
        transactions = self.get_account_transactions(public_key, limit=50)
        
        if not transactions:
            return None
        
        # Return most recent transaction date
        if transactions:
            return datetime.fromisoformat(transactions[0]['created_at'].replace('Z', '+00:00'))
        
        return None
    
    def _get_asset_price(self, asset_code: str) -> float:
        """
        Get current USD price for an asset
        
        Args:
            asset_code: Asset code (e.g., 'XLM', 'USDC')
            
        Returns:
            Price in USD
        """
        # Mock prices - in production, use a price oracle like CoinGecko
        prices = {
            'XLM': 0.12,
            'USDC': 1.00,
            'USDT': 1.00,
            'BTC': 45000.00,
            'ETH': 2500.00
        }
        return prices.get(asset_code, 0.10)
    
    def _get_mock_balances(self) -> List[Dict]:
        """Return mock balances for testing"""
        return [
            {
                'asset': 'XLM',
                'balance': 5000.0,
                'value_usd': 600.0,
                'asset_type': 'native'
            },
            {
                'asset': 'USDC',
                'balance': 1500.0,
                'value_usd': 1500.0,
                'asset_type': 'credit_alphanum4'
            }
        ]
    
    def get_current_timestamp(self) -> str:
        """Get current timestamp"""
        return datetime.utcnow().isoformat()
    
    def estimate_gas_cost(self, operation_count: int = 1) -> float:
        """
        Estimate transaction cost on Stellar
        
        Args:
            operation_count: Number of operations in transaction
            
        Returns:
            Cost in XLM
        """
        # Stellar base fee is 100 stroops (0.00001 XLM) per operation
        base_fee = 0.00001
        return base_fee * operation_count
    
    def build_payment_transaction(self, source: str, destination: str, 
                                  asset: str, amount: float) -> Dict:
        """
        Build a payment transaction (mock)
        
        Args:
            source: Source account public key
            destination: Destination account public key
            asset: Asset code
            amount: Amount to send
            
        Returns:
            Transaction object
        """
        return {
            'source': source,
            'destination': destination,
            'asset': asset,
            'amount': amount,
            'fee': self.estimate_gas_cost(),
            'memo': 'Stellar Compass Transaction'
        }
