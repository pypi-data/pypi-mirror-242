# Copyright 2023 Ant Group Co., Ltd.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#      https://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

from secretflow.component.feature.vert_woe_binning import (
    vert_woe_binning_comp,
    vert_woe_substitution_comp,
)
from secretflow.component.ml.boost.sgb.sgb import sgb_predict_comp, sgb_train_comp
from secretflow.component.ml.boost.ss_xgb.ss_xgb import (
    ss_xgb_predict_comp,
    ss_xgb_train_comp,
)
from secretflow.component.ml.eval.biclassification_eval import (
    biclassification_eval_comp,
)
from secretflow.component.ml.eval.prediction_bias_eval import prediction_bias_comp
from secretflow.component.ml.eval.ss_pvalue import ss_pvalue_comp
from secretflow.component.ml.linear.ss_sgd import ss_sgd_predict_comp, ss_sgd_train_comp
from secretflow.component.preprocessing.feature_filter import feature_filter_comp
from secretflow.component.preprocessing.psi import psi_comp
from secretflow.component.preprocessing.train_test_split import train_test_split_comp
from secretflow.component.stats.ss_pearsonr import ss_pearsonr_comp
from secretflow.component.stats.ss_vif import ss_vif_comp
from secretflow.component.stats.table_statistics import table_statistics_comp
from secretflow.protos.component.cluster_pb2 import SFClusterConfig
from secretflow.protos.component.comp_pb2 import CompListDef, ComponentDef
from secretflow.protos.component.evaluation_pb2 import NodeEvalParam, NodeEvalResult
from secretflow.component.ml.linear.ss_glm import ss_glm_predict_comp, ss_glm_train_comp

ALL_COMPONENTS = [
    train_test_split_comp,
    psi_comp,
    ss_sgd_train_comp,
    ss_sgd_predict_comp,
    feature_filter_comp,
    vert_woe_binning_comp,
    vert_woe_substitution_comp,
    ss_vif_comp,
    ss_pearsonr_comp,
    ss_pvalue_comp,
    table_statistics_comp,
    biclassification_eval_comp,
    prediction_bias_comp,
    sgb_predict_comp,
    sgb_train_comp,
    ss_xgb_predict_comp,
    ss_xgb_train_comp,
    ss_glm_predict_comp,
    ss_glm_train_comp,
]
COMP_LIST_NAME = "secretflow"
COMP_LIST_DESC = "First-party SecretFlow components."
COMP_LIST_VERSION = "0.0.1"


def gen_key(domain: str, name: str, version: str) -> str:
    return f"{domain}/{name}:{version}"


def generate_comp_list():
    comp_list = CompListDef()
    comp_list.name = COMP_LIST_NAME
    comp_list.desc = COMP_LIST_DESC
    comp_list.version = COMP_LIST_VERSION
    comp_map = {}
    all_comp_defs = []
    for x in ALL_COMPONENTS:
        x_def = x.definition()
        comp_map[gen_key(x_def.domain, x_def.name, x_def.version)] = x
        all_comp_defs.append(x_def)

    all_comp_defs = sorted(all_comp_defs, key=lambda k: (k.domain, k.name, k.version))
    comp_list.comps.extend(all_comp_defs)
    return comp_list, comp_map


COMP_LIST, COMP_MAP = generate_comp_list()


def get_comp_def(domain: str, name: str, version: str) -> ComponentDef:
    key = gen_key(domain, name, version)
    assert key in COMP_MAP
    return COMP_MAP[key].definition()


# FIXME(junfeng): Should load storage config from .sf_storage JSON file
def comp_eval(
    param: NodeEvalParam,
    cluster_config: SFClusterConfig,
    tracer_report: bool = False,
) -> NodeEvalResult:
    key = gen_key(param.domain, param.name, param.version)
    if key in COMP_MAP:
        comp = COMP_MAP[key]
        return comp.eval(param, cluster_config, tracer_report=tracer_report)
    else:
        raise RuntimeError("component is not found.")
