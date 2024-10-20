import re
import unicodedata
from pathlib import Path

import pandas as pd


def sanitize_filename(value):
    """
    Sanitizes a filename.

    Parameters:
        value (str): The string to sanitize.

    Returns:
        str: The sanitized filename.
    """
    value = unicodedata.normalize("NFD", value)
    value = value.encode("ascii", "ignore").decode("utf-8")
    value = re.sub(r"\s+", "_", value)
    value = re.sub(r"[^A-Za-z0-9_]", "", value)
    return value


def categorize_household(df):
    """
    Categorizes the 'Household' column based on the 'Libellé' column.

    Parameters:
        df (pd.DataFrame): The DataFrame to process.

    Returns:
        pd.DataFrame: The DataFrame with the 'Household' column added.
    """
    household = pd.Series("Ensemble des ménages", index=df.index)

    mask1 = df["Libellé"].str.contains(
        "Ménages urbains dont le chef est ouvrier ou employé",
        case=False,
        na=False,
    )
    household[mask1] = "Ménages urbains dont le chef est ouvrier ou employé"

    mask2 = df["Libellé"].str.contains(
        "Ménages du premier quintile de la distribution des niveaux de vie",
        case=False,
        na=False,
    )
    household[mask2] = (
        "Ménages du premier quintile de la distribution des niveaux de vie"
    )

    return household


def categorize_region(df):
    """
    Categorizes the 'Region' column based on the 'Libellé' column.

    Parameters:
        df (pd.DataFrame): The DataFrame to process.

    Returns:
        pd.DataFrame: The DataFrame with the 'Region' column added.
    """
    regions = [
        "Mayotte",
        "Guadeloupe",
        "Martinique",
        "La Réunion",
        "Guyane",
        "France métropolitaine",
    ]
    region_series = pd.Series("", index=df.index)
    for region in regions:
        mask = df["Libellé"].str.contains(region, case=False, na=False)
        region_series[mask] = region
    region_series[region_series == ""] = "France"
    region_series = region_series.str.title()
    return region_series


def categorize_index_type(df):
    """
    Categorizes the 'Index Type' and 'Variation Type' columns based on the 'Libellé' column.

    Parameters:
        df (pd.DataFrame): The DataFrame to process.

    Returns:
        pd.DataFrame: The DataFrame with the 'Index Type' and 'Variation Type' columns added.
    """
    index_type = pd.Series("IPC", index=df.index)
    variation_type = pd.Series("None", index=df.index)

    index_mask1 = df["Libellé"].str.contains(
        "Indice CVS des prix à la consommation", case=False, na=False
    )
    index_type[index_mask1] = "Indice CVS des prix à la consommation"

    index_mask2 = df["Libellé"].str.contains(
        "Indice d'inflation sous-jacente", case=False, na=False
    )
    index_type[index_mask2] = "Indice d'inflation sous-jacente"

    index_mask3 = df["Libellé"].str.contains(
        "Secteurs conjoncturels", case=False, na=False
    )
    index_type[index_mask3] = "Secteurs conjoncturels"

    variation_mask1 = df["Libellé"].str.contains(
        "Glissement annuel", case=False, na=False
    )
    variation_type[variation_mask1] = "Glissement annuel"

    variation_mask2 = df["Libellé"].str.contains(
        "Variations mensuelles", case=False, na=False
    )
    variation_type[variation_mask2] = "Variations mensuelles"

    return index_type, variation_type


def set_boolean_flags(df):
    """
    Sets boolean flags for 'IsNomenclature', 'IsBase100', and 'IsSerieArretee'.

    Parameters:
        df (pd.DataFrame): The DataFrame to process.

    Returns:
        pd.DataFrame: The DataFrame with the boolean flag columns added.
    """
    is_nomenclature = df["Libellé"].str.contains(
        "nomenclature", case=False, na=False
    )
    is_base_100 = df["Libellé"].str.contains("base 100", case=False, na=False)
    is_serie_arretee = df["Libellé"].str.contains(
        "série arrêtée", case=False, na=False
    )
    return is_nomenclature, is_base_100, is_serie_arretee


def main():
    df = pd.read_excel(
        "donnees_brutes.xlsx",
        usecols=lambda x: x
        not in {"idBank", "Dernière mise à jour", "Période"},
        dtype={"Libellé": str},
    )

    pattern = r"^(199[0-9]|20[0-9][0-9])-(0[1-9]|1[0-2])$"
    date_columns = df.columns[df.columns.str.match(pattern)]
    df[date_columns] = df[date_columns].apply(pd.to_numeric, errors="coerce")

    household = categorize_household(df)
    region = categorize_region(df)
    index_type, variation_type = categorize_index_type(df)
    is_nomenclature, is_base_100, is_serie_arretee = set_boolean_flags(df)

    df = df.assign(
        Household=household,
        Region=region,
        IndexType=index_type,
        VariationType=variation_type,
        IsNomenclature=is_nomenclature,
        IsBase100=is_base_100,
        IsSerieArretee=is_serie_arretee,
    )

    df = df[~(df["IsBase100"] | df["IsSerieArretee"])].reset_index(drop=True)

    output_folder = Path("donnees_traitees")
    output_folder.mkdir(parents=True, exist_ok=True)

    group_columns = [
        "Household",
        "Region",
        "IndexType",
        "VariationType",
        "IsNomenclature",
    ]
    grouped = df.groupby(group_columns)

    for group_keys, group_df in grouped:
        (
            household,
            region,
            index_type,
            variation_type,
            is_nomenclature,
        ) = group_keys
        nomenclature_str = (
            "Nomenclature" if is_nomenclature else "NonNomenclature"
        )
        filename = f"{household}_{region}_{index_type}_{variation_type}_{nomenclature_str}"
        filename = sanitize_filename(filename) + ".csv"

        columns_to_drop = [
            "Household",
            "Region",
            "IndexType",
            "VariationType",
            "IsNomenclature",
            "IsBase100",
            "IsSerieArretee",
        ]
        group_df = group_df.drop(columns=columns_to_drop)

        try:
            group_df.to_csv(output_folder / filename, index=False)
            print(f"File written: {filename}")
        except Exception as e:
            print(f"Error writing file {filename}: {e}")


if __name__ == "__main__":
    main()
