import http.client
import json
import csv

class Graph:

    # Do not modify
    def __init__(self, with_nodes_file=None, with_edges_file=None):
        """
        option 1:  init as an empty graph and add nodes
        option 2: init by specifying a path to nodes & edges files
        """
        self.nodes = []
        self.edges = []
        if with_nodes_file and with_edges_file:
            nodes_CSV = csv.reader(open(with_nodes_file))
            nodes_CSV = list(nodes_CSV)[1:]
            self.nodes = [(n[0], n[1]) for n in nodes_CSV]

            edges_CSV = csv.reader(open(with_edges_file))
            edges_CSV = list(edges_CSV)[1:]
            self.edges = [(e[0], e[1]) for e in edges_CSV]


    def add_node(self, id: str, name: str) -> None:
        """
        add a tuple (id, name) representing a node to self.nodes if it does not already exist
        The graph should not contain any duplicate nodes
        """
        if (id, name) not in self.nodes:
            self.nodes.append((id,name))
        


    def add_edge(self, source: str, target: str) -> None:
        """
        Add an edge between two nodes if it does not already exist.
        An edge is represented by a tuple containing two strings: e.g.: ('source', 'target').
        Where 'source' is the id of the source node and 'target' is the id of the target node
        e.g., for two nodes with ids 'a' and 'b' respectively, add the tuple ('a', 'b') to self.edges
        """
        if (source, target) not in self.edges:
            self.edges.append((source, target))
        


    def total_nodes(self) -> int:
        """
        Returns an integer value for the total number of nodes in the graph
        """
        return len(self.nodes)


    def total_edges(self) -> int:
        """
        Returns an integer value for the total number of edges in the graph
        """
        return len(self.edges)


    def max_degree_nodes(self) -> dict:
        """
        Return the node(s) with the highest degree
        Return multiple nodes in the event of a tie
        Format is a dict where the key is the node_id and the value is an integer for the node degree
        e.g. {'a': 8}
        or {'a': 22, 'b': 22}
        """
        degree={}
        
        for edge in self.edges:
            for node in edge:
                degree[node]=degree.get(node,0)+1
        
        max_degree=max(degree.values(),default=0)
        
        max_degree_nodes={node: degree for node, degree in degree.items() if degree==max_degree}
        
        return max_degree_nodes
        


    def print_nodes(self):
        """
        No further implementation required
        May be used for de-bugging if necessary
        """
        print(self.nodes)


    def print_edges(self):
        """
        No further implementation required
        May be used for de-bugging if necessary
        """
        print(self.edges)


    # Do not modify
    def write_edges_file(self, path="D:/HW1/edges.csv")->None:
        """
        write all edges out as .csv
        :param path: string
        :return: None
        """
        edges_path = path
        edges_file = open(edges_path, 'w', encoding='utf-8')

        edges_file.write("source" + "," + "target" + "\n")

        for e in self.edges:
            edges_file.write(str(e[0]) + "," + str(e[1]) + "\n")

        edges_file.close()
        print("finished writing edges to csv")


    # Do not modify
    def write_nodes_file(self, path="D:/HW1/nodes.csv")->None:
        """
        write all nodes out as .csv
        :param path: string
        :return: None
        """
        nodes_path = path
        nodes_file = open(nodes_path, 'w', encoding='utf-8')

        nodes_file.write("id,name" + "\n")
        for n in self.nodes:
            nodes_file.write(str(n[0]) + "," + str(n[1]) + "\n")
        nodes_file.close()
        print("finished writing nodes to csv")
        
        
class  TMDBAPIUtils:

    # Do not modify
    def __init__(self, api_key:str):
        self.api_key=api_key
    
    def make_api_request(self, endpoint: str) -> dict:
        conn=http.client.HTTPSConnection("api.themoviedb.org")
        conn.request("GET",f"{endpoint}&api_key={self.api_key}")
        response=conn.getresponse()
        data=json.loads(response.read())
        conn.close()
        return data


    def get_movie_cast(self, movie_id:str, limit:int=None, exclude_ids:list=None) -> list:
        endpoint=f"/3/movie/{movie_id}/credits?api_key=beb5789a7f43361a8aa50eb8e4bd5a41"
        data=self.make_api_request(endpoint)
        cast=data.get('cast',[])
        
        if limit is not None:
            cast=cast[:limit]
        if exclude_ids:
            cast=[member for member in cast if member['id'] not in exclude_ids]
        
        return cast

    def get_movie_credits_for_person(self, person_id:str, vote_avg_threshold:float=None)->list:
        endpoint=f"/3/person/{person_id}/movie_credits?api_key=beb5789a7f43361a8aa50eb8e4bd5a41"
        data=self.make_api_request(endpoint)
        movie_credits = data.get('cast', [])

        if vote_avg_threshold is not None:
            movie_credits = [credit for credit in movie_credits if credit.get('vote_average', 0.0) >= vote_avg_threshold]

        return movie_credits


api_key = "beb5789a7f43361a8aa50eb8e4bd5a41"
tmdb_api_utils = TMDBAPIUtils(api_key)

# Example: Get the cast for a movie with ID '123'
movie_cast = tmdb_api_utils.get_movie_cast(movie_id='123', limit=5, exclude_ids=[353, 455])
print("Movie Cast:", movie_cast)

# Example: Get movie credits for a person with ID '2975'
person_credits = tmdb_api_utils.get_movie_credits_for_person(person_id='2975', vote_avg_threshold=8.0)
print("Person Credits:", person_credits)


if __name__ == "__main__":

    graph = Graph()
    graph.add_node(id='2975', name='Laurence Fishburne')
    tmdb_api_utils = TMDBAPIUtils(api_key='20a760eac80d399f5d881cc3499215f0')

    # Build the base graph
    # Fetch Laurence Fishburne's movie credits with vote average >= 8.0
# Build the base graph
# Fetch Laurence Fishburne's movie credits with vote average >= 8.0
movie_credits = tmdb_api_utils.get_movie_credits_for_person('2975', vote_avg_threshold=8.0)

for credit in movie_credits:
    # Get the top 3 co-actors for each movie credit
    co_actors = tmdb_api_utils.get_movie_cast(credit['id'], limit=3)

    for co_actor in co_actors:
        # Add co_actor as a node (if it doesn't exist)
        graph.add_node(co_actor['id'], co_actor['name'])
        # Add an edge between Laurence Fishburne and the co_actor
        graph.add_edge('2975', co_actor['id'])

# Iterate for two times as instructed
for _ in range(2):
    nodes = graph.nodes.copy()  # Copy nodes added in the previous iteration

    for node in nodes:
        movie_credits = tmdb_api_utils.get_movie_credits_for_person(node[0], vote_avg_threshold=8.0)

        for credit in movie_credits:
            co_actors = tmdb_api_utils.get_movie_cast(credit['id'], limit=3)

            for co_actor in co_actors:
                graph.add_node(co_actor['id'], co_actor['name'])
                graph.add_edge(node[0], co_actor['id'])

# Write the graph to CSV files
graph.write_edges_file()
graph.write_nodes_file()