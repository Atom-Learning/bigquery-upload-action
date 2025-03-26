#!/usr/bin/env bash
set -euo pipefail
IFS=$'\n\t'
cd "$(dirname "$0")"/.. # repo root

NEW_TAG="${1:?Please specifiy the new tag version to build&push, such as v0.8.1}"

# Image needs to be built for both X64 and ARM64. 
# To do this we need to create a Docker builder that supports cross-platform and install emulators to build on the non-native CPU architectures
setup_docker_builder() {
  echo "Setting up Docker builder and emulators"

  docker run --privileged --rm tonistiigi/binfmt --install arm64,amd64

  docker buildx create --name bigqueryuploadaction-builder --driver docker-container --bootstrap
}

cleanup_docker_builder() {
  set +e
  echo "Cleaning up Docker builder and emulators"

  docker buildx rm bigqueryuploadaction-builder

  docker run --privileged --rm tonistiigi/binfmt --uninstall '*'
}

setup_docker_builder
trap "cleanup_docker_builder" EXIT

docker buildx build --builder bigqueryuploadaction-builder --tag "ghcr.io/atom-learning/bigquery-upload-action:${NEW_TAG}" --push --platform linux/amd64,linux/arm64 .