import pandas as pd
import numpy as np
from os.path import join
from typing import List, Any, Dict
from ailist import LabeledIntervalArray
from intervalframe import IntervalFrame

# Local imports
from ..genomes.genomes import InfoReader
from ..kmers.kmer_reader import read_kmers, read_sequence, gc_percent
from .utilities import adjust_bounds


class GenomeInfo(object):
    """
    Class for reading genome info files.
    """

    def __init__(self, genome_name: str) -> None:
        """
        Initialize the class.
        """

        # Read info file
        self.info = InfoReader(genome_name)
        self.name = self.info.name
        self.version = self.info.version
        self.keys = self.info.keys
        self.seq_file = join(self.info.data_directory, self.info.genome_name, "external", self.info.genome_name + ".2bit")
        self.pfm_scanner = None

        return None
    
    def __repr__(self):
        """
        Print the info file.
        """

        repr_string = "Genome info file for %s version %s\n" % (self.name, self.version)

        return repr_string
    

    def __getitem__(self, key):
        """
        Get an item from the info file.
        """

        try:
            value = self.info[key]
        except KeyError:
            value = self.info.base_object["properties"][key]

        return value

    
    def sequence(self,
                chromosome: str,
                start: int,
                end: int) -> str:
        """
        Get sequence

        Parameters
        ----------
            chromosome : str
                Chromosome name
            start : int
                Start position
            end : int
                End position

        Returns
        -------
            sequence : str
        """

        # Get sequence
        sequence = read_sequence(self.seq_file, chromosome, start, end)

        return sequence

    
    def interval_kmers(self,
                        intervals: LabeledIntervalArray,
                        k: int = 2,
                        last_n: int = 0) -> Dict[str,int]:
        """
        Get kmers from intervals

        Parameters
        ----------
            intervals : LabeledIntervalArray
                Intervals
            k : int
                Kmer length
            last_n : int
                Last n bases to query

        Returns
        -------
            kmers : Dict[str,int]
                Kmer counts
        """

        # Calculate kmers
        kmers = read_kmers(self.seq_file, intervals, k, last_n)

        return kmers


    def count_kmers(self,
                    chrom: str,
                    start: int,
                    end: int,
                    k: int = 2) -> Dict[str,int]:
        """
        Count kmers in interval

        Parameters
        ----------
            chrom : str
                Chromosome
            start : int
                Start position
            end : int
                End position
            k : int
                Kmer length

        Returns
        -------
            kmers : Dict[str,int]
                Kmer counts
        """

        # Calculate kmers
        intervals = LabeledIntervalArray()
        intervals.add(start, end, chrom)
        kmers = read_kmers(self.seq_file, intervals, k)

        return kmers


    def load_pfm_scanner(self):
        """
        """

        import MOODS.parsers
        import MOODS.tools
        import MOODS.scan

        # Get PFM scanner
        pfms = self["pfm"]
        bg = MOODS.tools.flat_bg(4)
        pvalue = 0.0001
        thresholds = [MOODS.tools.threshold_from_p(m, bg, pvalue) for m in pfms[1]]
        
        # Create scanner
        self.pfm_scanner = MOODS.scan.Scanner(7)
        self.pfm_scanner.set_motifs(pfms[1], bg, thresholds, )
        self.pfm_names = pfms[0]

        return None
    

    def pfm_scan(self,
                 sequence: str):
        """
        PFM scan sequence

        Parameters
        ----------
            sequence : str
                Sequence to scan

        Returns
        -------
            results : Dict[float]
                Dictionary of results
        """

        # Load scanner
        if self.pfm_scanner is None:
            self.load_pfm_scanner()

        # Scan sequence
        results = self.pfm_scanner.scan(sequence)

        # Process results
        pfm_results = {}
        for i, rs in enumerate(results):
            for r in rs:
                try:
                    pfm_results[self.pfm_names[i]]
                    pfm_results[self.pfm_names[i]] = max(pfm_results[self.pfm_names[i]], r.score)
                except KeyError:
                    pfm_results[self.pfm_names[i]] = r.score

        return pfm_results
    

    def get_intervals(self,
                        key: str,
                        upstream: int = 0,
                        downstream: int = 0,
                        filter_column: str = None,
                        filter_selection: str = None,
                        filter_duplicates: bool = True) -> IntervalFrame:
        """
        Get an item from the info file.
        """
        
        # Read intervals
        value = self.info[key]
        if not isinstance(value, IntervalFrame):
            return None
        
        # Filter intervals
        if filter_column is not None:
            if filter_selection is not None:
                chosen = value.df.loc[:,filter_column].values == filter_selection
                value = value.iloc[chosen,:]

        # Add upstream and downstream
        value = adjust_bounds(value,
                                upstream,
                                downstream,
                                filter_duplicates)

        return value


    def calculate_bias(self,
                        intervals: LabeledIntervalArray,
                        include_blacklist: bool = True,
                        include_repeat: bool = True,
                        include_gc: bool = True,
                        include_mappability: bool = True) -> IntervalFrame:
        """
        Calculate bias per interval
        
        Parameters
        ----------
            intervals : LabeledIntervalArray
                Labeled intervals
            include_blacklist : bool
                Flag to include blacklist
            include_repeat : bool
                Flag to include repeat
            include_gc : bool
                Flag to include gc
            include_mappability : bool
                Flag to include mappability

        Returns
        ----------
            bias_record : IntervalFrame
                Bias for given intervals
        """


        # Initialize bias records
        bias_record = IntervalFrame(intervals=intervals)

        # Calculate blacklist
        if include_blacklist:
            blacklist = self["blacklist"]
            bias_record.df.loc[:,"blacklist"] = intervals.percent_coverage(blacklist.index)

        # Calculate repeat
        if include_repeat:
            repeat = self["repeat"]
            bias_record.df.loc[:,"repeat"] = intervals.percent_coverage(repeat.index)

        # Calculate gc
        if include_gc:
            bias_record.df.loc[:,"gc"] = gc_percent(self.seq_file, intervals)

        # Calculate mappability
        if include_mappability:
            mappability = self["mappability"]
            bias_record.df.loc[:,"mappability"] = intervals.percent_coverage(mappability.index)

        return bias_record


    def calculate_bin_bias(self,
                            bin_size: int = 100000,
                            include_blacklist: bool = True,
                            include_repeat: bool = True,
                            include_gc: bool = True,
                            include_mappability: bool = True) -> IntervalFrame:
        """
        Calculate bias per bin
        
        Parameters
        ----------
            bin_size : int
                Size of bins
            include_blacklist : bool
                Flag to include blacklist
            include_repeat : bool
                Flag to include repeat
            include_gc : bool
                Flag to include gc
            include_mappability : bool
                Flag to include mappability

        Returns
        ----------
            bias_record : IntervalFrame
                Bias for given bin size
        """

        # Check previous calculation
        key = "bin_bias_%d" % bin_size
        if key in self.keys:
            return self[key]

        # Initialize bins
        intervals = LabeledIntervalArray.create_bin(self["chrom_sizes"], bin_size=bin_size)

        # Initialize bias records
        bias_record = self.calculate_bias(intervals,
                                            include_blacklist,
                                            include_repeat,
                                            include_gc,
                                            include_mappability)

        return bias_record
    

    def convert_gene_names(self,
                           names: np.ndarray) -> np.ndarray:
        """
        Convert gene names

        Parameters
        ----------
            names : np.ndarray
                Gene names
        
        Returns
        ----------
            converted_names : np.ndarray
                Converted gene names
        """

        # Read gene names
        gene_names = self["gene_names"]

        # Convert gene names
        converted_names = np.array([gene_names[name] for name in names])

        return converted_names