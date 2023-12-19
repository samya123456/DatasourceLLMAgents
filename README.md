# DatasourceLLMAgents

DatasourceLLMAgents is an API designed to interact with various datasources, including databases and PDF files, enabling seamless querying and retrieval of information.

## Installation

1. Install the required dependencies:

    ```bash
    pip install -r requirements.txt
    ```

2. Start the server using Uvicorn:

    ```bash
    uvicorn app:app --host 0.0.0.0 --port 8000 --reload
    ```

## Setting Up DB Agent

To use the Database Agent:

1. **Install MySQL**.
2. Run the `sql/dbsetup.sql` script within MySQL.
3. Set the `DB_URL` environment variable in the `.env` file following the format:

    ```
    DB_URL="mysql+pymysql://root:admin123@localhost:3306/company"
    ```

### Testing DB Agent

Send a POST request to `http://localhost:8000/prompt/db` with the following JSON payload:

```json
{
    "question": "Last name of Nancy"
} 

```


## PDF Agent Setup

The PDF Agent allows interaction with PDF files stored in an AWS S3 bucket. Follow these steps to set up and test the PDF Agent:

### Stored PDF Files in AWS S3

1. **AWS S3 Storage**: All PDF files are stored in the AWS S3 bucket named `bizzchatpdfsourcebucket1` and folder `barabellclub`

### Environment Variables

Set the following environment variables for local testing:

- `S3_BUCKET`: Set this variable to `bizzchatpdfsourcebucket1`.
- `S3_PREFIX`: Set the prefix or directory path within the S3 bucket to `barabellclub`.

For local testing and easy access to sample PDFs:

1. **Local Test Path**: A local path `bizzchatpdfsourcebucket1/barabellclub` has been created to simulate the S3 bucket structure for testing purposes.
2. **Sample PDFs**: Sample PDFs have been placed in the local path `bizzchatpdfsourcebucket1/barabellclub` for the agent to read.

### Testing the PDF Agent

To test the PDF Agent locally:

1. Ensure the environment variables (`S3_BUCKET` and `S3_PREFIX`) are correctly set in the `.env` file.
2. Send a POST request to `http://localhost:8000/prompt/pdf` with a JSON payload containing your query or request to extract information from the PDF file.

Example JSON payload:

```json
{
    "question":"contact number of the member"
}
```

Example .env file:

OPENAI_API_KEY=
DB_URL=
S3_BUCKET=bizzchatpdfsourcebucket1
S3_PREFIX=barabellclub