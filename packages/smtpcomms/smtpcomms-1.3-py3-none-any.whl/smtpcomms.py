import requests

def activate_license(api_key, url, ip, lang):
    activation_url = "https://admin.techscribesol.xyz/api/activate_license"
    
    while True:
        license_code = input("Enter License Code: ")
        client_name = input("Enter Client Name: ")

        headers = {
            'LB-API-KEY': api_key,
            'LB-URL': url,
            'LB-IP': ip,
            'LB-LANG': lang,
            'Content-Type': 'application/json',
        }

        payload = {
            "verify_type": "non_envato",
            "product_id": "8611FB65",  # Replace with your actual product ID
            "license_code": license_code,
            "client_name": client_name
        }

        response = requests.post(activation_url, headers=headers, json=payload)

        if response.status_code == 200:
            activation_result = response.json()
            if activation_result.get('status', False):
                print("License activation successful!")
                # Continue with your next functions here
                break
            else:
                print(f"License activation failed. Error: {activation_result.get('error', 'Unknown error')}")
        else:
            print(f"Failed to connect to the server. Error: {response.status_code}")

        retry = input("Do you want to retry? (y/n): ")
        if retry.lower() != 'y':
            print("Exiting the program.")
            break

if __name__ == "__main__":
    # Replace these values with your actual API key, URL, IP, and language
    api_key = "F1DEA71AC4B1D995BDEC"
    server_url = "https://your-licensebox-server/"
    server_ip = "127.0.0.1"
    language = "english"

    activate_license(api_key, server_url, server_ip, language)
