# The pyqec library

If you are reading this book,
it is because you want to run numerical simulations 
of classical or quantum error corrections.
Or at least,
someone told you that you should do that and 
you are not in a situation that you can say no.

The goal of `pyqec` is to make this as painless 
as possible for you.
You only need some knowledge of the 
[Python programming language](https://www.python.org/)
and of error correction.
But don't worry,
you don't need to be an expert to use this library.

## Installation

If you already have Python installed,
you only need to run

```bash
pip install pyqec
```

The library is currently is rapid development.
You should always check that you are running the most up-to-date version.
Else,
the information in this guide maybe be wrong.

## Open source software

`pyqec` is an open source software
built using other awesome open source softwares.

The backend of `pyqec` is actually written using the 
[Rust programming language](https://www.rust-lang.org/).
If you don't Rust,
you should definitely give it a try if you have some spare time.

To translate the Rust backend into a Python front-end,
I used the [pyo3 library](https://github.com/PyO3/PyO3).

## Contribution

You will find a Github icon in the top right corner of this book.
If you follow this link,
you will find the repository for the `pyqec` library.
Feel free to submit a pull request or the raise an issue if 
you want to improve either this book or the library itself.
All contributions,
as minor as they may seems,
are most welcome.
Thank you. 🚀
