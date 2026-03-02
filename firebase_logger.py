"""
Firebase State Manager for AEMP
Handles all Firebase interactions for logging, state persistence, and real-time monitoring
"""
import json
import logging
from typing import Dict, Any, Optional, List
from datetime import datetime
from dataclasses import asdict
import firebase_admin
from firebase_admin import credentials, firestore
from firebase_admin.exceptions import FirebaseError
from config import config

class FirebaseManager:
    """Manages Firebase Firestore connections and operations"""
    
    def __init__(self):
        self._initialized = False
        self._db = None
        self._strategies_collection = None
        self._metrics_collection = None
        
    def initialize(self) -> bool:
        """Initialize Firebase connection with error handling"""
        try:
            # Check if Firebase is already initialized
            if not firebase_admin._apps:
                if not config.firebase.credentials_path:
                    logging.error("Firebase credentials path not configured")
                    return False
                    
                # Verify credentials file exists
                import os
                if not os.path.exists(config.firebase.credentials_path):
                    logging.error(f"Firebase credentials file not found: {config.firebase.credentials_path}")
                    return False
                    
                cred = credentials.Certificate(config.firebase.credentials_path)
                firebase_admin.initialize_app(cred, {
                    'projectId': config.firebase.project_id,
                    'databaseURL': config.firebase.database_url
                })
                
            self._db = firestore.client()
            self._strategies_collection = self._db.collection(config.firebase.collection_name)
            self._metrics_collection = self._db.collection(f"{config.firebase.collection_name}_metrics")
            self._initialized = True
            logging.info("Firebase initialized successfully")
            return True
            
        except FileNotFoundError as e:
            logging.error(f"Firebase credentials file not found: {e}")
            return False
        except ValueError as e:
            logging.error(f"Firebase