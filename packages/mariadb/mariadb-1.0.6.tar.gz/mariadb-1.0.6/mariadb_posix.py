#!/usr/bin/env python

import subprocess
from distutils.version import StrictVersion
import sys, os
# from packaging import version


class MariaDBConfiguration():
    lib_dirs = []
    libs = []
    version = []
    includes = []
    extra_objects = []
    extra_compile_args = []
    extra_link_args = []


def mariadb_config(config, option):
    from os import popen
    file = popen("%s --%s" % (config, option))
    data = file.read().strip().split()
    rc = file.close()
    if rc:
        if rc / 256:
            data = []
        if rc / 256 > 1:
            raise EnvironmentError(
                "mariadb_config not found.\n\nPlease make sure, that MariaDB Connector/C is installed on your system.\n"
                "Either set the environment variable MARIADB_CONFIG or edit the configuration\n"
                "file 'site.cfg' and set the 'mariadb_config option, which should point\n"
                "to the mariadb_config utility.\n"
                "The MariaDB Download website at <https://downloads.mariadb.com/Connectors/c/>\n"
                "provides latest stable releease of Connector/C.")
    return data


def dequote(s):
    if s[0] in "\"'" and s[0] == s[-1]:
        s = s[1:-1]
    return s


def get_config(options):
    required_version = "3.1.5"
    no_env = 0
    static = options["link_static"]

    try:
        try:
            config_prg= os.environ["MARIADB_CONFIG"]
        except KeyError:
            config_prg = options["mariadb_config"]
        subprocess.call([config_prg, "--version"])
    except FileNotFoundError:
        # using default from path
        config_prg = "mariadb_config"

    cc_version = mariadb_config(config_prg, "cc_version")
    if StrictVersion(cc_version[0]) < StrictVersion(required_version):
        print ('MariaDB Connector/Python requires MariaDB Connector/C >= %s, found version %s' % (
            required_version, cc_version[0]))
        sys.exit(2)
    cfg = MariaDBConfiguration()
    cfg.version = cc_version[0]

    plugindir= mariadb_config(config_prg, "plugindir")
    libs = mariadb_config(config_prg, "libs")
    extra_libs= mariadb_config(config_prg, "libs_sys")
    cfg.lib_dirs = [dequote(i[2:]) for i in libs if i.startswith("-L")]

    cfg.libs = [dequote(i[2:]) for i in libs if i.startswith("-l")]
    includes = mariadb_config(config_prg, "include")
    mariadb_includes = [dequote(i[2:]) for i in includes if i.startswith("-I")]
    mariadb_includes.extend(["./include"])
    if static.lower() == "on":
        cfg.extra_link_args= ["-u mysql_ps_fetch_functions"]
        cfg.extra_objects = ['{}/lib{}.a'.format(cfg.lib_dirs[0], l) for l in ["mariadbclient"]]
        cfg.libs = [dequote(i[2:]) for i in extra_libs if i.startswith("-l")]
    cfg.includes = mariadb_includes
    cfg.extra_compile_args= ["-DDEFAULT_PLUGINS_SUBDIR=\"%s\"" % plugindir[0]]
    return cfg
