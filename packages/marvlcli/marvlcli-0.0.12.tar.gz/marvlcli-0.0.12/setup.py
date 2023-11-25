from setuptools import find_packages, setup

setup(
    name="marvlcli",
    version='0.0.12',
    py_modules= ['marvlcli','info','ssh','list', 'create', 'delete', 'client'],
    packages=find_packages(),
    install_requires=[
        'click',
        'pyyaml',
        'python-novaclient',
        'python-cinderclient',
        'python-neutronclient',
        'python-openstackclient',
        'ws4py'
        
    ],
    data_files=[('yaml', ['payloads.yaml'])],
    entry_points='''
    [console_scripts]
    marvl=marvlcli:marvlcli
    
    
    '''
    
)

