#!/usr/bin/env bash
set -euo pipefail

( cd frontend && npm run lint || true )
# Add Python linters when configured
