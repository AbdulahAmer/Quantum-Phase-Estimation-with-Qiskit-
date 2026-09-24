const pattern = /^v(0|[1-9]\d*)\.(0|[1-9]\d*)\.(0|[1-9]\d*)$/;

function nextVersion(tags, bump) {
  if (!['minor', 'major'].includes(bump)) throw new Error('Invalid release increment');
  const versions = tags.map(tag => tag.match(pattern)).filter(Boolean)
    .map(match => match.slice(1).map(Number))
    .sort((a, b) => b[0] - a[0] || b[1] - a[1] || b[2] - a[2]);
  if (!versions.length) return 'v1.0.0';
  const [major, minor] = versions[0];
  return bump === 'major' ? `v${major + 1}.0.0` : `v${major}.${minor + 1}.0`;
}

async function release({ github, context, core }) {
  if (context.ref !== 'refs/heads/master') throw new Error('Releases must run on master');
  const bump = context.eventName === 'workflow_dispatch'
    ? context.payload.inputs?.bump ?? 'minor' : 'minor';
  const repo = context.repo;
  // The run ID survives retries, so rerunning a successful job cannot mint another DOI.
  const marker = `<!-- release-run:${context.runId} -->`;
  const releases = await github.paginate(github.rest.repos.listReleases, { ...repo, per_page: 100 });
  const existing = releases.find(item => item.body?.includes(marker));
  if (existing) {
    core.info(`Already published: ${existing.html_url}`);
    return;
  }
  const tags = await github.paginate(github.rest.repos.listTags, { ...repo, per_page: 100 });
  const tag = nextVersion(tags.map(item => item.name), bump);
  // GitHub creates the tag at the exact triggering commit and provides ZIP/tar.gz archives.
  const { data } = await github.rest.repos.createRelease({
    ...repo,
    tag_name: tag,
    target_commitish: context.sha,
    name: tag,
    body: `${marker}\nSource and documentation snapshot of commit ${context.sha}.`,
    generate_release_notes: true,
    draft: false,
    prerelease: false,
    make_latest: 'true',
  });
  await core.summary.addHeading(`Released ${tag}`)
    .addLink('GitHub release', data.html_url)
    .addRaw('\n\nZenodo will archive this release if the repository integration is enabled. Check Zenodo for the DOI and any ingestion errors.')
    .write();
}

module.exports = { nextVersion, release };
