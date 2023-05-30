from .location import Location
from .establish_type import EstablishType
from .user import Gender, UserBase, ParentUser
from .child_school import ChildSchool, ChildSchoolUser
from .child import Child
from .article import Article
from . import payloads

__all__ = (
    "Location",
    "EstablishType",
    "Gender",
    "UserBase",
    "ParentUser",
    "ChildSchool",
    "ChildSchoolUser",
    "Child",
    "Article",
    "payloads"
)

ParentUser.update_forward_refs(Child=Child)
ChildSchool.update_forward_refs(Child=Child)
ChildSchoolUser.update_forward_refs(Child=Child)
Child.update_forward_refs(ParentUser=ParentUser, ChildSchool=ChildSchool)

print("Forward Reference Resolved.")