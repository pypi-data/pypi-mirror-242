import json


class ContractStrategy:

    def __init__(self):
        pass

    @staticmethod
    def execute(command_name: str, request_data: dict, **kwargs):

        try:
            with open("m3_python_sdk_contract.json", "r") as f:
                existing_data = json.load(f)
        except FileNotFoundError:
            existing_data = {}
        except json.JSONDecodeError:
            existing_data = {}

        naming_map = {
            'target_project': 'targetTenant',
            'target_account_number': 'targetAccountNumber',
            'target_region': 'targetRegion',
            'target_cloud': 'targetCloud',
            'credit_type': 'creditType',
            'currency_native': 'currencyNative',
            'source_project': 'sourceTenant',
            'source_account_number': 'sourceAccountNumber',
            'service_name': 'serviceName'
        }

        contract = {}
        for key, value in request_data.items():

            if key in naming_map:
                new_key = naming_map[key]
                contract.update({new_key: value})
            elif key == 'target':
                if ('onlyGrandTotal' in value and value['onlyGrandTotal']
                        == 'true'):
                    value['onlyGrandTotal'] = True
                else:
                    value['onlyGrandTotal'] = False
                contract.update({key: value})
            else:
                contract.update({key: value})

        if command_name not in existing_data.keys():
            existing_data.update({command_name: []})
            existing_data[command_name].append(contract)
        else:
            for i, existing_contract in enumerate(existing_data[command_name]):
                if existing_contract == contract:
                    existing_data[command_name][i] = contract
                    break
            else:
                existing_data[command_name].append(contract)

        with open("m3_python_sdk_contract.json", "w") as f:
            json.dump(existing_data, f)

        res = {}

        return res
