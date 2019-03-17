# Impactathon 2019
This project uses a map image and the corresponding satellite image at night and tries to find all the roads on the map that do not have street lights.

# To run
- Works with Python 3.6
```bash
 $ pip3.6 install virtualenv  # if not already installed
 $ virtualenv -p /usr/local/bin/python3.6 cv-env
 $ source cv-env/bin/activate
 $ pip3.6 install -r setup/requirements.txt
 $ python src/test.py --map_image <path> --night_image <path> --output <path> --background <path>
```
- Example:
```bash
 $ python src/test.py --map_image data/map_no_label.png --night_image data/night_pic.png --output data/output.png --background data/map_no_label.png
```
