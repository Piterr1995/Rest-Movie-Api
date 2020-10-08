<h3>IMDB Movie Fetcher with Django Rest Framework</h3>

This is a Rest API which allows you to get all the info about any movie that exists in IMDB database.

<b>Please follow the steps below in order to get it working on your local machine</b>
<ol>
  <li>Initialize an empty repository <br />
    $ git init
   </li>
   
   <li> Clone the repository <br />
   $ git clone https://github.com/avatarr95/Rest-Movie-Api
   </li>
   
   <li>Install requirements <br />
   $ pip install -r requirements.txt
   </li>
   <li> Run server <br />
   $ python manage.py runserver
   </li>
</ol>

<b> You are good to go! </b>

<b>Methods allowed</b>
<i>In case of any problems you will receive instructions on how to send requests properly</i>
<ul>
<li>​POST /movies</li>
<li>GET /movies</li>
<li>DELETE /movies/<movie-id>/</li>
<li>UPDATE /movies/<movie-id>/</li>
<li>POST /comments</li>
<li>GET /comments</li>
<li>GET /top</li>
</ul>

<b>The environmental variables from .env file should not be here! Please make sure you add .env to .gitignore file!</b>
