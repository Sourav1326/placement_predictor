Placement Predictor

This project is a complete career guidance platform designed to help students improve their job placement prospects through data-driven insights, skill verification, and AI-powered recommendations.

## Portable Environment (Recommended)

This project includes a self-contained portable environment with all dependencies pre-installed. This means you don't need to download packages every time or set up a new environment.

### Quick Start:

1. **To run the application directly:**
   - Double-click `run_direct.bat` or `run_app_portable.bat`

2. **To activate the environment for development:**
   - Double-click `activate_portable.bat`
   - Then run `python src/main.py` to start the application

For detailed instructions, see [PORTABLE_ENVIRONMENT.md](PORTABLE_ENVIRONMENT.md)

## Manual Setup (Alternative)

If you prefer to set up your own environment:

**1. Prerequisites:**
   - Python 3.x must be installed.

**2. Create a Virtual Environment:**
   Open a terminal in this project folder and run:
   ```bash
   python -m venv venv
   ```

**3. Activate the Environment:**

On Windows:
   ```bash
   venv\Scripts\activate
   ```

On macOS/Linux:
   ```bash
   source venv/bin/activate
   ```

**4. Install Dependencies:**
With the environment active, install all required libraries:
   ```bash
   pip install -r requirements.txt
   ```

**5. Run the Project:**
Execute the main script:
   ```bash
   python src/main.py
   ```
