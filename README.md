# TurkPro
Robotic arm chess teacher. 
# Table of Contents 
   * [What is this?](#what-is-this)
   * [Requirements](#requirements)
   * [Documentation](#documentation)
   * [How to use](#how-to-use)
   * [Authors](#authors)

# What is This ? 

This is a robotic chess teacher, he will play against you and explain your mistakes.

Features:  
- Auto Board detection: At launch detects the board position and orientation and adapts to it. 

- Move classification: The Robot keeps track of the game moves. 
    
- Text to speech: The Robot makes comentaries abaut your game and talks his moves. 
    
- Piece pointing: The Robot indicates his moves by pointing them
   
- Game analisis: The Robot uses stockfish in order to analize your game and play against you. It is also used to give player advice and hints. 

# Requirements.

- [ffmpeg](https://www.ffmpeg.org)

- Google gemini api key.

    name it text_to_speech.json and delete the current one.  
    if it's not changed text to speech wont work this api key is currently disabled. 

Install the required packages 

```
pip install -r requirements.txt
```
# Documentation
# How To Use
## Setup

### Fisical setup : 

#### Robot
#### Board 
- Place the board in front of the robot with a file touching the robot and 1s row at robots left : 

- Place two red points in h file and two blue points in a file. 
- Assure that the camera has a and unobstructed view of the board and the color points. 

## Gameplay

- Player starts by moving a white piece and selecting move on the web app. 
- The robot will say it's move and point it. 
- Make the robot's move and select move on the app. 
- Make your move, aand you know. 

When the player makes a mistake the Robot will explain it and when the game ends he will anounce it also.  