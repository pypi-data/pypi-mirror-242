# Introduction

[![crates.io](https://img.shields.io/crates/v/nanopub.svg)](https://crates.io/crates/nanopub)
[![PyPI](https://img.shields.io/pypi/v/nanopub-sign)](https://pypi.org/project/nanopub-sign/)
[![npm](https://img.shields.io/npm/v/@nanopub/sign)](https://www.npmjs.com/package/@nanopub/sign)

This project aims to provide a comprehensive cross-platform toolkit to sign, publish, and check **[Nanopublications](https://nanopub.net)**.

Sign and publish providing a private RSA key string, or a `profile.yml` file. Check the validity of signed or unsigned Nanopublications.

It is packaged to be used easily through various popular interfaces:

- ⌨️ Binary with a CLI for use in the terminal
- 🦀 Crate `nanopub` for Rust
- 🐍 Pip package `nanopub_sign` for Python
- 📦️ NPM package `@nanopub/sign` for JavaScript (compiled to WebAssembly) in the browser, or with NodeJS

On all platforms:

- 🐧 Linux
- 🍎 MacOS
- 🪟 Windows
- 🦊 Web browsers

The library automatically handles most RDF serializations supporting graphs for the nanopub:

- TriG
- Nquads
- JSON-LD
