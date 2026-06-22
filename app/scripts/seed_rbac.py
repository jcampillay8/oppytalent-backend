import asyncio
import os
import sys

# Ensure the app module can be imported
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "../..")))

from app.database import async_session
from app.models.rbac import Role, Permission, RolePermission
from sqlalchemy.future import select

async def seed_rbac():
    async with async_session() as session:
        # Define default permissions
        permissions = [
            {"codename": "can_execute_tribunal", "name": "Can Execute Tribunal", "description": "Can spend credits to run B2B Tribunals"},
            {"codename": "can_approve_kyc", "name": "Can Approve KYC", "description": "Can review and approve headhunter accounts"},
            {"codename": "can_use_b2b_search", "name": "Can Use B2B Search", "description": "Can search the talent database"},
            {"codename": "can_edit_portfolio", "name": "Can Edit Portfolio", "description": "Can manage personal talent portfolio"},
            {"codename": "can_view_own_feedback", "name": "Can View Own Feedback", "description": "Can read B2B battle feedback"},
            {"codename": "can_impersonate", "name": "Can Impersonate Users", "description": "Can generate impersonation tokens"},
            {"codename": "can_view_demand", "name": "Can View Demand", "description": "Can view B2B market demand insights"},
            {"codename": "can_manage_roles", "name": "Can Manage Roles", "description": "Can assign roles to users in the Admin panel"}
        ]
        
        # Insert or update permissions
        db_perms = {}
        for p_data in permissions:
            result = await session.execute(select(Permission).where(Permission.codename == p_data["codename"]))
            perm = result.scalars().first()
            if not perm:
                perm = Permission(**p_data)
                session.add(perm)
                print(f"Added permission: {p_data['codename']}")
            db_perms[p_data["codename"]] = perm
            
        await session.flush()
        
        # Define roles and their associated permission codenames
        roles = {
            "Owner": ["can_execute_tribunal", "can_approve_kyc", "can_use_b2b_search", "can_edit_portfolio", "can_view_own_feedback", "can_impersonate", "can_view_demand", "can_manage_roles"],
            "Admin": ["can_approve_kyc", "can_view_demand"],
            "Worker": ["can_view_demand"],
            "Hunter": ["can_execute_tribunal", "can_use_b2b_search", "can_view_demand"],
            "Talent": ["can_edit_portfolio", "can_view_own_feedback", "can_view_demand"]
        }
        
        # Insert or update roles
        for r_name, p_codenames in roles.items():
            result = await session.execute(select(Role).where(Role.name == r_name))
            role = result.scalars().first()
            if not role:
                role = Role(name=r_name, description=f"The {r_name} role")
                session.add(role)
                print(f"Added role: {r_name}")
            
            await session.flush()
            
            # Clear old permissions
            await session.execute(
                RolePermission.__table__.delete().where(RolePermission.role_id == role.id)
            )
            
            # Add new permissions
            for codename in p_codenames:
                perm = db_perms[codename]
                rp = RolePermission(role_id=role.id, permission_id=perm.id)
                session.add(rp)
                
            print(f"Updated permissions for role: {r_name}")

        await session.commit()
        print("RBAC Seeding completed successfully.")

if __name__ == "__main__":
    asyncio.run(seed_rbac())
