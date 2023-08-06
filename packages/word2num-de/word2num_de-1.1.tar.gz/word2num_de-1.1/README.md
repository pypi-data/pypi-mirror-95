# word2num-de
EN
- Transforms written numbers in German to numbers.
- Works for numbers 0-999999

DE
- Übersetzt ausgeschriebene Zahlen in (auf Deutsch) in Zahlen
- Unterstützt Zahlen zwischen 0 und 999999.

Implementation based on the following project: https://github.com/IBM/wort-to-number

## Installation

Package can be installed using pip.

```bash
pip install word2num-de
```

## Usage example

Import the main function word_to_number.

```
from word2num_de import word_to_number
```

Given a written-out number, the function returns the number as an integer.

```
print(word_to_number("sechshunderteinundzwanzig"))
621
```

Larger numbers are also supported.

```
print(word_to_number("zweiunddreißigtausendfünfhundertachtundvierzig"))
32548
```

None is returned in case the word is not a number.

```
print(word_to_number("bäckerei"))
None
```

The function should also be robust to words including numbers in them (e.g.; Viereck, Servieren, Tausendsassa, etc.).

```
print(word_to_number("tausendsassa"))
None
```

