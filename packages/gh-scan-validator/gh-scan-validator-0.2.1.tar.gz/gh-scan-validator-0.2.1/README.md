# greeHill TSE Scan input validator

## Set up for development

* Install Python >=3.7
* Install laszip

```bash
git clone https://github.com/LASzip/LASzip.git &&  cd LASzip && cmake . && make -j6 && make install
git clone https://github.com/LAStools/LAStools.git && cd LAStools && make -j6 && cp bin/laszip /usr/local/bin
```

```bash
pip install -e .
```

## Use

```bash
python -m tse_scan_validator.mls
```

## Release

```bash
python setup.py sdist bdist_wheel
twine upload dist/*
```
