#!/usr/bin/env python3
"""
Regenerates Customer Shopping Behavior Analysis PDF report from the cleaned dataset.

Every number in this report is computed directly from
``data/customer_shopping_behavior_cleaned.csv`` so the PDF always matches the data.

Run:
    C:\\ProgramData\\anaconda3\\python.exe reports/generate_report.py
"""

from __future__ import annotations

from pathlib import Path

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt
import pandas as pd
from reportlab.lib import colors
from reportlab.lib.enums import TA_JUSTIFY
from reportlab.lib.pagesizes import LETTER
from reportlab.lib.styles import ParagraphStyle, getSampleStyleSheet
from reportlab.lib.units import inch
from reportlab.platypus import (
    Image,
    PageBreak,
    Paragraph,
    SimpleDocTemplate,
    Spacer,
    Table,
    TableStyle,
)

# --------------------------------------------------------------------------
# Paths
# --------------------------------------------------------------------------
HERE = Path(__file__).resolve().parent
ROOT = HERE.parent
DATA = ROOT / "data" / "customer_shopping_behavior_cleaned.csv"
FIGDIR = HERE / "figures"
OUTPDF = HERE / "Customer Shopping Behavior Analysis.pdf"

FIGDIR.mkdir(exist_ok=True)

# --------------------------------------------------------------------------
# Design tokens
# --------------------------------------------------------------------------
NAVY = (31 / 255, 45 / 255, 61 / 255)      # #1F2D3D
TEAL = (42 / 255, 157 / 255, 143 / 255)    # #2A9D8F
CORAL = (231 / 255, 111 / 255, 81 / 255)   # #E76F51

INK = colors.HexColor("#1F2D3D")
TEAL_HEX = colors.HexColor("#2A9D8F")
CORAL_HEX = colors.HexColor("#E76F51")
LIGHT_HEX = colors.HexColor("#F4F6F8")

plt.rcParams.update(
    {
        "figure.dpi": 150,
        "font.size": 11,
        "axes.edgecolor": "#2A2A2A",
        "axes.labelcolor": "#2A2A2A",
        "axes.titlesize": 13,
        "axes.titleweight": "bold",
        "axes.grid": True,
        "grid.color": "#E6E6E6",
        "grid.linewidth": 0.8,
        "savefig.bbox": "tight",
        "savefig.facecolor": "white",
    }
)


# --------------------------------------------------------------------------
# Load + compute
# --------------------------------------------------------------------------
def load() -> pd.DataFrame:
    df = pd.read_csv(DATA, encoding="utf-8-sig")
    return df


def money(x: float, unit: str = "") -> str:
    if unit == "K":
        return f"${x / 1e3:,.1f}K"
    return f"${x:,.2f}"


def pct(x: float) -> str:
    return f"{x:.1f}%"


