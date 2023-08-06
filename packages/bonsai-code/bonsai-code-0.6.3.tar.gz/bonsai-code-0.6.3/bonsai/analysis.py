
#Copyright (c) 2017 Andre Santos
#
#Permission is hereby granted, free of charge, to any person obtaining a copy
#of this software and associated documentation files (the "Software"), to deal
#in the Software without restriction, including without limitation the rights
#to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
#copies of the Software, and to permit persons to whom the Software is
#furnished to do so, subject to the following conditions:

#The above copyright notice and this permission notice shall be included in
#all copies or substantial portions of the Software.

#THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
#IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
#FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
#AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
#LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
#OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN
#THE SOFTWARE.

###############################################################################
# Imports
###############################################################################

from __future__ import unicode_literals
from past.builtins import basestring
from builtins import object

from collections import namedtuple
import operator

try:
    DIV_OP = operator.truediv   # Python 3+
except AttributeError:
    DIV_OP = operator.div       # Python 2

from .model import (
    CodeEntity, CodeBlock, CodeControlFlow, CodeExpression, CodeFunction,
    CodeFunctionCall, CodeOperator, CodeReference, CodeVariable, CodeLoop,
    CodeDefaultArgument, CodeClass
)


###############################################################################
# AST Analysis
###############################################################################

class CodeQuery(object):
    DEFINITIONS = (CodeClass, CodeFunction, CodeVariable)

    def __init__(self, codeobj):
        assert isinstance(codeobj, CodeEntity)
        self.root = codeobj
        self.cls = None
        self.recursive = False
        self.attributes = {}

    @property
    def references(self):
        self.cls = CodeReference
        self.recursive = False
        return self

    @property
    def all_references(self):
        self.cls = CodeReference
        self.recursive = True
        return self

    @property
    def calls(self):
        self.cls = CodeFunctionCall
        self.recursive = False
        return self

    @property
    def all_calls(self):
        self.cls = CodeFunctionCall
        self.recursive = True
        return self

    @property
    def definitions(self):
        self.cls = self.DEFINITIONS
        self.recursive = False
        return self

    @property
    def all_definitions(self):
        self.cls = self.DEFINITIONS
        self.recursive = True
        return self

    def where_name(self, name):
        self.attributes['name'] = name
        return self

    def where_result(self, result):
        self.attributes['result'] = result
        return self

    def get(self):
        result = []
        for codeobj in self.root.filter(self.cls, recursive=self.recursive):
            passes = True
            for key, value in self.attributes.items():
                if isinstance(value, basestring):
                    if getattr(codeobj, key) != value:
                        passes = False
                else:
                    if getattr(codeobj, key) not in value:
                        passes = False
            if passes:
                result.append(codeobj)
        return result


###############################################################################
# Interface Functions
###############################################################################

operator_mapping = {
    '+': operator.add,
    '-': operator.sub,
    '*': operator.mul,
    '/': DIV_OP,
    '%': operator.mod
}

def resolve_expression(expression):
    assert isinstance(expression, CodeExpression.TYPES)

    if isinstance(expression, CodeReference):
        return resolve_reference(expression)

    if isinstance(expression, CodeOperator):
        args = []

        for arg in expression.arguments:
            arg = resolve_expression(arg)
            if not isinstance(arg, CodeExpression.LITERALS):
                return expression
            args.append(arg)

        if expression.is_binary:
            a = args[0]
            b = args[1]
            if not isinstance(a, CodeExpression.LITERALS) \
                    or not isinstance(b, CodeExpression.LITERALS):
                return expression
            if expression.name in operator_mapping:
                return operator_mapping[expression.name](a, b)

        if expression.is_unary:
            a = args[0]
            if not isinstance(a, CodeExpression.LITERALS):
                return expression
            if expression.name == "+":
                if isinstance(a, basestring):
                    try:
                        return int(a)
                    except ValueError:
                        pass
                    try:
                        return float(a)
                    except ValueError:
                        pass
                    return expression
                try:
                    return +a
                except TypeError:
                    return expression
            elif expression.name == "-":
                try:
                    return -a
                except TypeError:
                    return expression

    # if isinstance(expression, CodeExpression.LITERALS):
    # if isinstance(expression, SomeValue):
    # if isinstance(expression, CodeFunctionCall):
    # if isinstance(expression, CodeDefaultArgument):
    return expression


