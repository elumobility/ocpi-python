"""Simple CRUD implementation for the EMSP sessions example."""

from typing import Any

from ocpi.core.crud import Crud
from ocpi.core.enums import Action, ModuleID, RoleEnum

# Simple in-memory storage
storage: dict[str, dict] = {}


class SimpleCrud(Crud):
    """Simple CRUD implementation using in-memory storage."""

    @classmethod
    async def get(
        cls, module: ModuleID, role: RoleEnum, id: str, *args, **kwargs
    ) -> dict | None:
        """Get a single object by ID."""
        key = f"{module.value}:{id}"
        return storage.get(key)

    @classmethod
    async def list(
        cls, module: ModuleID, role: RoleEnum, filters: dict, *args, **kwargs
    ) -> tuple[list[dict], int, bool]:
        """Get a paginated list of objects."""
        items = [v for k, v in storage.items() if k.startswith(f"{module.value}:")]
        total = len(items)
        is_last_page = True
        return items, total, is_last_page

    @classmethod
    async def create(
        cls, module: ModuleID, role: RoleEnum, data: dict, *args, **kwargs
    ) -> dict:
        """Create a new object."""
        obj_id = data.get("id") or data.get("uid")
        key = f"{module.value}:{obj_id}"
        storage[key] = data
        return data

    @classmethod
    async def update(
        cls, module: ModuleID, role: RoleEnum, data: dict, id: str, *args, **kwargs
    ) -> dict:
        """Update an existing object."""
        key = f"{module.value}:{id}"
        if key in storage:
            storage[key].update(data)
            return storage[key]
        return data

    @classmethod
    async def delete(
        cls, module: ModuleID, role: RoleEnum, id: str, *args, **kwargs
    ) -> None:
        """Delete an object."""
        key = f"{module.value}:{id}"
        storage.pop(key, None)

    @classmethod
    async def do(
        cls,
        module: ModuleID,
        role: RoleEnum | None,
        action: Any,
        *args,
        data: dict | None = None,
        **kwargs,
    ) -> Any:
        """Handle non-CRUD actions like token authorization."""
        if module == ModuleID.tokens and action == Action.authorize_token:
            # Simple authorization logic
            # In production, check token validity, location access, etc.
            return {
                "status": "ACCEPTED",
                "location": data.get("location") if data else None,
            }
        return {}
