from setuptools import setup, find_packages

with open('README.md', 'r') as readme:
    documentation = readme.read()

if __name__ == '__main__':
    setup(name='MorseCodePy',
          packages=find_packages(),
          requires=['pygame'],
          package_data={'MorseCodePy': ['sounds/*.wav']},
          include_package_data=True,
          version='3.1',
          author='CrazyFlyKite',
          author_email='karpenkoartem2846@gmail.com',
          url='https://github.com/CrazyFlyKite/MorseCodePy/',
          description='Encode, Decode & Play Morse Code Easily',
          long_description=documentation,
          long_description_content_type='text/markdown'
          )
