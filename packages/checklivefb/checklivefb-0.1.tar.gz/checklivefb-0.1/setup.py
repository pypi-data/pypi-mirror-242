from setuptools import setup, find_packages
 
classifiers = [
  'Development Status :: 5 - Production/Stable',
  'Intended Audience :: Education',
  'Operating System :: Microsoft :: Windows :: Windows 10',
  'License :: OSI Approved :: MIT License',
  'Programming Language :: Python :: 3'
]
 
setup(
  name='checklivefb',
  version='0.1',
  description='Công cụ check live uid Facebook',
  long_description=open('README.txt',encoding='utf-8').read() + '\n\n' + open('CHANGELOG.txt',encoding='utf-8').read(),
  url='',  
  author='lam nioai',
  author_email='ldl.contact.booking@gmail.com',
  license='MIT', 
  classifiers=classifiers,
  keywords='check live', 
  packages=find_packages(),
  install_requires=[''] 
)