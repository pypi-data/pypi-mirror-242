import libcst as cst
from libcst import (
    Name,
    FunctionDef,
    Assign,
    Call,
    AssignTarget,
    Arg,
    SimpleStatementLine,
    FlattenSentinel,
    ClassDef,
    Subscript,
    SubscriptElement,
    Index
)
from libcst.codemod import (
    CodemodContext,
    VisitorBasedCodemodCommand,
)
from libcst.codemod.visitors import AddImportsVisitor
from libcst import matchers
from libcst.metadata import MetadataWrapper, ScopeProvider, Assignment, Scope
from typing import Any

from ..transformer import ReplaceTransformer
from .utils import gen_func_wrapper, gen_type_param

class TransformFormattedStringCommand(VisitorBasedCodemodCommand):
    METADATA_DEPENDENCIES = (ScopeProvider, )

    def __init__(self, context: CodemodContext) -> None:
        self.string_assigns: dict[cst.FormattedString, list[cst.Assign]] = {}
        super().__init__(context)

    def visit_FormattedString(self, node: cst.FormattedString):
        # TODO: support subnode
        return False

    def leave_FormattedString(self, original_node: cst.FormattedString, updated_node: cst.FormattedString):
        replacemences = {}
        string_assigns = []
        for part in original_node.parts:
            match part:
                case cst.FormattedStringExpression(expression):
                    string_name = cst.Name(value="__temp_string")
                    replacemences[expression] = string_name
                    string_assigns.append(SimpleStatementLine([Assign(
                        targets=[AssignTarget(string_name)],
                        value=expression,
                    )]))
        new_node = original_node.visit(ReplaceTransformer(replacemences))
        assert isinstance(new_node, cst.FormattedString)
        
        print(f"{"123"}")
        print((__temp_string := "123", f"{__temp_string}")[1] )
        print("{}".format("123") )

        print(f"{"123":.2f}")
        print((__temp_string := "123", f"{__temp_string:.2f}")[1] )
        print("{:.2f}".format("123") )

        return cst.FlattenSentinel([
            *string_assigns, new_node
        ])
    
        
