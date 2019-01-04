from __future__ import print_function
from googleapiclient.discovery import build
from httplib2 import Http
from oauth2client import file, client, tools
from apiclient import errors

# If modifying these scopes, delete the file token.json.
SCOPES = 'https://www.googleapis.com/auth/gmail.readonly'


def list_labels(service, user_id):
  """Get a list all labels in the user's mailbox.

  Args:
    service: Authorized Gmail API service instance.
    user_id: User's email address. The special value "me"
    can be used to indicate the authenticated user.

  Returns:
    A list all Labels in the user's mailbox.
  """
  try:
    response = service.users().labels().list(userId=user_id).execute()
    labels = response['labels']
    for label in labels:
      print('Label id: %s - Label name: %s' % (label['id'], label['name']))
    return labels
  except errors.HttpError as error:
    print('An error occurred: %s' % error)


def main():
    """Shows basic usage of the Gmail API.
    Lists the user's Gmail labels.
    """
    # The file token.json stores the user's access and refresh tokens, and is
    # created automatically when the authorization flow completes for the first
    # time.
    store = file.Storage('token.json')
    creds = store.get()
    if not creds or creds.invalid:
        flow = client.flow_from_clientsecrets('credentials.json', SCOPES)
        creds = tools.run_flow(flow, store)
    service = build('gmail', 'v1', http=creds.authorize(Http()))

    # list_labels(service, 'me')

    # Call the Gmail API
    response = service.users().messages().list(userId='me', maxResults=5, labelIds=['INBOX']).execute()

    messages = []
    if 'messages' in response:
        for message in response['messages']:
            messageResponse = service.users().messages().get(userId='me', id=message['id']).execute()
            print(messageResponse)

    # while 'nextPageToken' in response:
    #     page_token = response['nextPageToken']
    #     response = service.users().messages().list(userId='me', pageToken=page_token).execute()
    #     messages.extend(response['messages'])


if __name__ == '__main__':
    main()
