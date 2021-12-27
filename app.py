from flask import Flask, render_template, request, redirect
from QueryHandler import MovieQueryHandler, SearchQueryHandler
import urllib

app = Flask(__name__)
movie_handler = MovieQueryHandler()
search_handler = SearchQueryHandler()

@app.route('/', methods=(['GET']))
def index():
	searched = request.args.get("searchedMovie","")
	result = search_handler.query(searched)
	result = [d.asdict() for d in result]
	return render_template('index.html',list_data=result,searched=searched)

@app.route('/movie/<string:title_uri>', methods=(['GET']))
def movie(title_uri):
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
	return render_template('movie.html',result = result,abstract = abstract, distributor = distributor, distributor_uri = distributor_uri)


if __name__ == "__main__":
	app.run(debug=True)