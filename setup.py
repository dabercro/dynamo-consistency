import glob
import setuptools

import dynamo_consistency

setuptools.setup(
    name='dynamo-consistency',
    version=dynamo_consistency.__version__,
    packages=setuptools.find_packages(),
    author='Daniel Abercrombie',
    author_email='dabercro@mit.edu',
    description='Consistency plugin for Dynamo',
    url='https://github.com/SmartDataProjects/dynamo-consistency',
    install_requires=['pyyaml',
                      'docutils',
                      'customdocs>=0.2',
                      'cmstoolbox>=0.9.8'],  # Older version has slow unmerged cleaner
    scripts=[s for s in glob.glob('bin/*') if not s.endswith('~')],
    python_requires='>=2.6, <3',
    package_data={   # Test data for document building
        'dynamo_consistency': ['consistency_config.json',
                               'locks/gfal.lock',
                               'web/*']
        }
    )
