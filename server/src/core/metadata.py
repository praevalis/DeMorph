from enum import Enum

class ApiTags(str, Enum):
    auth = 'auth'
    user = 'user'

title='DeMorph Server'
version='0.0.1'
description= """
DeMorph is a multimodal deepfake detection solution. It offers deepfake detection services, social media analysis and analysis based on audio cues.

The API exposes endpoints for these services using a modular structure: 
- Auth: All authenticated related services.
- Core: Cross-module services central to the API.
- User: Non-authentication user services.
"""

tags = [
    {
        "name": ApiTags.auth,
        "description": "Handles all the authentication and security logic for API."
    },
    {
        "name": ApiTags.user,
        "description": "Handles user operations such as profile management."
    }
]