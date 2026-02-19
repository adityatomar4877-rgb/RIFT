import io
import vcf as pyvcf  # PyVCF3 — pure Python, works on Windows/Mac/Linux
from typing import List, Dict, Tuple

TARGET_GENES = {"CYP2D6", "CYP2C19", "CYP2C9", "SLCO1B1", "TPMT", "DPYD"}


def parse_vcf(content: str) -> List[Dict]:
    """
    Industry-grade VCF parsing using PyVCF3.
    Pure Python — works on Windows, Mac, Linux with no C dependencies.
    Handles VCF v4.1/4.2, multiallelic sites, missing fields gracefully.
    """
    variants = []

    # Normalize line endings (handles Windows \r\n)
    content = content.replace("\r\n", "\n").replace("\r", "\n")

    # Remove inline ## comment lines that appear AFTER the #CHROM header.
    # PyVCF3 only expects ## meta-lines before #CHROM; any ## lines after it
    # are treated as malformed data rows and cause "list index out of range".
    cleaned_lines = []
    past_chrom_header = False
    for line in content.splitlines():
        if line.startswith("#CHROM"):
            past_chrom_header = True
        if past_chrom_header and line.startswith("##"):
            continue  # drop inline block comments
        cleaned_lines.append(line)
    content = "\n".join(cleaned_lines)

    vcf_reader = pyvcf.Reader(fsock=io.StringIO(content))

    if not vcf_reader.samples:
        raise ValueError("VCF file has no sample data")

    for record in vcf_reader:
        gene = _get_info_str(record, "GENE")

        if gene not in TARGET_GENES:
            continue

        alt_alleles = [str(a) for a in record.ALT if a is not None]

        for sample in record.samples:
            gt_data = sample.data
            gt_str = getattr(gt_data, "GT", None)
            if gt_str is None or gt_str in ("./.", ".|."):
                continue

            phased = "|" in gt_str

            variants.append({
                "rsid":                  record.ID or ".",
                "gene":                  gene,
                "chrom":                 record.CHROM,
                "pos":                   int(record.POS),
                "ref":                   str(record.REF),
                "alt":                   ",".join(alt_alleles),
                "qual":                  float(record.QUAL) if record.QUAL is not None else None,
                "filter":                _get_filter(record),
                "genotype":              gt_str,
                "phased":                phased,
                "star_allele":           _get_info_str(record, "STAR"),
                "clinical_significance": _get_info_str(record, "CLINSIG", "Unknown"),
                "allele_freq":           _get_info_float(record, "AF"),
                "depth":                 _get_info_int(record, "DP"),
                "sample":                sample.sample,
            })

    return variants


def _get_info_str(record, key: str, default=None):
    try:
        val = record.INFO.get(key)
        if val is None:
            return default
        if isinstance(val, list):
            val = val[0]
        return str(val).strip() if val is not None else default
    except Exception:
        return default


def _get_info_float(record, key: str, default: float = 0.0) -> float:
    try:
        val = record.INFO.get(key)
        if val is None:
            return default
        if isinstance(val, list):
            val = val[0]
        return float(val)
    except (TypeError, ValueError):
        return default


def _get_info_int(record, key: str, default: int = 0) -> int:
    try:
        val = record.INFO.get(key)
        if val is None:
            return default
        if isinstance(val, list):
            val = val[0]
        return int(val)
    except (TypeError, ValueError):
        return default


def _get_filter(record) -> str:
    try:
        if not record.FILTER:
            return "PASS"
        return ",".join(record.FILTER)
    except Exception:
        return "UNKNOWN"


def get_gene_coverage(variants: List[Dict]) -> List[str]:
    return list(set(v["gene"] for v in variants))


def validate_vcf_content(content: str) -> Tuple[bool, str]:
    if not content.strip():
        return False, "File is empty"
    if "##fileformat=VCF" not in content[:500]:
        return False, "Not a valid VCF file (missing ##fileformat header)"
    has_chrom = any(line.startswith("#CHROM") for line in content.splitlines()[:50])
    if not has_chrom:
        return False, "Missing #CHROM header line"
    return True, ""