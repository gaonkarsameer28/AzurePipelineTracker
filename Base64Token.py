import base64

# use this code to convert your PAT to a base64 token . do not store the PAT in the code.
# Your PAT 
my_pat = 'Your_PAT'

# Encode PAT
encoded_pat = base64.b64encode(f":{my_pat}".encode('utf-8')).decode('utf-8')

# Construct the header value
header_value = f"Authorization: Basic {encoded_pat}"

print(header_value)
