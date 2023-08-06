# ---------------------------------------------------------
# Copyright (c) Microsoft Corporation. All rights reserved.
# ---------------------------------------------------------
"""Backwards compatible pass through during package migration."""
try:
    from azureml.automl.runtime.shared import forecasting_utils
    from azureml.automl.runtime.shared.forecasting_utils import \
        (array_equal_with_nans, flatten_list,
         get_period_offsets_from_dates, grain_level_to_dict, invert_dict_of_lists, is_iterable_but_not_string,
         make_groupby_map, subtract_list_from_list)
except ImportError:
    pass
