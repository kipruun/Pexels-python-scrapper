# A simple scrapper for pexels.com

### Main class: ``` Pexels ```
#### ```search(self, query:str, page=1, type="photos", size="all", orientation="all", raw=False)```
- Query: The query of user
- Page: page number
- Type: ```photos``` or ```videos```
- Size: Size of image (```small```, ```medium```, ```large```)
- Orientation: Orientation of the images (```portrait```, ```landscape```)
- Raw: If ```True``` return raw response.
#### ```get_photo_url(self, element)```
- Element: must be the id of image or ```PexelPhoto()``` element
#### ```download_photo(self, element, path="")```
- Element: must be the id of image or ```PexelPhoto()``` element
- path: keep empty for created file in local folder
### ```download_video(self, element, path="")```
- element: Must be a PexelVideo element
- path: keep empty for created file in local folder
