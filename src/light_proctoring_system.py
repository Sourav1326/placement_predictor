"""
🔒 LIGHT PROCTORING SYSTEM
Test integrity features for skill verification challenges
"""

import json
import time
from datetime import datetime, timedelta
from typing import Dict, List, Any, Optional, Tuple
from dataclasses import dataclass
from enum import Enum

class ProctorEventType(Enum):
    """Types of proctoring events"""
    SESSION_START = "session_start"
    SESSION_END = "session_end"
    TAB_SWITCH = "tab_switch"
    WINDOW_BLUR = "window_blur"
    WINDOW_FOCUS = "window_focus"
    COPY_ATTEMPT = "copy_attempt"
    PASTE_ATTEMPT = "paste_attempt"
    RIGHT_CLICK = "right_click"
    KEYBOARD_SHORTCUT = "keyboard_shortcut"
    TIME_WARNING = "time_warning"
    TIME_EXPIRED = "time_expired"
    SUSPICIOUS_ACTIVITY = "suspicious_activity"
    FULLSCREEN_EXIT = "fullscreen_exit"

class RiskLevel(Enum):
    """Risk assessment levels"""
    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"
    CRITICAL = "critical"

@dataclass
class ProctorEvent:
    """Represents a proctoring event"""
    event_type: ProctorEventType
    timestamp: datetime
    risk_level: RiskLevel
    details: Dict[str, Any]
    user_agent: str = ""
    ip_address: str = ""

@dataclass
class ProctorSession:
    """Represents a proctored session"""
    session_id: str
    user_id: int
    assessment_type: str
    start_time: datetime
    end_time: Optional[datetime]
    time_limit: int  # in seconds
    events: List[ProctorEvent]
    integrity_score: float
    risk_flags: List[str]
    is_valid: bool

