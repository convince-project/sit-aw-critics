Build and run
=============

in your pyproject.toml file add :

dependencies = [
  "critics"
]

[tool.uv.sources]
critics = {git = "https://github.com/convince-project/sit-aw-critics.git", branch= "mwe"}