# Install This Plugin

To include this plugin as part of your local or institutional NOMAD Oasis the following
line needs to be added to the `pyproject.toml` file of the Oasis repo:
```
[project.optional-dependencies]
plugins = [
 'nomad-battery-space @ git+https://https://github.com/nomad-hzb/nomad-battery-space.git',
]
```

For a detailed guide on how to setup and install a new Oasis, see the [Tutorial 13 part 4](https://github.com/FAIRmat-NFDI/AreaA-Examples/tree/main/tutorial13/part4) or [NOMAD Documentation](https://nomad-lab.eu/prod/v1/staging/docs/howto/oasis/install.html).


