# Pine Script™ v5 User Manual

This repo contains the source for the [Pine v5 User Manual](https://www.tradingview.com/pine-script-docs/en/v5/index.html) of TradingView's Pine programming language, which deprecates the [Pine Script™ v4 User Manual](https://www.tradingview.com/pine-script-docs/en/v4/index.html). The source uses [reStructuredText markup](https://docutils.sourceforge.io/docs/ref/rst/restructuredtext.html) and we use [Sphinx](https://www.sphinx-doc.org/en/master/) to build the final HTML content.


## How to build html docs
Follow these steps:

* Execute `sudo make install_tools`
* Execute `make syncpackages` (this will download the theme)
* Execute `make html`

Your docs will be in the `build/html` folder.


## Writing guidelines for contributors

See our [English language and RST writing guidelines](https://github.com/tradingview/documentation-guidelines/blob/main/PineUserManual/README.md) for this Manual.