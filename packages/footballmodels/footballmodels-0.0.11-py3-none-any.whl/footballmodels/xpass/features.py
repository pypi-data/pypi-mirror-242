import pandas as pd
from typing import Tuple
import numpy as np
from footballmodels.opta import functions as F
from footballmodels.opta.distance import distance
from footballmodels.opta.passes import is_open_play_pass


def filter_to_open_play_passes(data: pd.DataFrame) -> pd.DataFrame:
    print(data.shape[0])
    data_n = data.loc[is_open_play_pass(data)].copy()
    print(data_n.shape[0])
    data_n = data_n.loc[~F.col_has_qualifier(data_n, qualifier_code=123)].copy()
    print(data_n.shape[0])
    data_n = data_n.loc[~F.col_has_qualifier(data_n, qualifier_code=124)].copy()
    print(data_n.shape[0])
    return data_n


def x_pass_features(data: pd.DataFrame) -> Tuple[pd.DataFrame, np.ndarray]:
    data_n = filter_to_open_play_passes(data)

    data_n["pass_angle"] = F.col_get_qualifier_value(
        data_n, display_name="Angle"
    ).astype(float)
    data_n["pass_length"] = distance(
        data_n["x"].values,
        data_n["y"].values,
        data_n["endX"].values,
        data_n["endY"].values,
    )
    data_n["is_chipped"] = F.col_has_qualifier(data_n, qualifier_code=155).astype(int)
    data_n["is_headpass"] = F.col_has_qualifier(data_n, qualifier_code=3).astype(int)
    data_n["is_throughball"] = F.col_has_qualifier(data_n, qualifier_code=4).astype(int)
    columns = [
        "x",
        "y",
        "pass_angle",
        "pass_length",
        "is_chipped",
        "is_headpass",
        "is_throughball",
    ]
    return (data_n[columns], data_n["outcomeType"].values)