class LightProctoringSystem:
    """
    Lightweight proctoring system for maintaining test integrity
    """
    
    def __init__(self):
        self.active_sessions = {}  # session_id -> ProctorSession
        self.risk_thresholds = {
            'tab_switches': 3,           # Max allowed tab switches
            'suspicious_patterns': 2,     # Max suspicious events
            'copy_paste_attempts': 1,     # Max copy/paste attempts
            'window_blur_duration': 30,   # Max seconds window can be blurred
            'total_blur_time': 60        # Max total blur time
        }
        
        # JavaScript code for client-side monitoring
        self.client_monitoring_script = self._generate_monitoring_script()
    
    def start_proctored_session(self, user_id: int, assessment_type: str, 
                              time_limit: int, session_id: str) -> Dict[str, Any]:
        """
        Start a new proctored session
        """
        session = ProctorSession(
            session_id=session_id,
            user_id=user_id,
            assessment_type=assessment_type,
            start_time=datetime.now(),
            end_time=None,
            time_limit=time_limit,
            events=[],
            integrity_score=100.0,
            risk_flags=[],
            is_valid=True
        )
        
        self.active_sessions[session_id] = session
        
        # Log session start
        start_event = ProctorEvent(
            event_type=ProctorEventType.SESSION_START,
            timestamp=datetime.now(),
            risk_level=RiskLevel.LOW,
            details={
                'assessment_type': assessment_type,
                'time_limit': time_limit,
                'user_id': user_id
            }
        )
        self._log_event(session_id, start_event)
        
        return {
            'success': True,
            'session_id': session_id,
            'monitoring_script': self.client_monitoring_script,
            'proctoring_config': {
                'enable_tab_detection': True,
                'enable_copy_paste_detection': True,
                'enable_right_click_protection': True,
                'enable_keyboard_shortcuts_blocking': True,
                'show_time_warnings': True,
                'fullscreen_required': False  # Optional for better UX
            }
        }
    
    def log_proctor_event(self, session_id: str, event_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Log a proctoring event from the client
        """
        session = self.active_sessions.get(session_id)
        if not session:
            return {'success': False, 'error': 'Session not found'}
        
        # Create event
        event = ProctorEvent(
            event_type=ProctorEventType(event_data.get('event_type')),
            timestamp=datetime.now(),
            risk_level=self._assess_risk_level(event_data),
            details=event_data.get('details', {}),
            user_agent=event_data.get('user_agent', ''),
            ip_address=event_data.get('ip_address', '')
        )
        
        # Log the event
        self._log_event(session_id, event)
        
        # Update integrity score
        self._update_integrity_score(session_id, event)
        
        # Check for immediate actions needed
        response = self._check_immediate_actions(session_id, event)
        
        return {
            'success': True,
            'integrity_score': session.integrity_score,
            'risk_flags': session.risk_flags,
            'immediate_action': response
        }
    
    def end_proctored_session(self, session_id: str) -> Dict[str, Any]:
        """
        End a proctored session and generate integrity report
        """
        session = self.active_sessions.get(session_id)
        if not session:
            return {'success': False, 'error': 'Session not found'}
        
        session.end_time = datetime.now()
        
        # Log session end
        end_event = ProctorEvent(
            event_type=ProctorEventType.SESSION_END,
            timestamp=datetime.now(),
            risk_level=RiskLevel.LOW,
            details={
                'duration': (session.end_time - session.start_time).total_seconds(),
                'final_integrity_score': session.integrity_score
            }
        )
        self._log_event(session_id, end_event)
        
        # Generate integrity report
        integrity_report = self._generate_integrity_report(session)
        
        # Remove from active sessions
        del self.active_sessions[session_id]
        
        return {
            'success': True,
            'integrity_report': integrity_report,
            'session_valid': session.is_valid
        }
    
    def get_session_status(self, session_id: str) -> Dict[str, Any]:
        """
        Get current session status and integrity metrics
        """
        session = self.active_sessions.get(session_id)
        if not session:
            return {'success': False, 'error': 'Session not found'}
        
        current_time = datetime.now()
        elapsed_time = (current_time - session.start_time).total_seconds()
        time_remaining = max(0, session.time_limit - elapsed_time)
        
        # Count events by type
        event_counts = {}
        for event in session.events:
            event_type = event.event_type.value
            event_counts[event_type] = event_counts.get(event_type, 0) + 1
        
        return {
            'success': True,
            'session_id': session_id,
            'elapsed_time': elapsed_time,
            'time_remaining': time_remaining,
            'integrity_score': session.integrity_score,
            'risk_flags': session.risk_flags,
            'event_counts': event_counts,
            'is_valid': session.is_valid,
            'time_warnings_due': self._get_time_warnings(time_remaining)
        }
    
    def _generate_monitoring_script(self) -> str:
        """
        Generate JavaScript code for client-side monitoring
        """
        return '''
// Trust but Verify - Client-side Monitoring Script
class ProctorMonitor {
    constructor(sessionId, apiEndpoint) {
        this.sessionId = sessionId;
        this.apiEndpoint = apiEndpoint;
        this.events = [];
        this.isActive = true;
        this.tabSwitchCount = 0;
        this.windowBlurStart = null;
        this.totalBlurTime = 0;
        
        this.initializeMonitoring();
    }
    
    initializeMonitoring() {
        // Tab/Window visibility change detection
        document.addEventListener('visibilitychange', () => {
            if (document.hidden) {
                this.handleWindowBlur();
            } else {
                this.handleWindowFocus();
            }
        });
        
        // Window blur/focus events
        window.addEventListener('blur', () => this.handleWindowBlur());
        window.addEventListener('focus', () => this.handleWindowFocus());
        
        // Copy/Paste detection
        document.addEventListener('copy', (e) => this.handleCopyAttempt(e));
        document.addEventListener('paste', (e) => this.handlePasteAttempt(e));
        
        // Right-click protection
        document.addEventListener('contextmenu', (e) => this.handleRightClick(e));
        
        // Keyboard shortcuts detection
        document.addEventListener('keydown', (e) => this.handleKeyboardShortcut(e));
        
        // Fullscreen change detection
        document.addEventListener('fullscreenchange', () => this.handleFullscreenChange());
        
        // Prevent text selection in sensitive areas
        this.preventTextSelection();
        
        // Start heartbeat
        this.startHeartbeat();
    }
    
    handleWindowBlur() {
        this.windowBlurStart = Date.now();
        this.logEvent('window_blur', 'medium', {
            timestamp: Date.now(),
            tab_switch_count: ++this.tabSwitchCount
        });
    }
    
    handleWindowFocus() {
        if (this.windowBlurStart) {
            const blurDuration = Date.now() - this.windowBlurStart;
            this.totalBlurTime += blurDuration;
            this.windowBlurStart = null;
            
            this.logEvent('window_focus', 'medium', {
                blur_duration: blurDuration,
                total_blur_time: this.totalBlurTime
            });
            
            // Flag suspicious behavior
            if (blurDuration > 30000) { // 30 seconds
                this.logEvent('suspicious_activity', 'high', {
                    reason: 'Extended window blur',
                    duration: blurDuration
                });
            }
        }
    }
    
    handleCopyAttempt(event) {
        this.logEvent('copy_attempt', 'high', {
            selected_text_length: window.getSelection().toString().length,
            timestamp: Date.now()
        });
        
        // Optionally prevent copying
        // event.preventDefault();
    }
    
    handlePasteAttempt(event) {
        this.logEvent('paste_attempt', 'critical', {
            timestamp: Date.now()
        });
        
        // Prevent pasting in code areas
        if (event.target.classList.contains('code-editor')) {
            event.preventDefault();
            this.showWarning('Pasting is not allowed in the code editor.');
        }
    }
    
    handleRightClick(event) {
        this.logEvent('right_click', 'medium', {
            element: event.target.tagName,
            timestamp: Date.now()
        });
        
        // Prevent right-click context menu
        event.preventDefault();
    }
    
    handleKeyboardShortcut(event) {
        const forbiddenKeys = [
            'F12',           // Developer tools
            'Control+Shift+I', // Developer tools
            'Control+Shift+J', // Console
            'Control+U',       // View source
            'Control+Shift+C', // Element inspector
            'Alt+Tab',         // Application switcher
            'Control+Tab',     // Tab switcher
        ];
        
        const keyCombo = this.getKeyCombo(event);
        
        if (forbiddenKeys.includes(keyCombo)) {
            this.logEvent('keyboard_shortcut', 'critical', {
                key_combination: keyCombo,
                prevented: true
            });
            event.preventDefault();
            this.showWarning('This keyboard shortcut is not allowed during the assessment.');
        }
    }
    
    handleFullscreenChange() {
        if (!document.fullscreenElement) {
            this.logEvent('fullscreen_exit', 'medium', {
                timestamp: Date.now()
            });
        }
    }
    
    getKeyCombo(event) {
        let combo = '';
        if (event.ctrlKey) combo += 'Control+';
        if (event.altKey) combo += 'Alt+';
        if (event.shiftKey) combo += 'Shift+';
        combo += event.key;
        return combo;
    }
    
    preventTextSelection() {
        const style = document.createElement('style');
        style.textContent = `
            .no-select {
                -webkit-user-select: none;
                -moz-user-select: none;
                -ms-user-select: none;
                user-select: none;
            }
        `;
        document.head.appendChild(style);
    }
    
    logEvent(eventType, riskLevel, details) {
        if (!this.isActive) return;
        
        const event = {
            event_type: eventType,
            risk_level: riskLevel,
            details: details,
            user_agent: navigator.userAgent,
            timestamp: new Date().toISOString()
        };
        
        this.events.push(event);
        
        // Send to server
        fetch(`${this.apiEndpoint}/log-proctor-event/${this.sessionId}`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify(event)
        }).then(response => response.json())
          .then(data => {
              if (data.immediate_action) {
                  this.handleImmediateAction(data.immediate_action);
              }
              this.updateIntegrityDisplay(data.integrity_score);
          }).catch(error => {
              console.warn('Proctoring event logging failed:', error);
          });
    }
    
    handleImmediateAction(action) {
        switch(action.type) {
            case 'warning':
                this.showWarning(action.message);
                break;
            case 'suspend':
                this.suspendAssessment(action.message);
                break;
            case 'terminate':
                this.terminateAssessment(action.message);
                break;
        }
    }
    
    showWarning(message) {
        // Create warning modal
        const warning = document.createElement('div');
        warning.className = 'proctor-warning';
        warning.innerHTML = `
            <div class="warning-content">
                <h3>⚠️ Assessment Warning</h3>
                <p>${message}</p>
                <button onclick="this.parentElement.parentElement.remove()">Understood</button>
            </div>
        `;
        document.body.appendChild(warning);
        
        // Auto-remove after 5 seconds
        setTimeout(() => {
            if (warning.parentElement) {
                warning.remove();
            }
        }, 5000);
    }
    
    updateIntegrityDisplay(score) {
        const indicator = document.getElementById('integrity-indicator');
        if (indicator) {
            indicator.textContent = `Integrity: ${score.toFixed(1)}%`;
            
            if (score >= 80) {
                indicator.className = 'integrity-good';
            } else if (score >= 60) {
                indicator.className = 'integrity-warning';
            } else {
                indicator.className = 'integrity-critical';
            }
        }
    }
    
    startHeartbeat() {
        setInterval(() => {
            if (this.isActive) {
                this.logEvent('heartbeat', 'low', {
                    timestamp: Date.now(),
                    active_time: Date.now() - this.startTime
                });
            }
        }, 60000); // Every minute
    }
    
    suspendAssessment(message) {
        this.isActive = false;
        alert(`Assessment suspended: ${message}`);
        // Implement suspension logic
    }
    
    terminateAssessment(message) {
        this.isActive = false;
        alert(`Assessment terminated: ${message}`);
        window.location.href = '/assessment-terminated';
    }
    
    destroy() {
        this.isActive = false;
        // Remove event listeners
        document.removeEventListener('visibilitychange', this.handleVisibilityChange);
        // ... remove other listeners
    }
}

// CSS for warning modals
const proctorStyles = `
    .proctor-warning {
        position: fixed;
        top: 0;
        left: 0;
        width: 100%;
        height: 100%;
        background: rgba(0,0,0,0.8);
        display: flex;
        justify-content: center;
        align-items: center;
        z-index: 10000;
    }
    
    .warning-content {
        background: white;
        padding: 30px;
        border-radius: 10px;
        text-align: center;
        box-shadow: 0 10px 30px rgba(0,0,0,0.3);
    }
    
    .integrity-good { color: #28a745; font-weight: bold; }
    .integrity-warning { color: #ffc107; font-weight: bold; }
    .integrity-critical { color: #dc3545; font-weight: bold; }
    
    .no-select {
        -webkit-user-select: none;
        -moz-user-select: none;
        -ms-user-select: none;
        user-select: none;
    }
`;

const styleSheet = document.createElement('style');
styleSheet.textContent = proctorStyles;
document.head.appendChild(styleSheet);

// Export for use
window.ProctorMonitor = ProctorMonitor;
'''
    
    def _assess_risk_level(self, event_data: Dict[str, Any]) -> RiskLevel:
        """
        Assess risk level of an event
        """
        event_type = event_data.get('event_type')
        details = event_data.get('details', {})
        
        if event_type in ['copy_attempt', 'paste_attempt']:
            return RiskLevel.CRITICAL
        elif event_type == 'keyboard_shortcut' and details.get('prevented'):
            return RiskLevel.CRITICAL
        elif event_type == 'window_blur' and details.get('blur_duration', 0) > 30000:
            return RiskLevel.HIGH
        elif event_type in ['tab_switch', 'right_click']:
            return RiskLevel.MEDIUM
        else:
            return RiskLevel.LOW
    
    def _log_event(self, session_id: str, event: ProctorEvent):
        """
        Log an event to the session
        """
        session = self.active_sessions.get(session_id)
        if session:
            session.events.append(event)
    
    def _update_integrity_score(self, session_id: str, event: ProctorEvent):
        """
        Update session integrity score based on event
        """
        session = self.active_sessions.get(session_id)
        if not session:
            return
        
        # Score penalties based on risk level
        penalties = {
            RiskLevel.LOW: 0,
            RiskLevel.MEDIUM: 5,
            RiskLevel.HIGH: 15,
            RiskLevel.CRITICAL: 25
        }
        
        penalty = penalties.get(event.risk_level, 0)
        
        # Apply additional penalties for repeated violations
        event_type_count = sum(1 for e in session.events if e.event_type == event.event_type)
        if event_type_count > 1:
            penalty *= 1.5  # Increase penalty for repeated violations
        
        session.integrity_score = max(0, session.integrity_score - penalty)
        
        # Add risk flags
        if event.risk_level in [RiskLevel.HIGH, RiskLevel.CRITICAL]:
            flag = f"{event.event_type.value}_{event.risk_level.value}"
            if flag not in session.risk_flags:
                session.risk_flags.append(flag)
        
        # Mark session as invalid if integrity score drops too low
        if session.integrity_score < 50:
            session.is_valid = False
    
    def _check_immediate_actions(self, session_id: str, event: ProctorEvent) -> Optional[Dict[str, Any]]:
        """
        Check if immediate action is needed based on event
        """
        session = self.active_sessions.get(session_id)
        if not session:
            return None
        
        # Count critical events
        critical_events = sum(1 for e in session.events if e.risk_level == RiskLevel.CRITICAL)
        
        # Immediate termination conditions
        if critical_events >= 3:
            session.is_valid = False
            return {
                'type': 'terminate',
                'message': 'Assessment terminated due to multiple integrity violations.'
            }
        
        # Warning conditions
        if event.risk_level == RiskLevel.CRITICAL:
            return {
                'type': 'warning',
                'message': f'Integrity violation detected: {event.event_type.value}. Further violations may result in assessment termination.'
            }
        
        # Tab switch warnings
        tab_switches = sum(1 for e in session.events if e.event_type == ProctorEventType.TAB_SWITCH)
        if tab_switches >= self.risk_thresholds['tab_switches']:
            return {
                'type': 'warning',
                'message': 'Multiple tab switches detected. Please stay focused on the assessment.'
            }
        
        return None
    
    def _generate_integrity_report(self, session: ProctorSession) -> Dict[str, Any]:
        """
        Generate comprehensive integrity report
        """
        # Categorize events
        event_summary = {}
        risk_summary = {level.value: 0 for level in RiskLevel}
        
        for event in session.events:
            event_type = event.event_type.value
            event_summary[event_type] = event_summary.get(event_type, 0) + 1
            risk_summary[event.risk_level.value] += 1
        
        # Calculate session duration
        duration = (session.end_time - session.start_time).total_seconds() if session.end_time else 0
        
        # Assess overall integrity
        integrity_level = "High"
        if session.integrity_score < 70:
            integrity_level = "Low"
        elif session.integrity_score < 85:
            integrity_level = "Medium"
        
        # Generate recommendations
        recommendations = []
        if not session.is_valid:
            recommendations.append("Session marked as invalid due to integrity violations")
        if session.integrity_score < 80:
            recommendations.append("Consider manual review of assessment results")
        if risk_summary['critical'] > 0:
            recommendations.append("Critical violations detected - results may be compromised")
        
        return {
            'session_id': session.session_id,
            'user_id': session.user_id,
            'assessment_type': session.assessment_type,
            'duration_seconds': duration,
            'integrity_score': session.integrity_score,
            'integrity_level': integrity_level,
            'is_valid': session.is_valid,
            'event_summary': event_summary,
            'risk_summary': risk_summary,
            'risk_flags': session.risk_flags,
            'total_events': len(session.events),
            'recommendations': recommendations,
            'verification_confidence': self._calculate_verification_confidence(session)
        }
    
    def _calculate_verification_confidence(self, session: ProctorSession) -> float:
        """
        Calculate confidence level in the verification results
        """
        base_confidence = session.integrity_score
        
        # Factors that affect confidence
        duration_factor = min(1.0, session.time_limit / 600) * 10  # Longer assessments are more confident
        event_density = len(session.events) / max(1, session.time_limit / 60)  # Events per minute
        
        # Reduce confidence for suspicious patterns
        if event_density > 5:  # Too many events might indicate gaming
            base_confidence -= 10
        
        if session.risk_flags:
            base_confidence -= len(session.risk_flags) * 5
        
        return max(0, min(100, base_confidence + duration_factor))
    
    def _get_time_warnings(self, time_remaining: float) -> List[str]:
        """
        Generate time warnings based on remaining time
        """
        warnings = []
        
        if time_remaining <= 300:  # 5 minutes
            warnings.append("5 minutes remaining")
        elif time_remaining <= 600:  # 10 minutes
            warnings.append("10 minutes remaining")
        elif time_remaining <= 1800:  # 30 minutes
            warnings.append("30 minutes remaining")
        
        return warnings

# Example usage and testing
if __name__ == "__main__":
    # Initialize proctoring system
    proctor = LightProctoringSystem()
    
    # Start a proctored session
    session_result = proctor.start_proctored_session(
        user_id=1,
        assessment_type='live_coding',
        time_limit=900,  # 15 minutes
        session_id='test_session_123'
    )
    
    print("🔒 Proctored Session Started:")
    print(f"Success: {session_result['success']}")
    print(f"Session ID: {session_result['session_id']}")
    
    # Simulate some events
    test_events = [
        {
            'event_type': 'window_blur',
            'details': {'blur_duration': 5000},
            'user_agent': 'Test Browser'
        },
        {
            'event_type': 'tab_switch',
            'details': {'tab_switch_count': 1},
            'user_agent': 'Test Browser'
        },
        {
            'event_type': 'copy_attempt',
            'details': {'selected_text_length': 50},
            'user_agent': 'Test Browser'
        }
    ]
    
    print(f"\n📊 Logging Test Events:")
    for event in test_events:
        result = proctor.log_proctor_event('test_session_123', event)
        print(f"Event: {event['event_type']} - Integrity: {result.get('integrity_score', 0):.1f}%")
    
    # Get session status
    status = proctor.get_session_status('test_session_123')
    print(f"\n📈 Session Status:")
    print(f"Integrity Score: {status['integrity_score']:.1f}%")
    print(f"Risk Flags: {status['risk_flags']}")
    print(f"Valid: {status['is_valid']}")
    
    # End session and get report
    report_result = proctor.end_proctored_session('test_session_123')
    if report_result['success']:
        report = report_result['integrity_report']
        print(f"\n📋 Integrity Report:")
        print(f"Final Score: {report['integrity_score']:.1f}%")
        print(f"Integrity Level: {report['integrity_level']}")
        print(f"Verification Confidence: {report['verification_confidence']:.1f}%")
        print(f"Recommendations: {report['recommendations']}")
    
    print("\n🎯 Light Proctoring System ready for integration!")