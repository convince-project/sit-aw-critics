Build and run
=============

There is nothing really to install, the critics are already called has a library in the pyproject.toml file of the sit-aw-aip repository with the following lines :

.. code-block:: bash

    dependencies = [
      "critics"
    ]
    
    [tool.uv.sources]
    critics = {git = "https://github.com/convince-project/sit-aw-critics.git", branch= "mwe"}
