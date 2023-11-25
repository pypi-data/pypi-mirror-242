import json
import logging

from enum import Enum
from pathlib import Path
from typing import Literal

import defopt

from hostile import lib


class ALIGNER(Enum):
    """Provides auto enum for CLI, not to be confused with lib.ALIGNER"""

    bowtie2 = "bowtie2"
    minimap2 = "minimap2"
    auto = "auto"


def clean(
    *,
    fastq1: Path,
    fastq2: Path | None = None,
    aligner: ALIGNER = ALIGNER.auto,
    index: Path | None = None,
    rename: bool = False,
    reorder: bool = False,
    out_dir: Path = lib.CWD,
    threads: int = lib.THREADS,
    aligner_args: str = "",
    force: bool = False,
    debug: bool = False,
) -> None:
    """
    Remove reads aligning to a target genome from fastq[.gz] input files

    :arg fastq1: path to forward fastq.gz] file
    :arg fastq2: optional path to reverse fastq[.gz] file
    :arg aligner: alignment algorithm. Use Bowtie2 for short reads and Minimap2 for long reads
    :arg index: path to custom genome or index. For Bowtie2, exclude the .1.bt2 suffix
    :arg rename: replace read names with incrementing integers
    :arg reorder: ensure deterministic output order
    :arg out_dir: path to output directory
    :arg threads: number of alignment threads. A sensible default is chosen automatically
    :arg aligner_args: additional arguments for alignment
    :arg force: overwrite existing output files
    :arg debug: show debug messages
    """

    if debug:
        logging.getLogger().setLevel(logging.DEBUG)
    aligner_paired = (
        lib.ALIGNER.bowtie2
        if aligner == ALIGNER.auto or aligner == ALIGNER.bowtie2
        else lib.ALIGNER.minimap2
    )
    aligner_unpaired = (
        lib.ALIGNER.minimap2
        if aligner == ALIGNER.auto or aligner == ALIGNER.minimap2
        else lib.ALIGNER.bowtie2
    )
    if fastq2:
        stats = lib.clean_paired_fastqs(
            [(fastq1, fastq2)],
            index=index,
            rename=rename,
            reorder=reorder,
            out_dir=out_dir,
            aligner=aligner_paired,
            aligner_args=aligner_args,
            threads=threads,
            force=force,
        )
    else:
        stats = lib.clean_fastqs(
            [fastq1],
            index=index,
            rename=rename,
            reorder=reorder,
            out_dir=out_dir,
            aligner=aligner_unpaired,
            aligner_args=aligner_args,
            threads=threads,
            force=force,
        )
    print(json.dumps(stats, indent=4))


def mask(
    reference: Path, target: Path, out_dir: Path = Path("masked"), threads: int = 1
) -> None:
    """
    Mask reference genome against target genome(s)

    :arg reference: path to reference genome in fasta(.gz) format
    :arg target: path to target genome(s) in fasta(.gz) format
    :arg out_dir: path to output directory
    :arg threads: number of threads to use
    """
    lib.mask(reference=reference, target=target, out_dir=out_dir, threads=threads)


def fetch(
    filename: str = "",
    aligner: Literal["minimap2", "bowtie2", "both"] = "both",
    list_available: bool = False,
) -> None:
    """
    Download reference genomes (Minimap2) and/or indexes (Bowtie2). Run without
    arguments to fetch defaults

    :arg filename: filename of reference to download
    :arg aligner: aligner(s) for which to download the default reference
    :arg list_available: show a list of available reference filenames
    """
    if list_available:
        filenames = lib.list_references()
        default_filenames = lib.get_default_reference_filenames()
        for filename in filenames:
            filename_fmt = filename
            if filename.endswith(".fa.gz"):
                filename_fmt += "  (Minimap2"
            elif filename.endswith(".tar"):
                filename_fmt += "  (Bowtie2"
            if filename in default_filenames:
                filename_fmt += "; DEFAULT)"
            else:
                filename_fmt += ")"
            print(filename_fmt)
    elif filename:
        lib.fetch_reference(filename)
    else:
        if aligner == "minimap2" or aligner == "both":
            lib.ALIGNER.minimap2.value.fetch_default_index()
        if aligner == "bowtie2" or aligner == "both":
            lib.ALIGNER.bowtie2.value.fetch_default_index()


def main():
    defopt.run(
        {"clean": clean, "mask": mask, "fetch": fetch},
        no_negated_flags=True,
        strict_kwonly=False,
        short={},
    )


# def clean_many(
#     *fastqs: str,
#     aligner: lib.ALIGNER = lib.ALIGNER.bowtie2,
#     index: Path | None = None,
#     out_dir: Path = lib.CWD,
#     threads: int = lib.THREADS,
#     debug: bool = False,
# ) -> None:
#     """
#     Remove human reads from comma-separated pairs of fastq(.gz) files

#     :arg fastqs: path to fastq(.gz) or bam file(s). Paired fastq paths should be comma-separated, e.g. reads_1.fastq.gz,reads_2.fastq.gz
#     :arg aligner: alignment algorithm
#     :arg index: path to custom genome or index. For Bowtie2, provide an index path without the .bt2 extension
#     :arg out_dir: path to output directory
#     :arg threads: number of threads to use
#     :arg debug: show debug messages
#     """
#     if "," in fastqs[0]:  # Paired fastq
#         paired_fastqs = [tuple(pair.split(",")) for pair in fastqs]
#         paired_fastqs = [tuple([Path(fq1), Path(fq2)]) for fq1, fq2 in paired_fastqs]
#         stats = lib.clean_paired_fastqs(
#             paired_fastqs,
#             out_dir=out_dir,
#             threads=threads,
#             aligner=aligner,
#             index=index,
#         )
#         print(json.dumps(stats, indent=4))
#     else:
#         raise NotImplementedError(
#             "Forward and reverse fastq(.gz) paths should be separated with a comma"
#         )
