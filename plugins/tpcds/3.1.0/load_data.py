# coding: utf-8
# OceanBase Deploy.
# Copyright (C) 2021 OceanBase
#
# This file is part of OceanBase Deploy.
#
# OceanBase Deploy is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# OceanBase Deploy is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with OceanBase Deploy.  If not, see <https://www.gnu.org/licenses/>.


from __future__ import absolute_import, division, print_function


import re
import os
import time
from glob import glob
try:
    import subprocess32 as subprocess
except:
    import subprocess
from ssh import LocalClient
from tool import DirectoryUtil


def load_data(plugin_context, *args, **kwargs):
    def get_option(key, default=''):
        value = getattr(options, key, default)
        if value is None:
            value = default
        return value

    def local_execute_command(command, env=None, timeout=None):
        return LocalClient.execute_command(command, env, timeout, stdio)

    cluster_config = plugin_context.cluster_config
    stdio = plugin_context.stdio
    options = plugin_context.options
    clients = plugin_context.clients

    database = get_option('database')
    user = get_option('user')
    tenant_name = get_option('tenant')
    tenant_mode = get_option('mode')
    password = get_option('password')
    obclient_bin = get_option('obclient_bin')

    ddl_path = get_option('ddl_path')
    sql_path = get_option('sql_path')
    query_tpl = get_option('query_tpl')
    tmp_dir = get_option('tmp_dir')
    query_tpl = get_option('query_tpl')
    remote_dir = get_option('remote_dir')
    scale = get_option('scale')
    dsdgen_bin = get_option('dsdgen_bin')
    dsqgen_bin = get_option('dsqgen_bin')
    idx_file = get_option('idx_file')
    generate_parallel = get_option('generate_parallel')
    remote_dsdgen_bin = os.path.join(remote_dir, 'dsdgen')
    remote_idx_file = os.path.join(remote_dir, 'tpcds.idx')
    remote_data_dir = os.path.join(remote_dir, '%sG' % scale)

    if not sql_path:
        sql_path = []
        stdio.start_loading('Generate queries')
        sql_dir = os.path.join(tmp_dir, 'queries/%s' % tenant_mode)
        dialect = 'netezza' if tenant_mode == 'mysql' else tenant_mode
        idx_file_dir = os.path.dirname(idx_file)
        if not DirectoryUtil.mkdir(sql_dir, stdio=stdio):
            return
        for path in query_tpl:
            tpl_dir, tpl_name = os.path.split(path)
            sql_file = os.path.join(sql_dir, tpl_name.split('.')[0] + '.sql')
            ret = local_execute_command('cd %s; %s -DIRECTORY %s -TEMPLATE %s -DIALECT %s -FILTER Y > %s' % (idx_file_dir, dsqgen_bin, tpl_dir, tpl_name, dialect, sql_file))
            if not ret:
                stdio.error(ret.stderr)
                stdio.stop_loading('fail')
                return
            sql_path.append(sql_file)
        stdio.verbose('set sql_path: %s' % sql_path)
        setattr(options, 'sql_path', sql_path)
        stdio.stop_loading('succeed')

    if get_option('test_only'):
        return plugin_context.return_true()
        
    stdio.start_loading('Generate prepare')
    for server in cluster_config.servers:
        client = clients[server]
        if not client.put_file(dsdgen_bin, remote_dsdgen_bin) or not client.put_file(idx_file, remote_idx_file) or not client.execute_command('mkdir -p %s' % remote_data_dir):
            stdio.stop_loading('fail')
            return 
    stdio.stop_loading('succeed')

    get_table_cmd = "ls *.dat | grep -e '^[a-z_]*[a-z]' -o"
    if generate_parallel > 1:
        gen_cmd = 'cd %s; %s -scale %s -dir %s -parallel %s -child {child} -force Y' % (remote_dir, remote_dsdgen_bin, scale, remote_data_dir, generate_parallel)
    else:
        gen_cmd = 'cd %s; %s -scale %s -dir %s -force Y' % (remote_dir, remote_dsdgen_bin, scale, remote_data_dir)
    load_cmd = """cd %s; fs=`ls *.dat`; cpu=`grep -e 'processor\s*:' /proc/cpuinfo | wc -l`; for fn in ${fs[@]}; do table=`echo $fn | grep -e '^[a-z_]*[a-z]' -o`; fp=%s/$fn; echo "load $fp"; %%s -c -e "load data /*+ parallel($cpu) */ infile '$fp' into table $table fields terminated by '|';" ; done""" % (remote_data_dir, remote_data_dir)

    sql_cmd_temp = '%s -h{host} -P{port} -u%s@%s %s -A' % (obclient_bin, user, tenant_name, ("-p'%s'" % password) if password else '')
    if tenant_mode == 'mysql':
        sql_cmd_temp += ' -D %s' % database
    server = cluster_config.servers[0]
    sql_cmd_prefix = sql_cmd_temp.format(host=server.ip, port=cluster_config.get_server_conf(server).get('mysql_port'))

    stdio.start_loading('Create table')
    create_foreign_key = get_option('create_foreign_key', False)
    if get_option('create_foreign_key'):
        ddl_path.append(get_option('foreign_key_file'))
    start_time = time.time()
    for path in ddl_path:
        path = os.path.abspath(path)
        stdio.verbose('load %s' % path)
        ret = local_execute_command('%s < %s' % (sql_cmd_prefix, path))
        if not ret:
            stdio.stop_loading('fail')
            raise Exception(ret.stderr)
    stdio.stop_loading('succeed', text='Create table %.1fs' % (time.time() - start_time))

    concurrent_executor = plugin_context.concurrent_executor
    concurrent_executor.workers = generate_parallel

    if not get_option('disable_generate', False):
        stdio.start_loading('Generate Data (Scale: %s)' % scale)
        idx = 0
        server_num = len(cluster_config.servers)
        while idx < generate_parallel:
            server = cluster_config.servers[idx % server_num]
            idx += 1
            client = clients[server]
            concurrent_executor.add_task(client, gen_cmd.format(child=idx), timeout=86400)
        start_time = time.time()
        results = concurrent_executor.submit()
        if not all(results):
            for ret in results:
                if not ret:
                    stdio.error('(%s) %s' % (ret.client, ret.stdout))
            stdio.stop_loading('fail')
            return
        stdio.stop_loading('succeed', text='Generate Data (Scale: %s) %.1fs' % (scale, time.time() - start_time))


    stdio.start_loading('Load data')
    
    if tenant_mode == 'mysql':
        ret = local_execute_command('%s -e "SET GLOBAL secure_file_priv = \\"\\";"' % sql_cmd_prefix)
        if not ret:
            stdio.error(ret.stderr)
            stdio.stop_loading('fail')
            return 
    for server in cluster_config.servers:
        client = clients[server]
        sql_cmd_prefix = sql_cmd_temp.format(host=server.ip, port=cluster_config.get_server_conf(server).get('mysql_port'))
        concurrent_executor.add_task(client, load_cmd % sql_cmd_prefix, timeout=86400)
    start_time = time.time()
    results = concurrent_executor.submit()
    if not all(results):
        for ret in results:
            if not ret:
                stdio.error('(%s) %s' % (ret.client, ret.stdout))
        stdio.stop_loading('fail')
        return
    stdio.stop_loading('succeed', text='Load data %.1fs' % (time.time() - start_time))

    return plugin_context.return_true()

