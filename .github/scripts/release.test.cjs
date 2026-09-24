const { test } = require('node:test');
const assert = require('node:assert/strict');
const { nextVersion, release } = require('./release.cjs');

test('starts at 1.0.0 and increments minors numerically, never patches or majors', () => {
  assert.equal(nextVersion([], 'minor'), 'v1.0.0');
  assert.equal(nextVersion([], 'major'), 'v1.0.0');
  assert.equal(nextVersion(['v1.0.0'], 'minor'), 'v1.1.0');
  assert.equal(nextVersion(['v1.9.0', 'v1.10.0', 'v2.0.0-rc.1'], 'minor'), 'v1.11.0');
  assert.equal(nextVersion(['v2.3.9', 'v1.99.0'], 'minor'), 'v2.4.0');
  assert.equal(nextVersion(['v1.9.0'], 'major'), 'v2.0.0');
  assert.throws(() => nextVersion([], 'patch'));
});

function fixture(eventName = 'push', existing = []) {
  const calls = [];
  const github = {
    rest: { repos: {
      listReleases: 'releases', listTags: 'tags',
      createRelease: async data => { calls.push(data); return { data: { html_url: 'release-url' } }; },
    } },
    paginate: async endpoint => endpoint === 'releases' ? existing : [{ name: 'v1.2.0' }],
  };
  const summary = { addHeading() { return this; }, addLink() { return this; },
    addRaw() { return this; }, async write() {} };
  return { github, context: { ref: 'refs/heads/master', eventName, runId: 42,
    sha: 'exact-commit', repo: { owner: 'owner', repo: 'repo' }, payload: { inputs: { bump: 'major' } } },
  core: { info() {}, summary }, calls };
}

test('push ignores major input and publishes exact commit as a stable release', async () => {
  const f = fixture();
  await release(f);
  assert.equal(f.calls[0].tag_name, 'v1.3.0');
  assert.equal(f.calls[0].target_commitish, 'exact-commit');
  assert.equal(f.calls[0].draft, false);
  assert.equal(f.calls[0].prerelease, false);
});

test('major increment requires dispatch', async () => {
  const f = fixture('workflow_dispatch');
  await release(f);
  assert.equal(f.calls[0].tag_name, 'v2.0.0');
});

test('retries do not publish twice', async () => {
  const f = fixture('push', [{ body: '<!-- release-run:42 -->', html_url: 'existing' }]);
  await release(f);
  assert.equal(f.calls.length, 0);
});

test('rejects other branches', async () => {
  const f = fixture();
  f.context.ref = 'refs/heads/feature';
  await assert.rejects(release(f), /master/);
  assert.equal(f.calls.length, 0);
});
