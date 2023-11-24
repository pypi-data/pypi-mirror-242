# Generated file; do not edit. See the Rust `schema-gen` crate.

from .prelude import *

from .code_static import CodeStatic
from .cord import Cord


@dataclass(init=False)
class CodeBlock(CodeStatic):
    """
    A code block.
    """

    type: Literal["CodeBlock"] = field(default="CodeBlock", init=False)

    def __init__(self, code: Cord, id: Optional[str] = None, programming_language: Optional[str] = None):
        super().__init__(id = id, code = code, programming_language = programming_language)
        
