python -m venv .venv
source .venv/bin/activate

pip install -U pip
pip install .

rag-benchmark init

cp tests/datasets/* datasets/

rag-benchmark scan
rag-benchmark diagnose
rag-benchmark generate
rag-benchmark report
rag-benchmark inspect --file "Bank Statement.pdf"

pytest
python -m build