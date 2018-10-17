#!/bin/sh

awk -F "," '{print $2}' /path/to/IMDB-Movie-Data.csv > names

while read movies; do
  name=${movies}
  movies=${movies// /%20}
  echo ${movies}
 var=`curl --request GET --url \
 "https://api.themoviedb.org/3/search/movie?include_adult=false&page=1&language=en-US&api_key=2cf54f09f30ba8de0488419e02d1303b&query=${movies}" --data '{}'` 
  var=$(echo $var | jq '."results"[0]."poster_path"')
  var="${var%\"}"
  var="${var#\"}"
  wget https://image.tmdb.org/t/p/original${var} -O "TheMovieDatabase/static/img/${name}.jpg"
done<names




: '

Poster Path

var= curl --request GET --url "https://api.themoviedb.org/3/search/movie?include_adult=false&page=1&language=en-US&api_key=2cf54f09f30ba8de0488419e02d1303b&query=${movies}" --data '{}' | jq '."results"[0]."poster_path"'
 Poster = https://image.tmdb.org/t/p/original/var



Id of the movie 
curl --request GET --url "https://api.themoviedb.org/3/search/movie?include_adult=false&page=1&language=en-US&api_key=2cf54f09f30ba8de0488419e02d1303b&query=${movies}" --data '{}' | jq '."results"[0]."id"'


Backdrop of the movie
curl --request GET --url "https://api.themoviedb.org/3/search/movie?include_adult=false&page=1&language=en-US&api_key=2cf54f09f30ba8de0488419e02d1303b&query=${movies}" --data '{}' | jq '."results"[0]."backdrop_path"'

video of the movie

key = curl --request GET --url "https://api.themoviedb.org/3/movie/${id}/videos?include_adult=false&language=en-US&api_key=2cf54f09f30ba8de0488419e02d1303b" --data '{}' | jq '."results"[0]."key"'

video = https://www.youtube.com/watch?v=var

'
