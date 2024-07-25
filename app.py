from flask import Flask, render_template,request
from rdflib import RDFS, Graph, URIRef, Literal
from rdflib.namespace import RDF, OWL, XSD
from rdflib import Graph, Namespace
app = Flask(__name__)

# Load RDF data from file
# Moldify the path location of the rdf file.
rdf_file_path = r'C:/Users/rizwa/Desktop/univ/S01-3-KR& SW/Project/kr_website/ontology.ttl'
graph = Graph()
graph.parse(rdf_file_path, format='turtle')

# Define the namespaces
onto = Namespace("http://www.kr_paris.com/ontologies/tourism#")
dbo = Namespace("http://dbpedia.org/ontology/")

@app.route('/')
def home():
    # Query to retrieve data
    query = """
        SELECT ?label ?description ?image ?countryCode ?currency ?timeZone ?image_main ?german_map ?northgermany_img ?eastgermany_img ?southgermany_img ?westgermany_img ?visareq 
        WHERE {
            ?country rdf:type dbo:Country ;
                     rdfs:label ?label ;
                     dbo:description ?description ;
                     dbo:image ?image .
            ?countryInfo rdf:type dbo:CountryInfo ;
                          dbo:countryCode ?countryCode ;
                          dbo:currency ?currency ;
                          dbo:timeZone ?timeZone ;
                          dbo:image_main ?image_main;
                          dbo:german_map ?german_map;
                          dbo:northgermany_img ?northgermany_img ;
                          dbo:eastgermany_img ?eastgermany_img ;
                          dbo:southgermany_img ?southgermany_img ;
                          dbo:westgermany_img ?westgermany_img;
                          dbo:visareq ?visareq.
                          

        }
    """
    results = graph.query(query, initNs={"dbo": dbo, "rdf": Namespace("http://www.w3.org/1999/02/22-rdf-syntax-ns#")})

    # Extracting data from the query results
    for row in results:
        label, description, image, countryCode, currency, timeZone,image_main,german_map,northgermany_img,eastgermany_img,southgermany_img ,westgermany_img,visareq= row

    # Pass the data to the template
    return render_template('home.html', label=label, description=description, image=image,
                           countryCode=countryCode, currency=currency, timeZone=timeZone,image_main=image_main,german_map=german_map, northgermany_img=northgermany_img,eastgermany_img=eastgermany_img,southgermany_img=southgermany_img ,westgermany_img=westgermany_img,visareq=visareq)

@app.route('/regions_main')
def regions_main():
    # Query to retrieve data
    query1 = """
    SELECT ?region ?label ?description ?image ?cultureDescription
    WHERE {
        ?region rdf:type dbo:Region ;
                rdfs:label ?label ;
                dbo:description ?description ;
                dbo:cultureDescription ?cultureDescription;
                foaf:depiction ?image .
        FILTER (?region IN (<http://group12.org/places/northern-germany>,
                            <http://group12.org/places/southern-germany>,
                            <http://group12.org/places/eastern-germany>,
                            <http://group12.org/places/western-germany>))
    }
    """
    results = graph.query(query1, initNs={"dbo": dbo, "rdf": Namespace("http://www.w3.org/1999/02/22-rdf-syntax-ns#")})

    # Extracting data from the query results and storing in a list of dictionaries
    regions_data = [{'label': str(row.label), 'description': str(row.description),
                     'image': str(row.image), 'cultureDescription': str(row.cultureDescription),
                     'region_uri': str(row.region)} for row in results]

    # Pass the data to the template
    return render_template('regions_main.html', regions_data=regions_data)


@app.route('/region/<region_name>')
def show_region(region_name):
    # Replace spaces with underscores in the region name
    region_name_safe = region_name.replace(' ', '_')
    
    return render_template(f'{region_name_safe}.html')
   
@app.route('/region/northern_germany')
def northern():
    # Query to retrieve data
    query_north = """
    SELECT ?state ?label ?description ?image
    WHERE {
        ?state rdf:type dbo:State ;
                rdfs:label ?label ;
                dbo:description ?description ;
                foaf:depiction ?image .
        FILTER (?state IN (<http://group12.org/places/hamburg> ,
                            <http://group12.org/places/bremen>,
                           <http://group12.org/places/lower-saxony> ,
                            <http://group12.org/places/mecklenburg-vorpommern> ,
                            <http://group12.org/places/schleswig-holstein>))
    }
    """
    results = graph.query(query_north, initNs={"dbo": dbo, "rdf": Namespace("http://www.w3.org/1999/02/22-rdf-syntax-ns#")})

    # Extracting data from the query results and storing in a list of dictionaries
    regions_data = [{'label': str(row.label), 'description': str(row.description),
                     'image': str(row.image)} for row in results]

    # Pass the data to the template
    return render_template('northern_germany.html', regions_data=regions_data)

