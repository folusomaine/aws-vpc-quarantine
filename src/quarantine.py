import boto3
from aws_lambda_powertools.logging import Logger

logger = Logger()


def lambda_handler(event, context):
    logger.info(event)
    handler = QuarantineHandler(event)
    handler.quarantine_vpc()


class QuarantineHandler:
    def __init__(self, event) -> None:
        self.instance_id = event["detail"]["resource"]["instanceDetails"]["instanceId"]
        self.vpc_id = event["detail"]["resource"]["instanceDetails"][
            "networkInterfaces"
        ][0]["vpcId"]
        self.subnet_id = event["detail"]["resource"]["instanceDetails"][
            "networkInterfaces"
        ][0]["subnetId"]
        self.region = event["region"]
        self.ec2_client = boto3.client("ec2", region_name=self.region)

    @property
    def current_subnet_nacl_association_id(self):
        """
        Get the current association id for the subnet
        """
        response = self.ec2_client.describe_network_acls(
            Filters=[
                {
                    "Name": "association.subnet-id",
                    "Values": [
                        self.subnet_id,
                    ],
                },
            ]
        )
        return response["NetworkAcls"][0]["Associations"][0]["NetworkAclAssociationId"]

    def _if_quarantine_nacl_association_exists(self):
        """
        Check if the quarantine nacl exists
        """
        try:
            response = self.ec2_client.describe_network_acls(
                Filters=[
                    {
                        "Name": "tag:Name",
                        "Values": [
                            "quarantine-nacl",
                        ],
                    },
                ]
            )
            if response["NetworkAcls"][0]["Associations"][0]["SubnetId"] == self.subnet_id:
                logger.info("Quarantine nacl already enforced.")
                return True
        except (KeyError, IndexError) as e:
            logger.info(f"Quarantine nacl does not exist. Proceed with VPC subnet Quarantine.")
            return False

    def _create_quarantine_nacl(self):
        """
        Create the quarantine nacl
        """
        response = self.ec2_client.create_network_acl(
            VpcId=self.vpc_id,
            TagSpecifications=[
                {
                    "ResourceType": "network-acl",
                    "Tags": [
                        {"Key": "Name", "Value": "quarantine-nacl"},
                    ],
                },
            ],
        )
        logger.info(f"Quarantine nacl created. Response: {response}")
        self.quarantine_nacl_id = response["NetworkAcl"]["NetworkAclId"]
        return

    def _associate_quarantine_nacl_with_subnet(self):
        """
        Associate the quarantine nacl with the subnet
        """
        response = self.ec2_client.replace_network_acl_association(
            AssociationId=self.current_subnet_nacl_association_id,
            NetworkAclId=self.quarantine_nacl_id,
        )
        logger.info(
            f"Quarantine nacl associated with subnet successfully. Response: {response}"
        )
        return

    def quarantine_vpc(self):
        """
        Quarantine the vpc
        """
        logger.info(
            f"Indication of compromise - instance: {self.instance_id} in {self.subnet_id}. Quarantining vpc: {self.vpc_id}"
        )
        if self._if_quarantine_nacl_association_exists():
            return
        self._create_quarantine_nacl()
        self._associate_quarantine_nacl_with_subnet()
