#!/usr/bin/env python3
"""
Session tracking utility for infrastructure environments.
Tracks and displays recent session information.
"""

import json
import os
from datetime import datetime
from pathlib import Path


class SessionTracker:
    """Tracks and manages session information."""
    
    def __init__(self, data_file=None):
        """Initialize the session tracker."""
        if data_file is None:
            data_file = Path.home() / '.infra_env_sessions.json'
        self.data_file = Path(data_file)
        self.sessions = self._load_sessions()
    
    def _load_sessions(self):
        """Load sessions from the data file."""
        if self.data_file.exists():
            try:
                with open(self.data_file, 'r') as f:
                    return json.load(f)
            except (json.JSONDecodeError, IOError):
                return []
        return []
    
    def _save_sessions(self):
        """Save sessions to the data file."""
        self.data_file.parent.mkdir(parents=True, exist_ok=True)
        with open(self.data_file, 'w') as f:
            json.dump(self.sessions, f, indent=2)
    
    def add_session(self, environment, user, description=''):
        """Add a new session."""
        session = {
            'timestamp': datetime.now().isoformat(),
            'environment': environment,
            'user': user,
            'description': description
        }
        self.sessions.append(session)
        # Keep only the last 50 sessions
        if len(self.sessions) > 50:
            self.sessions = self.sessions[-50:]
        self._save_sessions()
        return session
    
    def get_recent_sessions(self, limit=10):
        """Get the most recent sessions."""
        return list(reversed(self.sessions[-limit:]))
    
    def clear_sessions(self):
        """Clear all sessions."""
        self.sessions = []
        self._save_sessions()


def format_session(session):
    """Format a session for display."""
    timestamp = datetime.fromisoformat(session['timestamp'])
    time_str = timestamp.strftime('%Y-%m-%d %H:%M:%S')
    env = session['environment']
    user = session['user']
    desc = session.get('description', '')
    
    if desc:
        return f"{time_str} | {env:15} | {user:15} | {desc}"
    else:
        return f"{time_str} | {env:15} | {user:15}"


def main():
    """Main CLI entry point."""
    import argparse
    
    parser = argparse.ArgumentParser(
        description='Track and display recent infrastructure sessions'
    )
    subparsers = parser.add_subparsers(dest='command', help='Commands')
    
    # List command
    list_parser = subparsers.add_parser('list', help='List recent sessions')
    list_parser.add_argument(
        '-n', '--number',
        type=int,
        default=10,
        help='Number of recent sessions to show (default: 10)'
    )
    
    # Add command
    add_parser = subparsers.add_parser('add', help='Add a new session')
    add_parser.add_argument('environment', help='Environment name')
    add_parser.add_argument('user', help='User name')
    add_parser.add_argument(
        '-d', '--description',
        default='',
        help='Optional session description'
    )
    
    # Clear command
    subparsers.add_parser('clear', help='Clear all sessions')
    
    args = parser.parse_args()
    
    tracker = SessionTracker()
    
    if args.command == 'list' or args.command is None:
        limit = getattr(args, 'number', 10)
        sessions = tracker.get_recent_sessions(limit=limit)
        if not sessions:
            print("No recent sessions found.")
        else:
            print("Recent Sessions:")
            print("-" * 80)
            for session in sessions:
                print(format_session(session))
    
    elif args.command == 'add':
        session = tracker.add_session(
            args.environment,
            args.user,
            args.description
        )
        print(f"Added session: {format_session(session)}")
    
    elif args.command == 'clear':
        tracker.clear_sessions()
        print("All sessions cleared.")


if __name__ == '__main__':
    main()
