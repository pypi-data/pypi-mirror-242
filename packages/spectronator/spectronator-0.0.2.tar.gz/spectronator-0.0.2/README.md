# A spectral sensitivity analyser

Spectronator is a graphical tool that quantifies spectral sensitivity from
time series data. In sensory neuroscience, for example, this data
can be eyes' responsivness to differently colored light flashes,
measured by extracellular ERG electrodes.

Features
- Open CSV and Biosyst data files
- Low and highpass filtering
- Response quantification by algorithms
    - minmax
    - start-vs-max
    - start-vs-min
- Spectral responsivness plotting
- Export to CSV and PNG


## Installing and launching

Select one of the following.

## A) All-in-one installer (Windows only)
TBA...

## B) Python standard

To install, open the command-line and type in

```bash
pip install spectronator
```

Then you can launch via the command-line by

```bash
python -m spectronator.tkgui
```

or alternatively via the Python interpreter by

```python
import spectronator.tkgui
spectronator.tkgui.main()
```
