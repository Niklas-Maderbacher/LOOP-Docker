# Install packages for backend

using uv instead of pip, because pip does not support **"pyproject.toml"** and requires a .txt file.

## But why uv instead of pip

As already mentioned, pip does not support pyproject.toml file. This type of file is better formated than a .txt file. \
As bigger, as the project grows, the more confusing it gets, when using a .txt file. Because of this reason, we are using uv.

## Adding package

If the package is used for project functionality, add the package under the **[project]** section in **dependencies**.

### Specific version or newer

```
package-name>=version
```

### Specific version

```
package-name==version
```

### Lock package version

To lock the version of a package (update uv.lock file), use following command in a terminal:

```bash
uv lock
```

### Localy installing package

To install a package localy, use following command in a terminal:

For windows:

```bash
pip install <package-name>
```

For arch-linux:

```bash
sudo pacman -S python-<package-name>
```
