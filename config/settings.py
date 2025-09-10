"""
Configuration management for Font Identifier application
Handles environment variables, config files, and settings validation
"""

import os
import json
import logging
from pathlib import Path
from typing import Dict, Any, Optional
from dataclasses import dataclass, asdict


@dataclass
class DatabaseConfig:
    """Database configuration"""
    path: str = "app_users.db"
    backup_enabled: bool = True
    backup_interval_hours: int = 24
    max_backups: int = 7


@dataclass
class ModelConfig:
    """Model configuration"""
    path: str = "model.pth"
    device: str = "auto"  # auto, cpu, cuda
    confidence_threshold: float = 0.5
    max_image_size: int = 2048  # pixels


@dataclass
class ServerConfig:
    """Server configuration"""
    host: str = "0.0.0.0"
    port: int = 8501
    debug: bool = False
    cors_enabled: bool = False
    max_upload_size: int = 50  # MB


@dataclass
class RecordingConfig:
    """Recording configuration"""
    directory: str = "recordings"
    max_file_size_mb: int = 500
    allowed_formats: list = None
    auto_cleanup_days: int = 30
    
    def __post_init__(self):
        if self.allowed_formats is None:
            self.allowed_formats = ["webm", "mp4", "avi", "mov", "png", "jpg", "jpeg"]


@dataclass
class SecurityConfig:
    """Security configuration"""
    secret_key: str = "change-me-in-production"
    session_timeout_hours: int = 24
    max_login_attempts: int = 5
    rate_limit_per_minute: int = 60
    password_min_length: int = 8


@dataclass
class PaymentConfig:
    """Payment integration configuration"""
    enabled: bool = False
    stripe_public_key: str = ""
    stripe_secret_key: str = ""
    paypal_client_id: str = ""
    paypal_client_secret: str = ""
    currency: str = "USD"


@dataclass
class PWAConfig:
    """Progressive Web App configuration"""
    enabled: bool = True
    app_name: str = "Font Identifier"
    short_name: str = "FontID"
    theme_color: str = "#6366f1"
    background_color: str = "#0a0f1e"
    offline_enabled: bool = True


@dataclass
class AppConfig:
    """Main application configuration"""
    # App info
    app_name: str = "Font Identifier"
    version: str = "1.0.0"
    environment: str = "development"  # development, staging, production
    
    # Component configs
    database: DatabaseConfig = None
    model: ModelConfig = None
    server: ServerConfig = None
    recording: RecordingConfig = None
    security: SecurityConfig = None
    payment: PaymentConfig = None
    pwa: PWAConfig = None
    
    # Logging
    log_level: str = "INFO"
    log_file: str = "app.log"
    log_max_bytes: int = 10485760  # 10MB
    log_backup_count: int = 5
    
    def __post_init__(self):
        if self.database is None:
            self.database = DatabaseConfig()
        if self.model is None:
            self.model = ModelConfig()
        if self.server is None:
            self.server = ServerConfig()
        if self.recording is None:
            self.recording = RecordingConfig()
        if self.security is None:
            self.security = SecurityConfig()
        if self.payment is None:
            self.payment = PaymentConfig()
        if self.pwa is None:
            self.pwa = PWAConfig()


