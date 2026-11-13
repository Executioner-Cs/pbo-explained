"""Build the working paper and brief from docs/source/ into docs/; logs go to .local/build/."""
import argparse
import hashlib
from pathlib import Path
import shutil
import subprocess

ROOT = Path(__file__).resolve().parents[1]
DOCS = ROOT / "docs"
BUILD = ROOT / ".local" / "build"


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--tectonic", default="tectonic", help="Tectonic executable (default: tectonic on PATH)")
    args = parser.parse_args()
    BUILD.mkdir(parents=True, exist_ok=True)
    for name in ("working-paper", "research-brief"):
        subprocess.run([args.tectonic, "-X", "compile", "--outdir", str(BUILD), "--keep-logs",
                        str(DOCS / "source" / f"{name}.tex")], check=True, cwd=DOCS / "source")
        shutil.copyfile(BUILD / f"{name}.pdf", DOCS / f"{name}.pdf")
    paths = ["working-paper.pdf", "research-brief.pdf", "source/working-paper.tex",
             "source/references.bib", "source/research-brief.tex"]
    (DOCS / "checksums.sha256").write_text("".join(
        f"{hashlib.sha256((DOCS / path).read_bytes()).hexdigest()}  {path}\n" for path in paths))


if __name__ == "__main__":
    main()
