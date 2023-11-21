#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include "2bit.h"
#include "src/labeled_aiarray/labeled_augmented_array.h"
#include "interval_kmer.h"


int chrom_in(char *chrom, char **chrom_list, size_t n_chroms)
{   
    size_t x;
    for (x = 0; x < n_chroms; x++)
    {
         if (strcmp(chrom, chrom_list[x]) == 0)
         {
             return 1;
         }
    }
    return 0;
}


char* substr(const char *src, int m, int n)
{
    // get the length of the destination string
    int len = n - m;
 
    // allocate (len + 1) chars for destination (+1 for extra null character)
    char *dest = (char*)malloc(sizeof(char) * (len + 1));
 
    // extracts characters between m'th and n'th index from source string
    // and copy them into the destination string
    int i;
    for (i = m; i < n && (*(src + i) != '\0'); i++)
    {
        *dest = *(src + i);
        dest++;
    }
 
    // null-terminate the destination string
    *dest = '\0';
 
    // return the destination string
    return dest - len;
}


base_freq_t *base_freq_init(int n_bases)
{
    // Reserve memory
    base_freq_t *bf = malloc(1 * sizeof(base_freq_t));

    bf->A = calloc(n_bases, sizeof(float));
    bf->T = calloc(n_bases, sizeof(float));
    bf->G = calloc(n_bases, sizeof(float));
    bf->C = calloc(n_bases, sizeof(float));
    bf->n_intervals = 0;
    bf->n_bases = n_bases;

    bf->up = (int)(n_bases / 2);
    bf->down = n_bases - bf->up;

    return bf;
}


void base_freq_destroy(base_freq_t *bf)
{
    if (bf == 0) 
    {
        return;
    }

    free(bf->A);
    free(bf->T);
    free(bf->G);
    free(bf->C);

    free(bf);
}


void base_freq_add(base_freq_t *bf, char *seq)
{
    int i;
    for (i = 0; i < bf->n_bases; i++)
    {
        if (*(seq + i) == 'A' || *(seq + i) == 'a')
        {
            bf->A[i] = bf->A[i] + 1;
        }
        else if (*(seq + i) == 'T' || *(seq + i) == 't')
        {
            bf->T[i] = bf->T[i] + 1;
        }
        else if (*(seq + i) == 'G' || *(seq + i) == 'g')
        {
            bf->G[i] = bf->G[i] + 1;
        }
        else if (*(seq + i) == 'C' || *(seq + i) == 'c')
        {
            bf->C[i] = bf->C[i] + 1;
        }
    }

    bf->n_intervals++;

    return;
}


void base_freq_normalize(base_freq_t *bf)
{
    float sum = 0;
    int i;
    for (i = 0; i < bf->n_bases; i++)
    {
        sum = bf->A[i] + bf->T[i] + bf->G[i] + bf->C[i];
        if (sum == 0)
        {
            continue;
        }

        bf->A[i] = bf->A[i] / sum;
        bf->T[i] = bf->T[i] / sum;
        bf->G[i] = bf->G[i] / sum;
        bf->C[i] = bf->C[i] / sum;
    }

    return;
}


interval_base_freq_t *interval_base_freq_init(int n_intervals, int n_bases)
{
    // Reserve memory
    interval_base_freq_t *ibf = malloc(1 * sizeof(interval_base_freq_t));

    ibf->start = base_freq_init(n_bases);
    ibf->end = base_freq_init(n_bases);

    return ibf;
}


void interval_base_freq_destroy(interval_base_freq_t *ibf)
{
    if (ibf == 0) 
    {
        return;
    }

    base_freq_destroy(ibf->start);
    base_freq_destroy(ibf->end);

    free(ibf);
}


void interval_base_freq_add(interval_base_freq_t *ibf, TwoBit *tb, char *name, uint32_t start, uint32_t end)
{
    char *start_seq = twobitSequence(tb, name, start - ibf->start->up, start + ibf->start->down);
    char *end_seq = twobitSequence(tb, name, end - ibf->end->up, end + ibf->end->down);

    base_freq_add(ibf->start, start_seq);
    base_freq_add(ibf->end, end_seq);

    free(start_seq);
    free(end_seq);

    return;
}


void interval_base_freq_normalize(interval_base_freq_t *ibf)
{
    base_freq_normalize(ibf->start);
    base_freq_normalize(ibf->end);

    return;
}


interval_base_freq_t *read_interval_base_freq(labeled_aiarray_t *laia, char *fname, int n_bases)
{
    // Open 2bit file
    TwoBit *tb = twobitOpen(fname, 0);
    interval_base_freq_t *ibf = interval_base_freq_init(laia->n_labels, n_bases);
    
    int t;
    for (t = 0; t < laia->n_labels; t++)
    {
        label_t *p = &laia->labels[t];
        char *name = p->name;
        uint32_t chrom_len = twobitChromLen(tb, name);

        // Check if chromosome is in the 2bit file
        if (chrom_in(name, tb->cl->chrom, tb->hdr->nChroms) == 0)
        {
            continue;
        }

        int i;
        for (i = 0; i < p->ail->nr; i++)
        {
            if (p->ail->interval_list[i].start > n_bases && p->ail->interval_list[i].end < (chrom_len - n_bases))
            {
                interval_base_freq_add(ibf, tb, name, p->ail->interval_list[i].start, p->ail->interval_list[i].end);
            }
        }

    }

    // Close 2bit file
    twobitClose(tb);

    interval_base_freq_normalize(ibf);

    return ibf;
}


