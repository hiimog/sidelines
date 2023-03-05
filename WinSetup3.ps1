$ErrorActionPreference = "Stop"
# does not need admin
pip install `
    click `
    chess `
    mako ` # had an install error with renderer
    orjson `
    seqlog

#needs admin
pip install --editable C:\src\sidelines\util
