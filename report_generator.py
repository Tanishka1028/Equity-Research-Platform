from reportlab.platypus import (
    SimpleDocTemplate,
    Paragraph,
    Spacer
)

from reportlab.lib.styles import getSampleStyleSheet


def generate_report(
    ticker,
    company,
    metrics,
    current_price,
    intrinsic_value,
    upside,
    rating
):

    filename = f"{ticker}_Research_Report.pdf"

    doc = SimpleDocTemplate(filename)

    styles = getSampleStyleSheet()

    content = []

    content.append(
        Paragraph(
            f"{company} Equity Research Report",
            styles["Title"]
        )
    )

    content.append(
        Spacer(1, 20)
    )

    content.append(
        Paragraph(
            f"Ticker: {ticker}",
            styles["Normal"]
        )
    )

    content.append(
        Paragraph(
            f"Current Price: ${current_price:.2f}",
            styles["Normal"]
        )
    )

    content.append(
        Paragraph(
            f"Intrinsic Value: ${intrinsic_value:.2f}",
            styles["Normal"]
        )
    )

    content.append(
        Paragraph(
            f"Upside Potential: {upside:.2f}%",
            styles["Normal"]
        )
    )

    content.append(
        Paragraph(
            f"Recommendation: {rating}",
            styles["Normal"]
        )
    )

    content.append(
        Spacer(1, 20)
    )

    content.append(
        Paragraph(
            "Financial Metrics",
            styles["Heading2"]
        )
    )

    for key, value in metrics.items():

        content.append(
            Paragraph(
                f"{key}: {value}",
                styles["Normal"]
            )
        )

    doc.build(content)

    return filename