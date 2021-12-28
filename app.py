from flask import Flask, render_template, request, redirect
from QueryHandler import MovieQueryHandler, SearchQueryHandler, GenreHandler
import urllib

app = Flask(__name__)
movie_handler = MovieQueryHandler()
search_handler = SearchQueryHandler()
genre_handler = GenreHandler()

@app.route('/', methods=(['GET']))
def home():
	return render_template('home.html')

@app.route('/title', methods=(['GET']))
def title():
	searched = request.args.get("searchedMovie","")
	result = search_handler.query(searched)
	result = [d.asdict() for d in result]
	return render_template('searchTitle.html',list_data=result,searched=searched)

@app.route('/genre', methods=(['GET']))
def genre():
	genres = ['Western', 'Parody', 'Travel', 'Romance', 'Superhero', 'Anthology', 'Music', 'Mystery', 'Spy/Espionage', 'Survival', 'Coming of Age', 'Soap Opera / Melodrama', 'Animation', 'Police/Cop', 'Biographical', 'Romantic Comedy', 'Crime', 'Dance', 'Family', 'Anime', 'Disaster', 'Docuseries', 'Lifestyle', 'Reality', 'Thriller', 'Science Fiction', 'Game Show / Competition', 'Talk Show', 'Movies', 'Sports', 'Musical', 'Variety', 'Medical', 'Series', 'Documentary', 'Kids', 'Drama', 'Animals & Nature', 'Fantasy', 'Concert Film', 'Historical', 'Buddy', 'Comedy', 'Action-Adventure']
	genres.sort()
	checked = request.args.getlist("genreCheckbox")
	result = genre_handler.query(checked)
	result = [d.asdict() for d in result]
	return render_template('searchGenre.html', list_data=result, genres = genres, checked=checked)


@app.route('/details/<string:title_uri>', methods=(['GET']))
def details(title_uri):
	title = urllib.parse.unquote(title_uri)
	local_result , dbpedia_result = movie_handler.query(title)
	result = local_result[0].asdict()
	abstract = None
	distributor = None
	distributor_uri = None
	if dbpedia_result:
		if 'abstract' in dbpedia_result[0]:
			abstract = dbpedia_result[0]['abstract']['value']
		if 'distributor' in dbpedia_result[0]:
			distributor_uri = dbpedia_result[0]['distributor']['value']
			if "/" in distributor_uri:
				temp = distributor_uri.split("/")
				distributor = temp[-1].replace("_"," ")
	return render_template('details.html',result = result,abstract = abstract, distributor = distributor, distributor_uri = distributor_uri)



if __name__ == "__main__":
	app.run(debug=True)