from distutils.core import setup
setup(
    name = 'simusys',
    packages = ['simusys'],
    version = '0.1',
    license='New BSD',
    description = 'Dynamic System Simulation',
    author = 'Mostapha Kalami Heris',
    author_email = 'sm.kalami@gmail.com',
    url = 'https://github.com/smkalami/simusys',
    download_url = 'https://github.com/smkalami/simusys',
    keywords = ['Simulation', 'Dynamic Systems'],
    install_requires=[
        'numpy',
    ],
    classifiers=[
        "Development Status :: 3 - Alpha",
        "License :: OSI Approved",
        "Intended Audience :: Science/Research",
        "Intended Audience :: Developers",
        "Topic :: Software Development",
        "Topic :: Scientific/Engineering",
        "Programming Language :: Python",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
    ],
)
