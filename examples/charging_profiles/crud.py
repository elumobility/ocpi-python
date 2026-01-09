"""CRUD implementation for the charging profiles example."""

from typing import Any

from ocpi.core.crud import Crud
from ocpi.core.enums import Action, ModuleID, RoleEnum

# Simple in-memory storage
storage: dict[str, dict] = {}


class SimpleCrud(Crud):
    """CRUD implementation using in-memory storage."""

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
        obj_id = data.get("id") or kwargs.get("session_id")
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
        """Handle charging profile actions."""
        if module == ModuleID.charging_profile:
            session_id = kwargs.get("session_id")
            duration = kwargs.get("duration")
            
            if action == Action.send_get_chargingprofile:
                # Return active charging profile
                profile_key = f"{ModuleID.charging_profile.value}:{session_id}"
                return storage.get(profile_key, {})
            
            elif action == Action.send_delete_chargingprofile:
                # Clear charging profile
                profile_key = f"{ModuleID.charging_profile.value}:{session_id}"
                storage.pop(profile_key, None)
                return {"result": "ACCEPTED"}
            
            elif action == Action.send_update_charging_profile:
                # Update charging profile
                if data and session_id:
                    profile_key = f"{ModuleID.charging_profile.value}:{session_id}"
                    storage[profile_key] = data
                    return {"result": "ACCEPTED"}
        
        return {}
