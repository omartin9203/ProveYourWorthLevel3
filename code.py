import requests
from PIL import Image, ImageDraw
from pathlib import Path

start_uri = "http://www.proveyourworth.net/level3/start"
activate_uri = "http://www.proveyourworth.net/level3/activate?statefulhash"
payload_uri = "http://www.proveyourworth.net/level3/payload"

file_path = Path("./")


class ProveYourWork:
    def __init__(self):
        self.session = requests.Session()
        self.session_id = ''
        self.token = ''
        self.post_back_to_uri = 'http://www.proveyourworth.net/level3/reaper'

    def start(self):
        response = self.session.get(start_uri)
        self.session_id = str(response.headers['Set-Cookie']).split(';')[0].split('PHPSESSID=')[1]
        print("-" * 8 + f" session_id: {self.session_id}" + "-" * 8)
        self.token = [x for x in response.content.decode().splitlines() if x.find('statefulhash') > -1][0].split('value=')[1][1:33]
        print("-" * 8 + f" token: {self.token}" + "-" * 8)

    def activate(self):
        self.session.get(activate_uri + f'={self.token}')

    def download(self, name, email, description):
        response = self.session.get(payload_uri, stream=True)
        self.post_back_to_uri = f"{response.headers['X-Post-Back-To']}"
        image = response.raw
        image = Image.open(image)
        draw = ImageDraw.Draw(image)
        draw.text((20, 70),
                  f"{name}, \n Token:{self.token} \n {email} \n {description}",
                  fill=(1024, 1024, 0))
        image.save("image.jpg", "JPEG")

    def upload(self, code_filename: str, resume_filename: str, image_filename: str, email, fullname):
        files = {
            "code": open(file_path / code_filename, "rb"),
            "resume": open(file_path / resume_filename, "rb"),
            "image": open(file_path / image_filename, "rb")
        }
        data = {
            "email": email,
            "name": fullname,
        }
        response = self.session.post(self.post_back_to_uri, data=data, files=files)
        print(response, 'response of upload')

    def run(self):
        print(print("-" * 8 + " START " + "-" * 8))
        self.start()
        print(print("-" * 8 + " ACTIVATE " + "-" * 8))
        self.activate()
        print(print("-" * 8 + " DOWNLOAD " + "-" * 8))
        self.download('Oscar Martin', 'o.martin9203@gmail.com', 'Software Developer')
        print(print("-" * 8 + " UPLOAD " + "-" * 8))
        self.upload('code.py', 'cv.pdf', 'image.jpg', 'o.martin9203@gmail.com', 'Oscar Martin Gonzalez-Chavez')


if __name__ == '__main__':
    test = ProveYourWork()
    test.run()
    print(print("-" * 8 + " FINISHED OK " + "-" * 8))
