# ---------------------------------------------------------
# Copyright (c) Microsoft Corporation. All rights reserved.
# ---------------------------------------------------------
"""Backwards compatible pass through during package migration."""
try:
    from azureml.automl.runtime.shared import time_series_data_frame
    from azureml.automl.runtime.shared.time_series_data_frame import TimeSeriesDataFrame
except ImportError:
    pass
