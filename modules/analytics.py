
import matplotlib.pyplot as plt


def create_damage_chart(classified_regions):

    categories = [
        "No Damage",
        "Minor Damage",
        "Major Damage",
        "Destroyed"
    ]

    counts = {category: 0 for category in categories}

    for region in classified_regions:
        category = region["damage_class"]

        if category in counts:
            counts[category] += 1

    fig, ax = plt.subplots(figsize=(8, 5))

    ax.bar(
        counts.keys(),
        counts.values()
    )

    ax.set_title("Disaster Damage Category Analysis")
    ax.set_xlabel("Damage Category")
    ax.set_ylabel("Number of Regions")

    plt.xticks(rotation=15)
    plt.tight_layout()

    return fig, counts