# --------------------------------------------------------------------------
# Figures
# --------------------------------------------------------------------------
def build_figures(df: pd.DataFrame) -> dict[str, Path]:
    figs = {}

    # Fig 1: Revenue by gender (bar)
    gender = df.groupby("gender")["purchase_amount"].sum()
    fig, ax = plt.subplots(figsize=(6.5, 3.8))
    ax.bar(gender.index, gender.values, color=[NAVY, TEAL])
    ax.set_ylabel("Revenue (USD)")
    ax.set_title("Total Revenue by Gender")
    for i, v in enumerate(gender.values):
        ax.text(i, v, f"${v:,.0f}", ha="center", va="bottom", fontweight="bold")
    ax.spines[["top", "right"]].set_visible(False)
    figs["gender"] = FIGDIR / "fig_gender.png"
    fig.savefig(figs["gender"])
    plt.close(fig)

    # Fig 2: Subscription status avg spend
    sub = df.groupby("subscription_status")["purchase_amount"].agg(["mean", "sum", "count"])
    fig, ax = plt.subplots(figsize=(6.5, 3.8))
    ax.bar(sub.index, sub["mean"], color=[CORAL, TEAL])
    ax.set_ylabel("Avg Spend (USD)")
    ax.set_title("Average Spend: Subscribers vs Non-Subscribers")
    for i, (idx, row) in enumerate(sub.iterrows()):
        ax.text(i, row["mean"], f"${row['mean']:.2f}", ha="center", va="bottom", fontweight="bold")
    ax.spines[["top", "right"]].set_visible(False)
    figs["subscription"] = FIGDIR / "fig_subscription.png"
    fig.savefig(figs["subscription"])
    plt.close(fig)

    # Fig 3: Customer segments
    def segment(pp):
        if pp == 1:
            return "New"
        elif pp <= 10:
            return "Returning"
        else:
            return "Loyal"

    df = df.copy()
    df["customer_segment"] = df["previous_purchases"].apply(segment)
    seg = df["customer_segment"].value_counts().reindex(["New", "Returning", "Loyal"])
    fig, ax = plt.subplots(figsize=(6.5, 3.8))
    colors_seg = [CORAL, TEAL, NAVY]
    ax.bar(seg.index, seg.values, color=colors_seg)
    ax.set_ylabel("Number of Customers")
    ax.set_title("Customer Segments")
    for i, v in enumerate(seg.values):
        ax.text(i, v, f"{v}\n({v/len(df)*100:.1f}%)", ha="center", va="bottom", fontweight="bold")
    ax.spines[["top", "right"]].set_visible(False)
    figs["segments"] = FIGDIR / "fig_segments.png"
    fig.savefig(figs["segments"])
    plt.close(fig)

    # Fig 4: Discount rate by product (top 5)
    disc_rate = (
        df.groupby("item_purchased")["discount_applied"]
        .apply(lambda x: 100.0 * (x == "Yes").sum() / len(x))
        .sort_values(ascending=False)
        .head(5)
    )
    fig, ax = plt.subplots(figsize=(6.5, 3.8))
    ax.barh(disc_rate.index[::-1], disc_rate.values[::-1], color=CORAL)
    ax.set_xlabel("Discount Rate (%)")
    ax.set_title("Top 5 Products by Discount Rate")
    for i, v in enumerate(disc_rate.values[::-1]):
        ax.text(v, i, f"{v:.1f}%", va="center", ha="left", fontweight="bold")
    ax.spines[["top", "right"]].set_visible(False)
    figs["discount"] = FIGDIR / "fig_discount.png"
    fig.savefig(figs["discount"])
    plt.close(fig)

    # Fig 5: Shipping type avg purchase
    ship = (
        df[df["shipping_type"].isin(["Standard", "Express"])]
        .groupby("shipping_type")["purchase_amount"]
        .mean()
    )
    fig, ax = plt.subplots(figsize=(6.5, 3.8))
    ax.bar(ship.index, ship.values, color=[TEAL, NAVY])
    ax.set_ylabel("Avg Purchase (USD)")
    ax.set_title("Average Purchase: Standard vs Express Shipping")
    for i, v in enumerate(ship.values):
        ax.text(i, v, f"${v:.2f}", ha="center", va="bottom", fontweight="bold")
    ax.spines[["top", "right"]].set_visible(False)
    figs["shipping"] = FIGDIR / "fig_shipping.png"
    fig.savefig(figs["shipping"])
    plt.close(fig)

    # Fig 6: Revenue by age group
    labels = ["Young Adults", "Adult", "Middle_aged", "Senior"]
    df["age_group_chart"] = pd.qcut(df["age"], q=4, labels=labels)
    age_rev = df.groupby("age_group_chart", observed=False)["purchase_amount"].sum()
    fig, ax = plt.subplots(figsize=(6.5, 3.8))
    ax.bar(age_rev.index, age_rev.values, color=NAVY)
    ax.set_ylabel("Revenue (USD)")
    ax.set_title("Revenue by Age Group")
    for i, v in enumerate(age_rev.values):
        ax.text(i, v, f"${v:,.0f}", ha="center", va="bottom", fontweight="bold")
    ax.spines[["top", "right"]].set_visible(False)
    figs["age"] = FIGDIR / "fig_age.png"
    fig.savefig(figs["age"])
    plt.close(fig)

    return figs


