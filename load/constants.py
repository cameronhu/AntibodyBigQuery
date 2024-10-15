from google.cloud import bigquery

DATASET_ID = "AIRR"
GCP_PROJECT_ID = "profluent-evo"

AUTHENTICATION_PATH = (
    "/home/cameronhu/.config/gcloud/application_default_credentials.json"
)

SCOPES = ["https://www.googleapis.com/auth/bigquery"]

SEQUENCE_SCHEMA = [
    bigquery.SchemaField("sequence", "STRING", "REQUIRED", None, None, (), None),
    bigquery.SchemaField("locus", "STRING", "NULLABLE", None, None, (), None),
    bigquery.SchemaField("stop_codon", "STRING", "NULLABLE", None, None, (), None),
    bigquery.SchemaField("vj_in_frame", "STRING", "NULLABLE", None, None, (), None),
    bigquery.SchemaField("v_frameshift", "STRING", "NULLABLE", None, None, (), None),
    bigquery.SchemaField("productive", "STRING", "NULLABLE", None, None, (), None),
    bigquery.SchemaField("rev_comp", "STRING", "NULLABLE", None, None, (), None),
    bigquery.SchemaField("complete_vdj", "STRING", "NULLABLE", None, None, (), None),
    bigquery.SchemaField("v_call", "STRING", "NULLABLE", None, None, (), None),
    bigquery.SchemaField("d_call", "STRING", "NULLABLE", None, None, (), None),
    bigquery.SchemaField("j_call", "STRING", "NULLABLE", None, None, (), None),
    bigquery.SchemaField(
        "sequence_alignment", "STRING", "NULLABLE", None, None, (), None
    ),
    bigquery.SchemaField(
        "germline_alignment", "STRING", "NULLABLE", None, None, (), None
    ),
    bigquery.SchemaField(
        "sequence_alignment_aa", "STRING", "NULLABLE", None, None, (), None
    ),
    bigquery.SchemaField(
        "germline_alignment_aa", "STRING", "NULLABLE", None, None, (), None
    ),
    bigquery.SchemaField(
        "v_alignment_start", "INTEGER", "NULLABLE", None, None, (), None
    ),
    bigquery.SchemaField(
        "v_alignment_end", "INTEGER", "NULLABLE", None, None, (), None
    ),
    bigquery.SchemaField(
        "d_alignment_start", "FLOAT", "NULLABLE", None, None, (), None
    ),
    bigquery.SchemaField("d_alignment_end", "FLOAT", "NULLABLE", None, None, (), None),
    bigquery.SchemaField(
        "j_alignment_start", "INTEGER", "NULLABLE", None, None, (), None
    ),
    bigquery.SchemaField(
        "j_alignment_end", "INTEGER", "NULLABLE", None, None, (), None
    ),
    bigquery.SchemaField(
        "v_sequence_alignment", "STRING", "NULLABLE", None, None, (), None
    ),
    bigquery.SchemaField(
        "v_sequence_alignment_aa", "STRING", "NULLABLE", None, None, (), None
    ),
    bigquery.SchemaField(
        "v_germline_alignment", "STRING", "NULLABLE", None, None, (), None
    ),
    bigquery.SchemaField(
        "v_germline_alignment_aa", "STRING", "NULLABLE", None, None, (), None
    ),
    bigquery.SchemaField(
        "d_sequence_alignment", "STRING", "NULLABLE", None, None, (), None
    ),
    bigquery.SchemaField(
        "d_sequence_alignment_aa", "STRING", "NULLABLE", None, None, (), None
    ),
    bigquery.SchemaField(
        "d_germline_alignment", "STRING", "NULLABLE", None, None, (), None
    ),
    bigquery.SchemaField(
        "d_germline_alignment_aa", "STRING", "NULLABLE", None, None, (), None
    ),
    bigquery.SchemaField(
        "j_sequence_alignment", "STRING", "NULLABLE", None, None, (), None
    ),
    bigquery.SchemaField(
        "j_sequence_alignment_aa", "STRING", "NULLABLE", None, None, (), None
    ),
    bigquery.SchemaField(
        "j_germline_alignment", "STRING", "NULLABLE", None, None, (), None
    ),
    bigquery.SchemaField(
        "j_germline_alignment_aa", "STRING", "NULLABLE", None, None, (), None
    ),
    bigquery.SchemaField("fwr1", "STRING", "NULLABLE", None, None, (), None),
    bigquery.SchemaField("fwr1_aa", "STRING", "NULLABLE", None, None, (), None),
    bigquery.SchemaField("cdr1", "STRING", "NULLABLE", None, None, (), None),
    bigquery.SchemaField("cdr1_aa", "STRING", "NULLABLE", None, None, (), None),
    bigquery.SchemaField("fwr2", "STRING", "NULLABLE", None, None, (), None),
    bigquery.SchemaField("fwr2_aa", "STRING", "NULLABLE", None, None, (), None),
    bigquery.SchemaField("cdr2", "STRING", "NULLABLE", None, None, (), None),
    bigquery.SchemaField("cdr2_aa", "STRING", "NULLABLE", None, None, (), None),
    bigquery.SchemaField("fwr3", "STRING", "NULLABLE", None, None, (), None),
    bigquery.SchemaField("fwr3_aa", "STRING", "NULLABLE", None, None, (), None),
    bigquery.SchemaField("fwr4", "STRING", "NULLABLE", None, None, (), None),
    bigquery.SchemaField("fwr4_aa", "STRING", "NULLABLE", None, None, (), None),
    bigquery.SchemaField("cdr3", "STRING", "NULLABLE", None, None, (), None),
    bigquery.SchemaField("cdr3_aa", "STRING", "NULLABLE", None, None, (), None),
    bigquery.SchemaField("junction", "STRING", "NULLABLE", None, None, (), None),
    bigquery.SchemaField("junction_length", "FLOAT", "NULLABLE", None, None, (), None),
    bigquery.SchemaField("junction_aa", "STRING", "NULLABLE", None, None, (), None),
    bigquery.SchemaField(
        "junction_aa_length", "FLOAT", "NULLABLE", None, None, (), None
    ),
    bigquery.SchemaField("v_score", "FLOAT", "NULLABLE", None, None, (), None),
    bigquery.SchemaField("d_score", "FLOAT", "NULLABLE", None, None, (), None),
    bigquery.SchemaField("j_score", "FLOAT", "NULLABLE", None, None, (), None),
    bigquery.SchemaField("v_cigar", "STRING", "NULLABLE", None, None, (), None),
    bigquery.SchemaField("d_cigar", "STRING", "NULLABLE", None, None, (), None),
    bigquery.SchemaField("j_cigar", "STRING", "NULLABLE", None, None, (), None),
    bigquery.SchemaField("v_support", "FLOAT", "NULLABLE", None, None, (), None),
    bigquery.SchemaField("d_support", "FLOAT", "NULLABLE", None, None, (), None),
    bigquery.SchemaField("j_support", "FLOAT", "NULLABLE", None, None, (), None),
    bigquery.SchemaField("v_identity", "FLOAT", "NULLABLE", None, None, (), None),
    bigquery.SchemaField("d_identity", "FLOAT", "NULLABLE", None, None, (), None),
    bigquery.SchemaField("j_identity", "FLOAT", "NULLABLE", None, None, (), None),
    bigquery.SchemaField(
        "v_sequence_start", "INTEGER", "NULLABLE", None, None, (), None
    ),
    bigquery.SchemaField("v_sequence_end", "INTEGER", "NULLABLE", None, None, (), None),
    bigquery.SchemaField(
        "v_germline_start", "INTEGER", "NULLABLE", None, None, (), None
    ),
    bigquery.SchemaField("v_germline_end", "INTEGER", "NULLABLE", None, None, (), None),
    bigquery.SchemaField("d_sequence_start", "FLOAT", "NULLABLE", None, None, (), None),
    bigquery.SchemaField("d_sequence_end", "FLOAT", "NULLABLE", None, None, (), None),
    bigquery.SchemaField("d_germline_start", "FLOAT", "NULLABLE", None, None, (), None),
    bigquery.SchemaField("d_germline_end", "FLOAT", "NULLABLE", None, None, (), None),
    bigquery.SchemaField(
        "j_sequence_start", "INTEGER", "NULLABLE", None, None, (), None
    ),
    bigquery.SchemaField("j_sequence_end", "INTEGER", "NULLABLE", None, None, (), None),
    bigquery.SchemaField(
        "j_germline_start", "INTEGER", "NULLABLE", None, None, (), None
    ),
    bigquery.SchemaField("j_germline_end", "INTEGER", "NULLABLE", None, None, (), None),
    bigquery.SchemaField("fwr1_start", "INTEGER", "NULLABLE", None, None, (), None),
    bigquery.SchemaField("fwr1_end", "INTEGER", "NULLABLE", None, None, (), None),
    bigquery.SchemaField("cdr1_start", "INTEGER", "NULLABLE", None, None, (), None),
    bigquery.SchemaField("cdr1_end", "INTEGER", "NULLABLE", None, None, (), None),
    bigquery.SchemaField("fwr2_start", "INTEGER", "NULLABLE", None, None, (), None),
    bigquery.SchemaField("fwr2_end", "INTEGER", "NULLABLE", None, None, (), None),
    bigquery.SchemaField("cdr2_start", "INTEGER", "NULLABLE", None, None, (), None),
    bigquery.SchemaField("cdr2_end", "INTEGER", "NULLABLE", None, None, (), None),
    bigquery.SchemaField("fwr3_start", "INTEGER", "NULLABLE", None, None, (), None),
    bigquery.SchemaField("fwr3_end", "INTEGER", "NULLABLE", None, None, (), None),
    bigquery.SchemaField("fwr4_start", "FLOAT", "NULLABLE", None, None, (), None),
    bigquery.SchemaField("fwr4_end", "FLOAT", "NULLABLE", None, None, (), None),
    bigquery.SchemaField("cdr3_start", "FLOAT", "NULLABLE", None, None, (), None),
    bigquery.SchemaField("cdr3_end", "FLOAT", "NULLABLE", None, None, (), None),
    bigquery.SchemaField("np1", "STRING", "NULLABLE", None, None, (), None),
    bigquery.SchemaField("np1_length", "INTEGER", "NULLABLE", None, None, (), None),
    bigquery.SchemaField("np2", "STRING", "NULLABLE", None, None, (), None),
    bigquery.SchemaField("np2_length", "FLOAT", "NULLABLE", None, None, (), None),
    bigquery.SchemaField("c_region", "STRING", "NULLABLE", None, None, (), None),
    bigquery.SchemaField(
        "ANARCI_numbering", "STRING", "NULLABLE", None, None, (), None
    ),
    bigquery.SchemaField("ANARCI_status", "STRING", "NULLABLE", None, None, (), None),
    bigquery.SchemaField("Redundancy", "INTEGER", "NULLABLE", None, None, (), None),
    bigquery.SchemaField("antibody_id", "STRING", "REQUIRED", None, None, (), None),
    bigquery.SchemaField("Isotype", "STRING", "NULLABLE", None, None, (), None),
    bigquery.SchemaField("Chain", "STRING", "NULLABLE", None, None, (), None),
    bigquery.SchemaField("sequence_id", "STRING", "REQUIRED", None, None, (), None),
    bigquery.SchemaField("Species", "STRING", "NULLABLE", None, None, (), None),
]

