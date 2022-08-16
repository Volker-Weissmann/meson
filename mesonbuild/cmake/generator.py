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
class CmgeAst:
    root: CmgeAstNode

    # todo: remove this function
    def eval_to_string_now(self) -> str:
        if len(self.root) != 1 or not isinstance(self.root[0], str):
            raise NotImplementedError('We cannot evaluate this right now.')
        return self.root[0]

# This class converts a string to a CmgeAst.
# The grammar is:
# expr = { ( plain | special )* }
# special = { "$<" ~ expr ~ ":" ~ expr ~ ("," ~ expr)* ~ ">" }
# plain = { ( !("$" | "<" | ">" | ":" | ",") ~ ANY )+ }
# (https://pest.rs/ has a live editor for this grammar)
class CmgeParser:
    @staticmethod
    def parse(src: str) -> 'CmgeAst':
        ret = CmgeParser.eat_expr(src, 0)
        if ret[0] != len(src):
            import pdb
            pdb.set_trace()
            raise MesonBugException('Unable to parse CMake Generator Expression')
        return CmgeAst(root=ret[1])

    @staticmethod
    def try_eat_plain(src: str, pos: int) -> T.Optional[T.Tuple[int, str]]:
        startpos = pos
        while(pos < len(src) and not src[pos] in ['$', '<', '>', ':', ',']):
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
        cmd = CmgeParser.eat_expr(src, pos)
        pos = cmd[0]
        if pos >= len(src) or src[pos] != ':':
            return None
        pos += 1
        args = []
        a = CmgeParser.eat_expr(src, pos)
        pos = a[0]
        args.append(a[1])
        while True:
            if pos >= len(src) or src[pos] != ',':
                break
            pos += 1
            a = CmgeParser.eat_expr(src, pos)
            pos = a[0]
            args.append(a[1])
        if pos >= len(src) or src[pos] != '>':
            return None
        pos += 1
        return pos, CmgeSpecial(cmd=cmd[1], args=args)

    @staticmethod
    def eat_expr(src: str, pos: int) -> T.Tuple[int, CmgeAstNode]:
        ret: T.List[CmgeSingle] = []
        while True:
            x = CmgeParser.try_eat_plain(src, pos) or CmgeParser.try_eat_special(src, pos)
            if x is None:
                return pos, ret
            pos = x[0]
            ret.append(x[1])

# This class converts our Cmge Ast to a corresponding Meson Ast.
class CmgeToMeson:
    @staticmethod
    def convert_ast(this: CmgeAst, trace: 'CMakeTraceParser') -> BaseNode:
        return CmgeToMeson.convert_list(this.root, trace)

    @staticmethod
    def token(val) -> Token:
        return Token('string', 'todo self.subdir.as_posix()', 0, 0, 0, None, val)

    emptyToken = Token('string', 'todo self.subdir.as_posix()', 0, 0, 0, None, '')

    @staticmethod
    def convert_single(this: CmgeSingle, trace: 'CMakeTraceParser') -> BaseNode:
        if isinstance(this, CmgeSpecial):
            if this.cmd == ['IF']:
                assert(len(this.args) == 3)
                args = ArgumentNode(self.emptyToken)
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
                    return StringNode(CmgeToMeson.token(locations[0]))
                else:
                    ret = MethodNode('todo self.subdir.as_posix()', 0, 0, IdNode(CmgeToMeson.token(exename)), 'full_path', ArgumentNode(self.emptyToken))
                    return ret
            else:
                raise NotImplementedError(f'Unsupported CMake Generator Expression: {this.cmd}')
        elif isinstance(this, str):
            return StringNode(CmgeToMeson.token(this))
        else:
            raise MesonBugException('Unreachable code')

    @staticmethod
    def convert_list(this: T.List[CmgeSingle], trace: 'CMakeTraceParser') -> BaseNode:
        if len(this) == 0:
            return StringNode(CmgeToMeson.token(''))
        elif len(this) == 1:
            return CmgeToMeson.convert_single(this[0], trace)
        else:
            return ArithmeticNode('add', CmgeToMeson.convert_list(this[:-1], trace), CmgeToMeson.convert_single(this[-1], trace))
