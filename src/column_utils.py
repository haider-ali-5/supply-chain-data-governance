"""Shared helpers for column-name handling across the pipeline steps."""

# Canonical spelling of columns the pipeline refers to by name. The raw DataCo
# CSV ships some of them with different capitalisation (e.g. "order date
# (DateOrders)"), so incoming names are matched case-insensitively.
CANONICAL_COLUMNS = [
    'Order Date (DateOrders)',
    'Shipping Date (DateOrders)',
]


def normalize_columns(df, canonical=CANONICAL_COLUMNS):
    """Rename columns that match a canonical name ignoring case/whitespace."""
    lookup = {name.lower(): name for name in canonical}
    rename = {}
    for col in df.columns:
        target = lookup.get(str(col).strip().lower())
        if target is not None and col != target:
            rename[col] = target
    return df.rename(columns=rename) if rename else df
