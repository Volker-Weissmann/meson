# Copyright 2019 The Meson development team

# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at

#     http://www.apache.org/licenses/LICENSE-2.0

# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

# This module concerns CMake Generator Expressions, abbreviated Cmge.
# Doc: https://cmake.org/cmake/help/latest/manual/cmake-generator-expressions.7.html

from .. import mesonlib
from ..mesonlib import MesonBugException
from .. import mlog
from .common import cmake_is_debug
import typing as T
from ..mparser import (
    Token,
    BaseNode,
    MethodNode,
    FunctionNode,
    ArgumentNode,
    ArithmeticNode,
    StringNode,
    IdNode,
)
from dataclasses import dataclass

if T.TYPE_CHECKING:
    from .traceparser import CMakeTraceParser, CMakeTarget

CmgeSingle = T.Union[str, 'CmgeSpecial']
CmgeAstNode = T.List[CmgeSingle]

# A CmgeSpecial is something like $<cmd:arg[0],arg[1]...>
@dataclass
class CmgeSpecial:
    cmd: CmgeAstNode
    args: T.List[CmgeAstNode]

@dataclass
class Cmge:
    raw: str
    def to_meson_ast(self, trace: 'CMakeTraceParser') -> BaseNode:
        ir = CmgeParser.parse(self.raw)
        return convert_list(ir, trace)


#todo codestyle: this should be a module
class CmgeParser:
    @staticmethod
    def parse(src: str) -> CmgeAstNode:
        ret = CmgeParser.eat_expr(src, 0, False)
        if ret[0] != len(src):
            raise MesonBugException('Unable to parse CMake Generator Expression')
        return ret[1]

    @staticmethod
    def try_eat_plain(src: str, pos: int, depth_greater_zero: bool) -> T.Optional[T.Tuple[int, str]]:
        startpos = pos
        while(pos < len(src) and not src[pos:].startswith('$<')):
            if depth_greater_zero and src[pos] in ['>', ':', ',']:
                break
            pos += 1
        if pos != startpos:
            return pos, src[startpos:pos]
        else:
            return None

    @staticmethod
    def try_eat_special(src: str, pos: int) -> T.Optional[T.Tuple[int, CmgeSpecial]]:
        if pos+1 >= len(src) or src[pos:pos+2] != '$<':
            return None
        pos += 2
        cmd = CmgeParser.eat_expr(src, pos, True)
        pos = cmd[0]
        if pos >= len(src) or src[pos] != ':':
            return None
        pos += 1
        args = []
        a = CmgeParser.eat_expr(src, pos, True)
        pos = a[0]
        args.append(a[1])
        while True:
            if pos >= len(src) or src[pos] != ',':
                break
            pos += 1
            a = CmgeParser.eat_expr(src, pos, True)
            pos = a[0]
            args.append(a[1])
        if pos >= len(src) or src[pos] != '>':
            return None
        pos += 1
        return pos, CmgeSpecial(cmd=cmd[1], args=args)

    @staticmethod
    def eat_expr(src: str, pos: int, depth_greater_zero: bool) -> T.Tuple[int, CmgeAstNode]:
        ret: T.List[CmgeSingle] = []
        while True:
            x = CmgeParser.try_eat_plain(src, pos, depth_greater_zero) or CmgeParser.try_eat_special(src, pos)
            if x is None:
                return pos, ret
            pos = x[0]
            ret.append(x[1])




emptyToken = Token('string', 'todo self.subdir.as_posix()', 0, 0, 0, None, '')

def token(val) -> Token:
    return Token('string', 'todo self.subdir.as_posix()', 0, 0, 0, None, val)

def convert_single(this: CmgeSingle, trace: 'CMakeTraceParser') -> BaseNode:
    if isinstance(this, CmgeSpecial):
        if this.cmd == ['IF']:
            assert(len(this.args) == 3)
            args = ArgumentNode(emptyToken)
            args.append(this.args[0])
            args.append(this.args[1])
            args.append(this.args[2])
            ret = FunctionNode('todo self.subdir.as_posix()', 0, 0, 'ternary', args)
        elif this.cmd == ['TARGET_FILE'] :
            assert(len(this.args) == 1)
            assert(len(this.args[0]) == 1)
            assert(isinstance(this.args[0][0], str))
            exename = this.args[0][0]
            if trace.targets[exename].imported:
                locations = trace.targets[exename].properties['IMPORTED_LOCATION']
                assert(len(locations) == 1)
                return StringNode(token(locations[0]))
            else:
                ret = MethodNode('todo self.subdir.as_posix()', 0, 0, IdNode(token(exename)), 'full_path', ArgumentNode(emptyToken))
                return ret
        else:
            raise NotImplementedError(f'Unsupported CMake Generator Expression: {this.cmd}')
    elif isinstance(this, str):
        return StringNode(token(this))
    else:
        raise MesonBugException('Unreachable code')

def convert_list(this: T.List[CmgeSingle], trace: 'CMakeTraceParser') -> BaseNode:
    if len(this) == 0:
        return StringNode(emptyToken)
    elif len(this) == 1:
        return convert_single(this[0], trace)
    else:
        return ArithmeticNode('add', convert_list(this[:-1], trace), convert_single(this[-1], trace))
