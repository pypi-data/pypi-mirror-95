==============
**S3Streamer**
==============

Overview
--------

A frontend module to upload files to AWS S3 storage. The module supports large files as it chunks them into smaller sizes and recombines them into the original file in the specified S3 bucket.

The module employs multiprocessing, and there is the option of specifying the size of each chunk as well as how many chunks to send in a single run. The defaults are listed in **Optional Arguments** below.

Prerequisites
-------------

- An S3 bucket to receive uploads.
- Several AWS Lambda functions to perform backend tasks including authentication and authorization.

Required (Positional) Arguments
-------------------------------

- Position 1: Authorization code
- Position 2: Filename (full path to the file)
- Position 3: Relative path (to root) in the S3 bucket

Optional (Keyword) Arguments
----------------------------

- parts: Number of multiprocessing parts to send simultaneously (default: 5)
- partsize: Size of each part in MB (default: 100)
- tmp: Location of local temporary directory to store temporary files created by the module (default: '/tmp')
- overwrite: Whether to overwrite existing files on S3 (default: 'NO')
- purge: Whether to purge the specified file instead of uploading it (default: 'NO')
- domain: The domain and path for visitors to access uploaded files (default: 'https://example.com/downloads')
- requrl: The endpoint URL for backend Lambda function (default: 'https://example.com/upload/request')
- reqapikey: The API key for backend Lambda function (default: 'ABCDEF1234567890')

Usage
-----

Installation:

.. code-block:: BASH

   pip3 install s3streamer
   # or
   python3 -m pip install s3streamer

In Python3:

.. code-block:: BASH

   # To upload a new file.
   from s3streamer.s3streamer import multipart
   response = multipart(
       '<token>', 
       '<path/filename>', 
       '<target/relative/path>', 
       domain = 'https://example.com/downloads'
   )

   # To overwrite an existing file.
   from s3streamer.s3streamer import multipart
   response = multipart(
       '<token>', 
       '<filename>', 
       '<target/relative/path>', 
       domain = 'https://example.com/downloads', 
       overwrite = 'YES'
   )

   # To remove a file from S3.
   from s3streamer.s3streamer import multipart
   response = multipart(
       '<token>', 
       '<filename>', 
       '<target/relative/path>', 
       domain = 'https://example.com/downloads', 
       purge = 'YES'
   )

In BASH:

.. code-block:: BASH

   # To upload a new file.
   python3 -c \
   "from s3streamer.s3streamer import multipart; \
   response = multipart(\
   '<token>', \
   '<path/filename>', \
   '<target/relative/path>', \
   domain = 'https://example.com/downloads')"

   # To overwrite an existing file.
   python3 -c \
   "from s3streamer.s3streamer import multipart; \
   response = multipart(\
   '<token>', \
   '<filename>', \
   '<target/relative/path>', \
   domain = 'https://example.com/downloads', \
   overwrite = 'YES')"

   # To remove a file from S3.
   python3 -c \
   "from s3streamer.s3streamer import multipart; \
   response = multipart(\
   '<token>', \
   '<filename>', \
   '<target/relative/path>', \
   domain = 'https://example.com/downloads', \
   purge = 'YES')"

If the upload is successful, the file will be available at http://target.domain/target/relative/path/filename.

Changelog
---------

2021.2.3.2

- Removed CDN cache purge request from the module. That requet can be made separately based on use-cases.

2021.2.3.1

- Updated README to account for recent changes.

2021.2.3.0

- Streamlined all backend HTTP calls to use *requests* instead of *urllib*.
- Updated backend to use API key and Bearer token for authentication and authorization.
- Updated frontend to follow suit.

2020.2.2.3

- Added link to project repository.

2020.2.2.2

- Updated HTTP method for geturl action.

2020.2.2.1

- Removed tqdm as dependency. The module works more silently now.

2020.2.2.0

- Streamlined HTTP response throughout all layers of the streaming process. The frontend now echoes the status from the backend instead of producing its own, where possible.
- Code cleanup.

2020.2.1.7

- Initial release of the finalized working module.

Special Note
------------

This module was created to accommodate a very specific need for a very specific organization, hence the multiple component prerequisites. If you're interested to use the full solution, the CloudFormation templates to create the corresponding AWS resources are available in the project repository (customizations may be necessary).

*Current version: 2021.2.3.2*
