from neo4j import GraphDatabase, exceptions as neo4j_exceptions
import logging

class Neo4jClient:
    def __init__(self, uri, user, password):
        self.driver = GraphDatabase.driver(uri, auth=(user, password))

    def run_query(self, query, params=None):
        try:
            with self.driver.session() as session:
                result = session.run(query, params or {})
                return [record.data() for record in result]  # fully consume the result
        except neo4j_exceptions.ServiceUnavailable as e:
            logging.error(f"Neo4j service unavailable: {e}")
            raise RuntimeError("Neo4j service is unavailable. Please check your database connection.") from e
        except neo4j_exceptions.AuthError as e:
            logging.error(f"Neo4j authentication failed: {e}")
            raise RuntimeError("Neo4j authentication failed. Please check your credentials.") from e
        except neo4j_exceptions.CypherSyntaxError as e:
            logging.error(f"Cypher syntax error: {e}")
            raise RuntimeError(f"Cypher syntax error: {e}") from e
        except neo4j_exceptions.Neo4jError as e:
            logging.error(f"Neo4j error: {e}")
            raise RuntimeError(f"Neo4j error: {e}") from e
        except Exception as e:
            logging.error(f"Unexpected error running Neo4j query: {e}")
            raise RuntimeError(f"Unexpected error running Neo4j query: {e}") from e

    def close(self):
        self.driver.close()