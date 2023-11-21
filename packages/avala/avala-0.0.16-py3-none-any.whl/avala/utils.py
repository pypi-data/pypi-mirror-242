import json
import os
import configparser

class ConfigValidator:
    def __init__(self):
        try:
            curdir = os.path.dirname(os.path.abspath(__file__))
            config_file = os.path.join(curdir, 'config.json')
            with open(config_file, "r") as json_file:
                self.config = json.load(json_file)
        except FileNotFoundError:
            self.config = None
        except json.JSONDecodeError:
            self.config = None


    def import_google_creds(self):
        try:
            curdir = os.path.dirname(os.path.abspath(__file__))
            creds_file = os.path.join(curdir, 'google_auth_creds.json')
            with open(creds_file, "r") as json_file:
                creds = json.load(json_file)
            self.config['ProviderConfig']['provider_config']['gc_storage_auth_json_content'] = json.dumps(creds)

            trim_fields = ['s3_bucket_name', 's3_bucket_region', 's3_bucket_prefix', 's3_access_key_id', 's3_secret_access_key']
            for field in trim_fields:
                if field in self.config['ProviderConfig']['provider_config']:
                    del self.config['ProviderConfig']['provider_config'][field]

        except FileNotFoundError:
            self.config = None
        except json.JSONDecodeError:
            self.config = None

        return self.config

    def validate_api_section(self):
        if 'API' not in self.config:
            return False
        required_fields = ['api_key', 'api_url']
        for field in required_fields:
            if field not in self.config['API']:
                return False
        return True

    def validate_provider_config(self):
        if 'ProviderConfig' not in self.config:
            return False
        if 'provider_config' not in self.config['ProviderConfig']:
            return False

        pc = self.get_provider_config()

        if pc['provider'] == 'aws_s3':
            required_fields = ['s3_bucket_name', 's3_bucket_region', 's3_bucket_prefix', 's3_access_key_id', 's3_secret_access_key']
        elif pc['provider'] == 'gc_storage':
            required_fields = ['gc_storage_bucket_name', 'gc_storage_prefix']
        else:
            return False

        for field in required_fields:
            if field not in pc:
                return False

        return True

    def validate_config(self):
        if self.config is None:
            return False
        if not self.validate_api_section():
            return False
        if not self.validate_provider_config():
            return False
        return True

    def get_config(self):
        return self.config

    def get_provider_config(self):
        return self.config['ProviderConfig']['provider_config']

    def requires_importing_creds(self):
        pc = self.get_provider_config()
        if pc['provider'] == 'aws_s3':
            return False
        return True