METADATA_SCHEMA = [
    bigquery.SchemaField("Run", "INTEGER", "NULLABLE", None, None, (), None),
    bigquery.SchemaField("Link", "STRING", "NULLABLE", None, None, (), None),
    bigquery.SchemaField("Author", "STRING", "NULLABLE", None, None, (), None),
    bigquery.SchemaField("Species", "STRING", "NULLABLE", None, None, (), None),
    bigquery.SchemaField("Age", "INTEGER", "NULLABLE", None, None, (), None),
    bigquery.SchemaField("BSource", "STRING", "NULLABLE", None, None, (), None),
    bigquery.SchemaField("BType", "STRING", "NULLABLE", None, None, (), None),
    bigquery.SchemaField("Vaccine", "STRING", "NULLABLE", None, None, (), None),
    bigquery.SchemaField("Disease", "STRING", "NULLABLE", None, None, (), None),
    bigquery.SchemaField("Subject", "STRING", "NULLABLE", None, None, (), None),
    bigquery.SchemaField("Longitudinal", "STRING", "NULLABLE", None, None, (), None),
    bigquery.SchemaField(
        "Unique sequences", "INTEGER", "NULLABLE", None, None, (), None
    ),
    bigquery.SchemaField(
        "Total sequences", "INTEGER", "NULLABLE", None, None, (), None
    ),
    bigquery.SchemaField("Isotype", "STRING", "NULLABLE", None, None, (), None),
    bigquery.SchemaField("Chain", "STRING", "NULLABLE", None, None, (), None),
    bigquery.SchemaField("metadata_id", "STRING", "REQUIRED", None, None, (), None),
]

ANTIBODY_SCHEMA = [
    bigquery.SchemaField("antibody_id", "STRING", "REQUIRED"),
    bigquery.SchemaField("metadata_id", "STRING", "REQUIRED"),
    bigquery.SchemaField("is_paired", "BOOLEAN", "REQUIRED"),
]
