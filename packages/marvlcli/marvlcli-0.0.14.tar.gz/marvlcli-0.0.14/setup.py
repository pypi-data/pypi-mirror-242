from setuptools import find_packages, setup

setup(
    name="marvlcli",
    version='0.0.14',
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
    data_files=[('yaml', ['./payloads.yaml']), ('txt', ['./myuserdata_marv_default.txt'])],
    entry_points='''
    [console_scripts]
    marvl=marvlcli:marvlcli
    
    
    '''
    
)

