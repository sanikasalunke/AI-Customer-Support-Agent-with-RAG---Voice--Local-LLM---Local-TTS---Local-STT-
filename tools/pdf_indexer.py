# tools/pdf_indexer.py
import shutil, os
from core.rag import DocStore

def add_pdf(filepath: str, dest_dir="data/docs"):
    os.makedirs(dest_dir, exist_ok=True)
    fname = os.path.basename(filepath)
    dest = os.path.join(dest_dir, fname)
    shutil.copy(filepath, dest)
    ds = DocStore(data_dir=dest_dir)
    ds.index_all()
    return {"indexed": fname}

if __name__ == "__main__":
    import sys
    p = sys.argv[1]
    print(add_pdf(p))
