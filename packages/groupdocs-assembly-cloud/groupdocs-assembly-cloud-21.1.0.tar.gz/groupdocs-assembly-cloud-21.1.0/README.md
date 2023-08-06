This repository contains GroupDocs.Assembly Cloud SDK for Python source code. This SDK allows you to work with GroupDocs.Assembly Cloud REST APIs in your Python applications quickly and easily, with zero initial cost.

See [API Reference](https://apireference.groupdocs.cloud/assembly) for full API specification.

# Key Features
* API to Define Templates, Fetch Data Source, Insert Data in Template & Generate on the fly Reports.

## How to use the SDK?
The complete source code is available in this repository folder. You can either directly use it in your project via source code or get [PyPi](https://pypi.org/project/groupdocs-assembly-cloud) (recommended).

### Prerequisites

To use GroupDocs.Assembly for Cloud Python SDK you need to register an account with [GroupDocs Cloud](https://www.groupdocs.cloud/) and lookup/create App Key and SID at [Cloud Dashboard](https://dashboard.groupdocs.cloud/applications). There is free quota available. For more details, see [GroupDocs Cloud Pricing](https://purchase.groupdocs.cloud/pricing).

### Installation
### pip install

If the python package is hosted on Github, you can install directly from Github

```sh
pip install groupdocs-assembly-cloud
```
(you may need to run `pip` with root permission: `sudo pip install groupdocs-assembly-cloud`)

Then import the package:
```python
import groupdocsassemblycloud
```

### Setuptools

Install via [Setuptools](http://pypi.python.org/pypi/setuptools).

```sh
python setup.py install --user
```
(or `sudo python setup.py install` to install the package for all users)

Then import the package:
```python
import groupdocsassemblycloud
```

### Sample usage
```python
import groupdocsassemblycloud
import groupdocsassemblycloud.models.requests
filename = 'TemplateFile'
with open(os.path.join(DataFile)) as f:
    data = f.read()
remote_name = os.path.join(self.remote_test_folder, filename)
self.uploadFileToStorage(open(os.path.join(self.local_test_folder, filename), 'rb'), remote_name)

template_file_info = groupdocsassemblycloud.models.TemplateFileInfo(remote_name)
assemble_data = groupdocsassemblycloud.models.AssembleOptions(template_file_info, "pdf", data)
request = groupdocsassemblycloud.models.requests.AssembleDocumentRequest(assemble_data)
result = self.assembly_api.assemble_document(request)
self.assertTrue(len(result) > 0, 'Error has occurred while building document')
```
      
[Tests](tests/) contain various examples of using the SDK.
Please put your credentials into [Configuration](Settings/servercreds.json).

# Dependencies
- Python 3.4+
- referenced packages (see [here](setup.py) for more details)

## Contact Us
[Product Page](https://products.groupdocs.cloud/assembly/python) | [Documentation](https://docs.groupdocs.cloud/display/assemblycloud/Home) | [API Reference](https://apireference.groupdocs.cloud/assembly/) | [Code Samples](https://github.com/groupdocs-assembly-cloud/groupdocs-assembly-cloud-python) | [Blog](https://blog.groupdocs.cloud/category/assembly/) | [Free Support](https://forum.groupdocs.cloud/c/assembly) | [Free Trial](https://dashboard.groupdocs.cloud/applications)
