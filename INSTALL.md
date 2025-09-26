# pYSFReflector3 Installation Guide

## Prerequisites
- Python 3.8 or higher (tested with Python 3.13)
- pip (Python package installer)

## Installation Steps

1. **Clone or download the pYSFReflector3 project**

2. **Install Python dependencies**
   ```bash
   pip install -r requirements.txt
   ```

3. **Verify installation**
   ```bash
   python3 YSFReflector -v
   ```

## Dependencies Installed

The requirements.txt will install:
- `aprslib` - APRS protocol support for position reporting
- `tinydb` - Lightweight JSON database for storing reflector data  
- `psutil` - System and process utilities for memory monitoring

## Optional Dependencies

- **psutil**: While optional, it's strongly recommended for production deployments as it provides:
  - Real-time memory usage monitoring
  - Intelligent cleanup triggers based on actual memory consumption
  - Better system resource visibility

## Running the Reflector

```bash
python3 YSFReflector <config_file>
```

## Production Deployment Notes

- The reflector now includes Phase 1 and Phase 2 stability improvements
- Supports graceful shutdown with SIGTERM/SIGINT signals
- Includes automatic memory monitoring and cleanup
- Network operations include retry logic and timeout handling
- Resource management with automatic cleanup

## System Requirements

- Stable internet connection for YSF protocol operation
- UDP port access for YSF communication
- Sufficient memory (recommendations based on expected load)
- For production: consider running as a systemd service