import os
import tkinter as tk
from tkinter import filedialog, messagebox
from tkinter import ttk
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import matplotlib
matplotlib.use('TkAgg')  # Ensure Tk compatibility for plotting

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
            self.df = pd.read_csv(path)
            self.lbl_status.config(text=f"Loaded: {os.path.basename(path)}", foreground=SUCCESS_COLOR)

            # Enable analyze button
            self.btn_analyze.config(state=tk.NORMAL)

            # Update summary stats text box
            self.txt_summary.config(state=tk.NORMAL)
            self.txt_summary.delete(1.0, tk.END)

            num_rows = len(self.df)
            num_cols = len(self.df.columns)
            columns = ", ".join(self.df.columns.tolist()[:6]) + "..."
            
            summary_text = (
                f"File: {path}\n"
                f"Records Count: {num_rows}\n"
                f"Features Count: {num_cols}\n"
                f"Available Fields: {columns}\n\n"
                f"Numeric Columns Summary:\n"
                f"{self.df.describe(include=[np.number]).iloc[:, :3].to_string()}\n"
            )
            self.txt_summary.insert(tk.END, summary_text)
            self.txt_summary.config(state=tk.DISABLED)

        except Exception as e:
            messagebox.showerror("Ingestion Error", f"Failed to parse CSV file: {e}")

    def generate_mock_dataset(self):
        # Create a mock Kaggle YouTube Statistics dataset
        np.random.seed(42)
        categories = ["Music", "Entertainment", "Education", "Gaming", "People & Blogs", "Comedy", "Howto & Style"]
        countries = ["US", "IN", "BR", "CA", "GB", "KR", "MX", "JP"]
        
        data = {
            "rank": list(range(1, 51)),
            "Youtuber": [f"Creator_{i}" for i in range(1, 51)],
            "subscribers": np.random.randint(10000000, 150000000, size=50),
            "video views": np.random.randint(1000000000, 50000000000, size=50),
            "category": np.random.choice(categories, size=50),
            "uploads": np.random.randint(100, 15000, size=50),
            "Country": np.random.choice(countries, size=50),
            "lowest_yearly_earnings": np.random.randint(50000, 500000, size=50),
            "highest_yearly_earnings": np.random.randint(800000, 8000000, size=50),
        }
        mock_df = pd.DataFrame(data)
        # Give some realistic names to first few creators
        mock_df.loc[0, "Youtuber"] = "MrBeast"
        mock_df.loc[1, "Youtuber"] = "PewDiePie"
        mock_df.loc[2, "Youtuber"] = "T-Series"
        mock_df.loc[3, "Youtuber"] = "Cocomelon"
        mock_df.loc[4, "Youtuber"] = "SET India"
        
        target_path = "Global_YouTube_Statistics.csv"
        mock_df.to_csv(target_path, index=False)
        messagebox.showinfo("Success", f"Generated mock dataset: {target_path}")
        self.load_data(target_path)

    def run_analysis(self):
        if self.df is None:
            return

        try:
            # Standardize column names (lowercase and strip spaces)
            df_cleaned = self.df.copy()
            df_cleaned.columns = [c.strip().lower() for c in df_cleaned.columns]

            # Map common Kaggle columns
            sub_col = 'subscribers' if 'subscribers' in df_cleaned.columns else df_cleaned.columns[2]
            views_col = 'video views' if 'video views' in df_cleaned.columns else 'views' if 'views' in df_cleaned.columns else df_cleaned.columns[3]
            cat_col = 'category' if 'category' in df_cleaned.columns else 'type' if 'type' in df_cleaned.columns else df_cleaned.columns[4]
            country_col = 'country' if 'country' in df_cleaned.columns else df_cleaned.columns[6] if len(df_cleaned.columns) > 6 else None
            earn_col = 'highest_yearly_earnings' if 'highest_yearly_earnings' in df_cleaned.columns else df_cleaned.columns[-1]

            # Generate Report file
            report_path = "youtube_report.txt"
            with open(report_path, "w") as f:
                f.write("=== AUTOMATED YOUTUBE STATISTICS REPORT ===\n")
                f.write(f"Analyzed File: {self.file_path}\n\n")
                f.write(f"1. Top 5 Creators by Subscribers:\n")
                top_subs = df_cleaned.sort_values(by=sub_col, ascending=False).head(5)
                for idx, row in top_subs.iterrows():
                    f.write(f"   - {row['youtuber'] if 'youtuber' in row else row.iloc[1]}: {row[sub_col]:,} subs\n")
                
                f.write(f"\n2. Category Distribution:\n")
                cat_counts = df_cleaned[cat_col].value_counts()
                for cat, count in cat_counts.items():
                    f.write(f"   - {cat}: {count} channels\n")

                if country_col:
                    f.write(f"\n3. Top 3 Countries represented:\n")
                    country_counts = df_cleaned[country_col].value_counts().head(3)
                    for c, count in country_counts.items():
                        f.write(f"   - {c}: {count} channels\n")

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
