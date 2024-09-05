#!/usr/bin/env just --justfile

set dotenv-load

run:
  docker compose up --build