class ConfigManager:
    """Configuration manager for the application"""
    
    def __init__(self, config_dir: str = "config"):
        self.config_dir = Path(config_dir)
        self.config_dir.mkdir(exist_ok=True)
        self.config_file = self.config_dir / "app_config.json"
        self.env_file = Path(".env")
        self._config: Optional[AppConfig] = None
        
    def load_config(self) -> AppConfig:
        """Load configuration from files and environment variables"""
        if self._config is not None:
            return self._config
            
        # Start with defaults
        config_dict = asdict(AppConfig())
        
        # Load from JSON file if exists
        if self.config_file.exists():
            try:
                with open(self.config_file, 'r') as f:
                    file_config = json.load(f)
                    self._deep_update(config_dict, file_config)
            except Exception as e:
                logging.warning(f"Failed to load config file: {e}")
        
        # Override with environment variables
        env_config = self._load_from_env()
        self._deep_update(config_dict, env_config)
        
        # Create AppConfig object
        self._config = self._dict_to_config(config_dict)
        
        # Validate configuration
        self._validate_config(self._config)
        
        return self._config
    
    def save_config(self, config: AppConfig):
        """Save configuration to JSON file"""
        config_dict = asdict(config)
        
        try:
            with open(self.config_file, 'w') as f:
                json.dump(config_dict, f, indent=2)
            logging.info(f"Configuration saved to {self.config_file}")
        except Exception as e:
            logging.error(f"Failed to save config: {e}")
    
    def _load_from_env(self) -> Dict[str, Any]:
        """Load configuration from environment variables"""
        env_mapping = {
            # Database
            "DB_PATH": ("database", "path"),
            "DB_BACKUP_ENABLED": ("database", "backup_enabled"),
            
            # Model
            "MODEL_PATH": ("model", "path"),
            "MODEL_DEVICE": ("model", "device"),
            "MODEL_CONFIDENCE_THRESHOLD": ("model", "confidence_threshold"),
            
            # Server
            "STREAMLIT_SERVER_ADDRESS": ("server", "host"),
            "STREAMLIT_SERVER_PORT": ("server", "port"),
            "DEBUG": ("server", "debug"),
            
            # Recording
            "RECORDINGS_DIR": ("recording", "directory"),
            "MAX_FILE_SIZE_MB": ("recording", "max_file_size_mb"),
            
            # Security
            "SECRET_KEY": ("security", "secret_key"),
            "SESSION_TIMEOUT_HOURS": ("security", "session_timeout_hours"),
            
            # Payment
            "PAYMENT_ENABLED": ("payment", "enabled"),
            "STRIPE_PUBLIC_KEY": ("payment", "stripe_public_key"),
            "STRIPE_SECRET_KEY": ("payment", "stripe_secret_key"),
            "PAYPAL_CLIENT_ID": ("payment", "paypal_client_id"),
            "PAYPAL_CLIENT_SECRET": ("payment", "paypal_client_secret"),
            
            # PWA
            "PWA_ENABLED": ("pwa", "enabled"),
            "PWA_APP_NAME": ("pwa", "app_name"),
            "PWA_THEME_COLOR": ("pwa", "theme_color"),
            
            # General
            "APP_NAME": ("app_name",),
            "VERSION": ("version",),
            "ENVIRONMENT": ("environment",),
            "LOG_LEVEL": ("log_level",),
        }
        
        config = {}
        
        for env_var, path in env_mapping.items():
            value = os.getenv(env_var)
            if value is not None:
                # Convert string values to appropriate types
                if value.lower() in ('true', 'false'):
                    value = value.lower() == 'true'
                elif value.isdigit():
                    value = int(value)
                elif self._is_float(value):
                    value = float(value)
                
                # Set nested value
                self._set_nested_value(config, path, value)
        
        return config
    
    def _deep_update(self, base_dict: dict, update_dict: dict):
        """Deep update dictionary"""
        for key, value in update_dict.items():
            if key in base_dict and isinstance(base_dict[key], dict) and isinstance(value, dict):
                self._deep_update(base_dict[key], value)
            else:
                base_dict[key] = value
    
    def _set_nested_value(self, config: dict, path: tuple, value: Any):
        """Set nested dictionary value"""
        current = config
        for key in path[:-1]:
            if key not in current:
                current[key] = {}
            current = current[key]
        current[path[-1]] = value
    
    def _is_float(self, value: str) -> bool:
        """Check if string can be converted to float"""
        try:
            float(value)
            return True
        except ValueError:
            return False
    
    def _dict_to_config(self, config_dict: dict) -> AppConfig:
        """Convert dictionary to AppConfig object"""
        # Create nested config objects
        database_config = DatabaseConfig(**config_dict.get('database', {}))
        model_config = ModelConfig(**config_dict.get('model', {}))
        server_config = ServerConfig(**config_dict.get('server', {}))
        recording_config = RecordingConfig(**config_dict.get('recording', {}))
        security_config = SecurityConfig(**config_dict.get('security', {}))
        payment_config = PaymentConfig(**config_dict.get('payment', {}))
        pwa_config = PWAConfig(**config_dict.get('pwa', {}))
        
        # Remove nested configs from main dict
        main_config = {k: v for k, v in config_dict.items() 
                      if k not in ['database', 'model', 'server', 'recording', 'security', 'payment', 'pwa']}
        
        return AppConfig(
            **main_config,
            database=database_config,
            model=model_config,
            server=server_config,
            recording=recording_config,
            security=security_config,
            payment=payment_config,
            pwa=pwa_config
        )
    
    def _validate_config(self, config: AppConfig):
        """Validate configuration values"""
        errors = []
        
        # Validate server port
        if not (1 <= config.server.port <= 65535):
            errors.append(f"Invalid server port: {config.server.port}")
        
        # Validate file paths
        if not config.database.path:
            errors.append("Database path cannot be empty")
        
        if not config.model.path:
            errors.append("Model path cannot be empty")
        
        # Validate security
        if config.security.secret_key == "change-me-in-production" and config.environment == "production":
            errors.append("Secret key must be changed in production")
        
        if config.security.password_min_length < 6:
            errors.append("Password minimum length must be at least 6 characters")
        
        # Validate recording
        if config.recording.max_file_size_mb <= 0:
            errors.append("Recording max file size must be positive")
        
        if errors:
            error_msg = "Configuration validation errors:\\n" + "\\n".join(f"- {error}" for error in errors)
            raise ValueError(error_msg)
    
    def get_config(self) -> AppConfig:
        """Get current configuration"""
        if self._config is None:
            return self.load_config()
        return self._config
    
    def reload_config(self) -> AppConfig:
        """Reload configuration from files"""
        self._config = None
        return self.load_config()
    
    def create_sample_config(self):
        """Create a sample configuration file"""
        sample_config = AppConfig()
        sample_file = self.config_dir / "app_config.sample.json"
        
        with open(sample_file, 'w') as f:
            json.dump(asdict(sample_config), f, indent=2)
        
        logging.info(f"Sample configuration created at {sample_file}")


# Global config manager instance
config_manager = ConfigManager()


def get_config() -> AppConfig:
    """Get application configuration"""
    return config_manager.get_config()


def reload_config() -> AppConfig:
    """Reload configuration from files"""
    return config_manager.reload_config()
