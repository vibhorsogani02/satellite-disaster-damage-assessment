def classify_damage(region_details):

    classified_regions = []

    for region in region_details:

        area = region.get("area", 0)

        if area < 500:
            damage_class = "Minor Damage"

        elif area < 2000:
            damage_class = "Major Damage"

        else:
            damage_class = "Destroyed"

        item = region.copy()
        item["damage_class"] = damage_class

        classified_regions.append(item)

    return classified_regions