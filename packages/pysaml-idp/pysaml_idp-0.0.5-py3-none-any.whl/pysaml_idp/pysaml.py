import zlib
import base64
import urllib.parse
import uuid
from datetime import datetime
import xml.etree.ElementTree as ET

def decode_base64_and_inflate( b64string ):
    decoded_data = base64.b64decode( b64string )
    return zlib.decompress( decoded_data , -15)

def deflate_and_base64_encode( string_val ):
    zlibbed_str = zlib.compress( string_val )
    compressed_string = zlibbed_str[2:-4]
    return base64.b64encode( compressed_string )


class SAML2:

    def __init__(self, application_ID, redirect_url, login_url, logout_url):
        self.application_ID=application_ID # 1d231f9b-f7d4-411f-a6b5-c2031e61518d
        self.redirect_url=redirect_url # https://127.0.0.1:3000/auth/callback
        self.login_url=login_url
        self.logout_url=logout_url

    def prepare_request(self):
        # Your XML request
        # xml_request = '''<samlp:AuthnRequest xmlns="urn:oasis:names:tc:SAML:2.0:metadata" ID="F84D888AA3B44C1B844375A4E8210D9E" Version="2.0" IssueInstant="2023-11-17T22:11:17.294Z" IsPassive="false" AssertionConsumerServiceURL="https://127.0.0.1:3000/auth/callback" xmlns:samlp="urn:oasis:names:tc:SAML:2.0:protocol" ForceAuthn="false"><Issuer xmlns="urn:oasis:names:tc:SAML:2.0:assertion">flask_saml</Issuer></samlp:AuthnRequest>'''
        now = datetime.now()
        formatted_date = now.strftime('%Y-%m-%dT%H:%M:%S.%fZ')
        saml_request_id = 'ID'+str(uuid.uuid4())

        # print(f"SAML2 Config:\nApp ID:{self.application_ID}\nCallback URL:{self.redirect_url}\nLogin URL:{self.login_url}")
        #xml_request = f'<samlp:AuthnRequest xmlns="urn:oasis:names:tc:SAML:2.0:metadata" ID="{saml_request_id}" Version="2.0" IssueInstant="{formatted_date}" IsPassive="false" AssertionConsumerServiceURL="https://127.0.0.1:3000/auth/callback" xmlns:samlp="urn:oasis:names:tc:SAML:2.0:protocol" ForceAuthn="false"><Issuer xmlns="urn:oasis:names:tc:SAML:2.0:assertion">flask_saml</Issuer></samlp:AuthnRequest>'
        #xml_request = f'<samlp:AuthnRequest xmlns="urn:oasis:names:tc:SAML:2.0:metadata" ID="{saml_request_id}" Version="2.0" IssueInstant="{formatted_date}" IsPassive="false" AssertionConsumerServiceURL="https://127.0.0.1:3000/auth/callback" xmlns:samlp="urn:oasis:names:tc:SAML:2.0:protocol" ForceAuthn="false"><Issuer xmlns="urn:oasis:names:tc:SAML:2.0:assertion">app-indra-idp-corp-Biometrico-Colombia-DES</Issuer></samlp:AuthnRequest>'
        xml_request = f'<samlp:AuthnRequest xmlns="urn:oasis:names:tc:SAML:2.0:metadata" ID="{saml_request_id}" Version="2.0" IssueInstant="{formatted_date}" IsPassive="false" AssertionConsumerServiceURL="{self.redirect_url}" xmlns:samlp="urn:oasis:names:tc:SAML:2.0:protocol" ForceAuthn="false"><Issuer xmlns="urn:oasis:names:tc:SAML:2.0:assertion">{self.application_ID}</Issuer></samlp:AuthnRequest>'

        # deflate and encode for Microsoft Entra ID
        deflate_encode_request_bytes = deflate_and_base64_encode(xml_request.encode())
        deflate_encode_request_string = deflate_encode_request_bytes.decode('utf-8')
        deflate_encode_request_string_url = urllib.parse.quote(deflate_encode_request_string)

        # print(deflate_encode_request_string_url)
        saml_redirect_url = self.login_url + '?SAMLRequest=' + deflate_encode_request_string_url
        return saml_redirect_url

    def extract_claims(self, saml_response):
        # Decode the SAMLResponse and decompress it
        decoded_response = base64.b64decode(saml_response)

        # Parse the decompressed SAML response XML and extract the claims
        root = ET.fromstring(decoded_response)

        namespace = {'saml': 'urn:oasis:names:tc:SAML:2.0:assertion'}
        claims = {}

        attribute_statements = root.findall('.//saml:AttributeStatement', namespace)
        for statement in attribute_statements:
            attribute_elements = statement.findall('.//saml:Attribute', namespace)
            for attribute in attribute_elements:
                name = attribute.get('Name')
                values = [value.text for value in attribute.findall('.//saml:AttributeValue', namespace)]
                claims[name] = values

        return claims