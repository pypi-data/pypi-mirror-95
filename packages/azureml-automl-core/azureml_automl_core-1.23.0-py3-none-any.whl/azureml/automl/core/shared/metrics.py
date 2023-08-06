# ---------------------------------------------------------
# Copyright (c) Microsoft Corporation. All rights reserved.
# ---------------------------------------------------------
"""Backwards compatible pass through during package migration."""
try:
    from azureml.automl.runtime.shared import metrics
    from azureml.automl.runtime.shared.metrics import \
        (minimize_or_maximize, is_better, compute_metrics_regression, compute_metrics, compute_metrics_classification)
except ImportError:
    pass
