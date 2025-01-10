set -euo pipefail

echo "Ensuring pip is up to date"
python -m pip install --upgrade pip

if [[ "${INSTALL_REQUIREMENTS}" == "true"  ]]; then
  echo "Installing code requirements"
  pip install --no-cache-dir -r plugin_scripts/requirements.lock
fi

if [[ "${INSTALL_TEST_REQUIREMENTS}" == "true"  ]]; then
  echo "Installing test requirements"
  pip install --no-cache-dir -r requirements-test.txt
fi