@app.route('/region/eastern_germany')
def eastern():
    # Query to retrieve data
    query_east = """
    SELECT ?state ?label ?description ?image
    WHERE {
        ?state rdf:type dbo:State ;
                rdfs:label ?label ;
                dbo:description ?description ;
                foaf:depiction ?image .
        FILTER (?state IN (<http://group12.org/places/brandenburg> ,
                            <http://group12.org/places/saxony> ,
                            <http://group12.org/places/saxonyAnhalt> ,
                            <http://group12.org/places/berlin> ,
                            <http://group12.org/places/thuringia>))
    }
    """
    results = graph.query(query_east, initNs={"dbo": dbo, "rdf": Namespace("http://www.w3.org/1999/02/22-rdf-syntax-ns#")})

    # Extracting data from the query results and storing in a list of dictionaries
    regions_data = [{'label': str(row.label), 'description': str(row.description),
                     'image': str(row.image)} for row in results]

   

    # Pass the data to the template
    return render_template('eastern_germany.html', regions_data=regions_data)

@app.route('/region/southern_germany')
def southern():
    # Query to retrieve data
    query_south = """
    SELECT ?state ?label ?description ?image
    WHERE {
        ?state rdf:type dbo:State ;
                rdfs:label ?label ;
                dbo:description ?description ;
                foaf:depiction ?image .
        FILTER (?state IN (<http://group12.org/places/bavaria> ,
                            <http://group12.org/places/hesse>,
                           <http://group12.org/places/rhineland-palatinate> ,
                            <http://group12.org/places/baden-wurttemberg>))
    }
    """
    results = graph.query(query_south, initNs={"dbo": dbo, "rdf": Namespace("http://www.w3.org/1999/02/22-rdf-syntax-ns#")})

    # Extracting data from the query results and storing in a list of dictionaries
    regions_data = [{'label': str(row.label), 'description': str(row.description),
                     'image': str(row.image)} for row in results]

    # Pass the data to the template
    return render_template('southern_germany.html', regions_data=regions_data)

@app.route('/region/western_germany')
def western():
    # Query to retrieve data
    # Query to retrieve data
    query_west = """
    SELECT ?state ?label ?description ?image
    WHERE {
        ?state rdf:type dbo:State ;
                rdfs:label ?label ;
                dbo:description ?description ;
                foaf:depiction ?image .
        FILTER (?state IN (<http://group12.org/places/saarland> ,
                            <http://group12.org/places/northrhinewestphalia>))
                            
    }
    """
    results = graph.query(query_west, initNs={"dbo": dbo, "rdf": Namespace("http://www.w3.org/1999/02/22-rdf-syntax-ns#")})

    # Extracting data from the query results and storing in a list of dictionaries
    regions_data = [{'label': str(row.label), 'description': str(row.description),
                     'image': str(row.image)} for row in results]

    # Pass the data to the template
    return render_template('western_germany.html', regions_data=regions_data)


@app.route('/destinations')
def destinations():
    # Query to retrieve data
    # Query to retrieve data
    query_destinations = """
    SELECT ?destination ?label ?description ?image
    WHERE {
        ?state rdf:type dbo:Destination ;
                rdfs:label ?label ;
                dbo:description ?description ;
                foaf:depiction ?image .
        FILTER (?state IN (<http://group12.org/destination/bavarianalps> ,
                            <http://group12.org/destination/berchtesgaden> ,
                            <http://group12.org/destination/blackForest> ,
                            <http://group12.org/destination/cologne> ,
                            <http://group12.org/destination/culturaroutes> ,
                            <http://group12.org/destination/dresen> ,
                            <http://group12.org/destination/frankfurt> ,
                            <http://group12.org/destination/heidelberg> ,
                            <http://group12.org/destination/neuschwansteincastle> ,
                            <http://group12.org/destination/nuremberg> ,
                            <http://group12.org/destination/rhinevalley> ,
                            <http://group12.org/destination/neuschwansteincastle> ,
                            <http://group12.org/destination/nuremberg> ,
                            <http://group12.org/destination/rhinevalley> ,
                            <http://group12.org/destination/munich> ,                    
                            <http://group12.org/destination/rothenburg>))
                            
    }
    """
    results = graph.query(query_destinations, initNs={"dbo": dbo, "rdf": Namespace("http://www.w3.org/1999/02/22-rdf-syntax-ns#")})

    # Extracting data from the query results and storing in a list of dictionaries
    dest_data = [{'label': str(row.label), 'description': str(row.description),
                     'image': str(row.image)} for row in results]

    # Pass the data to the template
    return render_template('destinations.html', dest_data=dest_data)

@app.route('/attraction')
def index():
    return render_template("attraction.html")

@app.route("/search", methods=["POST"])
def search():
    attraction_type = request.form.get("attraction_type")
    
    # Query RDF data to get places based on the selected attraction type
    query = f"""
    SELECT ?place ?label ?description
    WHERE {{
        ?place rdf:type dbo:Attraction ;
               rdfs:label ?label ;
               dbo:description ?description ;
               dbo:hasAttractionType onto:{attraction_type} .
    }}
    """
    results = graph.query(query, initNs={"dbo": dbo, "rdf": RDF, "rdfs": RDFS, "onto": onto})
    # Convert query results to a list of dictionaries
    attractions = [{"label": label, "description": description} for place, label, description in results]
    return render_template("search.html", attractions=attractions)


if __name__ == '__main__':
    app.run(debug=True)
