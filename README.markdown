Picgen
======

Picgen started with one idea : the number of possible images that can be described by black and white pixels is limited. If the area is small enough, it is possible to generate all images and have them checked by humans by crowdsourcing.

In order to find people willing to participate to this crowdsourcing experience, I imagined a game (composed by several little well known games such as nonograms).

Game description
----------------

The game design is still in progress, only a small fraction of it is currently implemented but it is slowly getting into shape as I learn how to use the different languages (I'm using this project to learn javascript (AJAX) and google app engine python webapp module).

The main goal of the game is to win little pictures that represent something, and then use those pictures to earn points, allowing you to gain more pictures...

**Mining**  
The main goal of the game is to win pictures by mining into the huge range of possible _Pictures_. The process of mining is done by solving a puzzle game (such as pattern (nonograms), mines, loopy, range... my inspiration comes from the games of Simon [Tatham's Portable Puzzle Collection](http://www.chiark.greenend.org.uk/~sgtatham/puzzles/)). All games that you solve gives you the property of the final _Picture_.

**Refining**  
After wining the _Picture_ the game ask you if you recognize something in the picture. If you do, the picture you now own will be able to make you earn more points. Most of the time, there is nothing, the _Picture_ is still yours but it will not become a source of wealth, you only earn points from solving the puzzle.

**Expertisation** 
The _Pictures_ that you just named is then put into the open for expertise. Expertise is a process where other players (acting as _Experts_) try to guess what you just saw into your _Picture_ (a word games is involved similar to pictionary...). Every _Experts_ that succeed will make your _Picture_ more likely to be validated, each _Experts_ that failed will do the opposite.
After some time, the name you propose for the _Picture_ is either validated or rejected.
_Experts_ are rewarded in points so they will try hard to find the good answer.

**Earning** 
Your _Picture_ has been validated ? You will be rewarded by a huge amount of points !

Development
-----------

I currently use [Google App Engine](http://code.google.com/appengine/) using the Python 2.7 version.
Server side is coded in python 2.7.
HTML templates use the django-style templates.
AJAX is done using json2.js.

If someone is interested, I will post the details of how to setup a testing environment, all necessary files should be in the git repository.
