#cython: embedsignature=True
#cython: profile=False

import numpy as np
cimport numpy as np

from libc.stdint cimport uint32_t, int32_t, int64_t, uint16_t
from ailist.LabeledIntervalArray_core cimport LabeledIntervalArray, labeled_aiarray_t
from ..genomes.genomes import InfoReader


cdef kmer_count_t *_read_kmers(char *fname, labeled_aiarray_t *laia, int k, int last_n):
    cdef kmer_count_t *kc = interval_kmer_count(laia, fname, k, last_n)

    return kc


def read_kmers(str seq_fn, LabeledIntervalArray laia, int k, int last_n = 0):

    cdef str twobit_name = seq_fn
    cdef bytes fname = twobit_name.encode()
    cdef kmer_count_t *kc = _read_kmers(fname, laia.laia, k, last_n)

    result = {}
    cdef bytes kmer_seq
    cdef int count
    cdef uint32_t t
    for t in range(kc.n_kmers):
        kmer_seq = kc.kmers[t].name
        count = fetch_kmer(kc, kmer_seq)

        result[kmer_seq.decode()] = count

    # Delete
    kmer_count_destroy(kc)

    return result


cdef bytes _fetch_sequence(char *fname, char *name, int start, int end):
    cdef bytes seq = fetch_sequence(fname, name, start, end)

    return seq

def read_sequence(str seq_fn, str chrom, int start, int end):

    cdef str twobit_name = seq_fn
    cdef bytes fname = twobit_name.encode()
    cdef bytes name = chrom.encode()

    cdef bytes seq = _fetch_sequence(fname, name, start, end)
    cdef str py_seq = seq.decode()

    return py_seq


cdef void _gc_percent(char *fname, labeled_aiarray_t *laia, float[::1] gc):
    gc_content(laia, fname, &gc[0])

    return


def gc_percent(str seq_fn, LabeledIntervalArray laia, str genome_version = "hg38"):
    cdef str twobit_name = seq_fn
    cdef bytes fname = twobit_name.encode()

    cdef np.ndarray gc = np.zeros(laia.size, dtype=np.single)
    cdef float[::1] gc_mem = gc

    _gc_percent(fname, laia.laia, gc_mem)

    return gc


def read_bounds_base_freq(str seq_fn, LabeledIntervalArray laia, int n_bases):

    cdef str twobit_name = seq_fn
    cdef bytes fname = twobit_name.encode()

    cdef np.ndarray start_freq = np.zeros((4, n_bases), dtype=float)
    cdef np.ndarray end_freq = np.zeros((4, n_bases), dtype=float)
    cdef interval_base_freq_t *ibf = read_interval_base_freq(laia.laia, fname, n_bases)
    cdef int i
    for i in range(n_bases):
        start_freq[0, i] = ibf.start.A[i]
        start_freq[1, i] = ibf.start.T[i]
        start_freq[2, i] = ibf.start.G[i]
        start_freq[3, i] = ibf.start.C[i]
        end_freq[0, i] = ibf.end.A[i]
        end_freq[1, i] = ibf.end.T[i]
        end_freq[2, i] = ibf.end.G[i]
        end_freq[3, i] = ibf.end.C[i]

    interval_base_freq_destroy(ibf)

    return start_freq, end_freq

    