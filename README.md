# Pine User Manual

This repo contains the source for the current [User Manual](https://www.tradingview.com/pine-script-docs/en/v5/index.html) of TradingView's Pine programming language. It deprecates the Pine Tutorial Wiki that used to be accessible via [this link](https://www.tradingview.com/wiki/Pine_Script_Tutorial). The source uses [reStructuredText markup](https://docutils.sourceforge.io/docs/ref/rst/restructuredtext.html) and we use [Sphinx](https://www.sphinx-doc.org/en/master/) to build the final HTML product.


## How to build html docs
Follow these steps:

* Execute `sudo make install_tools`
* Execute `make syncpackages` (this would download the theme)
* Execute `make html`

Your docs will be in the `build/html` folder.

