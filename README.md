# YouTube Data Analytics Tool

A desktop GUI utility built with **Python** and **Tkinter** for rapid exploratory data analysis, ingestion, and automated visualization of Kaggle YouTube creator datasets.

## Features

1. **Dataset Ingestion**: Easily load a Kaggle YouTube statistics CSV file via a native file browsing dialog.
2. **Mock Data Generation**: Provides a one-click button to generate a clean, realistic `Global_YouTube_Statistics.csv` file locally to test out the application instantly.
3. **Summary Metadata Output**: Auto-parses CSV headers, record counts, feature counts, and outputs descriptive numeric statistics using pandas under the hood.
4. **One-Click Reports**: Renders a Matplotlib graphical dashboard displaying:
   - Bar Chart: Top channel categories represented in the dataset.
   - Scatter Plot: Correlation between subscriber counts and overall video views.
   - Horizontal Bar Chart: Average yearly earnings (in Millions) grouped by category.
   - Pie Chart: Market share distribution by country of origin.
5. **Text Reports**: Automatically outputs a summarized text report `youtube_report.txt` in the root folder containing key creator statistics and list breakdowns.

---

## Folder Structure

```text
├── app.py              # Main Tkinter application
├── requirements.txt    # Python dependencies
├── .gitignore          # Git exclusion rules
└── README.md           # Documentation
```

---

## Installation & Setup

### 1. Requirements
Ensure you have Python 3.9+ installed.

```bash
pip install -r requirements.txt
```

*(Note: Tkinter is bundled with standard Python distributions on Windows/macOS. On Ubuntu/Debian, you may need to install it via `sudo apt-get install python3-tk`).*

### 2. Run the Tool
Run the python script directly:

```bash
python app.py
```

### 3. Generate Analysis
1. Click **Generate Mock CSV** to create a mock dataset file in the same directory.
2. The application will automatically ingest and display its stats.
3. Click **Automate Analytics & Charts** to open the interactive Plotly-inspired dark themed Matplotlib dashboard and output `youtube_report.txt`.
