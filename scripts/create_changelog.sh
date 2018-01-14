#!/usr/bin/env bash

pandoc --from=markdown --to=rst --output=CHANGELOG.rst CHANGELOG.md
