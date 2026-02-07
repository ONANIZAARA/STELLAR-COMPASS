"""
AI Agent System for Stellar Compass
Autonomous agents that monitor and alert users
"""

from datetime import datetime, timedelta
from typing import List, Dict, Optional
import threading
import time


class BaseAgent:
    """Base class for all AI agents"""
    
    def __init__(self, name: str, check_interval_minutes: int = 5):
        self.name = name
        self.check_interval = check_interval_minutes * 60  # Convert to seconds
        self.is_active = False
        self.last_check = None
        self.thread = None
    
    def start(self):
        """Start the agent monitoring"""
        self.is_active = True
        self.thread = threading.Thread(target=self._run_loop, daemon=True)
        self.thread.start()
    
    def stop(self):
        """Stop the agent"""
        self.is_active = False
    
    def _run_loop(self):
        """Main monitoring loop"""
        while self.is_active:
            try:
                self.check()
                self.last_check = datetime.now()
                time.sleep(self.check_interval)
            except Exception as e:
                print(f"Error in {self.name}: {e}")
                time.sleep(60)  # Wait a minute before retrying
    
    def check(self):
        """Override this method in subclasses"""
        raise NotImplementedError


class IdleAssetMonitorAgent(BaseAgent):
    """Monitors for idle assets and sends alerts"""
    
    def __init__(self, wallet_address: str, notification_callback):
        super().__init__("Idle Asset Monitor", check_interval_minutes=5)
        self.wallet_address = wallet_address
        self.notify = notification_callback
        self.idle_threshold_days = 30
    
    def check(self):
        """Check for idle assets"""
        # Mock: In production, fetch real wallet data
        idle_assets = self._get_idle_assets()
        
        for asset in idle_assets:
            if asset['days_idle'] >= self.idle_threshold_days:
                self.notify({
                    'type': 'IDLE_ASSET',
                    'priority': 'MEDIUM' if asset['days_idle'] < 60 else 'HIGH',
                    'title': f'{asset["asset"]} sitting idle for {asset["days_idle"]} days',
                    'message': f'${asset["value_usd"]:.2f} could be earning ${asset["potential_monthly"]:.2f}/month',
                    'action': 'Activate Now',
                    'timestamp': datetime.now().isoformat()
                })
    
    def _get_idle_assets(self):
        """Mock function - replace with real data"""
        return [
            {'asset': 'XLM', 'days_idle': 45, 'value_usd': 600, 'potential_monthly': 4.8},
            {'asset': 'USDC', 'days_idle': 33, 'value_usd': 1500, 'potential_monthly': 12}
        ]


class OpportunityScoutAgent(BaseAgent):
    """Finds new yield opportunities and APY spikes"""
    
    def __init__(self, wallet_address: str, notification_callback, risk_tolerance: str = 'moderate'):
        super().__init__("Opportunity Scout", check_interval_minutes=5)
        self.wallet_address = wallet_address
        self.notify = notification_callback
        self.risk_tolerance = risk_tolerance
        self.tracked_apys = {}
    
    def check(self):
        """Check for new opportunities"""
        opportunities = self._get_current_opportunities()
        
        for opp in opportunities:
            protocol = opp['protocol']
            current_apy = opp['apy']
            
            # Check if APY spiked
            if protocol in self.tracked_apys:
                previous_apy = self.tracked_apys[protocol]
                increase = current_apy - previous_apy
                
                if increase > 2:  # 2% increase
                    self.notify({
                        'type': 'APY_SPIKE',
                        'priority': 'HIGH',
                        'title': f'{protocol} APY jumped to {current_apy}%',
                        'message': f'Up {increase:.1f}% from {previous_apy:.1f}%. Time to invest?',
                        'action': 'View Details',
                        'timestamp': datetime.now().isoformat()
                    })
            
            self.tracked_apys[protocol] = current_apy
    
    def _get_current_opportunities(self):
        """Mock function"""
        return [
            {'protocol': 'Aquarius', 'apy': 12.5, 'risk': 'MODERATE'},
            {'protocol': 'Stellar Lend', 'apy': 8.3, 'risk': 'LOW'}
        ]


