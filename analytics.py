"""Data handling for the YouTube analytics tool, kept free of Tkinter so it
can be tested without a display."""

import numpy as np
import pandas as pd

# Kaggle's "Global YouTube Statistics" CSV is Latin-1, not UTF-8.
ENCODINGS = ("utf-8", "latin-1")


def read_dataset(path):
    """Read a CSV, falling back to Latin-1 when it is not valid UTF-8."""
    for encoding in ENCODINGS[:-1]:
        try:
            return pd.read_csv(path, encoding=encoding)
        except UnicodeDecodeError:
            continue
    return pd.read_csv(path, encoding=ENCODINGS[-1])


def summarize(df, path):
    columns = ", ".join(df.columns.tolist()[:6]) + "..."
    return (
        f"File: {path}\n"
        f"Records Count: {len(df)}\n"
        f"Features Count: {len(df.columns)}\n"
        f"Available Fields: {columns}\n\n"
        f"Numeric Columns Summary:\n"
        f"{df.describe(include=[np.number]).iloc[:, :3].to_string()}\n"
    )


def standardize(df):
    """Lowercase and strip column names, and map the common Kaggle columns."""
    cleaned = df.copy()
    cleaned.columns = [c.strip().lower() for c in cleaned.columns]
    cols = cleaned.columns

    def pick(*names, fallback=None):
        for name in names:
            if name in cols:
                return name
        return fallback

    mapping = {
        "subscribers": pick("subscribers", fallback=cols[2]),
        "views": pick("video views", "views", fallback=cols[3]),
        "category": pick("category", "type", fallback=cols[4]),
        "country": pick("country", fallback=cols[6] if len(cols) > 6 else None),
        "earnings": pick("highest_yearly_earnings", fallback=cols[-1]),
        "name": pick("youtuber", fallback=cols[1]),
    }
    return cleaned, mapping


def build_report(df, file_path):
    """Return the text report and the category and country counts it used."""
    cleaned, m = standardize(df)
    lines = [
        "=== AUTOMATED YOUTUBE STATISTICS REPORT ===",
        f"Analyzed File: {file_path}",
        "",
        "1. Top 5 Creators by Subscribers:",
    ]
    top = cleaned.sort_values(by=m["subscribers"], ascending=False).head(5)
    for _, row in top.iterrows():
        lines.append(f"   - {row[m['name']]}: {row[m['subscribers']]:,.0f} subs")

    lines += ["", "2. Category Distribution:"]
    cat_counts = cleaned[m["category"]].value_counts()
    for cat, count in cat_counts.items():
        lines.append(f"   - {cat}: {count} channels")

    country_counts = None
    if m["country"]:
        lines += ["", "3. Top 3 Countries represented:"]
        country_counts = cleaned[m["country"]].value_counts()
        for c, count in country_counts.head(3).items():
            lines.append(f"   - {c}: {count} channels")

    return "\n".join(lines) + "\n", cleaned, m, cat_counts, country_counts


def make_mock_dataset(seed=42, rows=50):
    """A small dataset shaped like Kaggle's Global YouTube Statistics."""
    rng = np.random.default_rng(seed)
    categories = [
        "Music",
        "Entertainment",
        "Education",
        "Gaming",
        "People & Blogs",
        "Comedy",
        "Howto & Style",
    ]
    countries = ["US", "IN", "BR", "CA", "GB", "KR", "MX", "JP"]
    df = pd.DataFrame(
        {
            "rank": range(1, rows + 1),
            "Youtuber": [f"Creator_{i}" for i in range(1, rows + 1)],
            "subscribers": rng.integers(10_000_000, 150_000_000, size=rows),
            "video views": rng.integers(1_000_000_000, 50_000_000_000, size=rows),
            "category": rng.choice(categories, size=rows),
            "uploads": rng.integers(100, 15_000, size=rows),
            "Country": rng.choice(countries, size=rows),
            "lowest_yearly_earnings": rng.integers(50_000, 500_000, size=rows),
            "highest_yearly_earnings": rng.integers(800_000, 8_000_000, size=rows),
        }
    )
    for i, name in enumerate(
        ["MrBeast", "PewDiePie", "T-Series", "Cocomelon", "SET India"]
    ):
        if i < rows:
            df.loc[i, "Youtuber"] = name
    return df
