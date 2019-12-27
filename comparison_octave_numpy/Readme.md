# Explanation
#### Purpose

  Verify the accuracy/difference between the octave and numpy implementation of the maximum achievable efficiency.

#### Motivation

  I decided to switch to numpy in order to process all the files in Python without the use of external software like Octave that I have been using so far.
  All this for speed. In fact, I would like to get the results faster and already well formatted and this could be achieved by integrating everything in Python

#### Content

  There are three different set of files:

  1. efficiency calculated with octave file: ***octave_out\_`parameter`\_`file_name`.csv***
  2. efficiency calculated with numpy file: ***numpy_out\_`parameter`\_`file_name`.csv***
  3. the file computing the absolute difference between their output values: ***difference\_`parameter`\_octave_numpy.csv***

#### Some statistics

|                                          | min  | max      | mean     | median |
| ---------------------------------------- | ---- | -------- | -------- | ------ |
| ***difference_zparam_octave_numpy.csv*** | 0    | 9.95E-14 | 2.39E-15 | 0      |
| ***difference_sparam_octave_numpy.csv*** | 0    | 1.14E-11 | 7.66E-13 | 0      |

#### Conclusion

  I could use numpy from now and speed up my analysis. (Hurray!!!)