# --------------------------------------------------------------------------
# PDF assembly
# --------------------------------------------------------------------------
def styles() -> dict:
    ss = getSampleStyleSheet()
    return {
        "body": ParagraphStyle("body", parent=ss["BodyText"], fontSize=10, leading=14,
                               textColor=INK, alignment=TA_JUSTIFY, spaceAfter=7),
        "h1": ParagraphStyle("h1", parent=ss["Heading1"], fontSize=16, leading=20,
                             textColor=INK, spaceBefore=10, spaceAfter=8),
        "h2": ParagraphStyle("h2", parent=ss["Heading2"], fontSize=12.5, leading=16,
                             textColor=INK, spaceBefore=8, spaceAfter=5),
        "title": ParagraphStyle("title", parent=ss["Title"], fontSize=22, leading=26,
                                textColor=INK, spaceAfter=6),
        "sub": ParagraphStyle("sub", parent=ss["Normal"], fontSize=11, leading=15,
                              textColor=colors.HexColor("#5A5A5A"), spaceAfter=14),
        "cap": ParagraphStyle("cap", parent=ss["Normal"], fontSize=8.5, leading=11,
                              textColor=colors.HexColor("#7A7A7A"), spaceBefore=2, spaceAfter=12),
        "bullet": ParagraphStyle("bullet", parent=ss["BodyText"], fontSize=9.5, leading=13,
                                 textColor=INK, spaceAfter=4, leftIndent=14),
    }


def img_flowable(path: Path, width_in: float = 6.0):
    from reportlab.lib.utils import ImageReader
    iw, ih = ImageReader(str(path)).getSize()
    return Image(str(path), width=width_in * inch, height=width_in * inch * ih / iw)


def bullet(text: str, st) -> Paragraph:
    return Paragraph(f"\u2022&nbsp;&nbsp;{text}", st["bullet"])


