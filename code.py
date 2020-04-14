import requests
from PIL import Image, ImageDraw
from pathlib import Path

start_uri = "http://www.proveyourworth.net/level3/start"
activate_uri = "http://www.proveyourworth.net/level3/activate?statefulhash="
payload_uri = "http://www.proveyourworth.net/level3/payload"

file_path = Path("./")


class ProveYourWork:
    def __init__(self):
        self.session = requests.Session()
        self.session_id = ''
        self.post_back_to_uri = 'http://www.proveyourworth.net/level3/reaper'

    def start(self):
        response = self.session.get(start_uri)
        self.session_id = self.session.cookies.get("PHPSESSID") # str(response.headers['Set-Cookie']).split(';')[0].split('PHPSESSID=')[1]
        print("-" * 8 + f" session_id: {self.session_id}" + "-" * 8)

    def get_token(self):
        response = self.session.get(start_uri)
        token = [x for x in response.content.decode().splitlines() if x.find('statefulhash') > -1][0].split('value=')[1][1:33]
        print("-" * 8 + f" token: {token}" + "-" * 8)
        return token

    def activate(self):
        token = self.get_token()
        self.session.get(activate_uri + token)

    def download(self, name, email, description, image_filename="image.jpg"):
        response = self.session.get(payload_uri, stream=True)
        image = Image.open(response.raw)
        draw = ImageDraw.Draw(image)
        draw.text((20, 70),
                  f" Name: {name} \n Token: {self.get_token()}",
                  fill=(1024, 1024, 0))
        image.save(image_filename, "JPEG")

    def upload(self, code_filename: str, resume_filename: str, image_filename: str, email, fullname):
        response = self.session.get(payload_uri)
        post_back_to_uri = f"{response.headers['X-Post-Back-To']}"
        print(post_back_to_uri)
        files = {
            "code": open(file_path / code_filename, "rb"),
            "resume": open(file_path / resume_filename, "rb"),
            "image": open(file_path / image_filename, "rb")
        }
        data = {
            "email": email,
            "name": fullname,
            "aboutme": "I'm an software developer",
            "code":"https://github.com/DennisMostajo/ProveYourWorthDennisLevel3/blob/master/ProveYourWorthDennis/ProveYourWorthDennis/code.py",
            "resume":"https://www.linkedin.com/in/dennis-mostajo-maldonado-536b9a68",
            "image":"https://github.com/DennisMostajo/ProveYourWorthDennisLevel3/blob/master/ProveYourWorthDennis/ProveYourWorthDennis/image.jpg"
        }
        response = self.session.post(post_back_to_uri, data=data, files=files)
        print(response.status_code)
        print(response.text)

    def run(self):
        print("-" * 8 + " STARTING " + "-" * 8)
        self.start()
        print("-" * 8 + " STARTED " + "-" * 8)
        print("-" * 8 + " ACTIVATING " + "-" * 8)
        self.activate()
        print("-" * 8 + " ACTIVATED " + "-" * 8)
        print("-" * 8 + " DOWNLOADING " + "-" * 8)
        self.download('Oscar Martin', 'o.martin9203@gmail.com', 'Software Developer')
        print("-" * 8 + " DOWNLOADED " + "-" * 8)
        print("-" * 8 + " UPLOADING " + "-" * 8)
        self.upload('code.py', 'resume.pdf', 'image.jpg', 'o.martin9203@gmail.com', 'Oscar Martin Gonzalez-Chavez')
        print("-" * 8 + " UPLOADED " + "-" * 8)


if __name__ == '__main__':
    try:
        test = ProveYourWork()
        test.run()
        print("-" * 8 + " FINISHED OK " + "-" * 8)
    except Exception as e:
        print("-" * 8 + " FINISHED FAILED " + "-" * 8)
        print(f"ERROR: {e}")
