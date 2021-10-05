""" Validate incoming http request, then aggregate data from JSON in S3. """
import json
import boto3


def main(event, _):
    """ Event Handler. """
    # Grab database from JSON.
    s3_client = boto3.client('s3')
    s3_object = s3_client.get_object(
        Bucket="rii-senior-dev-interview-db", Key="rii-dev-interview-db")
    db_json = json.loads(s3_object["Body"].read())

    # Perform error checking.
    resource = event["resource"]
    if event["httpMethod"] != "GET":
        return {
            "statusCode": 400,
            "body": json.dumps("That method not supported on this resource!")
        }
    if resource not in ["/books", "/authors"]:
        return {
            "statusCode": 400,
            "body": json.dumps("That resource does not exist!")
        }

    # Return data when input is valid.
    data = [obj for obj in db_json if obj["type"] == resource[1:-1]]
    return {
        "statusCode": 200,
        "body": json.dumps(data)
    }
