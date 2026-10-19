import os
import tkinter as tk
from tkinter import filedialog, messagebox
from tkinter import ttk
import matplotlib
matplotlib.use('TkAgg')  # Must be set before pyplot is imported
import matplotlib.pyplot as plt

from analytics import build_report, make_mock_dataset, read_dataset, summarize

# Color palette for modern dark theme
BG_COLOR = "#1e222b"
CARD_BG = "#282c34"
TEXT_COLOR = "#abb2bf"
ACCENT_COLOR = "#61afef"
SUCCESS_COLOR = "#98c379"
WHITE = "#ffffff"

class YouTubeAnalyticsApp:
    def __init__(self, root):
        self.root = root
        self.root.title("YouTube Data Analytics Tool")
        self.root.geometry("650x550")
        self.root.configure(bg=BG_COLOR)
        
        self.df = None
        self.file_path = ""

        # Configure style
        self.style = ttk.Style()
        self.style.theme_use('clam')
        self.style.configure('.', background=BG_COLOR, foreground=TEXT_COLOR, font=('Helvetica', 10))
        self.style.configure('TLabel', background=BG_COLOR, foreground=TEXT_COLOR)
        self.style.configure('TFrame', background=BG_COLOR)
        self.style.configure('Header.TLabel', font=('Helvetica', 16, 'bold'), foreground=WHITE)
        self.style.configure('Card.TFrame', background=CARD_BG, relief='flat', borderwidth=1)
        self.style.configure('Card.TLabel', background=CARD_BG, foreground=TEXT_COLOR)
        self.style.configure('Accent.TButton', background=ACCENT_COLOR, foreground=WHITE, borderwidth=0, font=('Helvetica', 10, 'bold'))
        self.style.map('Accent.TButton', background=[('active', '#528bff')])

        self.create_widgets()

    def create_widgets(self):
        # Main container
        main_frame = ttk.Frame(self.root, padding=20)
        main_frame.pack(fill=tk.BOTH, expand=True)

        # Header Title
        title_label = ttk.Label(main_frame, text="📹 YouTube Data Analytics Tool", style="Header.TLabel")
        title_label.pack(anchor=tk.W, pady=(0, 15))

        # Card 1: Ingestion Panel
        ingest_card = ttk.Frame(main_frame, style="Card.TFrame", padding=15)
        ingest_card.pack(fill=tk.X, pady=(0, 15))

        ingest_title = ttk.Label(ingest_card, text="File Ingestion (Kaggle Dataset)", font=('Helvetica', 11, 'bold'), style="Card.TLabel")
        ingest_title.pack(anchor=tk.W, pady=(0, 10))

        btn_row = ttk.Frame(ingest_card, style="Card.TFrame")
        btn_row.pack(fill=tk.X)

        self.btn_browse = ttk.Button(btn_row, text="Browse CSV File", command=self.browse_file, style="Accent.TButton")
        self.btn_browse.pack(side=tk.LEFT, padx=(0, 10))

        self.btn_mock = ttk.Button(btn_row, text="Generate Mock CSV", command=self.generate_mock_dataset)
        self.btn_mock.pack(side=tk.LEFT)

        self.lbl_status = ttk.Label(ingest_card, text="No dataset loaded. Browse for a CSV file.", font=('Helvetica', 9, 'italic'), style="Card.TLabel")
        self.lbl_status.pack(anchor=tk.W, pady=(10, 0))

        # Card 2: Summary Stats Panel
        self.stats_card = ttk.Frame(main_frame, style="Card.TFrame", padding=15)
        self.stats_card.pack(fill=tk.BOTH, expand=True, pady=(0, 15))

        stats_title = ttk.Label(self.stats_card, text="Dataset Summary Statistics", font=('Helvetica', 11, 'bold'), style="Card.TLabel")
        stats_title.pack(anchor=tk.W, pady=(0, 10))

        self.txt_summary = tk.Text(self.stats_card, height=10, bg="#21252b", fg=TEXT_COLOR, font=('Courier', 9), wrap=tk.WORD, relief='flat', borderwidth=0)
        self.txt_summary.pack(fill=tk.BOTH, expand=True)
        self.txt_summary.insert(tk.END, "Ingest a dataset to inspect metadata and summaries...")
        self.txt_summary.config(state=tk.DISABLED)

        # Card 3: Action Panel
        action_card = ttk.Frame(main_frame, padding=5)
        action_card.pack(fill=tk.X)

        self.btn_analyze = ttk.Button(action_card, text="⚡ Automate Analytics & Charts", command=self.run_analysis, style="Accent.TButton")
        self.btn_analyze.pack(fill=tk.X, ipady=5)
        self.btn_analyze.config(state=tk.DISABLED)

    def browse_file(self):
        filez = filedialog.askopenfilename(filetypes=[("CSV Files", "*.csv")])
        if filez:
            self.load_data(filez)

    def load_data(self, path):
        try:
            self.file_path = path
            self.df = read_dataset(path)
            self.lbl_status.config(text=f"Loaded: {os.path.basename(path)}", foreground=SUCCESS_COLOR)

            # Enable analyze button
            self.btn_analyze.config(state=tk.NORMAL)

            # Update summary stats text box
            self.txt_summary.config(state=tk.NORMAL)
            self.txt_summary.delete(1.0, tk.END)
            self.txt_summary.insert(tk.END, summarize(self.df, path))
            self.txt_summary.config(state=tk.DISABLED)

        except Exception as e:
            messagebox.showerror("Ingestion Error", f"Failed to parse CSV file: {e}")

    def generate_mock_dataset(self):
        mock_df = make_mock_dataset()
        target_path = "Global_YouTube_Statistics.csv"
        mock_df.to_csv(target_path, index=False)
        messagebox.showinfo("Success", f"Generated mock dataset: {target_path}")
        self.load_data(target_path)

    def run_analysis(self):
        if self.df is None:
            return

        try:
            report, df_cleaned, cols, cat_counts, country_counts = build_report(self.df, self.file_path)
            sub_col, views_col, cat_col = cols["subscribers"], cols["views"], cols["category"]
            country_col, earn_col = cols["country"], cols["earnings"]

            # Generate Report file
            report_path = "youtube_report.txt"
            with open(report_path, "w", encoding="utf-8") as f:
                f.write(report)

            # Create Matplotlib Plot
            plt.style.use('dark_background')
            fig, axes = plt.subplots(2, 2, figsize=(11, 8))
            fig.suptitle(f"YouTube Channel Analytics: {os.path.basename(self.file_path)}", fontsize=16, weight='bold', color='#61afef')

            # Plot 1: Category Count Bar Chart
            cat_counts.head(8).plot(kind='bar', ax=axes[0, 0], color='#61afef')
            axes[0, 0].set_title("Top Categories by Channel Count", fontsize=11, weight='bold')
            axes[0, 0].set_ylabel("Count")
            axes[0, 0].tick_params(axis='x', rotation=30)

            # Plot 2: Scatter plot (Subs vs Views)
            axes[0, 1].scatter(df_cleaned[sub_col] / 1e6, df_cleaned[views_col] / 1e9, color='#98c379', alpha=0.7, edgecolors='black')
            axes[0, 1].set_title("Subscribers vs Video Views", fontsize=11, weight='bold')
            axes[0, 1].set_xlabel("Subscribers (Millions)")
            axes[0, 1].set_ylabel("Video Views (Billions)")

            # Plot 3: Average Earnings by Category
            avg_earn = df_cleaned.groupby(cat_col)[earn_col].mean().sort_values(ascending=False).head(8)
            (avg_earn / 1e6).plot(kind='barh', ax=axes[1, 0], color='#e5c07b')
            axes[1, 0].set_title("Avg Yearly Earnings ($ Millions)", fontsize=11, weight='bold')
            axes[1, 0].set_xlabel("Earnings ($M)")
            axes[1, 0].invert_yaxis()

            # Plot 4: Top Countries represented
            if country_col:
                country_counts.head(5).plot(kind='pie', ax=axes[1, 1], autopct='%1.1f%%', colors=['#e06c75', '#98c379', '#61afef', '#c678dd', '#d19a66'])
                axes[1, 1].set_title("Top Represented Countries", fontsize=11, weight='bold')
                axes[1, 1].set_ylabel("")

            plt.tight_layout()
            
            messagebox.showinfo("Report Generated", f"1. Created report summary: {report_path}\n2. Renders analytics dashboard charts in new window.")
            plt.show()

        except Exception as e:
            messagebox.showerror("Analysis Error", f"An error occurred during metrics calculation: {e}")

if __name__ == "__main__":
    root = tk.Tk()
    app = YouTubeAnalyticsApp(root)
    root.mainloop()
