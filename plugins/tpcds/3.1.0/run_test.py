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
from ssh import LocalClient
from _rpm import Version
from tool import DirectoryUtil

stdio = None


def run_test(plugin_context, *args, **kwargs):
    def get_option(key, default=''):
        value = getattr(options, key, default)
        if value is None:
            value = default
        return value

    def local_execute_command(command, env=None, timeout=None):
        return LocalClient.execute_command(command, env, timeout, stdio)

    global stdio
    cluster_config = plugin_context.cluster_config
    stdio = plugin_context.stdio
    clients = plugin_context.clients
    options = plugin_context.options

    sql_path = get_option('sql_path')
    tmp_dir = get_option('tmp_dir')

    test_server = get_option('test_server')
    database = get_option('database')
    user = get_option('user')
    tenant_name = get_option('tenant')
    tenant_mode = get_option('mode')
    password = get_option('password')
    obclient_bin = get_option('obclient_bin')
    port_key = 'mysql_port' if cluster_config.name.startswith('oceanbase') else "listen_port"
    sql_cmd_temp = '%s -h{host} -P{port} -u%s@%s %s -A %s' % (obclient_bin, user, tenant_name, ("-p'%s'" % password) if password else '', '-D ' + database if tenant_mode == 'mysql' else '')
    sql_cmd_prefix = sql_cmd_temp.format(host=test_server.ip, port=cluster_config.get_server_conf(test_server).get(port_key))
    log_dir = os.path.join(tmp_dir, 'log/%s' % tenant_mode)

    if not DirectoryUtil.mkdir(log_dir, stdio=stdio):
        return
    
    sqls = [
        'set global ob_query_timeout=100000000000;',
        'set global ob_trx_timeout=10000000000;'
    ]
    if tenant_name == 'oracle':
        sqls.append('alter system set NLS_DATE_FORMAT = \'YYYY-MM-DD HH24:MI:SS\';')
    for sql in sqls:
        ret = local_execute_command('%s -e "%s"' % (sql_cmd_prefix, sql))
        if not ret:
            stdio.error(ret.stderr)
            return

    total_cost = 0
    result = []
    failed_num = 0
    sql_path = sorted(sql_path, key=lambda path: [int(n) for n in re.findall('\d+', path)])
    for path in sql_path:
        _, fn = os.path.split(path)
        log_path = os.path.join(log_dir, '%s.log' % fn)
        start_time = time.time()
        stdio.print('[%s]: start %s' % (time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(start_time)), path))
        ret = local_execute_command('echo source %s | %s -c > %s' % (path, sql_cmd_prefix, log_path))
        end_time = time.time()
        cost = end_time - start_time
        total_cost += cost
        stdio.print('[%s]: end %s, cost %.1fs' % (time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(end_time)), path, cost))
        if ret:
            result.append([fn, '%.1fs' % cost])
        else:
            failed_num += 1
            result.append([fn, 'Failed'])
            stdio.warn(ret.stderr)
    stdio.print_list(result, ['query', 'cost'], title='Result list')
    stdio.print('Total Cost: %.1fs,  Failed: %s' % (total_cost, failed_num))
    return plugin_context.return_true()
