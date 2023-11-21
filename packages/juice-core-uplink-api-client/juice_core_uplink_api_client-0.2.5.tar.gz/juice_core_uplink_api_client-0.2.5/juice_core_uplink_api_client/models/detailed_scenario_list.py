import datetime
from typing import Any, Dict, List, Type, TypeVar, Union

from attrs import define as _attrs_define
from attrs import field as _attrs_field
from dateutil.parser import isoparse

from ..types import UNSET, Unset

T = TypeVar("T", bound="DetailedScenarioList")


@_attrs_define
class DetailedScenarioList:
    """
    Attributes:
        trajectory (str):
        name (str):
        mnemonic (str):
        created (Union[Unset, datetime.datetime]):
        id (Union[Unset, int]):
        author (Union[Unset, str]):
        description (Union[Unset, None, str]):
        scenario_json_file (Union[Unset, str]):
        start (Union[Unset, None, str]):
        end (Union[Unset, None, str]):
    """

    trajectory: str
    name: str
    mnemonic: str
    created: Union[Unset, datetime.datetime] = UNSET
    id: Union[Unset, int] = UNSET
    author: Union[Unset, str] = UNSET
    description: Union[Unset, None, str] = UNSET
    scenario_json_file: Union[Unset, str] = UNSET
    start: Union[Unset, None, str] = UNSET
    end: Union[Unset, None, str] = UNSET
    additional_properties: Dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        trajectory = self.trajectory
        name = self.name
        mnemonic = self.mnemonic
        created: Union[Unset, str] = UNSET
        if not isinstance(self.created, Unset):
            created = self.created.isoformat()

        id = self.id
        author = self.author
        description = self.description
        scenario_json_file = self.scenario_json_file
        start = self.start
        end = self.end

        field_dict: Dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "trajectory": trajectory,
                "name": name,
                "mnemonic": mnemonic,
            }
        )
        if created is not UNSET:
            field_dict["created"] = created
        if id is not UNSET:
            field_dict["id"] = id
        if author is not UNSET:
            field_dict["author"] = author
        if description is not UNSET:
            field_dict["description"] = description
        if scenario_json_file is not UNSET:
            field_dict["scenario_json_file"] = scenario_json_file
        if start is not UNSET:
            field_dict["start"] = start
        if end is not UNSET:
            field_dict["end"] = end

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        d = src_dict.copy()
        trajectory = d.pop("trajectory")

        name = d.pop("name")

        mnemonic = d.pop("mnemonic")

        _created = d.pop("created", UNSET)
        created: Union[Unset, datetime.datetime]
        if isinstance(_created, Unset):
            created = UNSET
        else:
            created = isoparse(_created)

        id = d.pop("id", UNSET)

        author = d.pop("author", UNSET)

        description = d.pop("description", UNSET)

        scenario_json_file = d.pop("scenario_json_file", UNSET)

        start = d.pop("start", UNSET)

        end = d.pop("end", UNSET)

        detailed_scenario_list = cls(
            trajectory=trajectory,
            name=name,
            mnemonic=mnemonic,
            created=created,
            id=id,
            author=author,
            description=description,
            scenario_json_file=scenario_json_file,
            start=start,
            end=end,
        )

        detailed_scenario_list.additional_properties = d
        return detailed_scenario_list

    @property
    def additional_keys(self) -> List[str]:
        return list(self.additional_properties.keys())

    def __getitem__(self, key: str) -> Any:
        return self.additional_properties[key]

    def __setitem__(self, key: str, value: Any) -> None:
        self.additional_properties[key] = value

    def __delitem__(self, key: str) -> None:
        del self.additional_properties[key]

    def __contains__(self, key: str) -> bool:
        return key in self.additional_properties
