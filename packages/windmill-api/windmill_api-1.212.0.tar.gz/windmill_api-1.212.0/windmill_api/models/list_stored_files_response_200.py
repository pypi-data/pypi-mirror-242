from typing import TYPE_CHECKING, Any, Dict, List, Type, TypeVar

from attrs import define as _attrs_define
from attrs import field as _attrs_field

if TYPE_CHECKING:
    from ..models.list_stored_files_response_200_windmill_large_files_item import (
        ListStoredFilesResponse200WindmillLargeFilesItem,
    )


T = TypeVar("T", bound="ListStoredFilesResponse200")


@_attrs_define
class ListStoredFilesResponse200:
    """
    Attributes:
        file_count (int):
        windmill_large_files (List['ListStoredFilesResponse200WindmillLargeFilesItem']):
    """

    file_count: int
    windmill_large_files: List["ListStoredFilesResponse200WindmillLargeFilesItem"]
    additional_properties: Dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        file_count = self.file_count
        windmill_large_files = []
        for windmill_large_files_item_data in self.windmill_large_files:
            windmill_large_files_item = windmill_large_files_item_data.to_dict()

            windmill_large_files.append(windmill_large_files_item)

        field_dict: Dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "file_count": file_count,
                "windmill_large_files": windmill_large_files,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        from ..models.list_stored_files_response_200_windmill_large_files_item import (
            ListStoredFilesResponse200WindmillLargeFilesItem,
        )

        d = src_dict.copy()
        file_count = d.pop("file_count")

        windmill_large_files = []
        _windmill_large_files = d.pop("windmill_large_files")
        for windmill_large_files_item_data in _windmill_large_files:
            windmill_large_files_item = ListStoredFilesResponse200WindmillLargeFilesItem.from_dict(
                windmill_large_files_item_data
            )

            windmill_large_files.append(windmill_large_files_item)

        list_stored_files_response_200 = cls(
            file_count=file_count,
            windmill_large_files=windmill_large_files,
        )

        list_stored_files_response_200.additional_properties = d
        return list_stored_files_response_200

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
