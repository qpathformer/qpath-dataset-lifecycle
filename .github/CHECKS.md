# Repository checks

Two GitHub Actions jobs run on every pull request to `main`, every push to
`main`, and manual workflow runs. There are no path filters that could leave a
required check unreported for a documentation-only change.

| Required check | Scope | Limits |
| --- | --- | --- |
| **README links** | Local Markdown links and images in tracked Markdown files whose names contain `README`, ignoring letter case. Checks tracked targets, exact filename case, repository boundaries and Markdown heading or explicit HTML anchors. | Does not test external websites, bare URLs, paths shown as code, links in other documents, or citations inside PDFs and Word files. |
| **JSON syntax** | Every tracked `.json` file, ignoring extension case: valid UTF-8 JSON, unique object keys, and no `NaN` or `Infinity` constants. UTF-8 byte-order marks are rejected. | Does not validate schemas, execute tools, assess meaning, verify signatures or provenance, or inspect JSON inside ZIP archives. |

The README check runs offline. It handles inline and reference Markdown links,
images, angle-bracket paths containing spaces and HTML links. External URL
schemes are excluded. Fragment checking applies to Markdown destinations;
PDF fragment syntax is outside this check.

At the initial maintenance baseline, the five tracked README files contain
**zero local Markdown links** in this check's scope. They mostly present paths
as code and references as bare URLs. A green README result therefore does not
confirm those references work; review them manually. The baseline also contains
25 JSON files that pass the strict syntax check. These counts describe the
starting point, not a required fixed inventory.

The checks read files without rewriting them or running the dataset lifecycle
tools. They do not rebuild manifests or sealed packages. Original papers,
artifacts and release assets retain their published identities.

## Run locally

From the repository root, using Python 3.12:

```sh
python -m pip install --require-hashes -r .github/ci/requirements.txt
python -m unittest discover -s .github/ci/tests -v
python .github/ci/check_readme_links.py --root .
python .github/ci/check_json.py --root .
```

Pass `--root .` explicitly when invoking either checker from the repository
root. Only Git-tracked paths are examined. Stage intended new files before
checking their links locally so the local inventory matches the files available
in CI. The automated checks must still pass on the pull request.

The workflow pins actions and Python dependencies, uses a read-only token,
does not persist checkout credentials, and receives no repository secrets. It
uses `pull_request`, not `pull_request_target`. GitHub may require a maintainer
to approve the workflow run for a first-time external contributor.

## Merge requirements

The `main` rules require **README links** and **JSON syntax** from GitHub Actions.
Strict checking requires the pull-request branch to be up to date with `main`.
Failures must be corrected before merging. Human diff review and conversation
resolution remain part of the [contribution workflow](../CONTRIBUTING.md).

If a required job is renamed or removed, coordinate the workflow and ruleset
changes so merging is not blocked waiting for a check that no longer runs.
The tests under `.github/ci/tests/` exercise the maintenance checkers; they are
not a dataset lifecycle implementation test suite.

Passing CI is evidence only for these bounded checks. It is not independent
assurance, legal approval, governance authority or production permission.
