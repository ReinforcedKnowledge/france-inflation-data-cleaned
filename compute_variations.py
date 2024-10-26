from pathlib import Path

import pandas as pd

from processing import sanitize_filename

data_folder = Path("donnees_traitees")


def compute_variation(
    region,
    variation_to_compute,
    index_type="IPC",
    nomenclature="NonNomenclature",
    household="Ensemble des ménages",
):
    filename = f"{household}_{region}_{index_type}_None_{nomenclature}"
    filename = sanitize_filename(filename) + ".csv"
    df = pd.read_csv(data_folder / filename)
    df.set_index("Libellé", inplace=True)
    if variation_to_compute == "yoy":
        period = 12
        variation_name = "Glissement_annuel"
    if variation_to_compute == "mom":
        period = 1
        variation_name = "Variations_mensuelles"
    period_over_period = df.pct_change(periods=period, axis=1) * 100
    output_filename = filename.replace("None", variation_name)
    period_over_period.to_csv(data_folder / output_filename, index=False)
    print(f"Saved computed {variation_name} data for {index_type} for {region}")


def main():
    for region in ["Guadeloupe", "Guyane", "La Réunion", "Martinique"]:
        compute_variation(region, "yoy")
        compute_variation(region, "mom")


if __name__ == "__main__":
    main()
