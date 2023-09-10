from enum import Enum


class ArgsKeysEnums(Enum):
    FIWARE_ENTITY = "entity"
    FIWARE_ENTITY_TYPE = "type"
    FIWARE_ATTRS = "attribute"
    FIWARE_SERVICE = "fiware_service"
    FIWARE_SERVICE_PATH = "fiware_service_path"
    STH_AGGR_METHOD = "sth_aggr"
    DATASET = "dataset"
    CORRELATION_TARGET_COLLUMNS = "corr_target_collumns"
    LINEAR_REG_TARGET_COLLUMNS = "linear_reg_target_collumns"
    LINEAR_REG_ANALYSE_COLLUMNS = "linear_reg_analyse_collumns"

    RESULT_CORRELATION = "result_correlation"
    RESULT_LINEAR_REGRESSION = "result_linear_reg"