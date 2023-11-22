
# colorblind_pdf

![PyPI](https://img.shields.io/pypi/v/colorblind_pdf)
![Python Version](https://img.shields.io/pypi/pyversions/colorblind_pdf)
![License](https://img.shields.io/github/license/dvolgyes/colorblind_pdf)
![Downloads](https://img.shields.io/pypi/dm/colorblind_pdf)
![Issues](https://img.shields.io/github/issues/dvolgyes/colorblind_pdf)
![Pull Requests](https://img.shields.io/github/issues-pr/dvolgyes/colorblind_pdf)

`colorblind_pdf` is a tool designed to test the accessibility of PDF documents for individuals with color vision deficiencies. It processes PDFs to simulate how the contained images would appear to someone with various types of color vision deficiencies, such as deuteranopia, protanopia, and tritanopia.

## Installation

To install `colorblind_pdf`, use pipx for an isolated installation:

```bash
pipx install colorblind_pdf
```

## Usage

To use `colorblind_pdf`, provide the path to the PDF you want to process, the output directory, and specify the type of color deficiency simulation. For example:

```bash
colorblind_pdf my_document.pdf -o output_directory -d deuteranopia -d protanopia
```

This command will process `my_document.pdf` for deuteranopia and protanopia, and saving the resulting PDFs in `output_directory`.

### Default values

-o: current directory ('.')

-d: all deficiencies ('all')

## Contributing

Contributions are welcome! Feel free to open an issue or submit a pull request on our [GitHub repository](https://github.com/dvolgyes/colorblind_pdf).

## License

Distributed under the MIT License. See `LICENSE` for more information.
