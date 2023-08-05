#!/usr/bin/env python
# -*- coding: utf-8 -*-

__author__ = "Evangelos A. Dimopoulos, Evan K. Irving-Pease"
__copyright__ = "Copyright 2020, University of Oxford"
__email__ = "antonisdim41@gmail.com"
__license__ = "MIT"

from haystac.workflow.scripts.utilities import get_total_paths, PE


def get_bams_for_ts_tv_count(wildcards):
    sample, orgname, accession = wildcards.sample, wildcards.orgname, wildcards.accession
    if config["read_mode"] == PE:
        return config["analysis_output_dir"] + f"/alignments/{sample}/PE/{orgname}/{orgname}_{accession}.bam"
    else:
        return (
            config["analysis_output_dir"]
            + f"/alignments/{sample}/{config['read_mode']}/{orgname}/{orgname}_{accession}.bam"
        )


rule count_accession_ts_tv:
    input:
        get_bams_for_ts_tv_count,
    output:
        temp(config["analysis_output_dir"] + "/ts_tv_counts/{sample}/{orgname}_count_{accession}.csv"),
    params:
        pairs=config["read_mode"] == PE,
    message:
        "Counting the number of transitions and transversions per read for taxon {wildcards.orgname}."
    script:
        "../scripts/count_accession_ts_tv.py"


def get_counts(_):
    """Get ts and tv count file paths"""
    return [
        config["analysis_output_dir"] + "/ts_tv_counts/{sample}/" + f"{orgname}_count_{accession}.csv"
        for orgname, accession in get_total_paths(checkpoints, config)
    ]


rule initial_ts_tv:
    input:
        get_counts,
    output:
        config["analysis_output_dir"] + "/ts_tv_counts/{sample}/all_ts_tv_counts.csv",
    log:
        config["analysis_output_dir"] + "/ts_tv_counts/{sample}/all_ts_tv_counts.log",
    message:
        "Concatenating all the Ts and Tv count files for sample {wildcards.sample}."
    script:
        "../scripts/concat_files.py"


def get_right_readlen(wildcards):
    if config["read_mode"] == PE:
        return config["analysis_output_dir"] + f"/fastq/PE/{wildcards.sample}_mapq_pair.readlen"
    else:
        return config["analysis_output_dir"] + f"/fastq/{config['read_mode']}/{wildcards.sample}_mapq.readlen"


rule calculate_likelihoods:
    input:
        config["analysis_output_dir"] + "/ts_tv_counts/{sample}/all_ts_tv_counts.csv",
        get_right_readlen,
        get_counts,
    output:
        config["analysis_output_dir"] + "/probabilities/{sample}/{sample}_likelihood_ts_tv_matrix.csv",
        config["analysis_output_dir"] + "/probabilities/{sample}/{sample}_probability_model_params.json",
    log:
        config["analysis_output_dir"] + "/probabilities/{sample}/{sample}_likelihood_ts_tv_matrix.log",
    message:
        "Calculating the likelihoods and performing the Dirichlet assignment of the reads in sample "
        "{wildcards.sample} to the taxa in our database."
    script:
        "../scripts/calculate_likelihoods.py"


rule calculate_taxa_probabilities:
    input:
        config["analysis_output_dir"] + "/probabilities/{sample}/{sample}_likelihood_ts_tv_matrix.csv",
        config["analysis_output_dir"] + "/probabilities/{sample}/{sample}_probability_model_params.json",
        config["sample_output_dir"] + "/fastq_inputs/meta/{sample}.size",
    output:
        config["analysis_output_dir"] + "/probabilities/{sample}/{sample}_posterior_probabilities.tsv",
    log:
        config["analysis_output_dir"] + "/probabilities/{sample}/{sample}_posterior_probabilities.log",
    message:
        "Calculating the taxonomic assignment posterior probabilities for sample {wildcards.sample}."
    script:
        "../scripts/calculate_taxa_probabilities.py"


rule coverage_counts:
    input:
        config["analysis_output_dir"] + "/alignments/{sample}/{reads}/{orgname}/{orgname}_{accession}.bam",
    output:
        temp(config["analysis_output_dir"] + "/probabilities/{sample}/{orgname}_cov_count_{accession}_{reads}.txt"),
    message:
        "Counting coverage stats for sample {wildcards.sample} and taxon {wildcards.orgname}."
    conda:
        "../envs/samtools.yaml"
    shell:
        "(samtools mpileup {input} | "
        " awk 'NR>1 {{rows++; sum += $4}} END {{print rows, sum}}' OFS='\t'"
        ") 1> {output} 2> /dev/null"


rule coverage_chi2_contingency_test:
    input:
        config["analysis_output_dir"] + "/probabilities/{sample}/{orgname}_cov_count_{accession}_{reads}.txt",
        config["cache"] + "/ncbi/{orgname}/{accession}.fasta.gz.fai",
    output:
        temp(
            config["analysis_output_dir"] + "/probabilities/{sample}/{orgname}_chi2_test_pvalue_{accession}_{reads}.txt"
        ),
    message:
        "Performing a chi-squared contingency test to assess if reads from sample {wildcards.sample} "
        "represent a random genome sample of taxon {wildcards.orgname}."
    script:
        "../scripts/coverage_chi2_contingency_test.py"


def get_p_values(_):
    """Get p value file paths"""
    return [
        config["analysis_output_dir"]
        + "/probabilities/{sample}/"
        + f"{orgname}_chi2_test_pvalue_{accession}_"
        + config["read_mode"]
        + ".txt"
        for orgname, accession in get_total_paths(checkpoints, config)
    ]


rule cat_pvalues:
    input:
        get_p_values,
    output:
        config["analysis_output_dir"] + "/probabilities/{sample}/{sample}_chi2_test_pvalues.tsv",
    log:
        config["analysis_output_dir"] + "/probabilities/{sample}/{sample}_chi2_test_pvalues.log",
    message:
        "Concatenating all the chi-squared contingency test p-value outputs for sample {wildcards.sample}."
    script:
        "../scripts/concat_files.py"


rule calculate_dirichlet_abundances:
    input:
        config["analysis_output_dir"] + "/probabilities/{sample}/{sample}_likelihood_ts_tv_matrix.csv",
        config["analysis_output_dir"] + "/probabilities/{sample}/{sample}_chi2_test_pvalues.tsv",
        config["sample_output_dir"] + "/fastq_inputs/meta/{sample}.size",
    output:
        config["analysis_output_dir"] + "/probabilities/{sample}/{sample}_posterior_abundance.tsv",
    log:
        config["analysis_output_dir"] + "/probabilities/{sample}/{sample}_posterior_abundance.log",
    message:
        "Calculating the mean posterior abundance for sample {wildcards.sample}."
    script:
        "../scripts/calculate_dirichlet_abundances.py"
