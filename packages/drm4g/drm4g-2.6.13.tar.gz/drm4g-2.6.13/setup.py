#
# Copyright 2021 Santander Meteorology Group (UC-CSIC)
#
# Licensed under the EUPL, Version 1.1 only (the 
# "Licence"); 
# You may not use this work except in compliance with the
# Licence.
# You may obtain a copy of the Licence at:
#
# http://ec.europa.eu/idabc/eupl
#
# Unless required by applicable law or agreed to in
# writing, software distributed under the Licence is
# distributed on an "AS IS" basis,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either
# express or implied.
# See the Licence for the specific language governing
# permissions and limitations under the Licence.
#

from setuptools import setup
from setuptools import find_packages
from setuptools.command.install import install
from os import path
import os
import subprocess
import glob
import sys
import ast
import drm4g

#To ensure a script runs with a minimal version requirement of the Python interpreter
#assert sys.version_info >= (2,5)
if (sys.version_info[0]==2 and sys.version_info<=(2,5)) or (sys.version_info[0]==3 and sys.version_info<(3,3)):
    exit( 'The version number of Python has to be >= 2.6 or >= 3.3' )

try: 
    input = raw_input
except NameError:
    pass

here = path.abspath(path.dirname(__file__))
python_ver=sys.version[:3]
user_shell=os.environ['SHELL']
lib_dir=''
path_dir=''

#I consider bash a special case because of what is said here http://superuser.com/questions/49289/what-is-the-bashrc-file
if 'bash' in user_shell:
    user_shell='.bashrc'
else:
    user_shell='.profile' #maybe for zsh it should be ~/.zprofile

# read the contents of your README file
with open(path.join(here, 'README'), encoding='utf-8') as f:
    long_description = f.read()

def yes_no_choice( message,  default = 'y') :
    """
    Ask for Yes/No questions
    """
    choices = 'y/n' if default.lower() in ( 'y', 'yes' ) else 'y/N'
    values = ( 'y', 'yes', 'n', 'no' )
    choice = ''
    while not choice.strip().lower() in values:
        choice = input("{} ({}) \n".format(message, choices))
    return choice.strip().lower()

class Builder(object):

    export_dir=sys.prefix
    prefix_directory=''
    arguments=str(sys.argv)
    arguments=ast.literal_eval(arguments) #convert from string to list

    def call(self, cmd):
        return subprocess.call(cmd, shell=True)

    def prefix_option(self):
        #Going through the whole list since the options can be defined in different ways (--prefix=dir> or --prefix <dir>)
        #Which is why I'm not using self.arguments.index('--prefix') to find it, since it doesn't check if it's a substring
        #Could also do it with a while and make it stop if it finds '--prefix' or '--home'
        for i in range(len(self.arguments)):
            option=self.arguments[i]
            #folder name can't contain '--prefix' or '--home'
            if '--prefix' in option or '--home' in option:
                #I'm working under the impression that the path passed on to prefix has to be an absolute path
                #for the moment, if you use a relative path, gridway's binary files will be copied to a directory relative to where ./gridway-5.8 is
                if '=' in option:
                    self.export_dir=option[option.find('=')+1:]
                    self.prefix_directory='--prefix '+self.export_dir
                else:
                    self.export_dir=self.arguments[i+1]
                    self.prefix_directory='--prefix '+self.export_dir

                global lib_dir
                global path_dir
                if '--prefix' in option:
                    lib_dir=os.path.join(self.export_dir,'lib/python{}/site-packages'.format(python_ver))
                elif '--home' in option:
                    lib_dir=os.path.join(self.export_dir,'lib/python')

                path_dir=os.path.join(self.export_dir,'bin')

                try:
                    os.makedirs(lib_dir)
                except OSError:
                    print('\nDirectory {} already exists'.format(lib_dir))

                message="\nWe are about to modify your {} file.\n" \
                    "If we don't you'll have to define the environment variables PATH and PYTHONPATH" \
                    " or access your installation directory everytime you wish to execute DRM4G.\n" \
                    "Should we proceed?".format(user_shell)

                ans=yes_no_choice(message)
                if ans[0]=='y':
                    line_exists=False
                    home=os.path.expanduser('~') #to ensure that it will find $HOME directory in all platforms
                    python_export_line='export PYTHONPATH={}:$PYTHONPATH'.format(lib_dir)
                    path_export_line='export PATH={}:$PATH'.format(path_dir)

                    with open('{}/{}'.format(home,user_shell),'r') as f:
                        for i in f.readlines():
                            if python_export_line in i:
                                line_exists=True

                    if not line_exists :
                        with open('{}/{}'.format(home,user_shell),'a') as f:
                            f.write('\n'+python_export_line+'\n'+path_export_line+'\n')

    def build(self):
        gridway=path.join( here, "gridway-5.8")
        current_path = os.getcwd()

        self.prefix_option()
        
        if not path.exists(gridway) :
            raise Exception("The specified directory %s doesn't exist" % gridway)

        os.chdir( gridway )

        exit_code = self.call( 'chmod +x ./configure && ./configure' )
        if exit_code:
            raise Exception("Configure failed - check config.log for more detailed information")
        
        exit_code = self.call('make')
        if exit_code:
            raise Exception("make failed")

        os.chdir( current_path )


class build_wrapper(install):
    def run(self):
        Builder().build()
        install.run(self)

bin_scripts= glob.glob(os.path.join('bin', '*'))
bin_scripts.append('LICENSE')

setup(
    name='drm4g',
    packages=find_packages(),
    include_package_data=True,
    package_data={'drm4g' : ['conf/*.conf', 'conf/job_template.default', 'conf/*.sh']},
    data_files=[('bin', [
        'gridway-5.8/src/cmds/gwuser', 'gridway-5.8/src/cmds/gwacct', 'gridway-5.8/src/cmds/gwwait', 
        'gridway-5.8/src/cmds/gwhost', 'gridway-5.8/src/cmds/gwhistory', 'gridway-5.8/src/cmds/gwsubmit', 
        'gridway-5.8/src/cmds/gwps', 'gridway-5.8/src/cmds/gwkill', 'gridway-5.8/src/gwd/gwd', 
        'gridway-5.8/src/scheduler/gw_flood_scheduler', 'gridway-5.8/src/scheduler/gw_sched'])],
    version=drm4g.__version__,
    author='Santander Meteorology Group (UC-CSIC)',
    author_email='antonio.cofino@unican.es',
    url='https://meteo.unican.es/trac/wiki/DRM4G',
    license='European Union Public License 1.1',
    description='DRM4G is an open platform for DCIs.',
    long_description=long_description,
    long_description_content_type='text/markdown',
    classifiers=[
        "Intended Audience :: Science/Research",
        "Programming Language :: Python",
        "Topic :: Scientific/Engineering",
        "Topic :: Office/Business :: Scheduling",
        "Programming Language :: Python :: 2.6",
        "Programming Language :: Python :: 2.7",
        "Programming Language :: Python :: 3.3",
        "Programming Language :: Python :: 3.4",
        "Programming Language :: Python :: 3.5",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
    ],
    install_requires=['fabric', 'docopt', 'openssh-wrapper'],
    scripts=bin_scripts,
    cmdclass={
        'install': build_wrapper,
    },
)

if lib_dir:
    print('\n\033[93mTo finish with the installation, you have to add the following paths to your $PYTHONPATH and $PATH:\e[0m\n' \
        '    export PYTHONPATH={}:$PYTHONPATH\n' \
        '    export PATH={}:$PATH\033[0m'.format(lib_dir,path_dir))
