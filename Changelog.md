# Changelog
All the work that goes into the project will be documented here.

## 2022-11-28

### Added
* Added a static page article with Freedom Fighters Gallery page text content
 
### Modified
* Changed the default query parameters that get used while searching from header search button
  * Added 'album' and 'staticpage' types
  * Manually, need to modify a compressed file from static/CACHE/js for changing the params as there is a bug with freedom fighters album page JS (refer deployment steps for more information)

## 2022-11-28

### Modified
* For freedom fighters gallery page, change the description [For this, moved description to template file directly so as to allo hyperlinking]
* For freedom fighters gallery detail page, in the carousel section, now we are showing only description

## 2022-11-16

### Added
* Added Embed field to album slides
* Enable only embed button (one of the RichText features) in embed field

### Modified
* For freedom fighters album, 
  * when embed is available for a slide show embed in carousel and use the image in the photos list below carousel
  * in the images below carousel, add a play icon on top of images that belong to slides with embed

## 2022-11-09

### Modified
* Added recaptcha to both contact us form and upload file form
* Follow this [link](https://simpleisbetterthancomplex.com/tutorial/2017/02/21/how-to-add-recaptcha-to-django-site.html) for adding recaptcha to the existing form. The example is for adding simple form. We modified and adopted it to form model.
* This [link](http://www.googleappsscript.org/recent-additions/recaptchawithgoogleappsscript) is for adding recaptcha to google script forms
* Get authorization to the script form and then start modifying the files. To test there are 2 methods one is to do "test deployment" and the other is to create "new deployment". For every new deployment its recomended to give a short description of changes done in the script in the title. use the URL to check the script. Once everything is tested and working fine then copy the URL and update it in the templete file One example is for contribute page and "Upload Content" link. Edit the following file and replace the link with newly generated link in core/templates/core/contribute.html and core/templates/core/contact-us.html.
* The script version used on the site is bumped from 56 to 64.

## 2022-11-08

### Modified
* Removed Hcaptcha as it was not working post deployment
* Added Google reCaptcha-v2
* Used [this](https://simpleisbetterthancomplex.com/tutorial/2017/02/21/how-to-add-recaptcha-to-django-site.html) as a reference

## 2022-11-07

### Added
* Added Hcaptcha to contact us page. Now message which pass all the validations including captcha will be set to contact mail
* Used [this](https://djangowaves.com/tutorial/django-hcaptcha-contact-form/) as a reference

## 2022-08-14

## Added
### Album
* Boolean field to identify Freedom Fighters Gallery album
* Short description field used on Freedom Fighters Gallery Listing Page
* View for Freedom Fighters Gallery albums listing using the new boolean field
* Template for Freedom Fighters Gallery albums listing page

## Modified
### Album
* Album Detail Page to show different content for Freedom Fighters Gallery album
  * Used justifiedGallery library for styling images below the slider
  * First image from album is used as top image (shown above slider)
  * Clicking on image will select that image on the slider
### Core
* Modified grid title template to include additional content on Freedom Fighters Gallery albums listing page
