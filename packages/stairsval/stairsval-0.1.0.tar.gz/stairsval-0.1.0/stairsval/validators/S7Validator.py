import pandas as pd
import pkg_resources
from rich.console import Console
from stairs_mro.networks.DefectRes import DefectRes
from stairs_mro.networks.WorkResNet import WorkResNet

from stairsval.core.aggregator import Aggregator
from stairsval.core.dataset_processors.S7KSG import S7KSG
from stairsval.core.expert_metrics_estimator import ExpertMetricsEstimator
from stairsval.validation_checks.ResourcesChecker import ResourcesChecker
from stairsval.validation_checks.TimeChecker import TimeChecker
from stairsval.validators.BaseValidator import BaseValidator

res_work = "../tables/work_res_data_no_nan_new2.csv"
res_defect = "../tables//work_defect_res_data_no_nan_new2.csv"
res_work_path = pkg_resources.resource_filename(__name__, res_work)
res_defect_path = pkg_resources.resource_filename(__name__, res_defect)


class S7PlanValidator:
    def __init__(self, plan, work_res_model: str, defect_model: str):
        self.console = Console()
        self.ksg_data = S7KSG(ksg_data=plan).collect()
        self.aggregator = Aggregator()
        self.time_validator = TimeChecker()
        self.resources_validator = None
        self.work_res_model = work_res_model
        self.defect_model = defect_model

    def validate(self):
        pass

    def common_validate(self):
        val_df_res_work = pd.read_csv(res_work_path)
        val_df_res_defect = pd.read_csv(res_defect_path)

        (
            df_validation_table_res,
            fig_dict_res,
            norm_perc_res_val,
            not_perc_res_val,
        ) = ResourcesChecker(res=[]).common_validation(
            self.ksg_data, (val_df_res_work, val_df_res_defect), plan_type="s7"
        )

        model_work = WorkResNet(structure=[])
        model_work.load(self.work_res_model)

        model_defect = DefectRes(structure=[])
        model_defect.load(self.defect_model)

        proximity_model = (model_work, model_defect)
        df_vedom, not_perc_vedom, norm_perc_vedom = self.aggregator.get_res_ved_stat(
            proximity_model, self.ksg_data, plan_type="s7"
        )
        (
            df_validation_table_time,
            fig_dict_time,
            norm_perc_time,
            not_perc_time,
        ) = TimeChecker().common_validation(
            self.ksg_data, (val_df_res_work, val_df_res_defect), "s7"
        )
        return (
            df_validation_table_res,
            fig_dict_res,
            norm_perc_res_val,
            not_perc_res_val,
            df_vedom,
            not_perc_vedom,
            norm_perc_vedom,
            df_validation_table_time,
            fig_dict_time,
            norm_perc_time,
            not_perc_time,
        )


class S7Validator(BaseValidator):

    """Validator for S7 plans."""

    def __init__(self, project_ksg, work_res_model: str, defect_model: str):
        super().__init__(project_ksg)
        self.plan_type = "s7"
        self.work_res_model = work_res_model
        self.defect_model = defect_model

    def specific_validation(self):
        return self.common_validation()

    def common_validation(self, cut_to_n_works: int = None):
        if cut_to_n_works:
            self._trim_plan_to_n_works(cut_to_n_works)
        (
            df_validation_table_res,
            fig_dict_res,
            norm_perc_res_val,
            not_perc_res_val,
            df_vedom,
            not_perc_vedom,
            norm_perc_vedom,
            df_validation_table_time,
            fig_dict_time,
            norm_perc_time,
            not_perc_time,
        ) = S7PlanValidator(
            plan=self.project_ksg,
            work_res_model=self.work_res_model,
            defect_model=self.defect_model,
        ).common_validate()

        work_res_stat = dict()
        work_res_stat["Процент нормальных значений объёмов ресурсов"] = round(
            norm_perc_res_val
        )
        work_res_stat["Процент нетипичных значений объёмов ресурсов"] = 100 - round(
            norm_perc_res_val
        )
        work_res_stat["Процент нормальных ресурсов по ведомостям"] = round(
            norm_perc_vedom
        )
        work_res_stat["Процент нетипичных ресурсов по ведомостям"] = 100 - round(
            norm_perc_vedom
        )
        work_res_stat["Процент нормальных значений по всем ресурсам"] = round(
            (
                work_res_stat["Процент нормальных значений объёмов ресурсов"]
                + work_res_stat["Процент нормальных ресурсов по ведомостям"]
            )
            / 2
        )
        work_res_stat["Процент нетипичных значений по всем ресурсам"] = (
            100 - work_res_stat["Процент нормальных значений по всем ресурсам"]
        )
        work_res_stat["Процент нормальных значений времени работ"] = round(
            norm_perc_time
        )
        work_res_stat["Процент нетипичных значений времени работ"] = 100 - round(
            norm_perc_time
        )
        work_res_stat["Процент нормальных занчений по всем работам"] = round(
            norm_perc_time
        )
        work_res_stat["Процент нетипичных занчений по всем работам"] = 100 - round(
            norm_perc_time
        )
        work_res_stat["Процент нормальных значений плана"] = round(
            (
                work_res_stat["Процент нормальных значений по всем ресурсам"]
                + work_res_stat["Процент нормальных занчений по всем работам"]
            )
            / 2
        )
        work_res_stat["Процент нетипичных значений плана"] = (
            100 - work_res_stat["Процент нормальных значений плана"]
        )
        work_res_stat["Процент непокрытых валидацией значений плана"] = round(
            (not_perc_res_val + not_perc_vedom + not_perc_time) / 3
        )
        work_res_stat["Процент покрытых валидацией значений плана"] = 100 - round(
            (not_perc_res_val + not_perc_vedom + not_perc_time) / 3
        )

        result_dict = dict()
        result_dict["Common validation"] = {
            "Таблица валидации ресурсов": df_validation_table_res,
            "Данные для графиков ресурсов": fig_dict_res,
            "Ресурсная ведомость": df_vedom,
            "Таблица валидации рвемени работ": df_validation_table_time,
            "Данные для графиков времени": fig_dict_time,
            "Итоговая статистика плана": work_res_stat,
        }
        return result_dict

    def calculate_expert_metrics(self):
        metrics_calculator = ExpertMetricsEstimator(self.project_ksg)
        metrics = metrics_calculator.calculate_metrics()
        formal_metrics = metrics_calculator.calculate_formal_metrics()
        return metrics, formal_metrics
