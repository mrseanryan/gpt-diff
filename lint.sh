# so future errors halt the script.
set -e

./format.sh

echo Linting ...

ruff check gpt_diff

python -m mypy --install-types --non-interactive gpt_diff

echo [done]
