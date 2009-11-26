_SCHEME = {
    'unix': {
        'prefix': '/usr/local',
        'eprefix': '$prefix',
        'bindir': '$eprefix/bin',
        'sbindir': '$eprefix/sbin',
        'libdir': '$eprefix/lib',
        'includedir': '$prefix/include',
        'datarootdir': '$prefix/share',
        'datadir': '$datarootdir',
        'mandir': '$datarootdir/man',
    }
}

_SCHEME_OPTS = {
    'prefix': {'opts': ['--prefix'],
               'help': 'install architecture-independent files '
                       'in PREFIX [%s]'},
    'eprefix': {'opts': ['--exec-prefix'],
               'help': 'install architecture-dependent files '
                       'in EPREFIX [%s]'},
    'bindir': {'opts': ['--bindir'],
               'help': 'user executables [%s]'},
    'sbindir': {'opts': ['--sbindir'],
               'help': 'system admin executables [%s]'},
    'libdir': {'opts': ['--libdir'],
               'help': 'object code library [%s]'},
    'includedir': {'opts': ['--includedir'],
               'help': 'C header files [%s]'},
    'datarootdir': {'opts': ['--datarootdir'],
               'help': 'read-only arch.-independent data root [%s]'},
    'datadir': {'opts': ['--datadir'],
               'help': 'read-only arch.-independent data [%s]'},
    'mandir': {'opts': ['--mandir'],
               'help': 'man documentation [%s]'}
}


def get_scheme(platform, pkg_name):
    if platform.startswith('linux'):
        pkg_platform = 'unix'
    else:
        pkg_platform = platform

    try:
        scheme = _SCHEME[pkg_platform]
    except KeyError:
        raise ValueError("Platform %s not yet supported" % platform)

    scheme_opts = {}
    for k, v in _SCHEME_OPTS.items():
        val = _SCHEME_OPTS[k].copy()
        val['help'] = val['help'] % scheme[k]
        scheme_opts[k] = val

    return scheme, scheme_opts