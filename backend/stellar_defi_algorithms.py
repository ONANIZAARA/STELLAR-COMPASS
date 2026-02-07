"""
Stellar DeFi Analysis Algorithms
Core algorithms for portfolio analysis and yield optimization
"""

from datetime import datetime, timedelta
from typing import List, Dict, Tuple
import random


class IdleAssetDetector:
    """Detects crypto assets sitting idle without generating yield"""
    
    def __init__(self, idle_threshold_days: int = 30):
        self.idle_threshold_days = idle_threshold_days
    
    def detect_idle_assets(self, wallet_address: str, balances: List[Dict]) -> List[Dict]:
        """
        Scans wallet for assets sitting >30 days without activity
        
        Args:
            wallet_address: User's wallet address
            balances: List of balance objects
            
        Returns:
            List of idle assets with opportunity cost
        """
        idle_assets = []
        
        for balance in balances:
            # Mock: Check if asset has been idle
            # In production, query transaction history from Horizon
            days_idle = random.randint(0, 90)  # Mock data
            
            if days_idle >= self.idle_threshold_days and balance['balance'] > 0:
                # Calculate opportunity cost (assuming 8% average APY)
                daily_rate = 0.08 / 365
                opportunity_cost = balance['value_usd'] * daily_rate * days_idle
                
                idle_assets.append({
                    'asset': balance['asset'],
                    'balance': balance['balance'],
                    'value_usd': balance['value_usd'],
                    'days_idle': days_idle,
                    'opportunity_cost': opportunity_cost
                })
        
        return sorted(idle_assets, key=lambda x: x['opportunity_cost'], reverse=True)


class YieldOpportunityMatcher:
    """Matches user holdings with best yield opportunities"""
    
    def __init__(self):
        # Stellar DeFi protocols
        self.protocols = self._load_stellar_protocols()
    
    def _load_stellar_protocols(self) -> List[Dict]:
        """Load available Stellar DeFi protocols"""
        return [
            {
                'name': 'Aquarius',
                'type': 'liquidity_pool',
                'assets': ['XLM', 'USDC', 'USDT'],
                'base_apy': 12.5,
                'risk_level': 'MODERATE'
            },
            {
                'name': 'Stellar Lend',
                'type': 'lending',
                'assets': ['XLM', 'USDC'],
                'base_apy': 8.3,
                'risk_level': 'LOW'
            },
            {
                'name': 'Ultrastellar',
                'type': 'staking',
                'assets': ['XLM'],
                'base_apy': 5.2,
                'risk_level': 'LOW'
            },
            {
                'name': 'StellarX AMM',
                'type': 'liquidity_pool',
                'assets': ['XLM', 'USDC', 'BTC', 'ETH'],
                'base_apy': 15.8,
                'risk_level': 'MODERATE'
            },
            {
                'name': 'Yndx Finance',
                'type': 'yield_aggregator',
                'assets': ['XLM', 'USDC'],
                'base_apy': 10.2,
                'risk_level': 'MODERATE'
            }
        ]
    
    def find_opportunities(self, balances: List[Dict], risk_tolerance: str = 'moderate') -> List[Dict]:
        """
        Find yield opportunities based on user's holdings
        
        Args:
            balances: User's current balances
            risk_tolerance: 'conservative', 'moderate', or 'aggressive'
            
        Returns:
            Ranked list of yield opportunities
        """
        opportunities = []
        
        for balance in balances:
            if balance['balance'] == 0:
                continue
            
            asset = balance['asset']
            
            # Find protocols that support this asset
            for protocol in self.protocols:
                if asset in protocol['assets']:
                    # Filter by risk tolerance
                    if not self._matches_risk_tolerance(protocol['risk_level'], risk_tolerance):
                        continue
                    
                    # Calculate potential earnings
                    monthly_earnings = (balance['value_usd'] * protocol['base_apy'] / 100) / 12
                    
                    opportunities.append({
                        'protocol': protocol['name'],
                        'asset': asset,
                        'type': protocol['type'],
                        'apy': protocol['base_apy'],
                        'risk_level': protocol['risk_level'],
                        'potential_earnings': monthly_earnings,
                        'min_investment': 10  # USD
                    })
        
        # Rank by APY and risk-adjusted returns
        return sorted(opportunities, key=lambda x: x['apy'], reverse=True)
    
    def _matches_risk_tolerance(self, protocol_risk: str, user_tolerance: str) -> bool:
        """Check if protocol matches user's risk tolerance"""
        risk_map = {
            'conservative': ['LOW'],
            'moderate': ['LOW', 'MODERATE'],
            'aggressive': ['LOW', 'MODERATE', 'HIGH']
        }
        return protocol_risk in risk_map.get(user_tolerance.lower(), ['MODERATE'])


