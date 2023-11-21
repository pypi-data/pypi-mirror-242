from abc import ABC, abstractmethod
from tabulate import tabulate
import logging
import polars as pl

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class Comparison(ABC):
    @abstractmethod
    def generate_differenced_dataframe(self):
        pass

    @abstractmethod
    def generate_report(self):
        pass

    @abstractmethod
    def compare(self):
        pass

    @abstractmethod
    def validate(self, tested, expected, data_type):
        data_type = [data_type] if isinstance(data_type, str) else data_type
        schema_of_expected = expected.schema
        schema_of_tested = tested.schema
        # logger.info([str(dtype) for dtype in schema_of_expected.values()])
        # logger.info([str(dtype) == data_type for dtype in schema_of_expected.values()])
        # logger.info(data_type)
        if not all(str(dtype) in data_type for dtype in schema_of_expected.values()):
            logger.info(
                f"\n{tabulate( [ (name, dtype) for name, dtype in schema_of_expected.items() if dtype != data_type ], headers=['Column Name', 'Data Type'] )}"
            )
            raise TypeError(
                f"Non-{data_type} column passed to the {data_type} comparison utility"
            )
        else:
            logger.info("All columns are of type string")
    
    
    
    def calculate_jaccard_similarity(self,columns_names):        
        definition = "Jaccard Similarity is defined as the size of the intersection divided by the size of the union of the sets. J(A,B) = |A ∩ B| / |A ∪ B|."
        jaccard_similarity = [self.__jaccard_similarity__(self.expected[column], self.tested[column]) for column in columns_names]
        result = ["PASSED" if jaccard_score==1 else "FAILED" for jaccard_score in jaccard_similarity]
        self.report['jaccard_similarity'] = {}
        self.report['jaccard_similarity']['result'] = all(jaccard_score==1 for jaccard_score in jaccard_similarity)            
        self.report['jaccard_similarity']['report'] = tabulate([ (column, jaccard_score, result) for column, jaccard_score, result in zip(self.columns_names, jaccard_similarity, result)], headers=['Column Name', 'Jaccard Similarity', 'Result'], tablefmt='orgtbl')
        
        if not self.report['jaccard_similarity']['result']:
            self.report['jaccard_similarity']['explanation'] = f"{definition}\nThe Jaccard similarity between the expected and tested dataframes is not 1 for all columns. This means that the expected and tested dataframes have different values for the same column(s)."
        else:
            self.report['jaccard_similarity']['explanation'] = f"{definition}\nThe Jaccard similarity between the expected and tested dataframes is 1 for all columns. This means that the expected and tested dataframes have the same values for the same column(s)."
    
    def __jaccard_similarity__(self, s1: pl.Series, s2: pl.Series) -> float:
        """
        This method calculates the Jaccard similarity between two series.
        The Jaccard similarity is the size of the intersection divided by the size of the union of the two series.
        :param s1: The first series.
        :param s2: The second series.
        :return: The Jaccard similarity between the two series.
        """
        s1 = set(s1)
        s2 = set(s2)
        intersection = len(s1.intersection(s2))
        union = len(s1.union(s2))
        return intersection / union
    
def stringify_result (result):
        """
        This method is used to convert the result into a string format.
        :param result: The result to be converted into string format.
        :return: "PASSED" if result is True, else "FAILED".
        """
        return "PASSED" if result else "FAILED"

