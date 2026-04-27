import requests


class APIClient:
    def __init__(self, base_url):
        self.base_url = base_url

    def _post(self, endpoint, data=None, files=None):
        try:
            if files:
                response = requests.post(f"{self.base_url}{endpoint}", files=files)
            else:
                response = requests.post(f"{self.base_url}{endpoint}", json=data)

            return response.json()
        except Exception as e:
            return {"error": str(e)}

    # Website
    def website_full_data(self, data):
        return self._post("/report/website/full-data", data)

    def website_section(self, section, data):
        return self._post(f"/report/website/{section}", data)

    # Instagram
    def instagram_full_data(self, data):
        return self._post("/report/social/instagram/full-data", data)

    def instagram_section(self, section, data):
        return self._post(f"/report/social/instagram/{section}", data)

    # Visual
    def visual_brand_match(self, website_file, insta_file):
        files = {
            "website_screenshot": website_file,
            "instagram_screenshot": insta_file
        }
        return self._post("/report/visual/brand-match", files=files)