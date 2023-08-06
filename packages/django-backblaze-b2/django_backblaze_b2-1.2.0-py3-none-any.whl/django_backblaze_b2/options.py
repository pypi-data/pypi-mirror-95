from typing import Any, Dict, Optional, Union

try:
    from typing import TypedDict
except Exception:
    from mypy_extensions import TypedDict


class ProxiedBucketNames(TypedDict):
    public: Optional[str]
    loggedIn: Optional[str]
    staff: Optional[str]


class InMemoryAccountInfoConfig(TypedDict):
    type: str  # only "memory" is valid


class SqliteAccountInfoConfig(TypedDict):
    type: str  # only "sqlite" is valid
    databasePath: str


class BackblazeB2StorageOptions(TypedDict):
    """Configuration options."""

    realm: str  # default "production"
    application_key_id: str
    application_key: str
    bucket: str
    authorizeOnInit: bool
    validateOnInit: bool
    allowFileOverwrites: bool
    # see: https://b2-sdk-python.readthedocs.io/en/master/api/api.html#b2sdk.v1.B2Api.create_bucket
    nonExistentBucketDetails: Optional[Dict[str, Union[str, Dict[str, Any]]]]
    defaultFileInfo: Dict[str, Any]
    specificBucketNames: ProxiedBucketNames
    accountInfo: Optional[Union[InMemoryAccountInfoConfig, SqliteAccountInfoConfig]]


def getDefaultB2StorageOptions() -> BackblazeB2StorageOptions:
    return {
        "realm": "production",
        "application_key_id": "you must set this value yourself",
        "application_key": "you must set this value yourself",
        "bucket": "django",
        "authorizeOnInit": True,
        "validateOnInit": True,
        "allowFileOverwrites": False,
        "nonExistentBucketDetails": None,
        "defaultFileInfo": {},
        "specificBucketNames": {"public": None, "loggedIn": None, "staff": None},
        "accountInfo": {"type": "memory"},
    }
