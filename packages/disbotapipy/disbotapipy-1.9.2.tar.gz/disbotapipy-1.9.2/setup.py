from setuptools import setup
setup(
  name = 'disbotapipy',         # How you named your package folder (MyLib)
  packages = ["disbotapipy"],   # Chose the same as "name"
  version = '1.9.2',      # Start with a small number and increase it with every change you make
  license='MIT',        # Chose a license from here: https://help.github.com/articles/licensing-a-repository
  description = 'A simple Python module for the disbot.top service',   # Give a short description about your library
  author = 'Smirf123',                   # Type in your name
  author_email = 'matthewelert@gmail.com',      # Type in your E-Mail
  url = 'https://github.com/Smirf123/disbotapipy',   # Provide either the link to your github or to your website
  download_url = 'https://github.com/Smirf123/disbotapipy/archive/v1.9.2.tar.gz',    # I explain this later on
  keywords = ['disbot', 'discord', 'bot'],   # Keywords that define your package best
  install_requires=[            # I get to this in a second
          'requests',
      ],
  setup_requires=['wheel'],
  classifiers=[
    'Development Status :: 5 - Production/Stable',      # Chose either "3 - Alpha", "4 - Beta" or "5 - Production/Stable" as the current state of your package
    'Intended Audience :: Developers',      # Define that your audience are developers
    'Topic :: Software Development :: Build Tools',
    'License :: OSI Approved :: MIT License',   # Again, pick a license
    'Programming Language :: Python :: 3',      #Specify which pyhton versions that you want to support
    'Programming Language :: Python :: 3.4',
    'Programming Language :: Python :: 3.5',
    'Programming Language :: Python :: 3.6',
  ],
)
