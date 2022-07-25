import unittest
import io

from mesonbuild.mtest import TAPParser, TestResult


class CmakeGeneratorTests(unittest.TestCase):
    def test_something(self):
        print("abc")
        assert(false)


#target_compile_definitions(tgt PRIVATE
#  $<$<VERSION_LESS:$<CXX_COMPILER_VERSION>,4.2.0>:OLD_COMPILER>
#)
