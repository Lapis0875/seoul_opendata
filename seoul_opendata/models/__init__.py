from .location import Location
from .establish_type import EstablishType
from .user import UserBase, ParentUser
from .facility import ChildSchool, ChildSchoolUser
from .child import Child
from .article import Article
from . import payloads

refMap: dict[str, type] = {
    Location.__name__: Location,
    EstablishType.__name__: EstablishType,
    UserBase.__name__: UserBase,
    ParentUser.__name__: ParentUser,
    ChildSchool.__name__: ChildSchool,
    ChildSchoolUser.__name__: ChildSchoolUser,
    Child.__name__: Child,
    Article.__name__: Article
}
print(refMap)

ParentUser.update_forward_refs(Child=Child)
ChildSchool.update_forward_refs(Child=Child)
ChildSchoolUser.update_forward_refs(Child=Child)
Child.update_forward_refs(ParentUser=ParentUser, ChildSchool=ChildSchool)

print("Forward Reference Resolved.")