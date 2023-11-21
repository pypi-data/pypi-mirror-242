import distance_functions as dfn
from compare_datasets.structure import Comparison
from tabulate import tabulate
import polars as pl
from compare_datasets.structure import stringify_result



class StringComparisons(Comparison):
    def __init__(self, expected, tested):
        super().validate(tested, expected, "Utf8")
        self.data_type = 'STRING'
        self.expected = expected
        self.columns_names = list(expected.columns)
        self.tested = tested
        self.report = {}
        self.report["name"] = "String Column Comparison"
        super().calculate_jaccard_similarity(self.columns_names)
        self.compare()
        self.report['overall_result'] = self.report['jaccard_similarity']['result'] and self.report['value_by_value']['result']

    def levenshtein(self, c: pl.Expr) -> pl.Expr:
        return dfn.compute_levenshtein_distance(c, self.tested.select(c))        
        
    def generate_differenced_dataframe(self):
        """
        Generates a dataframe containing the difference between the expected and tested dataframes.
        """
        return pl.DataFrame(
            [
                pl.Series(
                    dfn.compute_levenshtein_distance(self.expected[c], self.tested[c])
                ).alias(c)
                for c in self.columns_names
            ]
        )

    def compare(self):
        self.differenced = self.generate_differenced_dataframe()
        levenshtein_distances = pl.Series(self.differenced.select(pl.all().sum()).melt()["value"])
        self.report['value_by_value'] = {}        
        self.report['value_by_value']['result'] = (
            levenshtein_distances.sum()
            == 0
        )
        self.report['value_by_value']['report'] = tabulate([(column, distance, stringify_result(result)) for column, distance, result in zip(self.columns_names, levenshtein_distances, levenshtein_distances==0) ], headers=['Column Name', 'Total Levenshtein Distance', 'Result'], tablefmt='orgtbl')
        self.report["differenced"] = self.differenced
        
        self.report['value_by_value']['explanation'] = "The string comparisons are done using the Levenshtein distance. The Levenshtein distance is the minimum number of single-character edits (insertions, deletions or substitutions) required to change one word into the other."
        
        if not self.report['value_by_value']['result']:
            self.report['value_by_value']['explanation'] += f"\nThe Levenshtein distance between the expected and tested dataframes is not 0 for all columns. This means that the expected and tested dataframes have different string values in the same column(s)."
        else:
            self.report['value_by_value']['explanation'] += f"\nThe Levenshtein distance between the expected and tested dataframes is 0 for all columns. This means that the expected and tested dataframes have the same values for the same column(s)."
        

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
        return super().validate(self.tested, self.expected, "Utf8")

