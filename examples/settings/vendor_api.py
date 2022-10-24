from httpx import HTTPStatusError

from ipfabric import IPFClient
from ipfabric.settings import VendorAPI, AWS, Azure, CheckPointApiKey, CheckPointUserAuth, \
    CiscoFMC, Merakiv1, NSXT, SilverPeak, Versa, Viptela, AWS_REGIONS

if __name__ == "__main__":

    ipf = IPFClient()
    # ipf = IPFClient('https://demo3.ipfabric.io/', token='token', verify=False, timeout=15, snapshot_id='$last')

    api = VendorAPI(ipf)

    current_apis = api.get_vendor_apis()

    try:
        delete = api.delete_vendor_api(api_id='1183688478')
    except HTTPStatusError as err:
        print(err)

    aws = AWS(apiKey='KEY', apiSecret='SECRET', regions=['eu-central-1'], respectSystemProxyConfiguration=True)
    aws_assume = AWS(apiKey='KEY', apiSecret='SECRET', regions=AWS_REGIONS, assumeRoles=['arn:aws:iam::ID:role/NAME'])
    # Above will add ALL AWS Regions

    add = api.add_vendor_api(aws_assume)
    print(add)
    """
    {
      "type": "aws-ec2",
      "apiKey": "KEY",
      "apiSecret": "SECRET",
      "isEnabled": true,
      "regions": [
            "us-east-2",
            "us-east-1",
            "us-west-1",
            "us-west-2",
            "af-south-1",
            ...
        ],
      "respectSystemProxyConfiguration": false,
      "assumeRoles": [
        {
          "role": "arn:aws:iam::ID:role/NAME"
        }
      ]
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
