import matplotlib.pyplot as plt
import seaborn as sns
import os

def generate_comparison_plots():
    # Data for comparison
    models = ['Random Forest\n(Baseline)', 'LightGBM\n(Advanced)', 'XGBoost\n(Tuned)']
    auc_scores = [0.7341, 0.7580, 0.7603]
    
    # 1. AUC-ROC Comparison Bar Chart
    plt.figure(figsize=(10, 6))
    sns.set_style("whitegrid")
    ax = sns.barplot(x=models, y=auc_scores, palette='viridis')
    
    # Add labels on top of bars
    for p in ax.patches:
        ax.annotate(f'{p.get_height():.4f}', (p.get_x() + p.get_width() / 2., p.get_height()),
                    ha='center', va='center', fontsize=12, color='black', xytext=(0, 8),
                    textcoords='offset points')

    plt.title('Model Performance Comparison (AUC-ROC Score)', fontsize=15, pad=20)
    plt.ylabel('AUC-ROC Score', fontsize=12)
    plt.ylim(0.70, 0.78) # Zoom in to show the difference
    
    os.makedirs('plots', exist_ok=True)
    plt.savefig('plots/model_auc_comparison.png')
    print("Generated: plots/model_auc_comparison.png")

    # 2. Model Size Comparison (Log Scale to show the massive difference)
    sizes = [370.42, 0.70, 0.23] # in MB
    plt.figure(figsize=(10, 6))
    ax_size = sns.barplot(x=models, y=sizes, palette='magma')
    
    for p in ax_size.patches:
        ax_size.annotate(f'{p.get_height()} MB', (p.get_x() + p.get_width() / 2., p.get_height()),
                    ha='center', va='center', fontsize=12, color='black', xytext=(0, 8),
                    textcoords='offset points')

    plt.title('Model Efficiency: File Size Comparison', fontsize=15, pad=20)
    plt.ylabel('File Size (MB)', fontsize=12)
    plt.yscale('log') # Log scale because 370 vs 0.2 is too vast for linear
    plt.savefig('plots/model_size_comparison.png')
    print("Generated: plots/model_size_comparison.png")

if __name__ == "__main__":
    generate_comparison_plots()
