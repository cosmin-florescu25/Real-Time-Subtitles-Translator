## Subtitles Translator

&nbsp;&nbsp;&nbsp;&nbsp;The idea came to me when I started to learn french this summer. In school I had enough hours to make me a B2 (500h), but the reality was different (I was A0). To learn a new language
you need first to consume it. So what's the best way to consume content ? Of course while watching a movie. In plus, each unknown word by the user, will be explaied, if it's hovered.          
&nbsp;&nbsp;&nbsp;&nbsp;Because many people don't know english in our country especially middle-aged people who have learnt russian at school. I've decided with my team to make a website/app 
to make learning english fun. So, therefore momentarly will only translate english to romanian for this project. (It can be easily swithed de language to translete to.). For the subttitles translater to work in `fullscreen`, press fn + f12. Don't forget that you can get the definiton of an unknown word by hovering it.
&nbsp;&nbsp;&nbsp;&nbsp;So, i've implemented a `chrome` extension for all movie sites. In the tutorial at the end I use brave.       
I suggest trying it on netflix or https://xprime.stream/ (here you can set the subtitles size and position to aligned in the specific area from the screenshot).                    
!Disclaimer: in setup.sh you can choose between a light variant (it needs tesseract installed on the computer to work) and a more accurate one made with easy.ocr.        
If run.sh and interface.py don't work try with app.py.        
Remember to have the `server on` for the extension to work. 
!
### Getting the subtittle text
To implement this, first things first we need the text.

&nbsp;&nbsp;&nbsp;&nbsp;I've considered some paths do to this.

I) Get the movie name and download the subtitles text.      
    - Pros: Efficient       
    - Cons: Needs to sync with the time from the player, netflix doesn't let you to have acces to its player

II) Get directly the subtitles from the player      
    - Pros: - easy to do for only one site that let's you to acces its player      
    - Cons: - netflix doesn't let you to have acces to its player      
    &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;- it would be specific for each site        

III) Screenshooting a select portion        
    - Pros: - can work with any site        
    - Cons - harder to implement        
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;- consuming a lot of resources

&nbsp;&nbsp;&nbsp;&nbsp;I've chosen the third option, I want to watch a movie even if it's not on Netflix, and I don't want to spend 20$ just a subscription. So, yeah, piracy time.
### 2. Implementation (Python backend)
So, the follwing functions from background made the possible the third choice.

`
doText.py
`
- make a screenshot to a specific area common for subtitles
- it uses the main monitor in case if the user has multiple monitors

`
analyzeImage.py
`
- analyze the screeshot
- It has 2 variants:
#### Variant 1:
- it uses easyOCR, but it will consume larger resources, 8gb of free storage and it takes a longer time to install, but it will be very `accurate`
#### Variant 2:
- it uses pytesseract, it's far lighter, but it is not as good (the text extracted won't be as good)

`
translateText.py
`
- the gem of this part of the project
- I've considered Translator from translate (it has a daily number of uses their api)
- In the end I've remained with deep_translator from GoogleTranslate, which is free and good enough.

Problems:
- First i used pytessract but it wasn't the best OCR, so i've switched to easyOCR. But it consumes a lot of resources, so i made the choice for the user to choose what variant to use.
- Screenshots? Because all is processed locally, the user's screenshot won't be shared with anyone

- Now, that we have the screenshots, I've wanted to implement hovering over words to give their meaning. At first glance, I've considered multiple hitboxex
(one hitbox per word), which was very hard. Then to make the logic easier, I've considered one big hitbox per line, and each word has its length so occupies a certain procentage of
the line length's. So I've divided the line into multiple mini hitboxes this way.

&nbsp;&nbsp;&nbsp;&nbsp;To not forget the words hovered, the user at the end of the session will get the words collected in the database with their meaning.

### 3. Implementation (javascript frontend)
- it get the information with the help of `app.py`, which start the server and offer information
- it stops everything when the extension is set to OFF
- updateSubtitle() -> get's the information via background.js, after that it shows the text in subtitleDiv
- fetchDefinition() -> get's the definiton of the word via background.js

Tutorial:       
&nbsp;&nbsp;&nbsp;&nbsp;If it doens't work try to reload the page, check if the server or extesion is on and disable the adblocker. The starting of the server can be slow.
- I) Add the extension
    - activate developer mode in the settings of extension, it is found in `Data/Extension`              
![Developer mode & load unpacked](Tutorialmages/1.png)     
    - click on load unpacked and navigate to the extension's path and add it
![Path](Tutorialmages/path.png)     
    - pin it to easily deactivate/activate later         
- II) Run setup.sh to choose the variant, then run 'run.sh'
    - click start server, it will allow to processed the data in python 
    (backend)           
![Demo from hotel Transylavania](Tutorialmages/3.png)       
- III) Stop the server
    - when done with watching movies while learning a new language ;)
    - click stop server, it imediatly stops the local server and it will give a list of the words you hovered

![Hovered unknown words](Tutorialmages/4.png)       

&nbsp;&nbsp;&nbsp;&nbsp;In the end, it was a project that I've enjoyed working on it. I've gave up this
idea in the summer, thinking it was too hard.

### Future plans for this project:
- to translate to all the languages
- to train a ML for the english version
- to add a better/fancy (eye-candy) interface
