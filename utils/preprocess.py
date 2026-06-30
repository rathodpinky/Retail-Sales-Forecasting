import pandas as pd


def preprocess_input(df):
    """
    Preprocess user input before prediction.
    """

    categorical_cols = [
        "Store_ID",
        "Store_Location",
        "Product_ID",
        "Product_Category",
        "Product_Subcategory",
        "Brand",
        "Customer_Type",
        "Payment_Mode",
        "Region",
        "Promotion_Applied"
    ]

    df = pd.get_dummies(
        df,
        columns=categorical_cols
    )

    return df