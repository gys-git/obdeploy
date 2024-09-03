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
from glob import glob
try:
    import subprocess32 as subprocess
except:
    import subprocess
from ssh import LocalClient
from tool import DirectoryUtil


def check_opt(plugin_context, db_cluster_config, *args, **kwargs):
    def get_option(key, default=''):
        value = getattr(options, key, default)
        if not value:
            value = default
        stdio.verbose('get option: %s value %s' % (key, value))
        return value

    def get_path(key, default):
        path = get_option('%s_path' % key)
        if path and os.path.exists(path):
            if os.path.isfile(path):
                path = [path]
            else:
                path = glob(os.path.join(path, '*.%s' % key))
        stdio.verbose('get %s_path: %s' % (key, path))
        return path if path else default

    def local_execute_command(command, env=None, timeout=None):
        return LocalClient.execute_command(command, env, timeout, stdio)

    cluster_config = plugin_context.cluster_config
    stdio = plugin_context.stdio
    options = plugin_context.options
    clients = plugin_context.clients

    stdio.start_loading('Check Options')

    local_dir, _ = os.path.split(__file__)
    tool_dir = get_option('tool_dir', '/usr/tpc-ds-tools')
    dsdgen_bin = get_option('dsdgen_bin', os.path.join(tool_dir, 'bin/dsdgen'))
    idx_file = get_option('idx_file', os.path.join(tool_dir, 'bin/tpcds.idx'))
    dsdgen_bin = get_option('dsdgen_bin', os.path.join(tool_dir, 'bin/dsdgen'))
    dsqgen_bin = get_option('dsqgen_bin', os.path.join(tool_dir, 'bin/dsqgen'))
    query_templates_dir = get_option('query_templates_dir', os.path.join(tool_dir, 'query_templates'))
    scale = get_option('scale', 1)
    remote_dir = get_option('remote_dir')
    generate_parallel = get_option('generate_parallel', len(db_cluster_config.servers))
    tenant_mode = get_option('mode', 'mysql')
    tenant_name = get_option('tenant', 'test')
    if tenant_name == 'sys':
        stdio.error('DO NOT use sys tenant for testing.')
        stdio.stop_loading('fail')
        return 
        
    database = get_option('database', 'test')
    user = get_option('user', 'root' if tenant_mode == 'mysql' else 'SYS')
    tenant_name = get_option('tenant', 'test')
    password = get_option('password', '')
    test_server = get_option('test_server')
    test_only = get_option('test_only', False)
    create_foreign_key = get_option('create_foreign_key', False)
    foreign_key_file = get_option('foreign_key_file', os.path.join(local_dir, 'tpcds_ri.sql'))
    ddl_path = get_path('ddl', [os.path.join(local_dir, 'create_tpcds_%s_table_part.ddl' % tenant_mode)])
    sql_path = get_path('sql', [])
    tmp_dir = os.path.abspath(get_option('tmp_dir', './tmp'))
    obclient_bin = get_option('obclient_bin', 'obclient')

    ret = local_execute_command('%s --help' % obclient_bin)
    if not ret:
        stdio.error('%s\n%s is not an executable file. Please use `--obclient-bin` to set.\nYou may not have obclient installed' % (ret.stderr, obclient_bin))
        stdio.stop_loading('fail')
        return
    stdio.verbose('set obclient_bin: %s' % obclient_bin)
    setattr(options, 'obclient_bin', obclient_bin)
    
    if not DirectoryUtil.mkdir(tmp_dir, stdio=stdio):
        stdio.stop_loading('fail')
        return
    stdio.verbose('set tmp_dir: %s' % tmp_dir)
    setattr(options, 'tmp_dir', tmp_dir)

    port_key = 'mysql_port' if cluster_config.name.startswith('oceanbase') else "listen_port"
    host = test_server.ip
    port = cluster_config.get_server_conf(test_server).get(port_key)
    sql_cmd_prefix = '%s -h%s -P%s -u%s@%s %s -A' % (obclient_bin, host, port, user, tenant_name, ("-p'%s'" % password) if password else '')
    if tenant_mode != 'mysql':
        ret = local_execute_command("%s -e 'select * from v$version;'" % (sql_cmd_prefix))
    elif test_only:
        ret = local_execute_command('%s -D %s -e "select version()"' % (sql_cmd_prefix, database))
    else:
        ret = local_execute_command('%s -e "%s"' % (sql_cmd_prefix, 'create database if not exists %s' % database))
    if not ret:
        stdio.error(ret.stderr)
        stdio.stop_loading('fail')
        return

    stdio.verbose('set host: %s' % host)
    setattr(options, 'host', host)
    stdio.verbose('set port: %s' % port)
    setattr(options, 'port', port)
    stdio.verbose('set tenant: %s' % tenant_name)
    setattr(options, 'tenant', tenant_name)
    stdio.verbose('set mode: %s' % tenant_mode)
    setattr(options, 'mode', tenant_mode)
    stdio.verbose('set database: %s' % database)
    setattr(options, 'database', database)
    stdio.verbose('set user: %s' % user)
    setattr(options, 'user', user)
    stdio.verbose('set password: %s' % password)
    setattr(options, 'password', password)
    
    if test_only:
        sql_path = []
        for path in get_path('sql', glob(os.path.join(tmp_dir, 'queries/%s/*.sql' % tenant_mode))):
            if re.search('\d+', path):
                sql_path.append(path)
            else:
                stdio.verbose('drop sql file: %s' % sql_path)
        stdio.verbose('set sql_path: %s' % sql_path)
        setattr(options, 'sql_path', sql_path)
        if sql_path:
            stdio.stop_loading('succeed')
            return plugin_context.return_true()

    if create_foreign_key:
        if not foreign_key_file:
            stdio.error('Not such file %s.\nPlease use --foreign-key-file to set a sql file for createing foregin key' % foreign_key_file)
            stdio.stop_loading('fail')
            return 
        setattr(options, 'foreign_key_file', foreign_key_file)
        stdio.verbose('set password: %s' % foreign_key_file)
    setattr(options, 'create_foreign_key', create_foreign_key)
    stdio.verbose('set create_foreign_key: %s' % create_foreign_key)
        
    if not sql_path:
        query_tpl = glob(os.path.join(query_templates_dir, '*.tpl'))
        if not query_tpl:
            stdio.error('Not found tpl file in %s.\nPlease use --query-templates-dir to set a dir for query templates' % query_templates_dir)
            stdio.stop_loading('fail')
            return 
        stdio.verbose('set query_tpl: %s' % query_tpl)
        setattr(options, 'query_tpl', query_tpl)

    if not sql_path:
        ret = local_execute_command('%s -h' % dsqgen_bin)
        if ret.code > 1:
            stdio.error('%s\n%s is not an executable file. Please use `--dsqgen-bin` to set.\nYou may not have obtpch installed' % (ret.stderr, dsqgen_bin))
            stdio.stop_loading('fail')
            return
        stdio.verbose('set dsqgen_bin: %s' % dsqgen_bin)
        setattr(options, 'dsqgen_bin', dsqgen_bin)
        

    if not sql_path or not test_only:
        if not remote_dir:
            stdio.error('Please use --remote-dir to set a dir for remote data files')
            stdio.stop_loading('fail')
            return

        stdio.verbose('set ddl_path: %s' % ddl_path)
        setattr(options, 'ddl_path', ddl_path)

        if not os.path.exists(idx_file):
            stdio.error('No such file: %s' % idx_file)
            stdio.stop_loading('fail')
            return
        stdio.verbose('set idx_file: %s' % idx_file)
        setattr(options, 'idx_file', idx_file)
        
    if not test_only:
        if scale < 1:
            stdio.error('scale must be > 0')
            stdio.stop_loading('fail')
            return
        stdio.verbose('set scale: %s' % scale)
        setattr(options, 'scale', scale)

        if generate_parallel < 0:
            stdio.error('generate-parallel must be >= 0')
            stdio.stop_loading('fail')
            return
        stdio.verbose('set generate_parallel: %s' % generate_parallel)
        setattr(options, 'generate_parallel', generate_parallel)
        
        ret = local_execute_command('%s -h' % dsdgen_bin)
        if ret.code > 1:
            stdio.error('%s\n%s is not an executable file. Please use `--dsdgen-bin` to set.\nYou may not have obtpch installed' % (ret.stderr, dsdgen_bin))
            stdio.stop_loading('fail')
            return
        stdio.verbose('set dsdgen_bin: %s' % dsdgen_bin)
        setattr(options, 'dsdgen_bin', dsdgen_bin)

    stdio.stop_loading('succeed')
    return plugin_context.return_true()
