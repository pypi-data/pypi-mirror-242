# from compare_datasets.prepare import PrepareForComparison
# from compare_datasets.string_comparisons import StringComparisons
# from compare_datasets.numeric_comparisons import NumericComparisons
# from datetime import datetime


# class Compare:
#     def __init__ (self, tested, expected, key=None):
#         self.data = PrepareForComparison(tested, expected, key)
#         self.tested = self.data.tested
#         self.expected = self.data.expected
#         self.string_comparisons = StringComparisons(expected=self.data.expected, tested=self.data.tested)
#         self.numeric_comparisons = NumericComparisons(expected=self.data.expected, tested=self.data.tested)
        
#     def report (self):
#         report = []
#         report.append(self.data.__str__())
#         report.append(self.string_comparisons.generate_report())
#         report.append(self.numeric_comparisons.generate_report())
#         return "\n \n".join(report)
        
#     def __repr__ (self):
#         return self.report()

      
#     def save_report (self, path=""):     
#         timestamp = datetime.now().strftime("%Y%m%d%H%M%S")
#         filename = f"report_{timestamp}.txt"
#         report = self.report()   
#         with open(f"{path}/{filename}", "w",encoding="utf-8") as f:
#             f.write(report)
        

