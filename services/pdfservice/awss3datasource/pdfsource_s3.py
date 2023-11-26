import boto3
from langchain.document_loaders import S3FileLoader
from langchain.document_loaders import UnstructuredFileLoader
import os
from services.pdfservice.awss3datasource.localfileloader import LocalFileLoader


class PdfSourceAwsS3:
    def __init__(self, bucket: str, prefix: str = ""):
        print("loading PdfSourceAwsS3.....")
        self.bucket = bucket
        self.prefix = prefix
        # self.session = session

    def load_s3_bucket(self):
        s3 = boto3.resource('s3')
        bucket = s3.Bucket(self.bucket)
        print(bucket)
        docs = []
        for obj in bucket.objects.filter(Prefix=self.prefix):
            print(obj)
            if obj.key.endswith('pdf'):
                print(obj.key)
                loader = S3FileLoader(self.bucket,   obj.key)
                # loader.load()
                docs.extend(loader.load())
        return docs

    def load_local_folder(self):
        docs = []
        for root, dirs, files in os.walk(self.bucket):
            print("inside for....root")
            for file in files:
                file_path = os.path.join(root, file)
                folder_name = os.path.dirname(file_path)
                if file_path.endswith('.pdf') and folder_name.find(self.prefix):
                    loader = UnstructuredFileLoader(file_path)
                    docs.extend(loader.load())
        return docs
