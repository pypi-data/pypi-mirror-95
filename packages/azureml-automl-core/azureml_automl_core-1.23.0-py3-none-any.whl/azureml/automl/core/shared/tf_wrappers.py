# ---------------------------------------------------------
# Copyright (c) Microsoft Corporation. All rights reserved.
# ---------------------------------------------------------
"""Backwards compatible pass through during package migration."""
try:
    from azureml.automl.runtime.shared import tf_wrappers
    from azureml.automl.runtime.shared.tf_wrappers import \
        (TFLinearClassifierWrapper, TFDNNClassifierWrapper, TFLinearRegressorWrapper,
         TFDNNRegressorWrapper, OPTIMIZERS, ACTIVATION_FNS)
except ImportError:
    pass
