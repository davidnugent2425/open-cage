import evervault
import urllib3
import requests
import time

attested_session = evervault.cage_requests_session({ 
    'open-cage': {
        'pcr_0': 'bbc1569170bba7e59a00f8b59aca4d6c5d78009fd2231f230adf331377db82ae0ae5c7a989da713be5de28de6cbf4649',
        'pcr_1': 'bcdf05fefccaa8e55bf2c8d6dee9e79bbff31e34bf28a99aa19e6b29c37ee80b214a414b7607236edf26fcb78654e63f',
        'pcr_2': 'ab53ae1deae63b0c1b63fb9c1904b3e9008103bcd640bf63d4d99cace91b39b80d965e5709c5bd5a60853d48981a25d4',
        'pcr_8': '7eda3ae5d2c373f7fdcdc5d9791f847000f233a96a11bd935133284c20a9457fd53bcc428e77af07b2832f1cb4175a91'
    } 
})

filename = "sample-image.png"
with open(filename, "rb") as file:
    file_bytes = file.read()

fields = {
    "upload": (filename, file_bytes),
}

body, header = urllib3.encode_multipart_formdata(fields)

start = time.time()

response = attested_session.post(
    'https://open-cage.app_263b254706c8.cages.evervault.com/upload',
    headers={'Content-Type': header},
	data=body
)

print(f'Time: {time.time() - start}')
print(response)

with open('response-image.png', 'wb') as output_file:
    output_file.write(response.content)