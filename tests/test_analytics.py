import pandas as pd

from analytics import (
    build_report,
    make_mock_dataset,
    read_dataset,
    standardize,
    summarize,
)


def test_reads_latin1_csv_like_the_kaggle_dataset(tmp_path):
    # Kaggle's Global YouTube Statistics file is Latin-1 and has names like this.
    path = tmp_path / "Global_YouTube_Statistics.csv"
    path.write_bytes(
        "rank,Youtuber,subscribers\n1,Ýôü Tübé,1000\n2,Plain,500\n".encode("latin-1")
    )
    df = read_dataset(path)
    assert df.loc[0, "Youtuber"] == "Ýôü Tübé"


def test_reads_utf8_csv(tmp_path):
    path = tmp_path / "utf8.csv"
    path.write_text("a,b\n1,ü\n", encoding="utf-8")
    assert read_dataset(path).loc[0, "b"] == "ü"


def test_mock_dataset_shape_and_names():
    df = make_mock_dataset()
    assert len(df) == 50
    assert df.loc[0, "Youtuber"] == "MrBeast"
    assert make_mock_dataset().equals(df)  # seeded, so reproducible


def test_standardize_maps_kaggle_columns():
    cleaned, m = standardize(make_mock_dataset())
    assert m == {
        "subscribers": "subscribers",
        "views": "video views",
        "category": "category",
        "country": "country",
        "earnings": "highest_yearly_earnings",
        "name": "youtuber",
    }
    assert "youtuber" in cleaned.columns


def test_standardize_falls_back_to_positions():
    df = pd.DataFrame(columns=["r", "who", "subs", "v", "cat"])
    _, m = standardize(df)
    assert (m["name"], m["subscribers"], m["views"], m["category"]) == (
        "who",
        "subs",
        "v",
        "cat",
    )
    assert m["country"] is None


def test_report_lists_top_creators_in_order():
    df = make_mock_dataset()
    report, _, _, cat_counts, country_counts = build_report(df, "x.csv")
    top = df.sort_values("subscribers", ascending=False).head(5)["Youtuber"].tolist()
    positions = [report.index(f"- {name}:") for name in top]
    assert positions == sorted(positions)
    assert "Analyzed File: x.csv" in report
    assert cat_counts.sum() == 50
    assert country_counts.sum() == 50


def test_report_handles_float_subscriber_counts():
    df = make_mock_dataset()
    df["subscribers"] = df["subscribers"].astype(float)
    report, *_ = build_report(df, "x.csv")
    assert " subs" in report


def test_summary_mentions_counts():
    text = summarize(make_mock_dataset(), "x.csv")
    assert "Records Count: 50" in text
    assert "Features Count: 9" in text
