---
layout: home

hero:
  name: "moles-tools"
  text: "Python tools from the underground"
  tagline: "A growing collection of handy command-line utilities for everyday developer tasks."
  image:
    src: /logo.svg
    alt: moles-tools
  actions:
    - theme: brand
      text: Get Started
      link: /installation
    - theme: alt
      text: View on GitHub
      link: https://github.com/the78mole/moles-tools

features:
  - icon: 🔧
    title: ENV File Updater
    details: >
      Update ENV variables in a target file from an update file.
      Auto-detects .env and .env.example files; new variables are appended,
      existing ones are updated in place.
    link: /tools/env-updater
    linkText: Learn more
  - icon: 📦
    title: Easy Installation
    details: >
      Install from PyPI with a single command. Works with pip, uv, and pipx.
    link: /installation
    linkText: Installation guide
  - icon: 🧪
    title: Well Tested
    details: >
      Every tool ships with a comprehensive test suite using pytest,
      with a minimum coverage threshold enforced in CI.
---
