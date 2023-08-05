from distutils.core import setup
from setuptools import setup, find_packages
from configparser import ConfigParser

# note: all settings are in settings.ini; edit there, not here
config = ConfigParser(delimiters=['='])
config.read('settings.ini')
cfg = config['DEFAULT']

cfg_keys = 'version description keywords author author_email'.split()
expected = cfg_keys + "lib_name user branch license status min_python audience language".split()
for o in expected: assert o in cfg, "missing expected setting: {}".format(o)
setup_cfg = {o:cfg[o] for o in cfg_keys}

statuses = [ '1 - Planning', '2 - Pre-Alpha', '3 - Alpha',
    '4 - Beta', '5 - Production/Stable', '6 - Mature', '7 - Inactive' ]
py_versions = '2.0 2.1 2.2 2.3 2.4 2.5 2.6 2.7 3.0 3.1 3.2 3.3 3.4 3.5 3.6 3.7 3.8'.split()
min_python = cfg['min_python']

licenses = {
    'apache2': ('Apache Software License 2.0','OSI Approved :: Apache Software License'),
}

lic = licenses[cfg['license']]

requirements = ['pip', 'packaging']
if cfg.get('requirements'): requirements += cfg.get('requirements','').split()
if cfg.get('pip_requirements'): requirements += cfg.get('pip_requirements','').split()
dev_requirements = (cfg.get('dev_requirements') or '').split()



setup(
    name = cfg['lib_name'],
    license = lic[0],
    classifiers = [
        'Development Status :: ' + statuses[int(cfg['status'])],
        'Intended Audience :: ' + cfg['audience'].title(),
        'License :: ' + lic[1],
        'Natural Language :: ' + cfg['language'].title(),
    ] + ['Programming Language :: Python :: '+o for o in py_versions[py_versions.index(min_python):]],
    # description = 'many function for myself to advance my coding',
    long_description = open(cfg['long_description'],'r',encoding='utf8').read(),
    long_description_content_type = 'text/markdown',
    python_require=">=3.5",
    install_requires = requirements,
    extras_require={ 'dev': dev_requirements },
    packages = find_packages("src"),# 需要打包的package,使用find_packages 来动态获取package，exclude参数的存在，使打包的时候，排除掉这些文件
    platforms = 'any',
    package_dir={"":"src"},
    entry_points = { 'console_scripts': cfg.get('console_scripts','').split() },
    include_package_data = True,
    **setup_cfg
)