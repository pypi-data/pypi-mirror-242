# IDE Plots

*Matplotlib styles for cleaner integration with IDEs running Jupyter Notebooks*

![Graph Example](examples/figures/chart_01_with_vscode_style.png)

## Getting Started

The fastest way to get up and running is to install IdePlots by using the `pip` command.

```bash
# to install the latest release from PyPi
pip install IdePlots

# to install the latest commit from GitHub
pip install git+https://github.com/benabernathy/IdePlots.git

```

In your notebook you need to first import ideplots...

```python
import ideplots
```

Then you may reference any of the available styles...

```python
plt.style.use("vscode-dark-modern")
```

Then your plots will no longer cause your eyese to bleed. 

## Examples

Here are some example plots without and with the styles enabled.

![Without Style Enabled](examples/figures/chart_01_without_vscode_style.png)

![With Style Enabled](examples/figures/chart_01_with_vscode_style.png)

