"""
AEMP Configuration Manager
Centralized configuration with environment variable handling and validation
"""
import os
from dataclasses import dataclass, field
from typing import Optional, Dict, List
from dotenv import load_dotenv
import logging

load_dotenv()

@dataclass
class FirebaseConfig:
    """Firebase configuration"""
    project_id: str = field(default_factory=lambda: os.getenv('FIREBASE_PROJECT_ID', 'aemp-evolution'))
    credentials_path: str = field(default_factory=lambda: os.getenv('FIREBASE_CREDENTIALS_PATH', './firebase-creds.json'))
    database_url: str = field(default_factory=lambda: os.getenv('FIREBASE_DATABASE_URL', ''))
    collection_name: str = field(default_factory=lambda: os.getenv('FIREBASE_COLLECTION', 'aemp_strategies'))

@dataclass
class TradingConfig:
    """Trading system configuration"""
    initial_capital: float = field(default_factory=lambda: float(os.getenv('INITIAL_CAPITAL', 10000.0)))
    transaction_cost: float = field(default_factory=lambda: float(os.getenv('TRANSACTION_COST', 0.001)))
    max_position_size: float = field(default_factory=lambda: float(os.getenv('MAX_POSITION_SIZE', 0.1)))
    risk_free_rate: float = field(default_factory=lambda: float(os.getenv('RISK_FREE_RATE', 0.02)))
    
@dataclass
class EvolutionConfig:
    """Neuroevolution configuration"""
    population_size: int = field(default_factory=lambda: int(os.getenv('POPULATION_SIZE', 50)))
    mutation_rate: float = field(default_factory=lambda: float(os.getenv('MUTATION_RATE', 0.15)))
    mutation_strength: float = field(default_factory=lambda: float(os.getenv('MUTATION_STRENGTH', 0.3)))
    crossover_rate: float = field(default_factory=lambda: float(os.getenv('CROSSOVER_RATE', 0.4)))
    elitism_count: int = field(default_factory=lambda: int(os.getenv('ELITISM_COUNT', 2)))
    
@dataclass
class RLConfig:
    """Reinforcement Learning configuration"""
    learning_rate: float = field(default_factory=lambda: float(os.getenv('LEARNING_RATE', 0.001)))
    gamma: float = field(default_factory=lambda: float(os.getenv('GAMMA', 0.99)))
    epsilon_start: float = field(default_factory=lambda: float(os.getenv('EPSILON_START', 1.0)))
    epsilon_end: float = field(default_factory=lambda: float(os.getenv('EPSILON_END', 0.01)))
    epsilon_decay: float = field(default_factory=lambda: float(os.getenv('EPSILON_DECAY', 0.995)))
    
@dataclass
class AEMPConfig:
    """Master configuration container"""
    firebase: FirebaseConfig = field(default_factory=FirebaseConfig)
    trading: TradingConfig = field(default_factory=TradingConfig)
    evolution: EvolutionConfig = field(default_factory=EvolutionConfig)
    rl: RLConfig = field(default_factory=RLConfig)
    log_level: str = field(default_factory=lambda: os.getenv('LOG_LEVEL', 'INFO'))
    data_source: str = field(default_factory=lambda: os.getenv('DATA_SOURCE', 'local_csv'))
    
    def validate(self) -> bool:
        """Validate all configuration parameters"""
        try:
            assert self.trading.initial_capital > 0, "Initial capital must be positive"
            assert 0 <= self.trading.transaction_cost <= 1, "Transaction cost must be between 0 and 1"
            assert 0 <= self.trading.max_position_size <= 1, "Max position size must be between 0 and 1"
            assert self.evolution.population_size > 0, "Population size must be positive"
            assert 0 <= self.evolution.mutation_rate <= 1, "Mutation rate must be between 0 and 1"
            assert 0 <= self.evolution.crossover_rate <= 1, "Crossover rate must be between 0 and 1"
            return True
        except AssertionError as e:
            logging.error(f"Configuration validation failed: {e}")
            return False

# Global configuration instance
config = AEMPConfig()