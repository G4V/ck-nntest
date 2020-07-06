#! /bin/bash

#
# Copyright (c) 2015-2020 cTuning foundation.
# See CK COPYRIGHT.txt for copyright details.
#
# SPDX-License-Identifier: BSD-3-Clause.
# See CK LICENSE.txt for licensing details.
#
# Installation script for CK packages.
#
# Developer(s): Grigori Fursin, Gavin Simpson
#

# PACKAGE_DIR
# INSTALL_DIR

echo ""
echo "Copying plugins ..."
echo ""

mkdir -p ${INSTALL_DIR}/plugins

cp ${PACKAGE_DIR}/*.py ${INSTALL_DIR}/plugins
echo "${PACKAGE_DIR}" > ${INSTALL_DIR}/packagedir.fdg

