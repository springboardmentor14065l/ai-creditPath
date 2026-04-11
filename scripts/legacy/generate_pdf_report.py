from fpdf import FPDF
import os

class PDFReport(FPDF):
    def header(self):
        self.set_font('Arial', 'B', 16)
        self.cell(0, 10, 'CreditPathAI: Project & Model Report', 0, 1, 'C')
        self.ln(5)

    def footer(self):
        self.set_y(-15)
        self.set_font('Arial', 'I', 8)
        self.cell(0, 10, f'Page {self.page_no()}', 0, 0, 'C')

def create_pdf_report():
    pdf = PDFReport()
    pdf.add_page()
    pdf.set_auto_page_break(auto=True, margin=15)

    # Project Overview
    pdf.set_font('Arial', 'B', 14)
    pdf.cell(0, 10, '1. Project Overview', 0, 1, 'L')
    pdf.set_font('Arial', '', 12)
    pdf.multi_cell(0, 10, (
        "CreditPathAI is an end-to-end credit risk assessment system designed to predict loan defaults. "
        "The project transforms raw application data into a predictive model using advanced feature engineering "
        "and a Random Forest Classifier."
    ))
    pdf.ln(5)

    # Data Cleaning & Engineering
    pdf.set_font('Arial', 'B', 14)
    pdf.cell(0, 10, '2. Data Cleaning & Feature Engineering', 0, 1, 'L')
    pdf.set_font('Arial', '', 12)
    pdf.multi_cell(0, 10, (
        "The pipeline consists of an 11-step process:\n"
        "- PostgreSQL extraction with CSV fallback.\n"
        "- Advanced Feature Engineering: Loan-to-Income, Credit Utilization, Employment Stability, and High DTI Flags.\n"
        "- Outlier management via Winsorization.\n"
        "- Standard scaling for all numerical features.\n"
        "- Categorical encoding for model compatibility."
    ))
    pdf.ln(5)

    # Model Performance
    pdf.set_font('Arial', 'B', 14)
    pdf.cell(0, 10, '3. Model Performance & Insights', 0, 1, 'L')
    pdf.set_font('Arial', '', 12)
    pdf.multi_cell(0, 10, (
        "The Random Forest model was trained on the engineered dataset. Key insights include "
        "the importance of credit scores and the newly created interaction features in driving "
        "default predictions."
    ))
    pdf.ln(10)

    # Visualizations
    plots_dir = os.path.join(os.path.dirname(__file__), '..', 'plots')
    
    # Feature Importance
    feat_imp_path = os.path.join(plots_dir, 'feature_importance.png')
    if os.path.exists(feat_imp_path):
        pdf.set_font('Arial', 'B', 12)
        pdf.cell(0, 10, 'Feature Importance Ranking:', 0, 1, 'L')
        pdf.image(feat_imp_path, x=15, w=180)
        pdf.ln(5)
    
    pdf.add_page()
    
    # Confusion Matrix
    cm_path = os.path.join(plots_dir, 'confusion_matrix.png')
    if os.path.exists(cm_path):
        pdf.set_font('Arial', 'B', 12)
        pdf.cell(0, 10, 'Confusion Matrix (Predicted vs Actual):', 0, 1, 'L')
        pdf.image(cm_path, x=30, w=150)
        pdf.ln(5)

    # Save the report
    save_path = os.path.join(os.path.dirname(__file__), '..', 'docs', 'CreditPathAI_EDA_Report.pdf')
    pdf.output(save_path)
    print(f"PDF Report successfully generated: {save_path}")

if __name__ == "__main__":
    create_pdf_report()
