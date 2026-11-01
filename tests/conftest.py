"""Shared pytest setup. pytest loads this before any test module."""

import os

# Tests must not depend on a developer's personal .env file.
os.environ["ENVIRONMENT"] = "test"
os.environ["POSTGRES_PASSWORD"] = "test_password"