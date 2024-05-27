# Google Scholar Datasets

This directory contains all the datasets scraped from Google Scholar. Currently, it contains datasets of universities within the University of California (UC) system. 

They can also be further cleaned by:

1. Removing Default Avatars

Filter out entries where the image URL includes the term "avatar". This helps in eliminating generic or placeholder images.

Example:
```bash
df = df[~df['Image'].str.contains("avatar", case=False)]
```

2. Making image bigger

Replace the term "view_photo" in the image URLs with "medium_photo" to retrieve images of better quality.

Example:
```bash
df['Image'] = df['Image'].str.replace("view_photo", "medium_photo", regex=False)
```