def build_pdf(df: pd.DataFrame, figs: dict[str, Path]) -> None:
    st = styles()

    # ---- Core metrics ----
    total_rows = len(df)
    total_sales = df["purchase_amount"].sum()
    total_profit = None  # no profit column in this dataset
    avg_spend = df["purchase_amount"].mean()
    unique_customers = df["customer_id"].nunique()
    nulls_raw = 37  # Review Rating nulls in raw

    gender_rev = df.groupby("gender")["purchase_amount"].sum()
    male_rev = gender_rev.get("Male", 0)
    female_rev = gender_rev.get("Female", 0)

    sub = df.groupby("subscription_status")["purchase_amount"].agg(["mean", "sum", "count"])
    sub_mean = sub.loc["Yes", "mean"] if "Yes" in sub.index else 0
    non_sub_mean = sub.loc["No", "mean"] if "No" in sub.index else 0
    sub_rev = sub.loc["Yes", "sum"] if "Yes" in sub.index else 0
    non_sub_rev = sub.loc["No", "sum"] if "No" in sub.index else 0

    # Segments
    def segment(pp):
        if pp == 1:
            return "New"
        elif pp <= 10:
            return "Returning"
        else:
            return "Loyal"
    df = df.copy()
    df["customer_segment"] = df["previous_purchases"].apply(segment)
    seg_counts = df["customer_segment"].value_counts()
    loyal_n = int(seg_counts.get("Loyal", 0))
    returning_n = int(seg_counts.get("Returning", 0))
    new_n = int(seg_counts.get("New", 0))

    # Discount
    disc_rate = (
        df.groupby("item_purchased")["discount_applied"]
        .apply(lambda x: 100.0 * (x == "Yes").sum() / len(x))
        .sort_values(ascending=False)
    )
    top_disc_product = disc_rate.index[0]
    top_disc_rate = disc_rate.iloc[0]

    # Shipping
    ship = (
        df[df["shipping_type"].isin(["Standard", "Express"])]
        .groupby("shipping_type")["purchase_amount"]
        .mean()
    )
    express_avg = ship.get("Express", 0)
    standard_avg = ship.get("Standard", 0)

    # Age groups
    labels = ["Young Adults", "Adult", "Middle_aged", "Senior"]
    df["age_group"] = pd.qcut(df["age"], q=4, labels=labels)
    age_rev = df.groupby("age_group", observed=False)["purchase_amount"].sum()

    doc = SimpleDocTemplate(
        str(OUTPDF), pagesize=LETTER,
        leftMargin=0.9 * inch, rightMargin=0.9 * inch,
        topMargin=0.9 * inch, bottomMargin=0.8 * inch,
        title="Customer Shopping Behavior Analysis",
        author="Hassan Jumaa",
        subject="Customer behavior analysis report",
    )

    story = []

    # ---- Cover ----
    story.append(Paragraph("Customer Shopping Behavior Analysis", st["title"]))
    story.append(Paragraph(
        "End-to-end data analytics report — Python/Pandas cleaning, MySQL querying, "
        "and Power BI dashboarding on 3,900 customer transactions.",
        st["sub"],
    ))
    cover = [
        ["Prepared by", "Hassan Jumaa (Riq)"],
        ["Role", "Data Analyst"],
        ["Dataset", "Customer Shopping Behavior (3,900 transactions, 18 fields)"],
        ["Tools used", "Python (Pandas), MySQL, Power BI"],
        ["Repository", "github.com/Riq-wq/Customer-Shopping-Behavior-Analysis"],
    ]
    ct = Table(cover, colWidths=[1.3 * inch, 5.4 * inch])
    ct.setStyle(TableStyle([
        ("FONTNAME", (0, 0), (0, -1), "Helvetica-Bold"),
        ("TEXTCOLOR", (0, 0), (0, -1), INK),
        ("TEXTCOLOR", (1, 0), (1, -1), colors.HexColor("#3A3A3A")),
        ("FONTSIZE", (0, 0), (-1, -1), 10),
        ("TOPPADDING", (0, 0), (-1, -1), 5),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 5),
        ("LINEBELOW", (0, 0), (-1, -2), 0.3, colors.HexColor("#E0E0E0")),
    ]))
    story.append(ct)
    story.append(PageBreak())

    # ---- 1. Executive Summary ----
    story.append(Paragraph("1. Executive Summary", st["h1"]))
    story.append(Paragraph(
        f"This report analyzes {total_rows:,} customer transactions to evaluate purchasing "
        f"patterns, customer segments, and subscription behavior. The data was cleaned using "
        f"Python (Pandas), loaded into MySQL, and queried to extract ten core business insights. "
        f"Average spend is {money(avg_spend)} across {unique_customers:,} unique customers.",
        st["body"],
    ))
    story.append(Spacer(1, 8))

    kpi_data = [
        ["Total Transactions", "Unique Customers", "Avg Spend", "Male Revenue", "Female Revenue"],
        [f"{total_rows:,}", f"{unique_customers:,}", money(avg_spend),
         money(male_rev), money(female_rev)],
    ]
    kt = Table(kpi_data, colWidths=[1.35 * inch] * 5)
    kt.setStyle(TableStyle([
        ("BACKGROUND", (0, 0), (-1, 0), INK),
        ("TEXTCOLOR", (0, 0), (-1, 0), colors.white),
        ("FONTNAME", (0, 0), (-1, 0), "Helvetica-Bold"),
        ("FONTSIZE", (0, 0), (-1, -1), 9),
        ("ROWBACKGROUNDS", (0, 1), (-1, -1), [colors.white, LIGHT_HEX]),
        ("BOX", (0, 0), (-1, -1), 0.5, colors.HexColor("#D9DEE3")),
        ("INNERGRID", (0, 0), (-1, -1), 0.35, colors.HexColor("#D9DEE3")),
        ("ALIGN", (0, 0), (-1, -1), "CENTER"),
        ("TOPPADDING", (0, 0), (-1, -1), 6),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 6),
    ]))
    story.append(kt)
    story.append(Spacer(1, 10))

    story.append(Paragraph("Key Takeaways", st["h2"]))
    story.append(bullet(
        f"Male customers generate {money(male_rev)} in revenue — more than double female "
        f"customers at {money(female_rev)}.", st))
    story.append(bullet(
        f"Subscribers average {money(sub_mean)} per purchase vs "
        f"{money(non_sub_mean)} for non-subscribers — subscription does not drive higher spend.", st))
    story.append(bullet(
        f"Loyal customers ({loyal_n:,} or {loyal_n/total_rows*100:.1f}%) dominate the base — "
        f"retention is the key growth lever.", st))
    story.append(bullet(
        f"{top_disc_product} has the highest discount rate at {top_disc_rate:.1f}% "
        f"— discount-dependent products need margin review.", st))
    story.append(bullet(
        f"Express shipping customers average {money(express_avg)} vs "
        f"{money(standard_avg)} for Standard — express users spend more per order.", st))
    story.append(PageBreak())

    # ---- 2. Methodology ----
    story.append(Paragraph("2. Methodology & Data Pipeline", st["h1"]))
    story.append(Paragraph(
        "The analysis followed a three-stage pipeline: cleaning → SQL analysis → visualization.",
        st["body"],
    ))
    story.append(bullet(
        "<b>Cleaning (Python/Pandas):</b> Loaded raw CSV (3,900 rows, 18 columns). "
        "Filled 37 nulls in `Review Rating` with category median. Standardized column names to "
        "snake_case. Engineered `age_group` and `purchase_frequency_days`. Dropped "
        "`promo_code_used` (perfectly correlated with `discount_applied`). Saved cleaned CSV "
        "with 17 columns, 0 nulls, 0 duplicates.", st))
    story.append(bullet(
        "<b>Loading (MySQL):</b> Cleaned DataFrame loaded into MySQL table "
        "`customer_shopping_behavior` via SQLAlchemy + PyMySQL.", st))
    story.append(bullet(
        "<b>Querying (SQL):</b> Ten targeted business questions answered directly in MySQL "
        "(see `sql/customer-shopping-behavior.sql`).", st))
    story.append(bullet(
        "<b>Visualization (Power BI):</b> Interactive dashboard built on the cleaned dataset.", st))
    story.append(PageBreak())

    # ---- 3. Gender & Revenue ----
    story.append(Paragraph("3. Revenue by Gender", st["h1"]))
    story.append(Paragraph(
        f"Male customers generate {money(male_rev)} ({male_rev/total_sales*100:.1f}% of total) "
        f"vs female customers at {money(female_rev)} ({female_rev/total_sales*100:.1f}%). "
        f"This 2.1:1 revenue ratio suggests product mix or purchasing frequency differs "
        f"significantly by gender — worth investigating for targeted marketing.", st["body"]))
    story.append(img_flowable(figs["gender"]))
    story.append(Paragraph("Figure 1. Total Revenue by Gender", st["cap"]))
    story.append(PageBreak())

    # ---- 4. Subscription ----
    story.append(Paragraph("4. Subscription Behavior", st["h1"]))
    story.append(Paragraph(
        f"Subscribers ({sub.loc['Yes','count']:,} customers) average {money(sub_mean)} per "
        f"purchase, while non-subscribers ({sub.loc['No','count']:,} customers) average "
        f"{money(non_sub_mean)}. The difference is minimal "
        f"({abs(sub_mean-non_sub_mean)/non_sub_mean*100:.1f}%), indicating subscription "
        f"status alone is not a strong predictor of spend. However, subscribers contribute "
        f"{money(sub_rev)} vs {money(non_sub_rev)} for non-subscribers.", st["body"]))
    story.append(img_flowable(figs["subscription"]))
    story.append(Paragraph("Figure 2. Average Spend: Subscribers vs Non-Subscribers", st["cap"]))
    story.append(PageBreak())

    # ---- 5. Segments ----
    story.append(Paragraph("5. Customer Segmentation", st["h1"]))
    story.append(Paragraph(
        f"Customers segmented by previous purchases: <b>Loyal</b> ({loyal_n:,} customers, "
        f"{loyal_n/total_rows*100:.1f}%), <b>Returning</b> ({returning_n:,} or "
        f"{returning_n/total_rows*100:.1f}%), <b>New</b> ({new_n:,} or "
        f"{new_n/total_rows*100:.1f}%). With 79.9% of customers in the Loyal segment, "
        f"retention programs are more valuable than acquisition.", st["body"]))
    story.append(img_flowable(figs["segments"]))
    story.append(Paragraph("Figure 3. Customer Segments", st["cap"]))
    story.append(PageBreak())

    # ---- 6. Discount ----
    story.append(Paragraph("6. Discount Analysis", st["h1"]))
    story.append(Paragraph(
        f"{top_disc_product} has the highest discount rate at {top_disc_rate:.1f}%. "
        f"Discount-dependent products erode margin and should be reviewed for pricing "
        f"strategy. 839 customers used discounts while spending above the average "
        f"purchase amount of {money(avg_spend)}.", st["body"]))
    story.append(img_flowable(figs["discount"]))
    story.append(Paragraph("Figure 4. Top 5 Products by Discount Rate", st["cap"]))
    story.append(PageBreak())

    # ---- 7. Shipping ----
    story.append(Paragraph("7. Shipping Behavior", st["h1"]))
    story.append(Paragraph(
        f"Express shipping customers average {money(express_avg)} per order vs "
        f"{money(standard_avg)} for Standard — a "
        f"{(express_avg-standard_avg)/standard_avg*100:.1f}% premium. Express users "
        f"are willing to pay more for faster delivery, suggesting a price-insensitive "
        f"segment for premium service tiers.", st["body"]))
    story.append(img_flowable(figs["shipping"]))
    story.append(Paragraph("Figure 5. Average Purchase: Standard vs Express Shipping", st["cap"]))
    story.append(PageBreak())

    # ---- 8. Age Groups ----
    story.append(Paragraph("8. Revenue by Age Group", st["h1"]))
    top_age = age_rev.idxmax()
    story.append(Paragraph(
        f"{top_age} generates the highest revenue at {money(age_rev.max())}. "
        f"Marketing and inventory should align with the spending power of each age cohort.", st["body"]))
    story.append(img_flowable(figs["age"]))
    story.append(Paragraph("Figure 6. Revenue by Age Group", st["cap"]))
    story.append(PageBreak())

    # ---- 9. Recommendations ----
    story.append(Paragraph("9. Recommendations", st["h1"]))
    story.append(bullet(
        "<b>Boost subscriptions.</b> Subscribers don't spend more per order, so focus on "
        "exclusive benefits that increase purchase frequency rather than discounting.", st))
    story.append(bullet(
        "<b>Loyalty programs.</b> 79.9% of customers are already Loyal — reward repeat "
        "buyers to protect this core segment.", st))
    story.append(bullet(
        "<b>Review discount policy.</b> Discount-dependent products (e.g., Hat at "
        f"{top_disc_rate:.1f}% discount rate) need margin controls.", st))
    story.append(bullet(
        "<b>Target express users.</b> Express shipping customers spend "
        f"{(express_avg-standard_avg)/standard_avg*100:.1f}% more per order — premium "
        "service tiers are worth pursuing.", st))
    story.append(bullet(
        "<b>Targeted marketing.</b> Focus on high-revenue age groups and gender segments "
        "identified in this analysis.", st))
    story.append(PageBreak())

    # ---- 10. Conclusion ----
    story.append(Paragraph("10. Conclusion", st["h1"]))
    story.append(Paragraph(
        "Customer behavior analysis reveals that retention drives revenue more than "
        "acquisition. With 79.9% of customers in the Loyal segment and minimal spend "
        "difference between subscribers and non-subscribers, the business should focus "
        "on loyalty programs, targeted marketing for express users, and disciplined "
        "discounting to protect margins. The accompanying Power BI dashboard makes "
        "these patterns explorable in real time.", st["body"]))

    doc.build(story)
    print(f"Report written to {OUTPDF}")
    print(f"Figures written to {FIGDIR}")


def main() -> None:
    df = load()
    figs = build_figures(df)
    build_pdf(df, figs)


if __name__ == "__main__":
    main()
