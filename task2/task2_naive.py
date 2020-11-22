from functools import total_ordering
from itertools import zip_longest
import re


@total_ordering
class Version:
    """
    A class used to represent a version string to enable semantic comparison between them.


    Attributes
    ----------
    version : str
        Version string as it was inputted.
    version_comparable : list[int]
        Version encoded as a list of ints to enable comparison.
    dev_stage_to_int_table : dict
        Lookup table for char to int conversion.

    Methods
    -------
    _is_valid_operand(Version instance)
        Checks for comparison ops whether other obj is a Version instance.
    _get_int(char)
        Return a corresponding int for a char from a lookup table.

    Example
    -------
    >>> a = Version("1.0.0")
    >>> b = Version("1.0.0-beta")
    >>> a > b
    True
    """
    dev_stage_to_int_table = {
        # alpha < beta < rc < final 0
        "r": -1,  # rc
        "c": -1,  # rc
        "b": -2,  # beta
        "a": -3,  # alpha
    }

    # int_to_dev_stage_table = {v: k for k, v in dev_stage_to_int_table.items()}

    def __init__(self, version):
        self.version = str(version)
        self.version_comparable = [int(s) if s.isdigit() else self._get_int(s[0])
                                   for s in re.findall("\d+|[a-z]+", self.version.lower())]

    # @property   # lazy compute?
    # def version_comparable(self):
    #     version_separated = re.findall("\d+|[a-z]+", self.version_lover)
    #     return [int(s) if s.isdigit() else self._get_int(s[0]) for s in version_separated]

    def __str__(self):
        return self.version

    def __repr__(self):
        return f"Version instance {str(self.version_comparable)}"

    @staticmethod
    def _is_valid_operand(other):
        return isinstance(other, Version)

    def _get_int(self, char):
        try:
            return self.dev_stage_to_int_table[char]
        except KeyError as error:
            msg = f"Unknown letter {char} in {self.version} REPLACED WITH Beta. " \
                  f"Known are {self.dev_stage_to_int_table.keys()}"
            print(msg)
            return self.dev_stage_to_int_table['b']

    def __eq__(self, other):
        if not self._is_valid_operand(other):
            return NotImplemented
        return self.version_comparable == other.version_comparable

    def __lt__(self, other):
        if not self._is_valid_operand(other):
            return NotImplemented
        for left, right in zip_longest(self.version_comparable, other.version_comparable, fillvalue=0):
            if left == right:
                continue
            elif left < right:
                return True
            elif left > right:
                return False
        else:
            return False


def main():
    to_test = [
        ("1.0.0", "2.0.0"),
        ("1.0.0", "1.42.0"),
        ("1.2.0", "1.2.42"),
        ("1.1.0-alpha", "1.2.0-alpha.1"),
        ("1.0.1b", "1.0.10-alpha.beta"),
        ("1.0.0-rc.1", "1.0.0"),
    ]

    for version_1, version_2 in to_test:
        assert Version(version_1) < Version(version_2), "le failed"
        assert Version(version_2) > Version(version_1), "ge failed"
        assert Version(version_2) != Version(version_1), "neq failed"


if __name__ == "__main__":
    main()