class RiskScoringEngine:
    """Evaluates protocol safety and assigns risk scores"""
    
    def score_protocol(self, protocol_name: str) -> Dict:
        """
        Evaluate protocol based on multiple factors
        
        Args:
            protocol_name: Name of the DeFi protocol
            
        Returns:
            Risk score object
        """
        # Mock data - in production, fetch real metrics
        protocols_data = {
            'Aquarius': {
                'time_active_days': 730,
                'tvl_usd': 45_000_000,
                'audit_status': 'audited',
                'exploit_history': []
            },
            'Stellar Lend': {
                'time_active_days': 365,
                'tvl_usd': 12_000_000,
                'audit_status': 'audited',
                'exploit_history': []
            },
            'Ultrastellar': {
                'time_active_days': 900,
                'tvl_usd': 8_500_000,
                'audit_status': 'audited',
                'exploit_history': []
            },
            'StellarX AMM': {
                'time_active_days': 1095,
                'tvl_usd': 28_000_000,
                'audit_status': 'audited',
                'exploit_history': []
            },
            'Yndx Finance': {
                'time_active_days': 180,
                'tvl_usd': 5_000_000,
                'audit_status': 'pending',
                'exploit_history': []
            }
        }
        
        data = protocols_data.get(protocol_name, {})
        
        # Calculate risk scores (0-100, lower is safer)
        time_score = max(0, 100 - (data.get('time_active_days', 0) / 10))
        tvl_score = max(0, 100 - (data.get('tvl_usd', 0) / 500_000))
        audit_score = 0 if data.get('audit_status') == 'audited' else 50
        exploit_score = len(data.get('exploit_history', [])) * 30
        
        overall_score = (time_score + tvl_score + audit_score + exploit_score) / 4
        
        # Categorize risk
        if overall_score < 30:
            risk_level = 'LOW'
        elif overall_score < 60:
            risk_level = 'MODERATE'
        else:
            risk_level = 'HIGH'
        
        return {
            'protocol': protocol_name,
            'overall_score': round(overall_score, 2),
            'risk_level': risk_level,
            'factors': {
                'time_active': time_score,
                'tvl': tvl_score,
                'audit': audit_score,
                'exploits': exploit_score
            },
            'recommendation': 'Recommended' if overall_score < 50 else 'Use caution'
        }


class PortfolioOptimizer:
    """Suggests optimal allocation across protocols"""
    
    def optimize_allocation(self, balances: List[Dict], opportunities: List[Dict], 
                          risk_tolerance: str = 'moderate') -> Dict:
        """
        Suggest optimal portfolio allocation
        
        Args:
            balances: Current holdings
            opportunities: Available yield opportunities
            risk_tolerance: User's risk tolerance
            
        Returns:
            Optimized allocation strategy
        """
        total_value = sum(b['value_usd'] for b in balances)
        
        # Allocation strategy based on risk tolerance
        allocation_strategies = {
            'conservative': {'LOW': 0.80, 'MODERATE': 0.20, 'HIGH': 0.00},
            'moderate': {'LOW': 0.50, 'MODERATE': 0.40, 'HIGH': 0.10},
            'aggressive': {'LOW': 0.30, 'MODERATE': 0.40, 'HIGH': 0.30}
        }
        
        target_allocation = allocation_strategies.get(risk_tolerance.lower(), 
                                                     allocation_strategies['moderate'])
        
        # Group opportunities by risk level
        allocations = []
        for risk_level, percentage in target_allocation.items():
            allocation_amount = total_value * percentage
            
            # Find best opportunities for this risk level
            risk_opps = [o for o in opportunities if o['risk_level'] == risk_level]
            
            if risk_opps and allocation_amount > 0:
                best_opp = max(risk_opps, key=lambda x: x['apy'])
                allocations.append({
                    'protocol': best_opp['protocol'],
                    'asset': best_opp['asset'],
                    'allocation_usd': allocation_amount,
                    'allocation_percentage': percentage * 100,
                    'expected_apy': best_opp['apy'],
                    'risk_level': risk_level
                })
        
        projected_annual_return = sum(
            a['allocation_usd'] * a['expected_apy'] / 100 
            for a in allocations
        )
        
        return {
            'allocations': allocations,
            'total_allocated': total_value,
            'projected_annual_return': projected_annual_return,
            'projected_monthly_return': projected_annual_return / 12,
            'strategy': risk_tolerance
        }


class TransactionOptimizer:
    """Optimizes transaction costs and batching"""
    
    def prepare_transaction(self, wallet_address: str, opportunity_id: str) -> Dict:
        """
        Prepare optimized transaction
        
        Args:
            wallet_address: User's wallet
            opportunity_id: ID of opportunity to execute
            
        Returns:
            Transaction details
        """
        # Stellar transactions are very cheap (0.00001 XLM per operation)
        base_fee_xlm = 0.00001
        
        return {
            'wallet_address': wallet_address,
            'opportunity_id': opportunity_id,
            'estimated_fee_xlm': base_fee_xlm,
            'estimated_fee_usd': base_fee_xlm * 0.12,  # Mock XLM price
            'recommended_time': 'now',  # Stellar is always fast
            'steps': [
                'Approve transaction in wallet',
                'Sign with your private key',
                'Transaction will confirm in ~5 seconds'
            ]
        }
    
    def estimate_batch_savings(self, transaction_count: int) -> Dict:
        """
        Estimate savings from batching transactions
        
        Args:
            transaction_count: Number of transactions to batch
            
        Returns:
            Savings breakdown
        """
        single_fee = 0.00001  # XLM per transaction
        batch_fee = 0.00001 * transaction_count  # Same on Stellar
        
        return {
            'individual_cost': single_fee * transaction_count,
            'batch_cost': batch_fee,
            'savings': 0,  # No savings on Stellar, fees are already minimal
            'savings_percentage': 0,
            'note': 'Stellar fees are already extremely low (<$0.0001 per transaction)'
        }
