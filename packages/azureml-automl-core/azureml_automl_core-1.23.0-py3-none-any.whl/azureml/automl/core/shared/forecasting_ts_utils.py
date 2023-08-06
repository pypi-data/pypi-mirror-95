# ---------------------------------------------------------
# Copyright (c) Microsoft Corporation. All rights reserved.
# ---------------------------------------------------------
"""Backwards compatible pass through during package migration."""
try:
    from azureml.automl.runtime.shared import forecasting_ts_utils
    from azureml.automl.runtime.shared.forecasting_ts_utils import\
        (construct_day_of_quarter, datetime_is_date, last_n_periods_split,
         detect_seasonality_tsdf, get_stl_decomposition)
except ImportError:
    pass
