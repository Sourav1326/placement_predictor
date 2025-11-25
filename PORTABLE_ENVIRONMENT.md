# Portable Environment Setup

This project includes a self-contained portable environment with all dependencies pre-installed. This means you don't need to download packages every time or set up a new environment.

## What's Included

- Python 3.x runtime
- All required packages (Flask, TensorFlow, scikit-learn, pandas, etc.)
- Pre-trained models
- All data files
- Templates and static assets

## Quick Start

### Option 1: Run the Application Directly
- Double-click `run_direct.bat` to start the application immediately

### Option 2: Activate the Environment for Development
- Double-click `activate_portable.bat` to activate the environment
- Then run `python src/main.py` to start the application

## Directory Structure

```
placement predictor/
├── portable_env/           # Portable Python environment
├── requirements_cache/     # Cached package files
├── src/                    # Application source code
├── data/                   # Data files
├── templates/              # HTML templates
├── run_direct.bat          # Direct run script
├── activate_portable.bat   # Environment activation script
└── ...
```

## How It Works

1. All dependencies are stored locally in the `requirements_cache/` directory
2. The portable environment in `portable_env/` contains all installed packages
3. No internet connection is required to run the application
4. No need to reinstall packages every time

## Running the Application

1. **Direct Run (Recommended):**
   ```
   Double-click run_direct.bat
   ```

2. **Manual Run:**
   ```
   portable_env\Scripts\python.exe src/main.py
   ```

3. **Development Mode:**
   ```
   Double-click activate_portable.bat
   python src/main.py
   ```

## Accessing the Application

Once the application is running, open your browser and go to:
- http://localhost:5000

Default admin credentials:
- Email: admin@placement.system
- Password: admin123

## Troubleshooting

### If the application fails to start:

1. Check that all required packages are installed:
   ```
   portable_env\Scripts\python.exe test_environment.py
   ```

2. If packages are missing, reinstall from cache:
   ```
   portable_env\Scripts\python.exe -m pip install --find-links requirements_cache --no-index <package_name>
   ```

### If you see import errors:

1. Make sure you're using the portable environment's Python:
   ```
   portable_env\Scripts\python.exe
   ```

2. Verify the package is installed:
   ```
   portable_env\Scripts\python.exe -m pip list
   ```

## Benefits

- ✅ No internet required after initial setup
- ✅ No repeated downloads
- ✅ Consistent environment across machines
- ✅ Quick setup on new systems
- ✅ No dependency conflicts
- ✅ Ready-to-run application

## Updating the Environment

To update packages in the portable environment:

1. Download new packages to the cache:
   ```
   python setup_local_env.py
   ```

2. Install updated packages:
   ```
   portable_env\Scripts\python.exe -m pip install --find-links requirements_cache --no-index <package_name>
   ```

## Creating a New Portable Environment

To create a fresh portable environment:

1. Delete the existing portable_env directory:
   ```
   rmdir /s portable_env
   ```

2. Run the setup script:
   ```
   python setup_portable_env.py
   ```

This will recreate the portable environment with all dependencies from the local cache.