kmer_count_t *kmer_count_init(int kmer)
{
    // Reserve memory
    kmer_count_t *kc = malloc(1 * sizeof(kmer_count_t));

    kc->max_kmers = 64;
    kc->kmers = malloc(kc->max_kmers * sizeof(kmer_t));
    kc->n_kmers = 0;
    kc->kmer_lookup = kh_init(khStrInt);

    return kc;

}

void kmer_count_destroy(kmer_count_t *kc)
{
    int32_t i;
	if (kc == 0) 
    {
        return;
    }

	for (i = 0; i < kc->n_kmers; ++i)
    {
		free((char*)kc->kmers[i].name);
	}
	free(kc->kmers);
	kh_destroy(khStrInt, (strhash_t*)kc->kmer_lookup);

	free(kc);
}


void add_kmer(kmer_count_t *kc, char *kmer_name)
{
    khiter_t k;
	strhash_t *h = (strhash_t*)kc->kmer_lookup;

	k = kh_get(khStrInt, h, kmer_name);
	if (k == kh_end(h))
    {
        if (kc->n_kmers == kc->max_kmers)
        {
			EXPAND(kc->kmers, kc->max_kmers);
        }

        // Add label_name to label_map
        int ret_name = kh_name_set(khStrInt, h, kmer_name, kc->n_kmers);
        kc->n_kmers++;

        // Determine label code
		uint32_t t = kh_value(h, k);

		kmer_t *p = &kc->kmers[t];
		p->name = strdup(kmer_name);
		p->count = 0;
    }

    // Determine label code
	uint32_t t = kh_value(h, k);
    kmer_t *p = &kc->kmers[t];
    p->count++;

    return;
}


int32_t get_kmer(kmer_count_t *kc, char *kmer)
{   /* Return index for given label */
	
    khint_t k;
	strhash_t *h = (strhash_t*)kc->kmer_lookup;
	k = kh_get(khStrInt, h, kmer);
    
	return k == kh_end(h)? -1 : kh_val(h, k);
}


void append_kmers(kmer_count_t *kc, int kmer, char *seq)
{
    int seq_length = strlen(seq);
    int i;
    for (i = 0; i <= seq_length - kmer; i++)
    {
        char *kmer_seq = substr(seq, i, i+kmer);
        //printf("i: %d seq_length: %d kmer: %s\n", i, seq_length, kmer_seq);
        add_kmer(kc, kmer_seq);
        free(kmer_seq);
    }

    return;
}


int fetch_kmer(kmer_count_t *kc, char *seq)
{
    uint32_t t = get_kmer(kc, seq);

    int count = 0;
    if (t >= 0)
    {
        count = kc->kmers[t].count;
    }
    
    return count;
}


kmer_count_t *interval_kmer_count(labeled_aiarray_t *laia, char *fname, int kmer, int last_n)
{
    kmer_count_t *kc = kmer_count_init(kmer);
    TwoBit *tb = twobitOpen(fname, 0);
    
    int t;
    for (t = 0; t < laia->n_labels; t++)
    {
        label_t *p = &laia->labels[t];
        char *name = p->name;

        // Check if chromosome is in the 2bit file
        if (chrom_in(name, tb->cl->chrom, tb->hdr->nChroms) == 0)
        {
            continue;
        }

        int i;
        if (last_n == 0)
        {
            for (i = 0; i < p->ail->nr; i++)
            {
                char *seq = twobitSequence(tb, name, p->ail->interval_list[i].start, p->ail->interval_list[i].end);
                append_kmers(kc, kmer, seq);
                free(seq);
            }
        }
        else {
            for (i = 0; i < p->ail->nr; i++)
            {
                if ((p->ail->interval_list[i].end - p->ail->interval_list[i].start) < last_n)
                {
                    continue;
                }

                char *seq = twobitSequence(tb, name, p->ail->interval_list[i].end - last_n, p->ail->interval_list[i].end);
                append_kmers(kc, kmer, seq);
                free(seq);
            }
        }
    }

    // Close 2bit file
    twobitClose(tb);

    return kc;
}


char *fetch_sequence(char *fname, char *name, int start, int end)
{
    // Open 2bit file
    TwoBit *tb = twobitOpen(fname, 0);

    // Fetch sequence
    char *seq = twobitSequence(tb, name, start, end);

    // Close 2bit file
    twobitClose(tb);

    return seq;
}


void gc_content(labeled_aiarray_t *laia, char *fname, float gc[])
{
    TwoBit *tb = twobitOpen(fname, 0);

    labeled_aiarray_iter_t *iter = labeled_aiarray_iter_init(laia);
    while (labeled_aiarray_iter_next(iter) == 1)
    {
        // Check if chromosome is in the 2bit file
        char const *name = iter->intv->name;
        if (chrom_in(name, tb->cl->chrom, tb->hdr->nChroms) == 0)
        {
            continue;
        }

        // Check if interval is within chromosome length
        if (iter->intv->i->end > twobitChromLen(tb, name))
        {
            continue;
        }

        // Fetch sequence
        char *seq = twobitSequence(tb, name, iter->intv->i->start, iter->intv->i->end);
        int seq_length = strlen(seq);

        // Calculate GC content
        int i;
        for (i = 0; i <= seq_length - 1; i++)
        {
            if (*(seq + i) == 'G' || *(seq + i) == 'C' || *(seq + i) == 'g' || *(seq + i) == 'c')
            {
                gc[iter->n] = gc[iter->n] + 1;
            }
        }
        
        // Free sequence
        free(seq);

        // Normalize GC content
        gc[iter->n] = gc[iter->n] / (float)seq_length;
    }

    // Close 2bit file
    twobitClose(tb);
    labeled_aiarray_iter_destroy(iter);

    return;
}