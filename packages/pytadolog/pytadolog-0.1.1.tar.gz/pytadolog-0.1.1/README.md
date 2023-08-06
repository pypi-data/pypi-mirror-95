# pytadolog: CSV logging for PyTado

``pyadolog`` is a Python module which extends the [``python-tado``](https://github.com/chrism0dwk/PyTado) package so that data can be logged from the Tado web API to a local CSV file.

## Installation
### Note about PyTado
This package requires python-tado to query the TADO web API, however development of the main package appears to have stalled. There are a number of forks available on PyPI with different APIs and varying aliases ([python-tadoac](https://pypi.org/project/python-tadoac/), [python-tado](https://pypi.org/project/python-tado/), [pytado](https://pypi.org/project/pytado/)). This package was developed with ``python-tado`` v0.2.9 cloned directly from GitHub, it has been tested to be compatible with [commit 00a9ab1](https://github.com/chrism0dwk/PyTado/tree/00a9ab12569e84a5537c2a0517c3a6b5cbb9d535).

Therefore, before installing pytadolog you must first install the correct version of pytado. This can be achieved using the package manager [pip](https://pip.pypa.io/en/stable/) as below:
```bash
pip install git+https://git@github.com/chrism0dwk/PyTado.git@00a9ab12569e84a5537c2a0517c3a6b5cbb9d535
```

pip can then be used to install ``pytadolog``.

```bash
pip install pytadolog
```
## Usage
``pytadolog`` includes a helpful console script and can easily be invoked with:

```bash
>>> tadolog
```

Commandline arguments can also be provided to customise ``pytadolog``. These can be explored using:

```bash
>>> tadolog -h

usage: __main__.py [-h] [-o OUTDIR] [--update-period UPDATE_PERIOD]
                   [--last-day LAST_DAY] [-m]

optional arguments:
  -h, --help            show this help message and exit
  -o OUTDIR, --outdir OUTDIR
                        path to output directory
  --update-period UPDATE_PERIOD
                        time in seconds between updates
  --last-day LAST_DAY   last day of week as 3 letter string
  --disable-multiproc   use single process for web query and csv saving
  -d, --debug           log debugging statements to file
  -v, --verbose         log info statements to file
```

### CSV conversion
This package includes a handy script to convert created CSV files to Excel files. Conversion requires [``openpyxl``](https://pypi.org/project/openpyxl/) to be installed. The script can be invoked from the commandline using:
```bash
>>> csv2excel path/to/csv
```
Again, commandline arguments can be passed to the script to customise execution:
```bash
>>> csv2excel -h

usage: csv2excel [-h] [-o OUTPATH] [--dropna] input

positional arguments:
  input                 path to csv to convert

optional arguments:
  -h, --help            show this help message and exit
  -o OUTPATH, --outpath OUTPATH
                        path to output xlsx
  --dropna              drop NaN values in xlsx
```

### Other methods for launching pytadolog
The package can be invoked using the ``main()`` method of the package:

```bash
>>> python -m pytadolog
Alternatively the class can be imported into Python and started explicitly:

```python
from pytadolog import TadoLogger


with TadoLogger() as tl:
    tl.start()  # Starts logging to CSV
```
Using the context manager ensures that scheduled events are cleaned up when the process is terminated. This can be handled explicitly by calling the ``close()`` method:
```python
from pytadolog import TadoLogger


tl = TadoLogger()
try:
    tl.start()  # Starts logging to CSV
except KeyboardInterrupt:
    tl.close()  # Cancels scheduled events
```

## Output
``pytadolog`` creates a CSV file containing weather data for the registered home and set temperature, heating power, measured temperature and relative humidity of each zone in the home. This is structured using a ``pandas`` [MultiIndex](https://pandas.pydata.org/pandas-docs/stable/user_guide/advanced.html). The CSV is updated at the ``update_period`` which defaults to 30s as this is the fastest Tado queries connected devices.
By default the CSVs will be stored in home/Documents/TadoLogs

The CSV will be structured like this:
Zone               |Weather          |Weather       |Weather     |Livingroom|Livingroom|Livingroom   |Livingroom       |Livingroom |Hall     |Hall    |Hall         |Hall             |Hall       
-------------------|-----------------|--------------|------------|----------|----------|-------------|-----------------|-----------|---------|--------|-------------|-----------------|-----------
Variable           |Outside Temp (°C)|Solar Int. (%)|Weather     |Temp (°C) |R.H. (%)  |Set Temp (°C)|Heating Power (%)|Open Window|Temp (°C)|R.H. (%)|Set Temp (°C)|Heating Power (%)|Open Window
2021-02-20 19:03:30|13.33            |0.0           |NIGHT_CLOUDY|23.88     |45.0      |20.0         |0.0              |FALSE      |18.56    |58.4    |13.0         |0.0              |FALSE      
2021-02-20 19:04:00|13.33            |0.0           |NIGHT_CLOUDY|23.88     |45.0      |20.0         |0.0              |FALSE      |18.56    |58.4    |13.0         |0.0              |FALSE      |
2021-02-20 19:04:30|13.33            |0.0           |NIGHT_CLOUDY|23.88     |45.0      |20.0         |0.0              |FALSE      |18.56    |58.4    |13.0         |0.0              |FALSE      

``pytadolog`` will also generate a logfile to track progress. This is stored in a logs/ subdirectory in the output directory, i.e. home/Documents/TadoLogs/logs by default.

## Tado credentials
``pytadolog`` uses [``keyring``](https://pypi.org/project/keyring/) to store the Tado log in credentials securely using the operating system's default keyring service.

From the ``keyring`` README:
   > These recommended keyring backends are supported:
   > * macOS [Keychain](https://en.wikipedia.org/wiki/Keychain_%28software%29)
   > * Freedesktop [Secret Service](http://standards.freedesktop.org/secret-service/) supports many DE including GNOME (requires [secretstorage](https://pypi.python.org/pypi/secretstorage>))
   > * KDE4 & KDE5 [KWallet](https://en.wikipedia.org/wiki/KWallet)
  (requires [dbus](https://pypi.python.org/pypi/dbus-python))
   > * [Windows Credential Locker](https://docs.microsoft.com/en-us/windows/uwp/security/credential-locker)
   > 
   > Other keyring implementations are available through [Third-Party Backends](https://github.com/jaraco/keyring/blob/main/README.rst#third-party-backends).

## Contributing
Pull requests are welcome. For major changes, please open an issue first to discuss what you would like to change.

## License
[MIT](https://choosealicense.com/licenses/mit/)