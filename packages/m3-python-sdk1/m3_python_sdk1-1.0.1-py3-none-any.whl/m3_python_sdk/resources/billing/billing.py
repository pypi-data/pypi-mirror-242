import os
import time

from m3_python_sdk.services.s3_client import S3Client
from m3_python_sdk.strategies.http import HttpStrategy
from m3_python_sdk.strategies.rabbitmq import RabbitMqStrategy
from m3_python_sdk.utils.constants import BillingApiActions, SdkCloud, \
    StatusCodes
from m3_python_sdk.utils.exeption import raise_application_exception
from m3_python_sdk.utils.file_utils import FileLikeObjectPrepare, \
    check_file_size


class BillingResource:

    def __init__(self, client: 'RabbitMqStrategy' or 'HttpStrategy',
                 s3_client: 'S3Client'):
        self._client = client
        self.s3_client = s3_client

    def describe_billing_month(self, year: int, month: int,
                               sync: bool = True, secure_parameters=None,
                               is_flat_request=None, compressed: bool = False
                               ) -> dict:
        params = {
            'year': year,
            'month': month
        }

        res = self._client.execute(
            command_name=BillingApiActions.DESCRIBE_BILLING_MONTH,
            request_data=params,
            sync=sync,
            secure_parameters=secure_parameters,
            is_flat_request=is_flat_request,
            compressed=compressed
        )

        return res

    def describe_currency(self, year: int, month: int, cloud: SdkCloud,
                          sync: bool = True, secure_parameters=None,
                          is_flat_request=None, compressed: bool = False
                          ) -> dict:
        params = {
            'year': year,
            'month': month,
            'cloud': cloud
        }

        res = self._client.execute(
            command_name=BillingApiActions.DESCRIBE_CURRENCY,
            request_data=params,
            sync=sync,
            secure_parameters=secure_parameters,
            is_flat_request=is_flat_request,
            compressed=compressed
        )

        return res

    def get_top_account_reports(self, year: int, month: int, bucket: str,
                                number: int = 10, email: str = None,
                                sync: bool = True, secure_parameters=None,
                                is_flat_request=None, compressed: bool = False
                                ) -> dict:
        params = {
            'year': year,
            'month': month,
            'number': number
        }

        res = self._client.execute(
            command_name=BillingApiActions.GET_TOP_ACCOUNTS_REPORT,
            request_data=params,
            sync=sync,
            secure_parameters=secure_parameters,
            is_flat_request=is_flat_request,
            compressed=compressed
        )

        result = res.get('items', [])
        formatted_report = []

        for data in result:
            replace_total = {item.replace('Total', ''): value for item, value
                             in data.items()}
            formatted_report.append(replace_total)

        if email:
            data_list = []
            for idx, data in enumerate(formatted_report):
                if idx == 0:
                    data_list.append(list(data))
                data_list.append(list(data.values()))

            time_str = time.strftime("%d%m%Y_%H%M%S")
            file_name = f'top_accounts_report_{time_str}.csv'
            raw_data = FileLikeObjectPrepare(file_name, data_list).transform()

            link = self.s3_client.get_presigned_url(
                file_name=file_name,
                content=raw_data,
                bucket=bucket
            )
            email_params = {
                'email': email,
                'fileName': file_name,
                'date': time.time_ns() // 1_000_000,
                'reportTitle': 'Top ${number} accounts',
                'placeholders': {'number': number},
                'command': 'billing get_top_accounts_report',
                'parameters': {
                    "year": year,
                    "month": month,
                    "number": number
                },
                'result': link
            }

            res = self._client.execute(
                command_name=BillingApiActions.SEND_COMMAND_EXECUTION_RESULT_REPORT,
                request_data=email_params,
                sync=sync,
                secure_parameters=secure_parameters,
                is_flat_request=is_flat_request,
                compressed=compressed
            )

            return {
                'status_code': res.get('status_code'),
                'status': res.get('status'),
                'message': f'An e-mail with a link to the report file '
                           f'has been sent to: \'{email}\'. '
                           f'Link (valid for 1 hour): {link}'
            }

        return {
            'formatted_reports': formatted_report,
            'table_title': 'Top accounts report'
        }

    def pricing_policy(self, action: str, region: str, file, bucket: str,
                       email: str = None):

        if action not in ['GET', 'UPDATE', 'CHECK',
                          'CHANGE_TIME_UNIT_TO_PER_SECOND']:
            raise_application_exception(
                code=StatusCodes.BAD_REQUEST_400,
                content={'error': 'Action not in allowed'}
            )

        # TODO check region

        if action == 'GET':
            return self.get_billing_pricing_policy(region, email, bucket)
        if action != 'CHANGE_TIME_UNIT_TO_PER_SECOND' and not file:
            raise_application_exception(
                code=StatusCodes.BAD_REQUEST_400,
                content=f'Parameter \'--file\' is required for action {action}'
            )
        if action == 'UPDATE' or action == 'CHECK':
            check_file_size(file_path=file,
                            max_size_bytes=1024 * 1024 * 3)
        elif action == 'UPDATE':
            return self.update_billing_pricing_policy(region, file)
        elif action == 'CHECK':
            return self.check_billing_pricing_policy(region, file)
        elif action == 'CHANGE_TIME_UNIT_TO_PER_SECOND':
            return self.billing_change_time_unit_to_per_second(region)

    def get_billing_pricing_policy(self, region: str, email: str = None,
                                   bucket: str = None, sync: bool = True,
                                   secure_parameters=None,
                                   is_flat_request=None,
                                   compressed: bool = False
                                   ):

        params = {'region': region}

        res = self._client.execute(
            command_name=BillingApiActions.GET_PRICING_POLICY,
            request_data=params,
            sync=sync,
            secure_parameters=secure_parameters,
            is_flat_request=is_flat_request,
            compressed=compressed
        )

        file_name = f'pricing_policy_{region.lower()}.xml'

        if email:
            content = res.get('message', None)
            raw_data = FileLikeObjectPrepare(file_name, content).transform()

            link = self.s3_client.get_presigned_url(
                file_name=file_name,
                content=raw_data,
                bucket=bucket,
            )

            email_params = {
                'email': email,
                'fileName': file_name,
                'date': time.time_ns() // 1_000_000,
                'reportTitle': 'Pricing policy for the ${region} region',
                'placeholders': {'region': region},
                'command': 'billing pricing_policy',
                'parameters': {
                    "action": 'GET',
                    "region": region
                },
                'result': link
            }

            res = self._client.execute(
                command_name=BillingApiActions.SEND_COMMAND_EXECUTION_RESULT_REPORT,
                request_data=email_params,
                sync=sync,
                secure_parameters=secure_parameters,
                is_flat_request=is_flat_request,
                compressed=compressed
            )

            return {
                'status_code': res.get('status_code'),
                'status': res.get('status'),
                'message': f'An e-mail with a link to the report file has been'
                           f' sent to: \'{email}\'.'
                           f' Link (valid for 1 hour): {link}'
            }

        return res

    def update_billing_pricing_policy(self, region, path,
                                      sync: bool = True,
                                      secure_parameters=None,
                                      is_flat_request=None,
                                      compressed: bool = False
                                      ):

        if not os.path.exists(path):
            raise_application_exception(
                code=400,
                content=f'There is no such file: {path}'
            )
        policy = ''
        with open(path) as policy_in_file:
            for each in policy_in_file:
                policy += each
            policy_in_file.close()

        params = {
            'region': region,
            'policy': policy
        }
        res = self._client.execute(
            command_name=BillingApiActions.GET_PRICING_POLICY,
            request_data=params,
            sync=sync,
            secure_parameters=secure_parameters,
            is_flat_request=is_flat_request,
            compressed=compressed
        )

        return res

    def check_billing_pricing_policy(self, region, path,
                                     sync: bool = True,
                                     secure_parameters=None,
                                     is_flat_request=None,
                                     compressed: bool = False
                                     ):
        if not os.path.exists(path):
            raise_application_exception(
                code=400,
                content=f'There is no such file: {path}'
            )
        policy = ''
        with open(path) as policy_in_file:
            for each in policy_in_file:
                policy += each
            policy_in_file.close()

        params = {
            'region': region,
            'policy': policy
        }

        res = self._client.execute(
            command_name=BillingApiActions.CHECK_PRICING_POLICY,
            request_data=params,
            sync=sync,
            secure_parameters=secure_parameters,
            is_flat_request=is_flat_request,
            compressed=compressed
        )

        return res

    def billing_change_time_unit_to_per_second(self, region,
                                               sync: bool = True,
                                               secure_parameters=None,
                                               is_flat_request=None,
                                               compressed: bool = False
                                               ):
        params = {
            'region': region
        }

        res = self._client.execute(
            command_name=BillingApiActions.CHANGE_TIME_UNIT_TO_PER_SECOND,
            request_data=params,
            sync=sync,
            secure_parameters=secure_parameters,
            is_flat_request=is_flat_request,
            compressed=compressed
        )

        return res

    # TODO 500 error, Unexpected error. Reason: The bucket name parameter
    #  must be specified when listing objects in a bucket
    def send_paas_reports(self, month: int, year: int,
                          sync: bool = True, secure_parameters=None,
                          is_flat_request=None, compressed: bool = False
                          ):

        params = {
            'year': year,
            'month': month
        }

        res = self._client.execute(
            command_name=BillingApiActions.SEND_PAAS_BILLING_REPORTS,
            request_data=params,
            sync=sync,
            secure_parameters=secure_parameters,
            is_flat_request=is_flat_request,
            compressed=compressed
        )

        return res

    # TODO check response
    def add_cost_center(self, regions: list, cost_center: str,
                        rewrite: bool = True,
                        sync: bool = True, secure_parameters=None,
                        is_flat_request=None, compressed: bool = False
                        ):

        params = {
            'zone': list(regions),
            'center': cost_center,
            'rewrite': rewrite
        }

        res = self._client.execute(
            command_name=BillingApiActions.ADD_COST_CENTER,
            request_data=params,
            sync=sync,
            secure_parameters=secure_parameters,
            is_flat_request=is_flat_request,
            compressed=compressed
        )

        return res

    def health_check(self, bill_from: str, skip_checkpoints: bool = False,
                     skip_volumes: bool = False,
                     skip_machine_images: bool = False,
                     skip_broken_events: bool = False,
                     skip_deleted_instances: bool = False,
                     skip_base_quantity: bool = False,
                     fix_events: bool = False,
                     sync: bool = True, secure_parameters=None,
                     is_flat_request=None, compressed: bool = False
                     ):

        params = {
            'bill_from': bill_from,
            'skip_checkpoints': skip_checkpoints,
            'skip_volumes': skip_volumes,
            'skip_machine_images': skip_machine_images,
            'skip_broken_events': skip_broken_events,
            'skip_deleted_instances': skip_deleted_instances,
            'skip_base_quantity': skip_base_quantity,
            'fix_events': fix_events
        }

        res = self._client.execute(
            command_name=BillingApiActions.BILLING_HEALTH_CHECK,
            request_data=params,
            sync=sync,
            secure_parameters=secure_parameters,
            is_flat_request=is_flat_request,
            compressed=compressed
        )

        return res

    def archive_big_query(self, admin_project_id: str, table_id: str,
                          year: int = None, month: int = None,
                          archivation: str = None,
                          sync: bool = True, secure_parameters=None,
                          is_flat_request=None, compressed: bool = False
                          ):

        if not (year and month) and not archivation:
            raise_application_exception(
                code=StatusCodes.BAD_REQUEST_400,
                content={
                    'error': 'year and month or archivation must be specified'
                }
            )

        params = {
            'adminProjectId': admin_project_id,
            'tableId': table_id
        }
        if archivation:
            archivation = True if archivation == 'enabled' else False
            params.update({'archivationEnabled': archivation})
        if year and month:
            params.update({'year': year, 'month': month})

        res = self._client.execute(
            command_name=BillingApiActions.ARCHIVE_BIG_QUERY,
            request_data=params,
            sync=sync,
            secure_parameters=secure_parameters,
            is_flat_request=is_flat_request,
            compressed=compressed
        )

        return res

    def health_check_v2(self, email: str,
                        sync: bool = True, secure_parameters=None,
                        is_flat_request=None, compressed: bool = False):

        params = {
            'email': email
        }

        res = self._client.execute(
            command_name=BillingApiActions.BILLING_HEALTH_CHECK_V2,
            request_data=params,
            sync=sync,
            secure_parameters=secure_parameters,
            is_flat_request=is_flat_request,
            compressed=compressed
        )

        return res

    def billing_configure(self, aws_athena_update_schedule: str,
                          aws_cost_explorer_update_schedule: str,
                          aws_cost_column, aws_update_period: str,
                          azure_update_schedule: str, supported_service: str,
                          customize_report_structure: str, describe: str,
                          sync: bool = True, secure_parameters=None,
                          is_flat_request=None, compressed: bool = False):

        aws_update_period = aws_update_period.upper()
        if aws_update_period not in ['DAYS', 'TWO_DAYS', 'THREE_DAYS',
                                     'WEEK', 'MONTH']:
            raise_application_exception(
                code=400,
                content={'error': 'aws_update_period value not allowed'}
            )
        if aws_cost_column not in ['BlendedCost', 'UnBlendedCost']:
            raise_application_exception(
                code=400,
                content={'error': 'aws_cost_column value not allowed'}
            )

        params = {
            'describe': describe,
            'awsAthenaUpdateSchedule': aws_athena_update_schedule,
            'awsCostExplorerUpdateSchedule': aws_cost_explorer_update_schedule,
            'awsCostColumnName': aws_cost_column,
            'awsUpdatePeriod': aws_update_period,
            'azureUpdateSchedule': azure_update_schedule,
            'customizeReportStructure': customize_report_structure,
            'supportedServices': supported_service,
        }

        res = self._client.execute(
            command_name=BillingApiActions.BILLING_CONFIGURE,
            request_data=params,
            sync=sync,
            secure_parameters=secure_parameters,
            is_flat_request=is_flat_request,
            compressed=compressed
        )

        return res
