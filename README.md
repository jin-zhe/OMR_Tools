# OMR_Tools
Some useful tools for Optical Mark Recognition (OMR). Note that only Python 3 is supported. There is no backward compatibility for Python 2 so you if you'd like to use Python 2, you'll have to make your own modifications.

## Installation
First, get this repo and its submodules on your machine:
```sh
git clone --recursive git@github.com:jin-zhe/OMR_Tools.git
```
TODO later

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
