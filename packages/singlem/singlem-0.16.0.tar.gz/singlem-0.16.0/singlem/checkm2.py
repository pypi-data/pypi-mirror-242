import polars as pl
import logging
from dataclasses import dataclass

@dataclass
class CheckM2Stats:
    completeness: float
    contamination: float


class CheckM2:
    def __init__(self, quality_file):
        self.quality_file = quality_file
        self.qualities = pl.read_csv(self.quality_file, separator='\t')
        logging.info("Read in {} genome qualities".format(self.qualities.shape[0]))

    def genomes_of_sufficient_quality(self, min_completeness, max_contamination):
        return list(
            self.qualities.filter((pl.col("Completeness") >= min_completeness) &
                                  (pl.col("Contamination") <= max_contamination)).select('Name').get_columns()[0])

    # Implement "in"
    def __contains__(self, item):
        return self.qualities.filter(pl.col("Name") == item).shape[0] > 0

    def get_stats(self, genome_name):
        found = self.qualities.filter(pl.col("Name") == genome_name)
        if found.shape[0] != 1:
            raise Exception("Expected to find 1 genome, found {}".format(found.shape[0]))
        
        for row in found.rows(named=True):
            return CheckM2Stats(
                completeness=row['Completeness'] / 100.,
                contamination=row['Contamination'] / 100.
            )
