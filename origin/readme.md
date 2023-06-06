# Answer Ranking algorithm

This repository input the data exported by the questionnaire app, calculate the optimal answer rank, and output the figure of the answer-prediction matrix.

## Our Data

Our data is in the `input` folder

## Our Algorithm

The code of our algorithm is in `algorithm.py`.

## System Requirements

The code is written for Python 3.7 or higher, recent versions of the following python packages must be installed:

- Matplotlib
- Numpy
- Pandas

Use the following instructions to install dependencies

```
pip3 install -r requirements.txt
```

## Usage

Run the code

```
python3 main.py
```

The results will in `output.csv`

The figure of the answer-prediction matrix will in the `output` folder.