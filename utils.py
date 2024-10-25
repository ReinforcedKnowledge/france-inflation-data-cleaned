from typing import Any

import pandas as pd


def parse_filenames(filenames: list[str]) -> pd.DataFrame:
    """
    Parses a list of filenames to extract availables parameters options and returns a DataFrame
    representing available data combinations.
    Parameters are:
        - Region
        - Household Type
        - Index Type
        - Variation Type
        - Nomenclature

    Parameters:
        filenames (list[str]): List of data filenames.

    Returns:
        pd.DataFrame: DataFrame with columns for each filter parameter.
    """
    known_household_types = sorted(
        [
            "Menages du premier quintile de la distribution des niveaux de vie",
            "Menages urbains dont le chef est ouvrier ou employe",
            "Ensemble des menages",
        ],
        key=lambda x: len(x.split()),
        reverse=True,
    )

    known_regions = sorted(
        [
            "France Metropolitaine",
            "La Reunion",
            "France",
            "Martinique",
            "Guadeloupe",
            "Guyane",
        ],
        key=lambda x: len(x.split()),
        reverse=True,
    )

    records = []
    for filename in filenames:
        if not filename.endswith(".csv"):
            continue

        name_without_ext = filename[:-4]

        parts = name_without_ext.split("_")

        if len(parts) < 5:
            continue

        nomenclature = parts[-1].replace("_", " ")

        if parts[-2].lower() == "none":
            variation_type = "None"
        else:
            # Assume VariationType is two parts
            variation_type = (
                f"{parts[-3].replace('_', ' ')} {parts[-2].replace('_', ' ')}"
            )

        variation_start_index = -2 if variation_type == "None" else -3
        main_parts = parts[:variation_start_index]

        household_type = None
        household_type_length = 0
        for ht in known_household_types:
            ht_parts = ht.split()
            ht_length = len(ht_parts)
            if main_parts[:ht_length] == ht.split():
                household_type = ht
                household_type_length = ht_length
                break
        if not household_type:
            print(
                f"HouseholdType not found in filename '{filename}'. Skipping."
            )
            continue

        remaining_parts = main_parts[household_type_length:]
        region = None
        region_length = 0
        for reg in known_regions:
            reg_parts = reg.split()
            reg_length = len(reg_parts)
            if remaining_parts[:reg_length] == reg.split():
                region = reg
                region_length = reg_length
                break
        if not region:
            print(f"Region not found in filename '{filename}'. Skipping.")
            continue

        index_type_parts = remaining_parts[region_length:]
        if not index_type_parts:
            print(f"IndexType not found in filename '{filename}'. Skipping.")
            continue
        index_type = " ".join(index_type_parts).replace("_", " ")

        record = {
            "HouseholdType": household_type,
            "Region": region,
            "IndexType": index_type,
            "VariationType": variation_type,
            "Nomenclature": nomenclature,
        }
        records.append(record)

    df = pd.DataFrame(records)
    return df


def build_mappings(df: pd.DataFrame) -> dict[str, Any]:
    """
    Builds mappings between parameters options based on data availability.

    Parameters:
        df (pd.DataFrame): DataFrame with columns with options for each parameter.

    Returns:
        Dict[str, Any]: A nested dictionary representing mappings.
    """
    mappings = {}

    household_groups = df.groupby("HouseholdType")
    household_mappings = {}
    for household, group in household_groups:
        household_mappings[household] = {
            "Regions": sorted(group["Region"].unique()),
            "IndexTypes": sorted(group["IndexType"].unique()),
            "VariationTypes": sorted(group["VariationType"].unique()),
            "Nomenclatures": sorted(group["Nomenclature"].unique()),
        }
    mappings["HouseholdType"] = household_mappings

    region_groups = df.groupby("Region")
    region_mappings = {}
    for region, group in region_groups:
        region_mappings[region] = {
            "HouseholdTypes": sorted(group["HouseholdType"].unique()),
            "IndexTypes": sorted(group["IndexType"].unique()),
            "VariationTypes": sorted(group["VariationType"].unique()),
            "Nomenclatures": sorted(group["Nomenclature"].unique()),
        }
    mappings["Region"] = region_mappings

    index_groups = df.groupby("IndexType")
    index_mappings = {}
    for index_type, group in index_groups:
        index_mappings[index_type] = {
            "HouseholdTypes": sorted(group["HouseholdType"].unique()),
            "Regions": sorted(group["Region"].unique()),
            "VariationTypes": sorted(group["VariationType"].unique()),
            "Nomenclatures": sorted(group["Nomenclature"].unique()),
        }
    mappings["IndexType"] = index_mappings

    variation_groups = df.groupby("VariationType")
    variation_mappings = {}
    for variation_type, group in variation_groups:
        variation_mappings[variation_type] = {
            "HouseholdTypes": sorted(group["HouseholdType"].unique()),
            "Regions": sorted(group["Region"].unique()),
            "IndexTypes": sorted(group["IndexType"].unique()),
            "Nomenclatures": sorted(group["Nomenclature"].unique()),
        }
    mappings["VariationType"] = variation_mappings

    nomenclature_groups = df.groupby("Nomenclature")
    nomenclature_mappings = {}
    for nomenclature, group in nomenclature_groups:
        nomenclature_mappings[nomenclature] = {
            "HouseholdTypes": sorted(group["HouseholdType"].unique()),
            "Regions": sorted(group["Region"].unique()),
            "IndexTypes": sorted(group["IndexType"].unique()),
            "VariationTypes": sorted(group["VariationType"].unique()),
        }
    mappings["Nomenclature"] = nomenclature_mappings

    return mappings