class RiskMonitorAgent(BaseAgent):
    """Monitors protocol risks and portfolio health"""
    
    def __init__(self, wallet_address: str, notification_callback):
        super().__init__("Risk Monitor", check_interval_minutes=10)
        self.wallet_address = wallet_address
        self.notify = notification_callback
    
    def check(self):
        """Check for risk issues"""
        risks = self._check_risks()
        
        for risk in risks:
            if risk['severity'] in ['HIGH', 'CRITICAL']:
                self.notify({
                    'type': 'RISK_ALERT',
                    'priority': 'CRITICAL' if risk['severity'] == 'CRITICAL' else 'HIGH',
                    'title': risk['title'],
                    'message': risk['message'],
                    'action': 'Review Position',
                    'timestamp': datetime.now().isoformat()
                })
    
    def _check_risks(self):
        """Mock function"""
        return [
            {
                'severity': 'MEDIUM',
                'title': 'Portfolio concentration risk',
                'message': '85% of portfolio in single protocol. Consider diversifying.'
            }
        ]


class AutoRebalancerAgent(BaseAgent):
    """Detects portfolio drift and suggests rebalancing"""
    
    def __init__(self, wallet_address: str, notification_callback, target_allocation: Dict):
        super().__init__("Auto Rebalancer", check_interval_minutes=60)
        self.wallet_address = wallet_address
        self.notify = notification_callback
        self.target_allocation = target_allocation
        self.drift_threshold = 0.10  # 10% drift triggers alert
    
    def check(self):
        """Check portfolio balance"""
        current_allocation = self._get_current_allocation()
        
        for risk_level, target_pct in self.target_allocation.items():
            current_pct = current_allocation.get(risk_level, 0)
            drift = abs(current_pct - target_pct)
            
            if drift > self.drift_threshold:
                self.notify({
                    'type': 'REBALANCE',
                    'priority': 'MEDIUM',
                    'title': 'Portfolio needs rebalancing',
                    'message': f'{risk_level} allocation drifted {drift*100:.1f}% from target',
                    'action': 'Rebalance',
                    'timestamp': datetime.now().isoformat()
                })
    
    def _get_current_allocation(self):
        """Mock function"""
        return {'LOW': 0.45, 'MODERATE': 0.35, 'HIGH': 0.20}


class YieldHarvesterAgent(BaseAgent):
    """Tracks unclaimed rewards and optimal claim times"""
    
    def __init__(self, wallet_address: str, notification_callback):
        super().__init__("Yield Harvester", check_interval_minutes=60)
        self.wallet_address = wallet_address
        self.notify = notification_callback
        self.min_claim_threshold = 1.0  # $1 minimum to claim
    
    def check(self):
        """Check for unclaimed rewards"""
        unclaimed = self._get_unclaimed_rewards()
        
        total_unclaimed = sum(r['value_usd'] for r in unclaimed)
        
        if total_unclaimed >= self.min_claim_threshold:
            self.notify({
                'type': 'HARVEST',
                'priority': 'LOW',
                'title': f'${total_unclaimed:.2f} in unclaimed rewards',
                'message': f'Ready to harvest from {len(unclaimed)} protocols',
                'action': 'Claim All',
                'timestamp': datetime.now().isoformat()
            })
    
    def _get_unclaimed_rewards(self):
        """Mock function"""
        return [
            {'protocol': 'Aquarius', 'asset': 'XLM', 'amount': 8.5, 'value_usd': 1.02}
        ]


class PriceMovementAgent(BaseAgent):
    """Monitors significant price movements"""
    
    def __init__(self, wallet_address: str, notification_callback):
        super().__init__("Price Movement Monitor", check_interval_minutes=5)
        self.wallet_address = wallet_address
        self.notify = notification_callback
        self.price_threshold = 0.05  # 5% movement triggers alert
        self.last_prices = {}
    
    def check(self):
        """Check for price movements"""
        current_prices = self._get_current_prices()
        
        for asset, price in current_prices.items():
            if asset in self.last_prices:
                previous = self.last_prices[asset]
                change = (price - previous) / previous
                
                if abs(change) >= self.price_threshold:
                    direction = "up" if change > 0 else "down"
                    self.notify({
                        'type': 'PRICE_MOVEMENT',
                        'priority': 'MEDIUM' if abs(change) < 0.10 else 'HIGH',
                        'title': f'{asset} {direction} {abs(change)*100:.1f}%',
                        'message': f'Current price: ${price:.4f}',
                        'action': 'Check Portfolio',
                        'timestamp': datetime.now().isoformat()
                    })
            
            self.last_prices[asset] = price
    
    def _get_current_prices(self):
        """Mock function"""
        return {'XLM': 0.12, 'USDC': 1.00, 'BTC': 45000}


