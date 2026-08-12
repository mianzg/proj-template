# Data

Nothing here is committed to git except this file and empty placeholders
(`.gitkeep`). This keeps the repo small and avoids leaking data through
git history even if a file is later deleted.

## Where the real data lives

> Fill this in for your project, e.g.:
> - Raw data: `s3://<bucket>/<project>/raw/` (request access from <owner>)
> - Processed data: regenerated locally via the pipeline — see below
> - External reference data: `<url or drive link>`

## Fetching data

```bash
# Example — replace with your actual fetch mechanism
python src/fetch_data.py --dest data/raw/
```

## Layout

- `raw/` — exactly as received from the source. Treat as read-only.
- `processed/` — cleaned/derived data, fully regenerable by running the
  pipeline in `src/` against `raw/`. If you can't regenerate it, document
  why in this file.
- `external/` — third-party datasets or reference tables used for joins,
  lookups, or benchmarks.

## Data sensitivity

If any data here is sensitive (PII, embargoed, proprietary), note the
handling requirements here explicitly — who can access it, whether it can
leave this machine, and retention/deletion expectations.
