
import requests
import json
import urllib

s = requests.Session()

zm_login_csrf = None
zm_auth_token = None
jsessionid = None
x_zimbra_csrf_token = None
session_id = None


# visit site
def visit_site():
    base_request = s.get('https://stdmail.knust.edu.gh/', verify=True)
    headers = base_request.headers
    cookies = headers['Set-Cookie'].split(';')
    extract_login_csrf_token(cookies)


def extract_login_csrf_token(cookies):
    global zm_login_csrf
    zm_login_csrf = cookies[1].split('=')[-1]


# login
def login():
    visit_site()
    payload = {
        'loginOp': 'login',
        'login_csrf': zm_login_csrf,
        'username': '${YOUR_STUDENT_USERNAME}',
        'password': '${YOUR_STUDENT_MAIL_PASSWORD}',
        # 'zrememberme':'1',
        'client': 'preferred'
    }

    auth_headers = {
        "Host": "stdmail.knust.edu.gh",
        "Cookie": "ZM_TEST=true;ZM_LOGIN_CSRF=" + zm_login_csrf,
        "Content-Length": str(len(payload)),
        "Cache-Control": "max-age=0",
        "Sec-Ch-Ua": '";Not A Brand";v="99", "Chromium";v="94"',
        "Sec-Ch-Ua-Mobile": "?0",
        "Sec-Ch-Ua-Platform": "Linux",
        "Upgrade-Insecure-Requests": "1",
        "Origin": "https://stdmail.knust.edu.gh",
        "Content-Type": "application/x-www-form-urlencoded",
        "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9",
        "Sec-Fetch-Site": "same-origin",
        "Sec-Fetch-Mode": "navigate",
        "Sec-Fetch-User": "?1",
        "Sec-Fetch-Dest": "document",
        "Referer": "https://stdmail.knust.edu.gh/",
        "Accept-Encoding": "gzip, deflate",
        "Accept-Language": "en-US,en;q=0.9",
        "Connection": "close"
    }
    s.headers.update(auth_headers)

    encoded_payload = urllib.parse.urlencode(payload)

    try:

        login_response = s.post('https://stdmail.knust.edu.gh/', data=encoded_payload)
    except Exception:
        raise Exception("Unable to authenticate, please check credentials")

    s.headers.update(login_response.request.headers)
    extract_zm_auth_token_and_jsessionid(login_response)
    extract_x_zimbra_csrf_token_and_session_id(login_response)


# Extract ZM_AUTH_TOKEN and JSESSIONID from Login cookies sessions
def extract_zm_auth_token_and_jsessionid(login_response):
    global zm_auth_token
    global jsessionid

    try:
        zm_auth_token = login_response.request.headers['Cookie'].split()[-1].split('=')[1]
        jsessionid = login_response.headers['Set-Cookie'].split(',')[-1].split(';')[0].split('=')[1]
        s.headers.update({'Cookie': s.headers['Cookie'] + ";JSESSIONID=" + jsessionid})
    except Exception:
        raise Exception("Error extracting auth token and jsessionid")


# Extract X-Zimbra-Csrf-Token and Session ID from SCRIPT
def extract_x_zimbra_csrf_token_and_session_id(login_response):
    from bs4 import BeautifulSoup
    try:
        soup = BeautifulSoup(login_response.text, 'html.parser')
        all_scripts = soup.find_all('script')

        token_scripts = all_scripts[0]

        global x_zimbra_csrf_token
        global session_id

        x_zimbra_csrf_token = list(token_scripts)[0].split('=')[-2].split(';')[0].split('"')[1]
        s.headers.update({"X-Zimbra-Csrf-Token": x_zimbra_csrf_token})

        json_string_start = login_response.text[
                            login_response.text.find("batchInfoResponse = "):login_response.text.find(
                                ',"refresh":{"version"')]
        json_string_end = json_string_start[json_string_start.find('{"id":'):]
        session_id = json.loads(json_string_end)['id']
    except Exception:
        raise Exception("Extract_x_zimbra_csrf token and session_id")


# search
def search_student(student_name):
    import json

    login()

    body = json.dumps({"Header": {"context": {"_jsns": "urn:zimbra",
                                              "userAgent": {"name": "ZimbraWebClient - GC95 (Win)",
                                                            "version": "8.6.0_GA_1242"},
                                              "session": {"_content": session_id, "id": session_id},
                                              "account": {"_content": "barhinacquaah@st.knust.edu.gh",
                                                          "by": "name"},
                                              "csrfToken": x_zimbra_csrf_token}}, "Body": {
        "SearchGalRequest": {"_jsns": "urn:zimbraAccount", "needIsOwner": "1", "needIsMember": "directOnly",
                             "type": "account", "name": student_name, "offset": 0, "limit": 100,
                             "locale": {"_content": "en_US"}, "sortBy": "nameAsc", "needExp": 1}}})

    search_headers = {
        "Host": "stdmail.knust.edu.gh",
        "Cookie": s.headers['Cookie'] + "; JSESSIONID=" + jsessionid,
        "Content-Length": str(len(body)),
        "Sec-Ch-Ua": '"Chromium";v="95", ";Not A Brand";v="99"',
        "X-Zimbra-Csrf-Token": x_zimbra_csrf_token,
        "Sec-Ch-Ua-Mobile": "?0",
        "Content-Type": "application/soap+xml; charset=UTF-8",
        "Sec-Ch-Ua-Platform": "Linux",
        "Accept": "*/*",
        "Origin": "https://stdmail.knust.edu.gh",
        "Sec-Fetch-Site": "same-origin",
        "Sec-Fetch-Mode": "cors",
        "Sec-Fetch-Dest": "empty",
        "Referer": "https://stdmail.knust.edu.gh/",
        "Accept-Encoding": "gzip, deflate",
        "Accept-Language": "en-US,en;q=0.9",
        "Connection": "close"
    }

    s.headers.clear()
    s.headers.update(search_headers)
    try:
        search_request = s.post('https://stdmail.knust.edu.gh/service/soap/SearchGalRequest', data=body, verify=True)
        print(search_request.text)
        json_response = json.loads(search_request.text)
        if search_request.status_code == 200:
            if "cn" in json_response["Body"]["SearchGalResponse"]:
                return json_response["Body"]["SearchGalResponse"]["cn"]
            else:
                raise Exception("This student could not be verified")
        else:
            raise Exception("Failed to verify student, please check the please double-check the information provided")
    except Exception as e:
        raise Exception(e)


def search_student_by_reference(student_response, reference):
    for student in student_response:
        if "pager" in student["_attrs"] and student["_attrs"]["pager"] == reference:
            return student
        else:
            raise Exception("A student with this reference number does not exist")

# get image for returned users
# return response

# search_student("Benjamin Arhin-Acquaah")
