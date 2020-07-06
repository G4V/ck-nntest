#
# Copyright (c) 2017 cTuning foundation.
# See CK COPYRIGHT.txt for copyright details.
#
# SPDX-License-Identifier: BSD-3-Clause.
# See CK LICENSE.txt for licensing details.
#
# Collective Knowledge (individual environment - setup)
#
# Developer: Grigori Fursin, Grigori.Fursin@cTuning.org, http://fursin.net
#

##############################################################################
# setup environment setup

def setup(i):
    """
    Input:  {
              cfg              - meta of this soft entry
              self_cfg         - meta of module soft
              ck_kernel        - import CK kernel module (to reuse functions)

              host_os_uoa      - host OS UOA
              host_os_uid      - host OS UID
              host_os_dict     - host OS meta

              target_os_uoa    - target OS UOA
              target_os_uid    - target OS UID
              target_os_dict   - target OS meta

              target_device_id - target device ID (if via ADB)

              tags             - list of tags used to search this entry

              env              - updated environment vars from meta
              customize        - updated customize vars from meta

              deps             - resolved dependencies for this soft

              interactive      - if 'yes', can ask questions, otherwise quiet
            }

    Output: {
              return       - return code =  0, if successful
                                         >  0, if error
              (error)      - error text if return > 0

              bat          - prepared string for bat file
            }

    """

    import os

    # Get variables
    ck=i['ck_kernel']

    iv=i.get('interactive','')

    env=i.get('env',{})
    cfg=i.get('cfg',{})
    deps=i.get('deps',{})
    tags=i.get('tags',[])
    cus=i.get('customize',{})

    target_d=i.get('target_os_dict',{})
    win=target_d.get('windows_base','')
    remote=target_d.get('remote','')
    mingw=target_d.get('mingw','')
    tbits=target_d.get('bits','')

    envp=cus.get('env_prefix','')
    pi=cus.get('path_install','')

    host_d=i.get('host_os_dict',{})
    sdirs=host_d.get('dir_sep','')

    fp=cus.get('full_path','')
    if fp!='':
       p1=os.path.dirname(fp)
       pi=os.path.dirname(p1)

       cus['path_include']=pi+sdirs+'include'

    ep=cus.get('env_prefix','')
    if pi!='' and ep!='':
       env[ep]=pi

    plugin_name=cus.get('plugin_name')
    model_name=cus.get('model_name')
    impl_name=cus.get('impl_name')

    upn = ep + '_' + model_name.upper() + '_' + impl_name.upper()
    env[upn]=os.path.join(pi, os.path.join('plugins', plugin_name))

    # Calc the soft package to add to the pythonpath
    pdfile = os.path.join(pi, 'packagedir.fdg')
    with open(pdfile, 'r') as f:
        package_dir = f.readline()

    base_dir=package_dir[:package_dir.index('ck-nntest')+9]
    soft_dir=os.path.join(base_dir, 'soft/nntest.plugin')

    env['PYTHONPATH'] = soft_dir + ':${PYTHONPATH}'

    return {'return':0, 'bat': ''}
