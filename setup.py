from setuptools import setup

requirements = ['requests']

setup(name='sygicmaps',
      version='0.2.8-dev',
      description='Python client library Sygic maps services.',
      scripts=[],
      url='https://github.com/Sygic/sygic-maps-services-python',
      packages=['sygicmaps'],
      license='MIT',
      platforms='Windows',
      setup_requires=requirements,
      install_requires=requirements,
      classifiers=[
          'Development Status :: 3 - Alpha',
          'Intended Audience :: Developers',
          'Topic :: Software Development',
          'License :: OSI Approved :: MIT License',
          'Programming Language :: Python :: 3.6'
      ])
