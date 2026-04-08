# CreditPathAI Project Context (Linux Environment)

CreditPathAI is an end-to-end credit risk assessment and loan default prediction system. It transforms raw loan application data into a high-performance predictive model and provides tools for real-time scoring and automated reporting.

## Project Overview

*   **Purpose:** To automate the identification of potential loan defaults using machine learning.
*   **Technologies:** 
    *   **Language:** Python 3.10+
    *   **Data Processing:** `pandas`, `numpy`, `SQLAlchemy`
    *   **Machine Learning:** `scikit-learn` (Random Forest), `XGBoost`, `LightGBM`
    *   **Visualization:** `matplotlib`, `seaborn`
    *   **Reporting:** `python-docx`, `fpdf` (or similar for PDF)
    *   **Persistence:** `joblib` (models), `SQLite` (local storage), `PostgreSQL` (source)

## Directory Structure

*   `data/`: Raw dataset (`Loan_default.csv`) and processed output (`clean_loans.csv`).
*   `docs/`: Project reports, EDA summaries, and informational handouts (PDF, DOCX, ODT).
*   `models/`: Trained model artifacts (`best_xgboost_model.pkl`, `best_lightgbm_model.pkl`, `scaler.joblib`).
*   `plots/`: Visualizations including performance comparisons and feature importance.
*   `scripts/`: Core logic for data pipeline, model training, and reporting.

## Key Workflows & Commands

The project follows a linear progression from data ingestion to scoring:

### 1. Data Cleaning & Ingestion
Executes the pipeline including missing value handling, outlier management (Winsorization), and feature scaling.
```bash
python scripts/pipeline.py
```

### 2. Advanced Model Training
Trains XGBoost and LightGBM models, performs hyperparameter tuning, and saves the best performing models.
```bash
python scripts/advanced_models.py
```

### 3. Performance Comparison
Generates comparison plots (AUC, Model Size) across different algorithms (Random Forest vs XGBoost vs LightGBM).
```bash
python scripts/plot_comparison.py
```

### 4. Real-Time Scoring
Interactive CLI for manual entry of loan application details to generate instant risk scores.
```bash
python scripts/model_prediction.py
```

### 5. Automated Reporting
Generates a comprehensive summary report of the data analysis and model performance.
```bash
python scripts/generate_report.py
# or for PDF
python scripts/generate_pdf_report.py
```

## Development Conventions

*   **Environment:** Linux (Arch Linux/Wayland) with NVIDIA CUDA support (`/opt/cuda`).
*   **Data Integrity:** The pipeline uses a read-only approach to ensure raw data remains immutable.
*   **Scaling:** Key numerical features (`income`, `loanamount`, `creditscore`) are standardized (Mean=0, Std=1) using `scaler.joblib`.
*   **Risk Thresholds:** The scoring engine uses a default 0.35 threshold for loan approval recommendations.

## Available MCP Tools

*   **email-mcp**: Manages email accounts (IMAP, iCloud, Gmail, Outlook).
*   **maverick-mcp**: AI-powered research and analysis tools.
*   **whatsapp-mcp**: Interaction with WhatsApp.
*   **jcodemunch-mcp**: Optimized for indexing and searching source code.
*   **jdocmunch-mcp**: Specialized in indexing and searching documentation files.
