import boto3

def upload_file(filename):
    try:
        s3_client = boto3.client('s3')
        s3_client.upload_file(f'{filename}', "wplnnewscast", f'rss/{filename}')
    except Exception as err:
        print(f'error uploading to S3: {err}')

def delete_file(filename):
    s3 = boto3.resource('s3')
    s3.Object('wplnnewscast', f'rss/{filename}').delete()

