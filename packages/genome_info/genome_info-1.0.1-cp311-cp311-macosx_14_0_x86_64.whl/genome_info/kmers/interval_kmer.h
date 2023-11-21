#ifndef __INTERVAL_KMER_H__
#define __INTERVAL_KMER_H__
#include <stdio.h>
#include <stdlib.h>
#include "2bit.h"
#include "src/labeled_aiarray/labeled_augmented_array.h"


typedef struct{
    char *name;
    int count;
} kmer_t;

typedef struct{
    int max_kmers;
    int n_kmers;
    kmer_t *kmers;
    void *kmer_lookup;
} kmer_count_t;

typedef struct {
    float *A;
    float *T;
    float *G;
    float *C;
    int n_intervals;
    int n_bases;
    int up;
    int down;
} base_freq_t;

typedef struct {
    base_freq_t *start;
    base_freq_t *end;
} interval_base_freq_t;


//-------------------------------------------------------------------------------------
// interval_kmer.c
//=====================================================================================
int chrom_in(char *chrom, char **chrom_list, size_t n_chroms);
char* substr(const char *src, int m, int n);

void interval_base_freq_destroy(interval_base_freq_t *ibf);
interval_base_freq_t *read_interval_base_freq(labeled_aiarray_t *laia, char *fname, int n_bases);

kmer_count_t *kmer_count_init(int kmer);
void kmer_count_destroy(kmer_count_t *kc);
void add_kmer(kmer_count_t *kc, char *kmer_name);
int32_t get_kmer(kmer_count_t *kc, char *kmer);
void append_kmers(kmer_count_t *kc, int kmer, char *seq);
int fetch_kmer(kmer_count_t *kc, char *seq);
kmer_count_t *interval_kmer_count(labeled_aiarray_t *laia, char *fname, int kmer, int last_n);
char *fetch_sequence(char *fname, char *name, int start, int end);
void gc_content(labeled_aiarray_t *laia, char *fname, float gc[]);

#endif