from setuptools import setup, find_packages

setup(
    name='esr_dt_model',
    version='0.0.4',
    packages=find_packages(),
    install_requires=[
        "dask",
        "dask[distributed]",
        "pygrib",
        "numpy"
    ],
    entry_points={
        'console_scripts': [
            'esr_dt_model=esr_dt_model.esr_dt_model:write_to_file',
        ],
    },
)