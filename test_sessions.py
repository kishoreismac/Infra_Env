#!/usr/bin/env python3
"""
Tests for the session tracking utility.
"""

import json
import os
import tempfile
import unittest
from pathlib import Path
from sessions import SessionTracker, format_session


class TestSessionTracker(unittest.TestCase):
    """Test cases for SessionTracker."""
    
    def setUp(self):
        """Set up test fixtures."""
        self.temp_file = tempfile.NamedTemporaryFile(delete=False, mode='w')
        self.temp_file.close()
        self.tracker = SessionTracker(data_file=self.temp_file.name)
    
    def tearDown(self):
        """Clean up test fixtures."""
        if os.path.exists(self.temp_file.name):
            os.unlink(self.temp_file.name)
    
    def test_add_session(self):
        """Test adding a session."""
        session = self.tracker.add_session('production', 'alice', 'Test session')
        self.assertEqual(session['environment'], 'production')
        self.assertEqual(session['user'], 'alice')
        self.assertEqual(session['description'], 'Test session')
        self.assertIn('timestamp', session)
    
    def test_get_recent_sessions(self):
        """Test getting recent sessions."""
        self.tracker.add_session('env1', 'user1', 'desc1')
        self.tracker.add_session('env2', 'user2', 'desc2')
        self.tracker.add_session('env3', 'user3', 'desc3')
        
        recent = self.tracker.get_recent_sessions(limit=2)
        self.assertEqual(len(recent), 2)
        self.assertEqual(recent[0]['environment'], 'env3')
        self.assertEqual(recent[1]['environment'], 'env2')
    
    def test_session_limit(self):
        """Test that sessions are limited to 50."""
        for i in range(60):
            self.tracker.add_session(f'env{i}', f'user{i}', f'desc{i}')
        
        self.assertEqual(len(self.tracker.sessions), 50)
        # First 10 sessions should be removed
        self.assertEqual(self.tracker.sessions[0]['environment'], 'env10')
    
    def test_clear_sessions(self):
        """Test clearing all sessions."""
        self.tracker.add_session('env1', 'user1', 'desc1')
        self.tracker.add_session('env2', 'user2', 'desc2')
        self.tracker.clear_sessions()
        self.assertEqual(len(self.tracker.sessions), 0)
        self.assertEqual(len(self.tracker.get_recent_sessions()), 0)
    
    def test_persistence(self):
        """Test that sessions are persisted to file."""
        self.tracker.add_session('env1', 'user1', 'desc1')
        
        # Create new tracker with same file
        tracker2 = SessionTracker(data_file=self.temp_file.name)
        sessions = tracker2.get_recent_sessions()
        self.assertEqual(len(sessions), 1)
        self.assertEqual(sessions[0]['environment'], 'env1')
    
    def test_format_session(self):
        """Test session formatting."""
        session = {
            'timestamp': '2026-02-18T08:50:14.651845',
            'environment': 'production',
            'user': 'alice',
            'description': 'Test'
        }
        formatted = format_session(session)
        self.assertIn('production', formatted)
        self.assertIn('alice', formatted)
        self.assertIn('Test', formatted)
    
    def test_format_session_no_description(self):
        """Test session formatting without description."""
        session = {
            'timestamp': '2026-02-18T08:50:14.651845',
            'environment': 'staging',
            'user': 'bob',
            'description': ''
        }
        formatted = format_session(session)
        self.assertIn('staging', formatted)
        self.assertIn('bob', formatted)


if __name__ == '__main__':
    unittest.main()