class AgentOrchestrator:
    """Manages all AI agents and coordinates notifications"""
    
    def __init__(self, wallet_address: str, notification_channels: Dict,
                 phone_number: str = '', risk_tolerance: str = 'moderate'):
        self.wallet_address = wallet_address
        self.notification_channels = notification_channels
        self.phone_number = phone_number
        self.risk_tolerance = risk_tolerance
        self.agents = []
        self.alert_history = []
        
        # Target allocation for rebalancer
        self.target_allocation = {
            'conservative': {'LOW': 0.80, 'MODERATE': 0.20, 'HIGH': 0.00},
            'moderate': {'LOW': 0.50, 'MODERATE': 0.40, 'HIGH': 0.10},
            'aggressive': {'LOW': 0.30, 'MODERATE': 0.40, 'HIGH': 0.30}
        }.get(risk_tolerance.lower(), {'LOW': 0.50, 'MODERATE': 0.40, 'HIGH': 0.10})
    
    def activate_all_agents(self):
        """Start all AI agents"""
        self.agents = [
            IdleAssetMonitorAgent(self.wallet_address, self._handle_notification),
            OpportunityScoutAgent(self.wallet_address, self._handle_notification, self.risk_tolerance),
            RiskMonitorAgent(self.wallet_address, self._handle_notification),
            AutoRebalancerAgent(self.wallet_address, self._handle_notification, self.target_allocation),
            YieldHarvesterAgent(self.wallet_address, self._handle_notification),
            PriceMovementAgent(self.wallet_address, self._handle_notification)
        ]
        
        for agent in self.agents:
            agent.start()
            print(f"✅ {agent.name} activated")
    
    def deactivate_all_agents(self):
        """Stop all agents"""
        for agent in self.agents:
            agent.stop()
            print(f"⏹️ {agent.name} deactivated")
    
    def _handle_notification(self, alert: Dict):
        """Process and route notifications"""
        # Add to history
        self.alert_history.append(alert)
        
        # Keep only last 100 alerts
        if len(self.alert_history) > 100:
            self.alert_history = self.alert_history[-100:]
        
        print(f"🔔 Alert: [{alert['priority']}] {alert['title']}")
        
        # Route to appropriate channels
        if self.notification_channels.get('push', True):
            self._send_push_notification(alert)
        
        if self.notification_channels.get('email', True):
            self._send_email_notification(alert)
        
        if self.notification_channels.get('sms', False) and alert['priority'] in ['HIGH', 'CRITICAL']:
            self._send_sms_notification(alert)
    
    def _send_push_notification(self, alert: Dict):
        """Send push notification (implement with FCM/APNS)"""
        print(f"  📱 Push: {alert['message']}")
    
    def _send_email_notification(self, alert: Dict):
        """Send email notification (implement with SendGrid/SES)"""
        print(f"  📧 Email: {alert['message']}")
    
    def _send_sms_notification(self, alert: Dict):
        """Send SMS notification (implement with Twilio)"""
        if not self.phone_number:
            return
        
        # Truncate for SMS (160 chars)
        sms_message = f"[{alert['priority']}] Stellar Compass: {alert['message'][:120]}"
        print(f"  📱 SMS to {self.phone_number}: {sms_message}")
    
    def get_recent_alerts(self, limit: int = 20) -> List[Dict]:
        """Get recent alerts"""
        return self.alert_history[-limit:]
    
    def update_settings(self, settings: Dict):
        """Update agent settings"""
        if 'phoneNumber' in settings:
            self.phone_number = settings['phoneNumber']
        
        if 'riskTolerance' in settings:
            self.risk_tolerance = settings['riskTolerance']
        
        if 'emailNotifications' in settings:
            self.notification_channels['email'] = settings['emailNotifications']
        
        if 'smsNotifications' in settings:
            self.notification_channels['sms'] = settings['smsNotifications']
        
        if 'pushNotifications' in settings:
            self.notification_channels['push'] = settings['pushNotifications']
        
        print(f"⚙️ Settings updated for {self.wallet_address}")
