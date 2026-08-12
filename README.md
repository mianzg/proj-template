# <Project Name>

> One-paragraph summary: what question this project answers, why it matters,
> and the current status (e.g. "exploratory", "under review", "archived").

**Status:** 🚧 in progress &nbsp;|&nbsp; **Owner:** <you> &nbsp;|&nbsp; **Started:** YYYY-MM

---

## Using this as a GitHub template

This repo is meant to be marked as a template so new projects can start
from it directly:

1. In this repo's GitHub settings, check **"Template repository"**
   (Settings → General → Template repository).
2. For new projects, use the **"Use this template"** button on the repo
   page (instead of forking or cloning) to create a fresh repo with its
   own history — it will still be private if this template is.
3. In the new repo, run `python init_template.py` once to fill in the
   project name across `README.md`, `environment.yml`, and `.env.example`,
   then delete that script.

## Remote / HPC setup

On a shared/remote server, home directories are often small and quota-limited
while a separate scratch filesystem has the space and I/O speed you actually
want for data and environments. Do this right after cloning, before running
anything:

```bash
# 1. Clone into your home dir as usual
git clone git@github.com:<org-or-user>/<repo>.git
cd <repo>

# 2. Create the real storage-heavy dirs on scratch, then symlink them in
SCRATCH=/scratch/<user>/<repo>   # adjust to your cluster's scratch path
mkdir -p "$SCRATCH"/{data,results}
rm -rf data results               # remove the empty dirs created by git clone
ln -s "$SCRATCH/data" data
ln -s "$SCRATCH/results" results

# 3. Build the conda environment on scratch too, rather than the default
#    (often quota-limited) location under $HOME/.conda
conda env create -f environment.yml -p "$SCRATCH/envs/research-project"
conda activate "$SCRATCH/envs/research-project"
```

Notes:
- `data/` and `results/` are git-ignored already (see `.gitignore`), so
  turning them into symlinks changes nothing about what git tracks — just
  where the bytes physically live.
- Do this **before** populating `data/` with anything, so you don't end up
  copying large files twice.
- Keep the symlink target path itself out of git — it's machine-specific.
  If a script or notebook needs to know the scratch root explicitly, put it
  in `.env` (e.g. `DATA_ROOT=/scratch/<user>/<repo>/data`), not hardcoded.
- Confirm scratch is actually the right tier for your data — some clusters
  purge scratch after N days of inactivity, which is fine for regenerable
  `results/` but worth checking for `data/raw/` if it's not backed up
  elsewhere.

## Quick start

```bash
# 1. Clone (this repo is private — make sure you're authenticated)
git clone git@github.com:<org-or-user>/<repo>.git
cd <repo>

# 2. Create the environment
conda env create -f environment.yml   # or: pip install -r requirements.txt
conda activate research-project

# 3. Copy the env template and fill in secrets/paths locally (never commit this file)
cp .env.example .env

# 4. Run something
python src/run_example.py --config example_experiment
```

## Repo structure

```
.
├── data/            # never committed except tiny fixtures — see data/README.md
│   ├── raw/         # untouched source data, read-only in practice
│   ├── processed/   # cleaned/derived data, regenerable from raw/
│   └── external/    # third-party reference data
├── notebooks/       # exploratory analysis, numbered by date or step (01_eda.ipynb)
├── src/             # all code: importable modules + runnable scripts
├── config/          # YAML/JSON configs for experiments, kept out of code
└── results/         # generated figures, tables, model checkpoints (git-ignored)
```

## Data & reproducibility

- Raw data is **not** committed to git. See `data/README.md` for where it actually
  lives (e.g. shared drive, S3 bucket, DVC remote) and how to fetch it.
- On a remote/HPC server, symlink `data/` and `results/` to scratch storage
  before populating them — see **Remote / HPC setup** above.
- Every result in `results/` should be regenerable by running a script or notebook
  against `data/` — if it can't be, that's a bug in the pipeline, not a shortcut.
- Random seeds are fixed and logged for anything stochastic (see `config/`).
- Large binary artifacts (checkpoints, big CSVs) belong in Git LFS or an external
  store, not in the git history.

## Environment & secrets

- All dependencies are pinned in `environment.yml` (conda) or `requirements.txt` (pip).
- API keys, credentials, and machine-specific paths go in `.env`, which is
  git-ignored. `.env.example` documents what's expected without real values.
- Never hardcode credentials in notebooks or scripts.

## Conventions

- Code that's used more than once lives in `src/`, as an importable module —
  scripts should mostly call into it rather than duplicating logic.
- Import style is consistent everywhere: the project root goes on `sys.path`,
  and modules are imported as `src.<module>` — see `src/run_example.py` and
  `notebooks/_bootstrap.py`. This means code moves between scripts and
  notebooks without changing its imports.
- Notebooks are for exploration and figures, not for logic you depend on elsewhere —
  if a notebook cell is doing something important, move it into `src/`.
- Commit messages: short imperative summary line, more detail in the body if needed.
