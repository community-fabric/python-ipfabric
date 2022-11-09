import argparse
import yaml
from ipfabric import IPFClient
import logging
import sys
import os

logger = logging.getLogger("RBAC")

def delete_rbac(ipf) -> int:
    logger.info("Deleting RBAC")
    resp = ipf.get('roles')
    resp.raise_for_status()


    for role in resp.json()['data']:
        if not role['isSystem']:
            logger.info(f"Deleting Role: {role['name']}")
            resp = ipf.delete(f'roles/{role["id"]}')
            resp.raise_for_status()

    resp = ipf.get('policies')
    resp.raise_for_status()

    for policy in resp.json()['data']:
        if not policy['isSystem']:
            logger.info(f"Deleting Policy {policy['name']}")
            resp = ipf.delete(f'policies/scopes/api/{policy["id"]}')
            resp.raise_for_status()

    return 0

def create_rbac(ipf, roles, policies) -> int:
    data = yaml.safe_load(policies)

    for k, v in data.items():
        for method, m_values in v.items():
            if len(k) <= 4:
                name = k.upper()
            else:
                name = k.replace('_', ' ').capitalize()

            scopes = [x['scope'] for x in m_values]
            if scopes:
                name = f"{name} ({method.upper()})"
                payload = {
                    "name": name,
                    "description": name,
                    "apiScopeIds": scopes
                }
                try:
                    logger.info(f"Creating Policy {name}")
                    res = ipf.post('policies/scopes/api', json=payload)
                    res.raise_for_status()
                except Exception as e:
                    logger.info(f"Policy Already Present: {name}")

    data = yaml.safe_load(roles)
    data = data['roles']
    
    policies = ipf.get('policies').json()['data']
    

    name_to_id = {}

    for policy in policies:
            name_to_id[policy['name']] = policy['id']

    for role in data:
        policies = [name_to_id[f"{x}"] for x in role['policies']]
        payload = {"name":role['name'],"description": role.get("description", ""),"policyIds": policies}
        try:
            logger.info(f"Creating Role: {role['name']}")
            resp = ipf.post('roles', json=payload)
            resp.raise_for_status()
        except Exception as e:
            logger.info(f"Role Already Present: {role['name']}")


    return 0

def main() -> int:
    parser = argparse.ArgumentParser(prog="IP Fabric RBAC Script", description="Configures IP Fabric RBAC Policies from YAML files.")
    parser.add_argument("--roles", type=argparse.FileType('r'), default="roles.yaml", help="Path to roles YAML file.")
    parser.add_argument("--policies", type=argparse.FileType('r'), default="policies.yaml", help="Path to policies YAML file.")
    parser.add_argument("--delete-all", action="store_true", help="Delete all RBAC none default roles and policies.")
    parser.add_argument("--verify", action="store_false", help="This will disable SSL certificate verification.")
    parser.add_argument("--version", help="Specify API Version.")
    parser.add_argument("--verbose", action="store_true", help="Enable stdout console logging.")
    args = parser.parse_args()

    if args.verbose:
        handler = logging.StreamHandler(sys.stdout)
        handler.setLevel(logging.DEBUG)
        handler.setFormatter(logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s'))
        logger.addHandler(handler)
        logger.setLevel(logging.DEBUG)
    
    ipf = IPFClient(api_version=args.version, verify=args.verify)

    if args.delete_all:
        delete_rbac(ipf)
    else:
        create_rbac(ipf, args.roles, args.policies)

    return 0


if __name__ == "__main__":
    raise SystemExit(main())