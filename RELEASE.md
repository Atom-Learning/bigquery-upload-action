# Release Process

How to release a new version of this Action.

## Prerequisites
* All changes to go into the release are merged into `main`
* A Linux machine with Docker installed, such as an Atom remote development environment
* [Authenticated with ghcr.io with `docker login` with an account/token](https://docs.github.com/en/packages/working-with-a-github-packages-registry/working-with-the-container-registry#authenticating-with-a-personal-access-token-classic) which can push to `ghcr.io/atom-learning/bigquery-upload-action`

## Steps
1. Decide the appropriate new version tag per semantic versioning e.g. `v0.8.1`
2. Run `bash scripts/push-new-release.bash <new tag>` e.g. `bash scripts/push-new-release.bash v0.8.1`
    - This script build the new Docker image for the Action and pushes them to ghcr.io
3. Update `runs.image` in `actions.yml` to `docker://ghcr.io/atom-learning/bigquery-upload-action:<new tag>`
4. Commit with change to `main`
5. Finally tag with Git and push: `git tag <new tag> && git push --tags origin main`

After this the release will be complete. Then update any dependent Actions workflows to reference the new version.