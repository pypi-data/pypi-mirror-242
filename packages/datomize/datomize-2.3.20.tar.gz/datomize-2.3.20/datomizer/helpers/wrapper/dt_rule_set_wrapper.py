from datomizer.helpers.wrapper.schema_wrapper import SchemaWrapper
from datomizer.protos.autodiscoveryservice_pb2 import HistogramEntryDTO, ColumnHistogramDTO, SchemaHistogramDTO
from datomizer.protos.datatunerservice_pb2 import DataTunerDTO, ClauseDTO, CategoricalClauseDTO, \
    NumericNormalDistClauseDTO, RangeClauseDTO


class DTRulesWrapper(object):
    rules: DataTunerDTO = None
    schema: SchemaWrapper = None
    histogram: SchemaHistogramDTO = None

    def __init__(self, rules, schema, histogram):
        self.rules = rules
        self.schema = schema
        self.histogram = histogram

    def set_output_amount(self, output_amount: int = 50):
        if output_amount > 0:
            self.rules.ruleSets[0].rules[0].outputAmount = output_amount
        else:
            raise Exception("output minimum is 1")

    def get_clause_by_column_name(self, column_name):
        clauses: list = self.rules.ruleSets[0].rules[0].clauses
        clause: ClauseDTO
        for clause in clauses:
            if clause.columnName == column_name:
                return clause

        return None

    def has_clause_for_column(self, column_name):
        if self.get_clause_by_column_name(column_name) is not None:
            return True
        else:
            return False

    def remove_clause_by_column_name(self,column_name):
        clause = self.get_clause_by_column_name(column_name)
        if clause is not None:
            self.rules.ruleSets[0].rules[0].clauses.remove(clause)

    def remove_all_clause(self):
        self.rules.ruleSets[0].rules[0].ClearField('clauses')

    def add_or_replace_clause(self, clause: ClauseDTO):
        if self.has_clause_for_column(clause.columnName):
            self.remove_clause_by_column_name(clause.columnName)
        self.rules.ruleSets[0].rules[0].clauses.append(clause)

    def add_uniform_dist_clause(self, column_name, min_val, max_val):
        self.min_max_validation(column_name, min_val, max_val)
        clause = ClauseDTO(columnName=column_name, rangeClause=RangeClauseDTO(minValue=str(min_val),
                                                                              maxValue=str(max_val)))
        self.add_or_replace_clause(clause)

    def add_normal_dist_clause(self, column_name, mean_value, std_value, min_val, max_val):
        self.mean_std_validation(column_name, mean_value, std_value, min_val, max_val)
        clause = ClauseDTO(columnName=column_name, numericNormalDistClause=NumericNormalDistClauseDTO(
            meanValue=str(mean_value),
            stdValue=str(std_value),
            minValue=str(min_val),
            maxValue=str(max_val)))
        self.add_or_replace_clause(clause)

    def add_categorical_clause(self, column_name, category_value):
        category_value = str(category_value)
        self.category_validation(column_name, category_value)
        clause = ClauseDTO(columnName=column_name, categoricalClause=CategoricalClauseDTO(categoryValue=category_value))
        self.add_or_replace_clause(clause)

    def min_max_validation(self, column_name, min_val, max_val):
        column = self.schema.column(self.schema.tables()[0].name, column_name)
        assert column.role == "numeric", "column must be of role numeric"
        assert min_val >= 0, "min value cannot be below 0"
        assert min_val <= max_val, "min value cannot be over max value"
        assert max_val <= float(column.maxValue), "max value cannot be over the columns max value"

    def mean_std_validation(self, column_name, mean_value, std_value, min_val, max_val):
        self.min_max_validation(column_name, min_val, max_val)
        assert mean_value > min_val, "mean_value value cannot be below min value"
        assert mean_value < max_val, "mean_value cannot be over max value"
        assert std_value >= 0, "std_value value cannot be below 0"
        assert std_value < (self.schema.column(self.schema.tables()[0].name, column_name).
                            statistics.standardDeviation * 3), "std_value cannot be over the columns std * 3"

    def category_validation(self, column_name, category_value):
        column_histogram: ColumnHistogramDTO = self.get_column_histogram_by_column_name(column_name)
        assert category_value is not None, "category value cannot be None"
        assert column_histogram is not None, "the column must have a histogram"
        assert column_histogram.role == "label", "column must be of role label"
        assert self.is_value_in_column_histogram(column_histogram, category_value), \
            "value must be in the columns histogram"

    def get_column_histogram_by_column_name(self, column_name):
        columns_histogram: list = self.histogram.tableHistogram[0].columnsHistogram
        column_histogram: ColumnHistogramDTO
        for column_histogram in columns_histogram:
            if column_histogram.columnName == column_name:
                return column_histogram

        return None

    def is_value_in_column_histogram(self, column_histogram, value):
        histogram_entry: HistogramEntryDTO
        for histogram_entry in column_histogram.entries:
            if histogram_entry.isNull is False and histogram_entry.value == value:
                return True

        return False

    def __str__(self):
        return str(self.rules)
