from setuptools import setup, find_packages

setup(
  name = 'nfnets-pytorch',
  packages = find_packages(),
  version = '0.0.4',
  license='MIT',
  description = 'NFNets, PyTorch',
  author = 'Vaibhav Balloli',
  author_email = 'balloli.vb@gmail.com',
  url = 'https://github.com/vballoli/nfnets-pytorch',
  keywords = [
    'computer vision',
    'image classification',
    'pytorch',
    'adaptive gradient clipping'
  ],
  install_requires=[
    'torch',
    'torchvision',
  ],
  classifiers=[
    'Development Status :: 4 - Beta',
    'Intended Audience :: Developers',
    'Topic :: Scientific/Engineering :: Artificial Intelligence',
    'License :: OSI Approved :: MIT License',
    'Programming Language :: Python :: 3.6',
    'Programming Language :: Python :: 3.7',
    'Programming Language :: Python :: 3.8',
  ],
)