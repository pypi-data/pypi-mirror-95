
import os

AWS_ACCESS_KEY_ID = os.environ['AWS_ACCESS_KEY_ID']
AWS_SECRET_ACCESS_KEY = os.environ['AWS_SECRET_ACCESS_KEY']
BUCKET = os.environ['BUCKET']
ES_HOST = os.environ['ES_HOST']
ES_PORT = 9200


def get_custodian_policies(type: str = None):
    """
    This method return a list of policies name without extension, that can filter by type
    @return: list of custodian policies name
    """
    custodian_policies = []
    policies_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'policy')
    for (dirpath, dirnames, filenames) in os.walk(policies_path):
        for filename in filenames:
            if not type:
                custodian_policies.append(os.path.splitext(filename)[0])
            elif type and type in filename:
                custodian_policies.append(os.path.splitext(filename)[0])
    return custodian_policies


regions = ['us-east-1', 'us-east-2', 'us-west-1', 'us-west-2']

print("Upload data to ElasticSearch - ec2 index")
policies = get_custodian_policies(type='ec2')
es_index = 'cloud-governance-ec2'
for region in regions:
    for policy in policies:
        os.system(f"sudo podman run --rm --name cloud-governance -e upload_data_es='upload_data_es' -e es_host={ES_HOST} -e es_port={ES_PORT} -e es_index={es_index} -e bucket={BUCKET} -e policy={policy} -e AWS_DEFAULT_REGION={region} -e AWS_ACCESS_KEY_ID={AWS_ACCESS_KEY_ID} -e AWS_SECRET_ACCESS_KEY={AWS_SECRET_ACCESS_KEY} -e log_level=INFO quay.io/ebattat/cloud-governance")


print("Upload data to ElasticSearch - ebs index")
es_index = 'cloud-governance-ebs'
policies = ['ebs_unattached']
for region in regions:
    for policy in policies:
        os.system(f"sudo podman run --rm --name cloud-governance -e upload_data_es='upload_data_es' -e es_host={ES_HOST} -e es_port={ES_PORT} -e es_index={es_index} -e bucket={BUCKET} -e policy={policy} -e AWS_DEFAULT_REGION={region} -e AWS_ACCESS_KEY_ID={AWS_ACCESS_KEY_ID} -e AWS_SECRET_ACCESS_KEY={AWS_SECRET_ACCESS_KEY} -e log_level=INFO quay.io/ebattat/cloud-governance")


print("Upload data to ElasticSearch - gitleaks index")
es_index = 'cloud-governance-gitleaks'
region = 'us-east-1'
policy = 'gitleaks'
os.system(f"sudo podman run --rm --name cloud-governance -e upload_data_es='upload_data_es' -e es_host={ES_HOST} -e es_port={ES_PORT} -e es_index={es_index} -e bucket={BUCKET} -e policy={policy} -e AWS_DEFAULT_REGION={region} -e AWS_ACCESS_KEY_ID={AWS_ACCESS_KEY_ID} -e AWS_SECRET_ACCESS_KEY={AWS_SECRET_ACCESS_KEY} -e log_level=INFO quay.io/ebattat/cloud-governance")
