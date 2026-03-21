"""
Translates raw event_code values in a DataFrame into
human-readable descriptions, severity, and category.
Applied after SQL execution so the user never sees raw codes.
"""
import pandas as pd
from config.event_codes import get_event_description, get_event_severity, get_event_category

def translate_event_codes_in_df(df: pd.DataFrame) -> pd.DataFrame:
    """
    If the DataFrame has an 'event_code' column, add enriched columns:
    - event_description
    - event_severity
    - event_category
    """
    if df.empty or "event_code" not in df.columns:
        return df

    df = df.copy()
    df["event_description"] = df["event_code"].apply(
        lambda c: get_event_description(c) if pd.notna(c) else None
    )
    df["event_severity"] = df["event_code"].apply(
        lambda c: get_event_severity(c) if pd.notna(c) else None
    )
    df["event_category"] = df["event_code"].apply(
        lambda c: get_event_category(c) if pd.notna(c) else None
    )
    return df
