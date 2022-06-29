from httpx import HTTPStatusError

from ipfabric import IPFClient
from ipfabric.settings import VendorAPI, AWS, Azure, CheckPointApiKey, CheckPointUserAuth, \
    CiscoFMC, Merakiv1, NSXT, SilverPeak, Versa, Viptela

if __name__ == "__main__":

    ipf = IPFClient()
    # ipf = IPFClient('https://demo3.ipfabric.io/', token='token', verify=False, timeout=15, snapshot_id='$last')

    api = VendorAPI(ipf)

    current_apis = api.get_vendor_apis()

    try:
        delete = api.delete_vendor_api(api_id='1183688478')
    except HTTPStatusError as err:
        print(err)

    aws = AWS(apiKey='KEY', apiSecret='SECRET', region='eu-central-1', respectSystemProxyConfiguration=True)
    aws_assume = AWS(apiKey='KEY', apiSecret='SECRET', region='eu-central-1', assumeRole='arn:aws:iam::ID:role/NAME')

    add = api.add_vendor_api(aws)
    print(add)
    """
    {
        'region': 'eu-central-1', 
        'isEnabled': True, 
        'type': 'aws-ec2', 
        'apiVersion': '2016-11-15', 
        'baseUrl': 'https://ec2.eu-central-1.amazonaws.com', 
        'id': '1379621882', 
        'details': 'eu-central-1'
    }
    """

    azure = Azure(clientId='CLIENTID', clientSecret='CLIENTSECRET', subscriptionId='SUBSCRIPTION', tenantId='TENANTID')
    checkpoint_api = CheckPointApiKey(apiKey='APIKEY', baseUrl='https://test.com', domains=['test'],  # domains is optional
                                      respectSystemProxyConfiguration=True, rejectUnauthorized=True)
    checkpoint = CheckPointUserAuth(username='user', password='password', baseUrl='https://test.com')
    cisco = CiscoFMC(username='user', password='password', baseUrl='https://test.com')
    meraki = Merakiv1(apiKey='APIKEY', baseUrl='https://test.com', organizations=['test'])  # organizations is optional
    nsxt = NSXT(username='user', password='password', baseUrl='https://test.com')
    silverpeak = SilverPeak(username='user', password='password', baseUrl='https://test.com')
    versa = Versa(username='user', password='password', baseUrl='https://test.com')
    viptela = Viptela(username='user', password='password', baseUrl='https://test.com')
