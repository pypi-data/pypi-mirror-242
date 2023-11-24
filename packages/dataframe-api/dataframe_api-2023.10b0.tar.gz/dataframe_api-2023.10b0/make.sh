ruff format dataframe_api examples
ruff dataframe_api examples
mypy dataframe_api --no-incremental && mypy examples
cd ../../. && . clean.sh
sphinx-build -b html -WT --keep-going spec build/draft -d doctrees
cd spec/API_specification
