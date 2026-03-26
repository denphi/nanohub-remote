"""
Session Management Examples

This script demonstrates advanced session management features including
state management, context managers, and custom configuration.
"""

import nanohubremote as nr

# Example 1: Managing Authentication State
print("=" * 60)
print("Example 1: Managing Authentication State")
print("=" * 60)

auth_data = {
    'grant_type': 'personal_token',
    'token': 'your_token'
}

with nr.Session(auth_data) as session:
    # Check if authenticated
    if session.authenticated:
        print("Session is authenticated")
    
    # Get the current access token
    token = session.access_token
    print(f"Access token: {token[:20]}..." if token else "No token")
    
    # Clear session state (resets authentication)
    session.clearSession()
    print(f"Authenticated after clear: {session.authenticated}")

# Example 2: URL Construction
print("\n" + "=" * 60)
print("Example 2: URL Construction")
print("=" * 60)

with nr.Session(auth_data) as session:
    # Construct full URL for an endpoint
    url = session.getUrl('users/profile')
    print(f"Full URL: {url}")

# Example 3: Custom Configuration
print("\n" + "=" * 60)
print("Example 3: Custom Configuration")
print("=" * 60)

# Custom timeout and retry settings
session = nr.Session(
    auth_data,
    timeout=30,      # 30 second timeout
    max_retries=10   # Retry up to 10 times
)

try:
    response = session.requestGet('users/profile')
    print(f"Request status: {response.status_code}")
finally:
    session.close()

# Example 4: Connection Pooling
print("\n" + "=" * 60)
print("Example 4: Connection Pooling")
print("=" * 60)

# Larger connection pool for concurrent requests
session = nr.Session(
    auth_data,
    pool_connections=50,
    pool_maxsize=50
)

try:
    # Make multiple requests (connection is reused)
    responses = []
    for i in range(3):
        response = session.requestGet(f'endpoint/{i}')
        responses.append(response.status_code)
    print(f"Response codes: {responses}")
finally:
    session.close()

# Example 5: Session Reuse
print("\n" + "=" * 60)
print("Example 5: Session Reuse")
print("=" * 60)

# Reuse session for multiple requests
with nr.Session(auth_data) as session:
    # Request 1
    profile = session.requestGet('users/profile')
    print(f"Profile request: {profile.status_code}")
    
    # Request 2
    citations = session.requestGet('citations/list')
    print(f"Citations request: {citations.status_code}")
    
    # Request 3
    status = session.requestGet('status')
    print(f"Status request: {status.status_code}")
    
    # Connection is reused automatically for better performance
    print("All requests completed with connection reuse")

print("\n" + "=" * 60)
print("All examples completed!")
print("=" * 60)
