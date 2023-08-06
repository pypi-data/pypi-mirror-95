# ---------------------------------------------------------
# Copyright (c) Microsoft Corporation. All rights reserved.
# ---------------------------------------------------------
"""Backwards compatible pass through during package migration."""
try:
    from azureml.automl.runtime.shared import model_wrappers
    from azureml.automl.runtime.shared.model_wrappers import _AbstractModelWrapper, LightGBMClassifier, \
        XGBoostClassifier, CatBoostClassifier, SparseNormalizer, SparseScaleZeroOne, PreprocWrapper, \
        StandardScalerWrapper, NBWrapper, TruncatedSVDWrapper, SVCWrapper, NuSVCWrapper, SGDClassifierWrapper, \
        EnsembleWrapper, LinearSVMWrapper, CalibratedModel, LightGBMRegressor, XGBoostRegressor, CatBoostRegressor, \
        RegressionPipeline, ForecastingPipelineWrapper, PipelineWithYTransformations, QuantileTransformerWrapper, \
        IdentityTransformer, LogTransformer, PowerTransformer, BoxCoxTransformerScipy, PreFittedSoftVotingClassifier, \
        PreFittedSoftVotingRegressor, StackEnsembleBase, StackEnsembleClassifier, StackEnsembleRegressor
except ImportError:
    pass
