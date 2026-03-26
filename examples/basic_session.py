"""
Basic Session Usage Examples

This script demonstrates basic session usage with the nanohubremote library,
including authentication, HTTP methods, and error handling.
"""

import nanohubremote as nr

# Example 1: Personal Token Authentication
print("=" * 60)
print("Example 1: Personal Token Authentication")
print("=" * 60)

auth_data = {
    'grant_type': 'personal_token',
    'token': 'your_personal_token_here'
}

# Create session with context manager (recommended)
with nr.Session(auth_data) as session:
    print(f"Session authenticated: {session.authenticated}")
    
    # Example 2: Simple GET Request
    print("\n" + "=" * 60)
    print("Example 2: Simple GET Request")
    print("=" * 60)
    
    response = session.requestGet('users/profile')
    if response.status_code == 200:
        data = response.json()
        print(f"User: {data.get('name', 'Unknown')}")
    else:
        print(f"Request failed with status code: {response.status_code}")
    
    # Example 3: POST Request with JSON
    print("\n" + "=" * 60)
    print("Example 3: POST Request with JSON")
    print("=" * 60)
    
    payload = {
        'name': 'Test',
        'value': 123,
        'enabled': True
    }
    response = session.requestPost('endpoint', json=payload)
    print(f"POST Status: {response.status_code}")
    
    # Example 4: PUT Request
    print("\n" + "=" * 60)
    print("Example 4: PUT Request")
    print("=" * 60)
    
    resource_id = '123'
    updates = {
        'status': 'active',
        'updated_at': '2024-12-01'
    }
    
    response = session.requestPut(
        f'resource/{resource_id}',
        json=updates
    )
    
    if response.status_code == 200:
        print("Resource updated successfully")
    
    # Example 5: Error Handling
    print("\n" + "=" * 60)
    print("Example 5: Error Handling")
    print("=" * 60)
    
    from requests.exceptions import RequestException, Timeout
    
    try:
        response = session.requestGet('users/profile')
        response.raise_for_status()
        data = response.json()
        print("Request successful")
    except Timeout:
        print("Request timed out")
    except RequestException as e:
        print(f"Request failed: {e}")
    except ValueError:
        print("Invalid JSON response")

print("\n" + "=" * 60)
print("All examples completed!")
print("=" * 60)
