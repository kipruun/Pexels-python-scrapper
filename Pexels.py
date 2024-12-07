import requests

class PexelsElement():
    def __init__(self, json_element) -> None:
        self.id = json_element.get("id")
        self.type = json_element.get("type")
        attribute = json_element.get("attributes")
        self.slug = attribute.get("slug")
        self.width = attribute.get("width")
        self.aspect_ratio = attribute.get("aspect_ratio")
        self.height = attribute.get("height")
        self.created_at = attribute.get("created_at")
        self.updated_at = attribute.get("updated_at")
        self.publish_at = attribute.get("publish_at")
        self.title = attribute.get("title")
        self.license = attribute.get("license")
        user = attribute.get("user")
        self.user = {
            "id": user.get("id"),
            "username": user.get("username"),
            "avatar": user.get("avatar"),
                     }
        self.tags = attribute.get("tags")

class PexelPhoto(PexelsElement):
    def __init__(self, json_element) -> None:
        super().__init__(json_element)
        self.images = json_element.get("attributes").get("image")
        

class PexelVideo(PexelsElement):
    def __init__(self, json_element) -> None:
        super().__init__(json_element)
        self.videos = json_element.get("attributes").get("video")

class Pexels():
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.36 Edge/16.16299',
    }
    
    
    def __init__(self, secret_key) -> None:
        self.headers["secret-key"] = secret_key
            
    
    def search(self, query:str, page=1, type="photos", size="all", orientation="all", raw=False) -> dict:
        """Allow search photos, videos and get results

        Args:
            query (str): Query
            page (int, optional): Page number. Defaults to 1.
            type (str, optional): Type of content (photos, videos). Defaults to "photos".
            size (str, optional): Size of image (small, medium, large). Defaults to "all".
            orientation (str, optional): Orientation of the images (portrait, landscape) Defaults to "all".
            raw (bool, optional): If True return raw response. Defaults to False.

        Returns:
            dict: response formated / raw (if raw==True)
        """
        url = "https://www.pexels.com/fr-fr/api/v3/search/"+type+"?query="+query+"&page="+str(page)+"&per_page=24&orientation="+orientation+"&size="+size+"&color=all&sort=popular&seo_tags=true"  
        request = requests.get(url, headers=self.headers)
        request_json = request.json()
        if raw:
            return request_json
        rsps = {
            "search_info": {
                "page": request_json.get("pagination").get("current_page"),
                "total_page": request_json.get("pagination").get("total_pages"),
                "total_result": request_json.get("pagination").get("total_results"),
                "query": request_json.get("meta").get("raw_query"),
                "total_result": request_json.get("meta").get("total_results")
                },
        }
        results = []
        
        for result in request_json.get("data"):
            if type=="photos":
                results.append(PexelPhoto(result))
            else:
                results.append(PexelVideo(result))
        rsps["data"] = results
        return rsps
    
    
    def get_photo_url(self, element):
        if type(element) == PexelPhoto:
            element = element.id
        url_image = "https://images.pexels.com/photos/"+element+"/pexels-photo-"+element+".jpeg"
        return element, url_image
        
        
    def download_photo(self, element, path=""):
        """A function which allow to download photo

        Args:
            element (dict/str): Must be the photo's id or a photo element
            path (str, optional): If path empty the file is going to be saved at local folder. Defaults to "".
        """
        element, url = self.get_photo_url(element)
        if path=="":
            path = "./"+element+".jpeg"
        elif path[-5:]!=".jpeg":
            path = path+".jpeg"
        response = requests.get(url)
        file = open(path, "wb")
        file.write(response.content)
        file.close()
        
        
    def download_video(self, element, path="", quality="original"):
        """A function which allow to download video

        Args:
            element (PexelVideo): Must be a PexelVideo element
            path (str, optional): If path empty the file is going to be saved at local folder. Defaults to "".
            quality (str, optional): The quality of the video which going to be download (sd, hd, original). Defaults to "original"
        """
        if quality=="original":
            url = element.videos.get("src")
            
        elif quality=="sd":
            videos = element.videos.get("video_files")
            for video in videos:
                if video.get("quality") == "sd":
                    url = video.get("link")
                    
        elif quality=="hd":
            videos = element.videos.get("video_files")
            for video in videos:
                if video.get("quality") == "hd":
                    url = video.get("link")
        print(url.split("/"))
        if path=="":
            path = "./"+url.split("/")[-1]
        elif path[-5:]!=".mp4":
            path = path+".mp4"
        response = requests.get(url)
        file = open(path, "wb")
        file.write(response.content)
        file.close()
