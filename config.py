import os
from pathlib import Path

ROOT_DIR = os.path.dirname(os.path.abspath(__file__))  # This is your Project Root Directory

DATA_DIR = str(Path(ROOT_DIR) / "data")

OUTPUT_DIR = str(Path(ROOT_DIR) / "output")

LOG_DIR = str(Path(ROOT_DIR) / "log")

FEATURE_VECTOR_DIR = str(Path(OUTPUT_DIR) / "feature_vector")

METRICS_DIR = str(Path(ROOT_DIR) / "metrics")

MODEL_DIR = str(Path(ROOT_DIR) / "model")

WORD2VEC_MODEL_NAME = 'word2vec-google-news-300'

WORD2VEC_DIM = 300

ONEHOT_DIM = 0

# for mozilla
DATETIME_FORMAT = '%Y-%m-%dT%H:%M:%SZ'

# for eclipse
# DATETIME_FORMAT = '%Y-%m-%d %H:%M:%S'

MOZILLA_URL = 'https://bugzilla.mozilla.org/show_bug.cgi?id='

ECLIPSE_URL = 'https://bugs.eclipse.org/bugs/show_bug.cgi?id='

MOZILLA_PROJ = 'mozilla'

ECLIPSE_PROJ = 'eclipse'

MOZILLA_SUMMARY_LEN = 13

ECLIPSE_SUMMARY_LEN = 11
