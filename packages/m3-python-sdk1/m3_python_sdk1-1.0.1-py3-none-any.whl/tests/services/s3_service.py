class S3Client:

    @staticmethod
    def get_presigned_url(file_name: str, content: str, bucket: str):

        data_for_url = {
            'file_name': file_name,
            'content': content,
            'bucket': bucket
        }

        return f'data for url: {data_for_url}'
