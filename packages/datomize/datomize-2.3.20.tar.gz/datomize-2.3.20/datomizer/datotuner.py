import io

from datomizer import DatoMapper
from datomizer.helpers.common_helper import wait_for_step_type, get_generated_zip, get_generated_csv
from datomizer.helpers.train import datatuner_helper, train_helper
from datomizer.helpers.wrapper.dt_rule_set_wrapper import DTRulesWrapper
from datomizer.utils.general import ID, MODELS, ERROR
from datomizer.utils.interfaces import DatoGenInterface
from datomizer.utils.step_types import DT_TRAIN_AND_GENERATE
from datomizer.protos.datatunerservice_pb2 import DataTunerDTO, RuleSetDTO, RuleDTO


class DatoTuner(DatoGenInterface):
    dato_mapper: DatoMapper
    dt_rules_wrapper: DTRulesWrapper
    train_id = 0
    model_id = 0

    def __init__(self, dato_mapper: DatoMapper):
        """Create DatoTuner object for training a tuned model for the mapped input data.
        Args:
            dato_mapper: the DatoMapper object for the input data."""
        dato_mapper.next_step_validation()
        dato_mapper.single_table_validation()
        self.dato_mapper = dato_mapper
        self.dato_mapper.get_schema()
        self.dato_mapper.get_schema_histogram()
        self.dt_rules_wrapper: DTRulesWrapper = DTRulesWrapper(
            DataTunerDTO(ruleSets=[RuleSetDTO(tableName=self.dato_mapper.schema.tables()[0].name,
                                              rules=[RuleDTO(id=1, outputAmount=50, clauses=[])])]),
            self.dato_mapper.schema,
            self.dato_mapper.histogram)

    @classmethod
    def restore(cls, dato_mapper: DatoMapper, train_id):
        dato_trainer = cls(dato_mapper)
        dato_trainer.train_id = train_id
        dato_trainer.wait()
        return dato_trainer

    def tune(self, wait=True) -> None:
        """Train a generative model.
        Args:
            wait: use wait=False for asynchronous programming; True by default (awaits for the results)."""
        assert self.train_id == 0, "tuner cannot be used twice"
        assert len(self.dt_rules_wrapper.rules.ruleSets[0].rules[0].clauses) >= 1, "at least 1 clause is needed"
        self.train_id = datatuner_helper.put_rules_and_tune(self.dato_mapper, self.dt_rules_wrapper.rules)
        if wait:
            self.wait()

    def wait(self) -> None:
        """Wait until the train method returns."""
        self.restore_validation()
        status = wait_for_step_type(datomizer=self.dato_mapper.datomizer,
                                    business_unit_id=self.dato_mapper.business_unit_id,
                                    project_id=self.dato_mapper.project_id,
                                    flow_id=self.dato_mapper.flow_id,
                                    step_type=DT_TRAIN_AND_GENERATE,
                                    train_id=self.train_id)
        if status == ERROR:
            raise Exception("Trainer Failed")
        self.model_id = train_helper.get_train_iteration(self.dato_mapper, self.train_id)[MODELS][0][ID]

    def list_tables(self):
        return self.dato_mapper.schema.tables_name()

    def get_generated_data(self) -> None:
        self.next_step_validation()
        print(get_generated_zip(datomizer=self.dato_mapper.datomizer,
                                business_unit_id=self.dato_mapper.business_unit_id,
                                project_id=self.dato_mapper.project_id,
                                flow_id=self.dato_mapper.flow_id,
                                train_id=self.train_id,
                                model_id=self.model_id))

    def get_generated_data_csv(self, table_name: str = None) -> io.StringIO:
        """Get the generated data in a csv format.
                Args:
                    table_name: the name of the generated data
                Returns:
                    StringIO object containing the generated data"""
        self.next_step_validation()

        table_name = self.dato_mapper.schema.table(table_name).name

        return get_generated_csv(datomizer=self.dato_mapper.datomizer,
                                 business_unit_id=self.dato_mapper.business_unit_id,
                                 project_id=self.dato_mapper.project_id,
                                 flow_id=self.dato_mapper.flow_id,
                                 train_id=self.train_id,
                                 model_id=self.model_id,
                                 table_name=table_name)

    def restore_validation(self):
        if not (self.train_id > 0):
            raise Exception("flow id required for this step")

    def next_step_validation(self):
        self.restore_validation()
        if not (self.model_id > 0):
            raise Exception("DatoTrainer not ready")
