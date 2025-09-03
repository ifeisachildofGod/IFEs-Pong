# IFEs Pong
This is pong but a little better, this is an archive of all my previous iterations of this project. Any errors, mistakes or just a pure face-palm moment in the code or the program's functioning is entirely my younger self's fault as the code you are about to see is purely unedited (apart from the pyuac part, which was added recently). Also, the description of each version comes from the description I gave at the time I created it, so don't mind my use of tenses.

## Table of Contents
- [Installation](#installation)
- [Usage](#usage)
- [License](#license)
- [V1](#ifes-pong-v1)
- [V2](#ifes-pong-v2)
- [V3](#ifes-pong-v3)
- [V4](#ifes-pong-v4)
- [V5](#ifes-pong-v5)
- [V6](#ifes-pong-v6)

## Installation
Here are the steps needed to install and run the code properly
- Download the zip file and enter the folder you would like to try first
- If Python is not installed on your system install it from their official website: [https://www.python.org](https://www.python.org)
- As you install Python, pip is also installed, so in the cmd run:
    - `pip install pyuac`
    - `pip install pywintypes`
    - `pip install bleak`
    - If you're on Windows then you have to clone the pybluez git repository, navigate into the cloned repository and then run: `pip setup.py install` and Bluetooth will be installed on your machine but if you're on a Linux machine (Note I do not have a Linux machine, I am guessing here, so don't trust me on the Bluetooth installation) just run `pip install bluetooth`, I think Bluetooth is installed by default on Linux

## Usage
In the cmd navigate to the folder you want to use with the main.py file, run `py main.py` and sit back and enjoy the game

## License
This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## IFEs Pong v1
Hello my name is Nwufo Ifechukwu and this is my version of pong but better. It was released on the 31st of July 2023 as you know it has taken me some time to make and believe it or not this is the most complicated and difficult project I have made so far. At the end of the screen, you will find some links you can go to to support me.

### Table of Contents
- [Game-play-and-ui](#gameplay-and-ui)
- [Future-updates](#future-updates-will-include)

### Gameplay and UI
- If you remember pong you will know how to play it, click 'a' to toggle the control options of player one (on the left) and 'i' for player two (on the right)
- Click the ESCAPE button to go back to any of the previous windows and 'Enter' to activate it
- The 'Resume', 'Restart' and 'Quit' menu options are very self explanatory and you know what they do

### Future updates will include
- The options 
-   colour scheme change option         
-   character skin change              
-   font change
-   ai difficulty
-   default player choice              
-   others
- Better sound effects                
- Some bug fixes
- Better AI
- Background 
- Others


## IFEs Pong v2
Hello my name is Nwufo Ifechukwu and this my version of pong but better. It was released on 31st of July 2023 and this the update which was released on 14 on August 2023. As you know it has taken me sometime to make and believe it or not this is the most complicated and difficult project I have made so far. At the end of the screen you will find some links you can go to to support me.

### Table of Contents
- [Updates](#Updates)
- [Game-play-and-ui](#gameplay-and-ui-1)
- [Future-updates](#Future-updates-will-include-1)

### Updates
- The biggest update is that the settings menu has been added (In the previous version it was referenced as option but I think settings is a better name)
    - Under the settings menu there are 7 options: Background color, Foreground color, Link color, player one and player two control, AI Difficulty and Character skin. Their names are self explanatory
    - AI Difficulty is a selector type input, the control pickers are the inputs where you click the key you want and it is updated (a key is a single character) while the other inputs are text fields
    - The color text fields accepts string inputs like "blue", "green" and "black", It also accepts RGBA inputs but if you have checked it out you will find out that you can't input brackets or braces so if you want to input yellow in RGBA instead of inputing "(255, 255, 0, 255)" you instead input "255, 255, 0, 255", Same with hex values instead of "#123123" you input "123123" ad the game will automatically compute it.             
- The game mechanics have been better optimized to fit the original pong game and bug fixes have been made to the player one character especially, (fixes have also been made to other aspects of the game) and the size of the characters have been changed also
- A better AI has been added and in a future update I will use machine learning to train the AI instead of using the current method I am using
- Some other miscellaneous updates were made like the blinking of the focus rectangles has been increased or the movement of the scores to align with the centre properly and some others

### Gameplay and UI
- If you remember pong you will know how to play it, click 'a' to toggle the control options of player one (on the left) and 'i' for player two (on the right), the default control for player one is 'w' for up and 's' for down while for player two it the UP for up and the DOWN button for down
- Click the ESCAPE button to go back to any of the previous windows and ENTER to activate and deactivate any option that is in focus
- For now you will have to manually type in the directory so it is advisable to have it in the same directory as the main.py file. So if you have a file named "foo.jpg" in the file named folder utils, you input "utils/foo.jpg" or if it is in the directory where main.py is in you input "foo.jpg"
- If you want to add a new key control setting just click the key when the option is in focus and to toggle between up and down movement just click home to go to the down option and home for the up option

### Future updates will include
- Better sound effects
- Text field bug fixes 
- An option in the settings menu used for changing the control option, ie "KEYS and AI" remotely from the main game



## IFEs Pong v3
Hello world, this is my version of pong but better. This is the 3rd and one of near-final updates. It has taken me a lot to make and this is the most complicated and difficult project I have made so far, users might look at it and think it was easy to make but a programmer who looks at the code and sees what I did in with python, a Windows 10 HP laptop and pygame will see why this was so hard, but that's just me talking. Below you will find some more info about the game and at the end of the screen you will find some links that I think you would like to see.

### Table of Contents
- [Updates](#updates-1)
- [Game-play-and-ui](#game-features-and-menus)
- [What's-next](#what's-next)
- [Other-info](#also)

### Updates
- The ability to control the player to pause, resume and go back with your mouse has been added. Your mouse can also be used to click on options and use the scroll wheel.
- The text fields have been vastly improved making text fields in pygame is not easy and I have done my best to make it feel real.
- The Character Skin option has been removed. If you want to add skins and backgrounds, all you have to do is to get an image you would like to use and add it to the folder called SKINS, then if the picture is for the background rename it to the background, if it is for the player rename it to player and the same for ui and ball. Note: It is advisable to use a complete image not an image that has some transparent parts for better performance.
- The Link Color option has been removed, I realised that you guys don't really need access to the color of those sweet juicy links that you might want to click on and check out and support you know
- A major part of the update is the addition of a better UI, basically what you can do with your keyboard you can do with the mouse. Pause, Back and resume buttons have been added to the game (all at the top left of the screen). The pause button is in the main game, resume button is in the pause menu, back button is in the settings and help menu screen (statistics coming later).

### Game features and menus
These are the features that make the basic UI of the game

#### Contents
- [Pause-screen](#pause)
- [Settings-screen](#settings)
- [Information-screen](#information)
- [Statistics-screen](#statistics)

#### Pause
- Resume: As it says resumes the game, or you can use the button at the top left of the screen to resume
- Settings: Provides options that change the outlook and performance of the game. Better definition below
- Restart: Resets the game
- Exit: Helps you to leave the game, which I don't think you should do

#### Settings
- Background Color: This is used to change the color of the background of all the menus
- Foreground Color: This is used to change the color of the foreground of the screen like text, buttons and the scroll wheel
- AI Difficulty: This is to change the difficulty of the opposing AI. Their values are [Easy, Medium, Normal, Hard, Impossible]
- Player one Binding: This is used to change the keyboard binding that controls player one, when focused on the up or down option click enter and then press any key you want to you want to bind to up in the mini window that appears and vice versa for down.
- Player two Binding: Same as Player one Binding
- Player one Control: This is to change the control method of player one (the bat on the left). Their values are [KEYS, AI, MOUSE]
- Player two Control: This is to change the control method of player two (the bat on the right). Their values are [KEYS, AI, MOUSE]
    
##### note:
- The color text fields accepts string inputs like "blue", "green" and "black", It also accepts RGBA inputs but if you have checked it out you will find out that you can't input brackets or braces so if you want to input yellow in RGBA instead of inputing "(255, 255, 0, 255)" you instead input "255, 255, 0, 255", Same with hex values instead of "#123abc" you replace the '#' for a '.' as in ".123123" and the game will add the values that ought to be there it.
- Those things besides the AI DIfficulty and Player Control options are like cursors you can click to toggle the options just like you use in your keyboard

#### Information
As you have noticed a scroll wheel has been added to the information (formally known as help screen) screen to help you Get to the bottom of the page faster, you can also use home and end to get to see the links that you might want to check out. I've also changed the name from Help to Information for certain reasons you may not understand

#### Statistics
This is a new aspect of the update and it shows multiple statistics that you probably don't need but I will still give because I can. like longest play time, best score and others (coming soon)

### What's next
Multiplayer is going to be added in another update apart from that I have no idea, whatever bugs I find and things I can optimize I will optimize I will fix and optimize, If you find anything wrong comment on my itch page and I will get to it when I can. Links below at the end of the screen. And there were some other features I couldn't mention but you'll have to see them for yourself

### Also
If any error was made in this menu or the game in general, I was tired and I didn't care anymore because I was returning to school and missed the error. Thanks and bye for now.


## IFEs Pong v4
Hi, I didn't think version 4 would be out so soon, in the last update, I insinuated that I might not make or release the game so soon, but the fact is that I love to code, and I couldn't stay away from my laptop the entire time I was in school. So this is version 4, as with every update there are some nice links at the bottom of the screen, that you should check out, soo see ya. Oh and this is some sort of a prototype (for testing purposes), and might have some bugs and errors, especially in the multiplayer part (Bluetooth).

### Table of Contents
- [Updates](#updates-2)
- [Game-play-features-and-ui](#game-features-and-menus-1)
- [Future-updates](#what's-next-1)
- [Other-info](#also-1)

### Updates
- Fixed all of the widgets and improved them so very much, you might not really see it, but it is much better.
- Some certain sound effects have been added, but they have not been added everywhere bcos as I said this is a prototype and for testing purposes.
- Multiplayer has finally been added, but it is only Bluetooth for now, and that is mainly why I am posting the game, to test some aspects with other computers
- Other aspects of the game, apart from some of the visuals have largely remained unchanged, but some of the parts of it might be a little buggy, but a new version will come out soon...enough

### Game features and menus
Basically, everything is the same from the last update

#### Contents
- [Pause-screen](#pause-1)
- [Settings-screen](#settings-1)
- [Statistics-screen](#statistics-1)

#### Pause
- Resume: As it says resumes the game, or you can use the button at the top left of the screen to resume                                                                            
- Settings: Provides options that change the outlook and performance of the game. Better definition below                                                                                 
- Restart: Resets the game
- Exit: Helps you to leave the game, which I don't think you should do

#### Settings
- Background Color: This is used to change the color of the background of all the menus        
- Foreground Color: This is used to change the color of the foreground of the screen like text, buttons and the scroll wheel
- AI Difficulty: This is to change the difficulty of the opposing AI. Their values are [Easy, Medium, Normal, Hard, Impossible]
- Player One Binding: This is used to change the keyboard binding that controls Player One, when focused on the up or down option click enter and then press any key you want to bind to up in the mini window that appears and vice versa for down.
- Player two Binding: Same as Player one Binding                                               
- Player One Control: This is to change the control method of player one (the bat on the left). Their values are [KEYS, AI, MOUSE]
- Player Two Control: This is to change the control method of player two (the bat on the right). Their values are [KEYS, AI, MOUSE]

##### Note:
- The colour text fields accept string inputs like "blue", "green" and "black", It also accepts RGBA inputs but if you have checked it out you will find out that you can't input brackets or braces so if you want to input yellow in RGBA instead of inputing "(255, 255, 0, 255)" you instead input "255, 255, 0, 255", Same with hex values instead of "#123abc" you replace the '#' for a '.' as in ".123123" and the game will add the values that ought to be there it.
- Those things besides the AI DIfficulty and Player Control options are like cursors you can click to toggle the options just like you use in your keyboard                     

#### Statistics
I have been putting off this part, but....later                                              

### What's next
Multiplayer is going to be improved in the next update apart from that, multitudes of fixes are going to happen, just be patient

### Also
If any error was made in this menu or the game in general, I was tired bcos I have spent a lot of time working on this game, so...sorry or whatever. I have finished my first term in school and we are entering Christmas holidays, so more things are coming. Thanks and see you soon.


## IFEs Pong v5
Version 5 is here and from making this I've found out that this game is almost done, I've looked for what to improve and I couldn't find much, (apart from the features I put coming soon on). But a very big update has been added (MORE INFO AT THE UPDATE SECTION), I have fixed every single bug not relating to the multiplayer, and have added a permission screen as you might have already seen. The permission screen has given me the power to make an MSI version of this game, bcos during testing, I found out that I get errors from my system involving permissions. So now you don't have to install a sketchy zip file on your system. If you want to get the playable version of the game check out the game at [IFEsPong](https://ifeisachildofgod.itch.io/ifes-pong), while your there you can also check out my other serious game at [IFEsPixelRunner](https://ifeisachildofgod.itch.io/ifes-pixel-runner), heck just visit [IFEsItchpage](https://ifeisachildofgod.itch.io/) to see all my projects and if you want to hire you can also visit [IFEsFreelance](https://www.upwork.com/freelancers/~0113b8c14366fba047?referrer_url_path=%2Fab%2Fprofiles%2Fsearch%2Fdetails%2F~0113b8c14366fba047%2Fprofile). Thanks.

### Table of Contents
- [Updates](#updates-3)
- [Game-play-features-and-ui](#game-features-and-menus-2)
- [Future-updates](#what's-next-2)
- [Other-info](#also-2)

### Updates
-  Permission checking has been added
-  The code has vastly been improved
-  Most, if not all bugs in the Bluetooth multiplayer have been fixed
-  The ball physics have been improved
-  Tiny optimizations, fixes and adjustments have been made
    
### Game features and menus
I forgot to mention that the main menu had been added in the main update but am sure that you might have figured it out. I don't plan on adding any more menus, so I may remove this section in the next update

#### Contents
- [Settings-screen](#settings-2)
- [Statistics-screen](#statistics-2)

#### Settings
-  Background Color: This is used to change the colour of the background of all the menus
-  Foreground Color: This is used to change the colour of the foreground of the screen like text, buttons and the scroll wheel
-  AI Difficulty: This is to change the difficulty of the opposing AI. Their values are [Easy, Medium, Normal, Hard and Very Hard]
-  Player one(two) Binding: This is used to change the keyboard binding that controls each player, when focused on the up or down option click enter and then press any key you want to you want to bind to up in the mini window that appears and the same for down.
-  Player one(two) Control: This is to change the control method the player selected. Their values are [KEYS, AI and MOUSE]

##### Note:
- The colour text fields accept string inputs like "blue", "green" and "black", It also accepts RGBA inputs but if you have checked it out you will find out that you can't input brackets or braces so if you want to input yellow in RGBA instead of inputting "(255, 255, 0, 255)" you instead input "255, 255, 0, 255", Same with hex values instead of "#123abc" you replace the '#' for a '.' as in ".123123" and the game will add the values that ought to be there it.
- Those things besides the AI DIfficulty and Player Control options are like cursors you can click to toggle the options just like you use in your keyboard

#### Statistics
I got my priorities straight and had a reality check, and I realised that the game does not need another menu, so this feature will not be coming out in this update, and probably not in any update from now on. This is the last version that will have this section in the info screen.

### What's next
-  I am currently experimenting and working on server multiplayer, but it proves to be quite difficult, so I can't make any promises that this will be added in the next update.
-  A better system for adding custom skins may be added, if I can figure it out

### Also
If any error was made in this menu or the game in general, I am sorry. I'm currently returning back to school, and somewhat had to rush certain fixes and optimizations so as to make it release ready, due to our school's resumption I be focusing more on my studies, that is why updates might not come out for a while. Bye for now thanks and see you soon.

### Links that support me
- [IFEsPong](https://ifeisachildofgod.itch.io/ifes-pong)
- [IFEsItchpage](https://ifeisachildofgod.itch.io/)
- [IFEsPixelRunner](https://ifeisachildofgod.itch.io/ifes-pixel-runner)
- [IFEsYTVDownloader](https://ifeisachildofgod.itch.io/ifes-ytvideo-downloader)
- [IFEsFreelance](https://www.upwork.com/freelancers/~0113b8c14366fba047?referrer_url_path=%2Fab%2Fprofiles%2Fsearch%2Fdetails%2F~0113b8c14366fba047%2Fprofile)


## IFEs Pong v6
#### Update coming