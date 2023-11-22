from setuptools import setup, find_packages

setup(
    author="Amir Motamedi",
    author_email="seyedamirhosein.motamedi@charite.de",
    name='octvol',
    version='0.1.0',
    description="A package to read, write, and crop OCT .vol files.",
    packages=find_packages(),
    install_requires=['numpy'],
    python_requires='>=3.5',
    classifiers=[
        'Development Status :: 4 - Beta',
        'Intended Audience :: Science/Research',
        'License :: OSI Approved :: MIT License',
        'Natural Language :: English',
        'Programming Language :: Python :: 3'
    ]
)
