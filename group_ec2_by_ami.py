import json
from unittest.mock import Mock

def get_instances_grouped_by_ami():
    # Mock the AWS EC2 client
    ec2 = Mock()

    # Mock response for describe_instances
    ec2.describe_instances.return_value = {
        'Reservations': [
            {
                'Instances': [
                    {'ImageId': 'ami-12345', 'InstanceId': 'i-12345'},
                    {'ImageId': 'ami-12345', 'InstanceId': 'i-67890'},
                    {'ImageId': 'ami-67890', 'InstanceId': 'i-13579'},
                ]
            }
        ]
    }

    # Mock response for describe_images
    def mock_describe_images(ImageIds):
        if ImageIds[0] == "ami-unknown":
            return {"Images": []}
        else:
            return {
                "Images": [
                    {
                        "ImageId": ImageIds[0],
                        "Description": f"Mock description for {ImageIds[0]}",
                        "Name": f"Mock name for {ImageIds[0]}",
                        "ImageLocation": f"mock_account/{ImageIds[0]}",
                        "OwnerId": "mock_owner_id",
                    }
                ]
            }
    ec2.describe_images.side_effect = mock_describe_images

    # Dictionary to store grouped data
    ami_data = {}

    # Fetch mock data
    instances_response = ec2.describe_instances()
    for reservation in instances_response['Reservations']:
        for instance in reservation['Instances']:
            ami_id = instance['ImageId']
            instance_id = instance['InstanceId']

            # Get AMI details
            ami_details = ami_data.get(ami_id)
            if not ami_details:
                image_response = ec2.describe_images([ami_id])
                if image_response["Images"]:
                    image = image_response["Images"][0]
                    ami_details = {
                        "ImageDescription": image.get("Description"),
                        "ImageName": image.get("Name"),
                        "ImageLocation": image.get("ImageLocation"),
                        "OwnerId": image.get("OwnerId"),
                        "InstanceIds": [],
                    }
                else:
                    ami_details = {
                        "ImageDescription": None,
                        "ImageName": None,
                        "ImageLocation": None,
                        "OwnerId": None,
                        "InstanceIds": [],
                    }
            ami_details["InstanceIds"].append(instance_id)
            ami_data[ami_id] = ami_details

    # Output the grouped data as JSON
    print(json.dumps(ami_data, indent=4))

# Execute the function
if __name__ == "__main__":
    get_instances_grouped_by_ami()
