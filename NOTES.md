# installing vsketch

first install `pipx`:

```
brew install pipx
```

somehow `pipx` wants to use Python 3.11 which is not supported by `vsketch`, but
`python --version` shows a 3.10 version, which is apparently due to `pyenv` and
my `pyenv` config.

I tried installing `vsketch` via `pipenv` but that failed with an error about eggs.

ok let's install with `pipx` but override the Python version:

```
PIPX_DEFAULT_PYTHON=`which python` pipx install "git+https://github.com/abey79/vsketch"
```

# running examples

```
vsk run vsketch-master/examples/schotter
```

# running from a notebook

```
pipenv --rm # clear out previous virtualenv (stored under ~/.local/share/virtualenvs)
pipenv --python 3.10 # make a new virtualenv (need to switch VS Code to point to it)
pipenv install ipython
pipenv install ipykernel
pipenv install "git+https://github.com/abey79/vsketch#egg=vsketch"
```

# using ipywidgets

install:

```
pipenv install ipywidgets
```

use:

```
import ipywidgets as widgets

def sketch(count):
  # do the sketch, call display

# makes an IntSlider with range 3 to 20
widgets.interact(sketch, count=(3, 20))
```
