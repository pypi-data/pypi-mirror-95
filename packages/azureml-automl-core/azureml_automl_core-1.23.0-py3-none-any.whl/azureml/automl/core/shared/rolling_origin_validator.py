# ---------------------------------------------------------
# Copyright (c) Microsoft Corporation. All rights reserved.
# ---------------------------------------------------------
"""Backwards compatible pass through during package migration."""
try:
    from azureml.automl.runtime.shared import rolling_origin_validator
    from azureml.automl.runtime.shared.rolling_origin_validator import RollingOriginValidator
except ImportError:
    pass
