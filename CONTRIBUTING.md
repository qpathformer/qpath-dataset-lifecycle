# Contributing to Q-Pathformer Dataset Lifecycle

This repository is a reference implementation for governed dataset lifecycle
tooling. Proposals can improve documentation, reproducibility, validation and
implementation clarity within the [declared boundary](compliance/BOUNDARY.md).
Identify the affected component, source version and reason for the change.

The [published v1.0 release](https://github.com/qpathformer/qpath-dataset-lifecycle/releases/tag/v1.0-qpath-dataset-lifecycle)
is a preserved artifact set. Later repository maintenance does not rebuild,
reseal or publish that release. Changes to implementation meaning, release
scope or packaging require a new version and release record, as stated in the
[release status](compliance/RELEASE_STATUS.md).

## Normal change workflow

1. **Create a focused branch from current `main`.** For example, use
   `docs/clarify-passport-validation`. Contributors without write access can
   propose changes from a fork. Keep published packages and preserved evidence
   separate from the working checkout.
2. **Prepare the change and its provenance.** Preserve original papers,
   artifacts, attribution and licence notices. Describe corrections through
   errata, supplementary guidance or clearly versioned additions. Identify any
   third-party material and confirm that you have permission to submit it.
3. **Check the work locally, then push the branch.** Follow the commands in
   [Repository checks](.github/CHECKS.md). Review the complete diff and document
   any relevant manual checks. These checks do not run the dataset workflows.
4. **Open a draft pull request to `main`.** Explain the problem, resulting
   behavior, affected files, provenance and validation. State whether the change
   is maintenance guidance or a proposal for a future release. Do not upload
   private datasets, credentials or restricted third-party content.
5. **Complete review and resolve feedback.** Mark the pull request ready when
   the work is complete. Review the diff, rights and attribution, preservation
   of original material, and both required check results. Resolve conversations.
   If `main` advances, update the branch and wait for the checks to pass again.
6. **Merge deliberately.** A maintainer performs the merge after review and
   passing checks. Squash merging is suitable for a focused change. Delete the
   completed working branch if no longer needed, then update local `main`.
   A merge is not release publication or production authorization.

## Required checks and merge rules

Changes to `main` must use a pull request. The exact required GitHub Actions
checks are **README links** and **JSON syntax**, with the proposed branch up to
date with `main` and review conversations resolved. Force pushes and deletion
of `main` are blocked, and no bypass actors are configured.

The current single-maintainer workflow requires **zero approving reviews**;
the maintainer can merge their own pull request after the other conditions are
met. This records the proposal, review and result without representing
independent approval. Review remains a human responsibility. An independent
approval requirement can be introduced when another eligible reviewer is
available.

The automated checks cover local Markdown links in tracked README files and
strict syntax of tracked JSON files. External websites, bare URLs, paths shown
as code, and links in other documents need manual review. Passing these checks
does not establish schema agreement, semantic correctness, rights, governance
adequacy, preservation of every original file or readiness for production.
See [Repository checks](.github/CHECKS.md) for their precise scope and limits.

## Licences and contribution scope

Read [LICENSE](LICENSE) and the
[Q-Pathformer Platform License 1.0](QPATHFORMER-PLATFORM-1.0.txt) before proposing
material. The existing terms distinguish research, evaluation and internal
development from derivative-build distribution and production or commercial
integration. This guide adds no licence grant and changes none of those terms.
Do not assume that public availability or acceptance of a pull request provides
additional redistribution or production rights.

Identify the source and applicable terms of contributed code, data and
documents. Preserve copyright and attribution notices and disclose material
adapted from elsewhere. Explain any AI-assisted contribution so a maintainer
can review its sources, accuracy and suitability. Do not remove or bypass
governance safeguards as part of a proposed change.

The repository-maintenance helpers under `.github/ci/` are adapted from MIT
licensed Access PoD helpers and carry their own scoped
[MIT notice](.github/ci/LICENSE). That notice applies to those helpers; it does
not relicense the Q-Pathformer platform, papers or artifacts. Existing
file-specific notices remain applicable.

## Preserve published records

- Keep `v1.0-qpath-dataset-lifecycle` at its published commit. Its tag protection
  prevents movement and deletion; it does not make release assets immutable.
- Do not replace, delete or regenerate the published ZIP packages, checksums,
  manifests or other release assets as part of repository maintenance.
- Preserve original papers, example records and evidence. Label later
  observations and additions with their own source version and status.
- Keep [manifest.external.json](manifest.external.json) as the published
  snapshot record. Do not refresh it to include later contribution or CI files.
- Prepare any future release separately with a new version, tag and integrity
  records. Review publication scope and permissions explicitly.

Check that every pull-request diff contains only the intended changes. Any
later publication work must also compare the existing release tag and asset
identities and hashes before and after the work.
