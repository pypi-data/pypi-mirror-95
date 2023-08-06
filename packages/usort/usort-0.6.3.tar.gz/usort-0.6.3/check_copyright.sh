#!/bin/bash

# Copyright (c) Facebook, Inc. and its affiliates.
#
# This source code is licensed under the MIT license found in the
# LICENSE file in the root directory of this source tree.

set -eu

die() { echo "$1"; exit 1; }

while read filename; do \
  grep -q "^# Copyright (c) Facebook" "$filename" ||
    die "Missing copyright in $filename"
done < <( git ls-tree -r --name-only HEAD | grep "\(.py\|\.sh\)$" )