def resolve_reference(reference):
    assert isinstance(reference, CodeReference)

    if reference.statement is None:
        return None     # TODO investigate

    si = reference.statement._si
    if (reference.reference is None
            or isinstance(reference.reference, basestring)):
        return None

    if isinstance(reference.reference, CodeVariable):
        var = reference.reference
        value = var.value
        function = reference.function
        for w in var.writes:
            ws = w.statement
            if w.function is not function:
                continue
            if ws._si < si:
                if w.arguments[0].reference is var:
                    value = resolve_expression(w.arguments[1])
                else:
                    continue # TODO
            elif ws._si == si:
                if w.arguments[0] is reference:
                    value = resolve_expression(w.arguments[1])
                else:
                    continue # TODO
        if value is None:
            if var.is_parameter:
                if _get_function(var) is not function:
                    return None
                calls = [call for call in function.references
                         if isinstance(call, CodeFunctionCall)]
                if len(calls) != 1:
                    return None
                i = function.parameters.index(var)
                if len(calls[0].arguments) <= i:
                    return None
                arg = calls[0].arguments[i]
                if isinstance(arg, CodeReference):
                    return resolve_reference(arg)
                return arg
            if var.member_of is not None:
                if (function.is_constructor
                        and function.member_of is var.member_of):
                    # variable is an auto-initialised member of the class
                    return var.auto_init()
                if len(var.writes) == 1:
                    w = var.writes[0]
                    if (w.function.is_constructor
                            and w.arguments[0].reference is var):
                        return resolve_expression(w.arguments[1])
        if isinstance(value, CodeExpression.TYPES):
            return resolve_expression(value)
        return value
    return reference.reference


def is_under_control_flow(codeobj, recursive = False):
    return get_control_depth(codeobj, recursive) > 0


def get_control_depth(codeobj, recursive = False):
    depth = 0
    while not codeobj is None:
        if (isinstance(codeobj, CodeBlock)
                and isinstance(codeobj.parent, CodeControlFlow)):
            depth += 1
        elif isinstance(codeobj, CodeFunction):
            if recursive:
                calls = [get_control_depth(call) for call in codeobj.references
                                if isinstance(call, CodeFunctionCall)]
                if calls:
                    depth += max(calls)
            return depth
        codeobj = codeobj.parent
    return depth


def is_under_loop(codeobj, recursive = False):
    while not codeobj is None:
        if (isinstance(codeobj, CodeBlock)
                and isinstance(codeobj.parent, CodeLoop)):
            return True
        elif isinstance(codeobj, CodeFunction):
            if recursive:
                return any(is_under_loop(call)
                           for call in codeobj.references
                           if isinstance(call, CodeFunctionCall))
            return False
        codeobj = codeobj.parent
    return False


ConditionObject = namedtuple("ConditionObject",
    ("value", "statement", "is_bonsai", "file", "line", "column", "function"))


def get_conditions(codeobj, recursive=False, objs=False):
    conditions = []
    while not codeobj is None:
        if (isinstance(codeobj, CodeBlock)
                and isinstance(codeobj.parent, CodeControlFlow)):
            if objs:
                conditions.append(_condition_obj(
                    codeobj.parent.condition, codeobj.parent))
            else:
                conditions.append(codeobj.parent.condition)
        elif isinstance(codeobj, CodeFunction):
            if recursive:
                for call in codeobj.references:
                    if isinstance(call, CodeFunctionCall):
                        conditions.extend(get_conditions(call, objs=objs))
            return conditions
        codeobj = codeobj.parent
    return conditions


def get_condition_paths(codeobj):
    paths = _get_condition_paths_rec(codeobj, {}, [])
    for path in paths:
        path.reverse()
    return paths

def _get_condition_paths_rec(codeobj, visited, wip_path):
    if codeobj in visited:
        intra_fun = visited[codeobj]
        wip_path.extend(intra_fun)
        # FIXME this is not complete
        return [wip_path]
    intra_fun, fun = _intra_fun_path(codeobj)
    visited[codeobj] = intra_fun
    wip_path.extend(intra_fun)
    if fun is None or not fun.references:
        return [wip_path]
    paths = []
    for call in fun.references:
        copy = list(wip_path)
        if isinstance(call, CodeFunctionCall):
            for path in _get_condition_paths_rec(call, visited, copy):
                paths.append(path)
        else:
            paths.append(copy)
    return paths

def _intra_fun_path(codeobj):
    conditions = get_conditions(codeobj, recursive=False, objs=True)
    return conditions, codeobj.function


def _condition_obj(value, ctrl_flow_stmt):
    return ConditionObject(value, ctrl_flow_stmt.name,
        isinstance(value, CodeEntity), ctrl_flow_stmt.file,
        ctrl_flow_stmt.line, ctrl_flow_stmt.column, ctrl_flow_stmt.function)

def _get_function(codeobj):
    f = codeobj._lookup_parent(CodeFunction)
    if f is None or isinstance(f, CodeFunction):
        return f
    return None
