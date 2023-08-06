# ---------------------------------------------------------
# Copyright (c) Microsoft Corporation. All rights reserved.
# ---------------------------------------------------------
"""Backwards compatible pass through during package migration."""
try:
    from azureml.automl.runtime.shared import memory_utilities
    from azureml.automl.runtime.shared.memory_utilities import (get_data_memory_size, get_all_ram,
                                                                get_available_physical_memory, get_memory_footprint)
except ImportError:
    pass
