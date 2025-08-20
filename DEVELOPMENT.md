# Development Documentation

This website runs on Django and uses Wagtail for the blog interface. 


## Updating Wagtail and other dependencies

To update a dependency that the website uses:

1. Go to the pyproject.toml file
2. In the `[dependencies]` table, manually update the dependency version.
3. Run `uv sync` to update the UV lock file associated with the website build.
4. Push your changes to GitHub.