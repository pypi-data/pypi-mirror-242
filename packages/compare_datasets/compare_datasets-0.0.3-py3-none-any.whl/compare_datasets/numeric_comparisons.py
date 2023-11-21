import distance_functions as dfn
from compare_datasets.structure import Comparison
from tabulate import tabulate
import polars as pl
from compare_datasets.structure import stringify_result



class NumericComparisons(Comparison):
    def __init__(self, expected, tested):
        super().validate(tested, expected, ["Int64", "Float64", "UInt64", "Int32", "Float32", "UInt32", "Int16", "UInt16", "Int8", "UInt8"])
        self.data_type = 'NUMERIC'
        self.expected = expected
        self.columns_names = list(expected.columns)
        self.tested = tested
        self.report = {}
        self.report["name"] = "Numeric Column Comparison"
        super().calculate_jaccard_similarity(self.columns_names)
        self.compare()
        self.report['overall_result'] = self.report['jaccard_similarity']['result'] and self.report['value_by_value']['result']
    
    def generate_differenced_dataframe(self):
        """
        Generates a dataframe containing the difference between the expected and tested dataframes.
        """
        differenced = pl.DataFrame([
                (c, dfn.compute_euclidean_distance(self.expected[c], self.tested[c])) for c in self.columns_names
            ],
        schema= ["Column Name", "Euclidean Distance"]
        )
        return differenced.with_columns([(pl.col("Euclidean Distance")==0).alias('Result')])
        
    def compare(self):
        self.differenced = self.generate_differenced_dataframe()
        self.report['value_by_value'] = {}        
        self.report['value_by_value']['result'] = (
            self.differenced['Euclidean Distance'].sum()
            == 0
        )
        self.report['value_by_value']['report'] = tabulate([(column, distance, stringify_result(result)) for column, distance, result in self.differenced.rows()], headers=['Column Name', 'Euclidean Distance', 'Result'], tablefmt='orgtbl')
        
        self.report['value_by_value']['explanation'] = "The string comparisons are done using the Euclidean distance. The Euclidean distance is a measure of the straight line distance between two points in a space. Given two points P and Q with coordinates (p1, p2, ..., pn) and (q1, q2, ..., qn) respectively, the Euclidean distance d between P and Q is: d(P, Q) = sqrt((q1 - p1)² + (q2 - p2)² + ... + (qn - pn)²)"
        
        if not self.report['value_by_value']['result']:
            self.report['value_by_value']['explanation'] += f"\nThe Euclidean distance between the expected and tested dataframes is not 0 for all columns. This means that the expected and tested dataframes have different numeric values in the same column(s)."
        else:
            self.report['value_by_value']['explanation'] += f"\nThe Euclidean distance between the expected and tested dataframes is 0 for all columns. This means that the expected and tested dataframes have the same numeric values for the same column(s)."
    
    def generate_report(self):
        report = f"""COMPARISON FOR {self.data_type} COLUMNS
-----------------------------------------

OVERALL RESULT: {stringify_result(self.report['overall_result'])}

-----------------------------------------
TEST 1: Jaccard Similarity

RESULT: {stringify_result(self.report['jaccard_similarity']['result'])}

{self.report['jaccard_similarity']['report']}

{self.report['jaccard_similarity']['explanation']}

-----------------------------------------
TEST 2: Value by Value Comparison

RESULT: {stringify_result(self.report['value_by_value']['result'])}

{self.report['value_by_value']['report']}

{self.report['value_by_value']['explanation']}

"""
        return report
        
    def validate(self):
        return super().validate(self.tested, self.expected, ["Int64", "Float64", "UInt64", "Int32", "Float32", "UInt32", "Int16", "UInt16", "Int8", "UInt8"])

