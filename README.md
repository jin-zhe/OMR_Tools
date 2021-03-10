# OMR_Tools
Some useful tools for Optical Mark Recognition (OMR). Note that only Python 3 is supported. There is no backward compatibility for Python 2 so you if you'd like to use Python 2, you'll have to make your own modifications.

## Installation
First, get this repo and its submodules on your machine:
```sh
git clone --recursive git@github.com:jin-zhe/OMR_Tools.git
```
I recommend installing the necessary python packages via [Conda](https://docs.conda.io/en/latest/index.html) which has become the de facto virtual environment manager for AI/ML projects (which this might potentially turn into). Conda also makes the installation process really simple because it is also a package-management system. If you rather not use Conda, you may refer to [OMRChecker](https://github.com/Udayraj123/OMRChecker)'s original installation guide using `pip`. Should you do that, just make sure you have the important packages listed under [Packages](https://github.com/jin-zhe/OMR_Tools#packages).

### Installing with Conda

1. Follow this [quickstart guide](https://jin-zhe.github.io/guides/getting-up-to-speed-with-conda/) to install and understand how to use Conda
2. Create a new Conda environment with necessary packages:
  * `conda create -n omr_tools python=3.5 opencv matplotlib numpy pandas tqdm -y`
3. Enter newly created environment
  * `conda activate omr_tools`
4. `pip install pdf2image imutils` (these are the only two you have to install via `pip`)

### Packages
This repo has been tested to work with the following python package versions:

Package | Version
--- | ---
`opencv` | v3.4.2
`opencv-contrib-python` | 4.2.0.32
`matplotlib` | 3.1.1
`numpy` | 1.18.1
`pandas` | 1.0.1
`imutils` | 0.5.3
`tqdm` | 4.42.1
`PyPDF2` | 1.26.0

opencv-contrib-python

### Submodules
As submodules are included in this repository, make sure you get the right one. If you didn't clone this repo with the `--recursive` flag, you'll need to run:
```sh
git submodule update --init --recursive
```
#### [OMRChecker](https://github.com/leongwaikay/OMRChecker/tree/extension-framework)
* Branch: [extension-framework](https://github.com/leongwaikay/OMRChecker/tree/extension-framework)
* Commit: `'bc9310135602bfedf47c0db99ab60c5aae9935c4'`
---
## Scripts
### [`stuID_checker.py`](stuID_checker.py)
Conducts OMR on student exam script scans to determine their student ID.

#### Sample usage
```sh
python stuID_checker.py -i $script_dir -o output.csv -r
```
#### Arguments
Longform | Shortform | Optional | Description
--- | --- | --- | ---
`--input-dir` | `-i` | NO | Input directory containing script PDFs.
`--output` | `-o` | NO | Output path for the CSV.
`--page` | `-p` | YES | Specify the page to conduct OMR on (defaults to first).
`--rename` | `-r` | YES | Flag for whether to rename documents based on their student numbers.
`---save-level` | `-s` | YES | Specify `saveimglvl` of [OMRChecker](https://github.com/Udayraj123/OMRChecker) (defaults as `0`).

## Related tools
Refer to [this gist](https://gist.github.com/jin-zhe/2efc348f58002f54e1ed90ab5323e56a) if you need a script to break up a pdf of multiple document scans (with same number of pages) into individual pdf doucments.
