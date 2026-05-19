"""Write transformed OCEL logs with resource and role annotations."""

import pandas as pd
import pm4py


def add_is_resource_and_discovered_roles_and_export(ocel, resource_types, discovered_roles, output_file):
    """Tag resource objects with isResource=True and discoveredRoles, then export the OCEL to XML."""
    if not resource_types:
        return

    objects_df = ocel.objects
    object_type_column = ocel.object_type_column
    object_id_column = ocel.object_id_column
    resource_type_set = {str(resource_type).strip() for resource_type in resource_types}

    # Check if attributes already exist
    if "isResource" in objects_df.columns:
        return

    # Initialize attributes
    if "isResource" not in objects_df.columns:
        objects_df["isResource"] = pd.Series(pd.NA, index=objects_df.index, dtype="boolean")
    
    if "discoveredRoles" not in objects_df.columns:
        objects_df["discoveredRoles"] = None

    # Assign isResource for all resource types
    object_type_mask = objects_df[object_type_column].astype(str).str.strip().isin(resource_type_set)
    objects_df.loc[object_type_mask, "isResource"] = True

    # Build and assign discoveredRoles for each resource type
    for resource_type in resource_type_set:
        roles = discovered_roles.get(resource_type, {})
        
        if not roles or len(roles) == 1:
            # No roles or single role discovered - use default
            role_value = f"default_for_{resource_type}"
            # Assign the same role value to all objects of this type
            type_mask = objects_df[object_type_column].astype(str).str.strip() == resource_type
            objects_df.loc[type_mask, "discoveredRoles"] = role_value
        else:
            # Multiple roles - assign each resource only the roles it's involved in
            type_mask = objects_df[object_type_column].astype(str).str.strip() == resource_type
            type_objects = objects_df[type_mask]
            
            # Create a mapping of object_id -> list of role strings it belongs to
            object_to_roles = {}
            for role_id, role_info in sorted(roles.items()):
                role_object_ids = {str(oid) for oid in role_info["object_ids"]}
                event_types = sorted(role_info["event_types"])
                event_types_str = str(event_types)
                role_str = f"Role {role_id + 1}: {event_types_str}"
                
                for oid in role_object_ids:
                    if oid not in object_to_roles:
                        object_to_roles[oid] = []
                    object_to_roles[oid].append(role_str)
            
            # Assign role strings to each object
            for idx in type_objects.index:
                obj_id = str(objects_df.loc[idx, object_id_column])
                if obj_id in object_to_roles:
                    role_value = str(object_to_roles[obj_id])
                    objects_df.loc[idx, "discoveredRoles"] = role_value

    pm4py.write_ocel2_xml(ocel, str(output_file))
