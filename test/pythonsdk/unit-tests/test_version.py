#!/usr/bin/env python3
# SPDX-License-Identifier: Apache-2.0
"""Test version module."""

import oransdk.version as version

def test_version():
  """Check version is the right one."""
  assert version.__version__ == '1.0.0'
