# Releases and DOIs

The **Release** GitHub Actions workflow publishes a stable release on each push
to `master`, including merged pull requests and direct pushes. Protect `master`
with a pull-request requirement if releases should only follow merges.

The first release is `v1.0.0`, followed by `v1.1.0`, `v1.2.0`, and so on.
The workflow selects the highest numeric `vMAJOR.MINOR.PATCH` tag, increments
the minor number, and sets the patch to zero. Prerelease and unrelated tags are
ignored. No automatic run increments the major version.

For a deliberate major release, go to **Actions → Release → Run workflow**,
select **master**, and choose **major**. After `v2.0.0`, automatic releases
continue at `v2.1.0`. A manual run with **minor** can also create a release.
Rerunning the same completed workflow run does not create another release;
starting a new manual run does.

Each release tags the exact triggering commit, includes generated release notes,
and provides GitHub's source ZIP and tar.gz downloads. This project currently
has no installable package or modern executable build; these are source and
document releases. The historical Qiskit script is not executed by this workflow.
Release runs are serialized, with up to 100 pending runs queued, to avoid
competing version assignments. Avoid creating tags or releases manually while
this workflow is running. The workflow uses the built-in `GITHUB_TOKEN` with
`contents: write`; repository rules must permit it to create release tags.

## One-time Zenodo setup (before the first merge)

1. Sign in to [Zenodo](https://zenodo.org) and connect your GitHub account.
2. Open your profile's **GitHub** page, select **Sync now**, and enable
   `AbdulahAmer/Quantum-Phase-Estimation-with-Qiskit-`.
3. Merge this workflow into `master`. After the GitHub release publishes, check
   the repository on Zenodo for the processed record and its DOI.

Zenodo's [repository integration](https://help.zenodo.org/docs/github/enable-repository/)
installs the release webhook and archives new GitHub releases. No Zenodo API
token or separate DOI-publishing workflow is needed. `CITATION.cff` supplies
authorship and license metadata; the version and publication date are left to
the release integration so they cannot become stale in the source file.
The two listed licenses cover different portions of the repository, as described
in the citation abstract and README; they are not alternative licenses for every file.

Each archived version receives its own DOI. Cite that version's DOI when
reproducibility matters; Zenodo also provides a concept DOI for the project
across versions. Copy the real DOI from Zenodo into any badges or publications
after the first successful deposit. No DOI is invented or reserved by CI.

GitHub release success does not prove Zenodo ingestion succeeded. In Zenodo's
GitHub page, inspect the release status and **Errors** if no record appears;
see [Zenodo's troubleshooting guide](https://help.zenodo.org/docs/github/archive-software/github-upload/).
Enable the integration before releasing: existing releases are not automatically
backfilled. If a release already exists, enable the integration and start a new
manual minor release to trigger a new deposit.

## Verify locally

Run `node --test .github/scripts/release.test.cjs` to check version selection,
manual major releases, retry handling, and branch restrictions without publishing.
