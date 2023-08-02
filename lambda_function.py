import boto3

def get_volume_id_from_arn(volume_arn):
    # Split the ARN string using the ':' separator
    parts = volume_arn.split(':')

    # Get the last part of the ARN
    last_part = parts[-1]

    # Split the last part using the '/' separator and get the volume ID
    volume_id = last_part.split('/')[-1]

    return volume_id

def lambda_handler(event, context):
    print(f"Event received: {event}")
    
    try:
        resource_arn = event['resources'][0]
    except KeyError:
        return {
            'statusCode': 400,
            'body': 'Invalid event format: missing "resources".'
        }

    resource_id = resource_arn.split('/')[-1]

    client = boto3.client('ec2', region_name='eu-north-1')

    # Check if the resource is a volume or a snapshot
    if 'volume' in resource_arn:
        volume_id = get_volume_id_from_arn(resource_arn)

        try:
            response = client.modify_volume(
                VolumeId=volume_id,
                VolumeType='gp3',
            )
            print(f"Modify volume response: {response}")
        except Exception as e:
            return {
                'statusCode': 500,
                'body': f'Failed to modify volume: {str(e)}'
            }

        # Create the snapshot and add the desired tag in one step
        tag_key = 'Description'
        tag_value = 'This is a test snapshot creation by Salman'
        try:
            response_snapshot = client.create_snapshot(
                VolumeId=volume_id,
                Description='Snapshot created by Lambda function',
                TagSpecifications=[
                    {
                        'ResourceType': 'snapshot',
                        'Tags': [
                            {
                                'Key': tag_key,
                                'Value': tag_value
                            },
                        ]
                    },
                ]
            )
            print(f"Create snapshot response: {response_snapshot}")
        except Exception as e:
            return {
                'statusCode': 500,
                'body': f'Failed to create snapshot: {str(e)}'
            }

        snapshot_id = response_snapshot['SnapshotId']

    elif 'snapshot' in resource_arn:
        snapshot_id = resource_id

        # Add the desired tag to the snapshot
        tag_key = 'Description'
        tag_value = 'This is a test snapshot creation by Salman'
        try:
            response = client.create_tags(
                Resources=[snapshot_id],
                Tags=[
                    {
                        'Key': tag_key,
                        'Value': tag_value
                    },
                ]
            )
            print(f"Create tags response: {response}")

        except Exception as e:
            return {
                'statusCode': 500,
                'body': f'Failed to create tag: {str(e)}'
            }

    else:
        return {
            'statusCode': 400,
            'body': 'Invalid resource type. This function only supports volumes and snapshots.'
        }

    return {
        'statusCode': 200,
        'body': 'Operation completed successfully.'
    }
