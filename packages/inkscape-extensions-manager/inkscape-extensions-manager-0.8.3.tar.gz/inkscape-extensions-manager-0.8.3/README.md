# Inkscape Extensions Manager

This Gtk3 application is actually an Inkscape Extension which manages
other Inkscape extensions. It's intended to be installed alongside
Inkscape and also to be shipped with Inkscape.

## Installation

Install this repository if you need to test the latest version or are
doing development work on the extension manager.

### Installing Requirements

You will need python3 and virtualenv as well as the gobject libraries.

    sudo apt install python3 python3-dev virtualenv

You will also need to install pyobject, which needs to be installed WITHIN your pythonenv

`https://pygobject.readthedocs.io/en/latest/getting_started.html`

You may also need to install lxml and other tools to get inkex to work.

### Testing the latest version

    export INKSCAPE_PROFILE_DIR="my-testing-prefix"
    mkdir -p $INKSCAPE_PROFILE_DIR/extensions
    virtualenv -p python3 $INKSCAPE_PROFILE_DIR/extensions
    $INKSCAPE_PROFILE_DIR/extensions/bin/pip install git+https://gitlab.com/inkscape/extras/extension-manager.git#egg=inkscape-extensions-manager

This will install the latest checkout of this manager under a custom prefix so it won't disrupt your installed version. Then to see this version of the extension run inkscape with:

    INKSCAPE_PROFILE_DIR="my-testing-prefix" inkscape

## Development

You can set the -e flag in your prefix to develop 'in-situ' which can be useful. Python provides a way of checking out the repository and allowing you to modify them.

    export INKSCAPE_PROFILE_DIR="my-dev-prefix"
    mkdir -p $INKSCAPE_PROFILE_DIR/extensions
    virtualenv -p python3 $INKSCAPE_PROFILE_DIR/extensions
    $INKSCAPE_PROFILE_DIR/extensions/bin/pip install -e git+ssh://git@gitlab.com/inkscape/extras/extension-manager.git#egg=inkscape-extensions-manager

You can then edit the files in `my-dev-prefix/extensions/src/` and commit them and push them as you would any repository in development. Running inkscape is as above but this this dev prefix instead.

