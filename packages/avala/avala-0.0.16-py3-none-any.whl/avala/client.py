import json
import os
import re
import requests

class APIClient:
    def __init__(self, valid_config):
        self.config = valid_config
        self.api_url = valid_config['API']['api_url']
        self.api_key = valid_config['API']['api_key']
        self.provider_config = valid_config['ProviderConfig']['provider_config']
        self.organization_config = valid_config['Organization']['organization_config']

        self.headers = {
            'accept': 'application/json',
            'Content-Type': 'application/json',
            'X-AVALA-API-KEY': self.api_key,
        }

    def is_valid_id(self, input_id, json_data):
        """
        Validate if the input_id is a valid "id" within the given JSON data.
        """
        if not isinstance(input_id, int):
            return False

        for item in json_data.get('results', []):
            if item.get('id') == input_id:
                return True

        return False

    def is_dataset_name_valid(self, name):
        """
        Check if the given dataset name is valid
        """
        api_url = self.api_url + '/datasets/validate/name'
        response = requests.post(api_url, headers=self.headers,
                                 data=json.dumps({"name": name}))

        if response.status_code == 200:
            pattern = re.compile(r'^[a-zA-Z0-9_\- ]+$')
            return bool(pattern.match(name))

        return False


    def is_valid_email(self, email):
        pattern = r'^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$'
        match = re.match(pattern, email)
        return match is not None and match.group() == email


    def generate_slug(self, name):
        slug = name.lower().replace(" ", "-").replace("_", "-")
        return slug


    def make_get_request(self, api_url):
        response = requests.get(api_url, headers=self.headers)

        if response.status_code == 200 or response.status_code == 201:
            return response.json()

        return None


    def import_dataset(self, args):
        api_url = self.api_url + '/datasets/'
        dataset_info = {
            'name': args.name,
            'slug': self.generate_slug(args.name),
            'visibility': args.visibility,
            'industry': args.industry,
            'license': args.license,
            'citation': args.citation,
            'creator': args.creator,
            'description': args.description
        }

        dataset_info.update({'provider_config': self.provider_config})
        print(dataset_info)

        response = requests.post(api_url, headers=self.headers,
                                 data=json.dumps(dataset_info))

        if response.status_code == 201:
            print("Successfully created dataset")
        else:
            print(f"Failed to create dataset. Status code: {response.status_code}")
            return None

    def import_annotations(self, args):
        api_url = self.api_url + f'/datasets/upload-existing-annotations'

        json_file = args.annotations_file
        try:
            with open(json_file, 'r') as file:
                annotations_data = json.load(file)
        except FileNotFoundError:
            print(f"Error: '{json_file}' file not found")
            return
        except json.JSONDecodeError:
            print(f"Error: '{json_file}' does not contain valid JSON data")
            return

        # Note: At this time, only 'Coco' format is supported for ingesting
        # annotations.

        annotations = {
            'dataset_uid': args.dataset_uid,
            'annotation_source_format': 'Coco',
            'project_name': args.project_name,
            'annotations_data': annotations_data,
            'keep_annotations': args.keep_annotations,
        }

        response = requests.post(api_url, headers=self.headers,
                                 data=json.dumps(annotations))

        if response.status_code == 202:
            print("Successfully accepted addition of annotations to new project linked to dataset")
        else:
            print(f"Failed to accept addition of annotations for new project linked to dataset. Status code: {response.status_code}")
            return None


    def add_dataset_collaborator(self, args):
        email = args.email
        dataset_uid = args.dataset_uid
        user_uid = self.get_user_uid(email)

        if user_uid is None:
            print("Error adding user with email %s as collaborator to dataset" % args.email)
            return None

        user_info = {'uid': user_uid}
        api_url = self.api_url + f'/datasets/{dataset_uid}/collaborators/'

        response = requests.post(api_url, headers=self.headers,
                      data=json.dumps(user_info))

        if response.status_code != 200:
            print("Requested user could not be added as a collaborator to dataset. Status code: %s" % response.status_code)
            return None

        print("Successfully added user with email %s as collaborator to dataset" % email)

    def add_project_collaborator(self, args):
        email = args.email
        project_uid = args.project_uid
        user_uid = self.get_user_uid(email)

        if user_uid is None:
            print("Error adding user with email %s as collaborator to project" % args.email)
            return None

        user_info = {'uid': user_uid}
        api_url  = self.api_url + f'/projects/manage/{project_uid}/collaborators/'
        response = requests.post(api_url, headers=self.headers,
                                 data=json.dumps(user_info))

        if response.status_code != 200:
            print("Requested user could not be added as a collaborator to project. Status code: %s" % response.status_code)
            return None

        print("Successfully added user with email %s as collaborator to project" % email)


    def download_url(self, destination, filename, url):
        response = requests.get(url)
        if response.status_code == 200:
            with open(f"{destination}/{filename}", 'wb') as file:
                file.write(response.content)
            print(f"Download {url} successful. File saved to {destination}")
        else:
            print(f"Failed to download {url}. Status code: {response.status_code}")


    def dataset_export(self, args):
        if args.dataset_uid is not None:
            dataset_uid = args.dataset_uid
            filename = f"{dataset_uid}.json"
        else:
            dataset_uid = None
            filename = "all.json"

        destination = args.destination

        if destination is None:
            destination = os.getcwd()
        elif not os.path.isdir(os.path.dirname(destination)):
            print("Provided destination is a not a valid directory path")
            return

        api_url = self.api_url + '/exports/'
        data = self.make_get_request(api_url)

        if 'results' in data:
            for item in data['results']:
                if 'download_url' not in item:
                    continue
                if 'datasets' not in item:
                    continue
                if len(item['datasets']) < 1:
                    continue
                if 'status' not in item:
                    continue
                if item['status'] != 'exported':
                    continue
                if 'name' not in item:
                    continue
                if dataset_uid is not None:
                    if item['datasets'][0] != dataset_uid:
                        continue
                filename = f"{item['name']}-{filename}"
                self.download_url(destination, filename, item['download_url'])


    def trigger_export(self, args):
        dataset_uid = args.dataset_uid
        export_format = args.format
        name = args.name

        payload = {
            "name": name,
            "format": export_format,
            "datasets": [dataset_uid],
            "projects": []
        }

        api_url = self.api_url + f'/exports/'

        response = requests.post(api_url, headers=self.headers, data=json.dumps(payload))

        if response.status_code != 201:
            print("Export could not be triggered. Status code: %s" % response.status_code)
            return None

        print("Successfully triggered an export for dataset. Status code: %s" % response.status_code)


    def get_user_uid(self, email):
        api_url = self.api_url + f'/users/@{email}/'
        response = self.make_get_request(api_url)

        if (response is None) or ('uid' not in response):
            print("Email address %s not found. Status code: 404" % email) 
            return None

        return response['uid']

    def get_exports(self):
        api_url = self.api_url + '/exports/'
        data = self.make_get_request(api_url)
        return json.dumps(data, indent=4)

    def get_industries(self):
        api_url = self.api_url + '/project-config/industries/'
        return self.make_get_request(api_url)

    def get_licenses(self):
        api_url = self.api_url + '/licenses/'
        return self.make_get_request(api_url)

    def get_projects(self):
        api_url = self.api_url + '/users/me/projects/'
        return self.make_get_request(api_url)

    def get_datasets(self):
        api_url = self.api_url + '/datasets/'
        return self.make_get_request(api_url)

    def show(self, response):
        if response is None or ('results' not in response) or len(response['results']) == 0:
            print("{}")
            return

        test_element = response['results'][0]
        if 'id' in test_element:
            field = 'id'
        elif 'uid' in test_element:
            field = 'uid'
        else:
            field = None

        state = 0

        if field is None:
            output = response['results']
        else:
            output = sorted(response['results'], key=lambda z: z[field])

        for idx, item in enumerate(output):
            if state == 0:
                print("{")
                state = 1
            if idx == len(response['results'])-1:
                print('  "%s": "%s"' % (item[field], item['name']))
            else:
                print('  "%s": "%s",' % (item[field], item['name']))

        if state == 1:
            print("}")




