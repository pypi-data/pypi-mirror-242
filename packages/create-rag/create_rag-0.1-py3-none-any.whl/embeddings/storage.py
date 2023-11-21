import csv
import json
import numpy as np
import os
import psycopg2

class Database:
    def __init__(self, conn_str):
        self.conn = psycopg2.connect(conn_str)
    
    def create_table(self, name: str, vector_length: int = 2, max_vectors: int = 10_000):
        """Creates a table with the given name and specified vector length."""
        with self.conn.cursor() as cur:
            cur.execute(f"""
                CREATE TABLE {name} (
                    id SERIAL PRIMARY KEY,
                    embedding silverarrow_vector({vector_length}, 1, {max_vectors}, 0), 
                    text TEXT,
                    metadata JSONB
                )
            """)
        self.conn.commit()
        return Table(self.conn, name)
    
    def load(self, name: str):
        """Connects to an existing table and returns a Table instance for it."""
        return Table(self.conn, name)
    
    def list_tables(self) -> list:
        """Lists all the tables in the database."""
        with self.conn.cursor() as cur:
            cur.execute("SELECT table_name FROM information_schema.tables WHERE table_schema='public'")
            tables = cur.fetchall()
        return [table[0] for table in tables]

    def close(self):
        """Closes the database connection."""
        self.conn.close()

class Table:  

    def __init__(self, conn, name: str):
        self.conn = conn
        self.table_name = name  

    def add(self, embedding: tuple) -> None:
        """Adds an embedding to the table."""
        embedding_vector, text_data, metadata = embedding
        embedding_str = '[' + ', '.join(map(str, embedding_vector)) + ']'
        json_metadata = json.dumps(metadata)  # Convert dictionary to JSON string
        with self.conn.cursor() as cur:
            cur.execute(f"""
                INSERT INTO {self.table_name} (embedding, text, metadata)
                VALUES (%s, %s, %s)
            """, (embedding_str, text_data, json_metadata))
        self.conn.commit()

    def batch_add(self, embeddings: list) -> None:
        """Adds a batch of embeddings to the table."""
        with self.conn.cursor() as cur:
            # Create a list of tuples containing the data to be inserted
            data = [(
                '[' + ', '.join(map(str, embedding_vector)) + ']',
                text_data.replace("'", "''"),  # escape single quotes
                json.dumps(metadata)
            ) for embedding_vector, text_data, metadata in embeddings]

            args_str = ",".join(cur.mogrify("(%s, %s, %s)", (x, y, z)).decode('utf-8') for x, y, z in data)
            cur.execute(f"INSERT INTO {self.table_name} (embedding, text, metadata) VALUES " + args_str)
        self.conn.commit()


    def semantic_query(self, embedding_vector: str, num_results: int, pf_blocks: int = None, pf_thresh: float = None, metadata_filter: dict = None) -> list:
        """Queries the table for the embedding with optional metadata-based filtering."""
        
        # if we have a pf_blocks and pf_thresh, use the optimized version of the query
        if pf_blocks and pf_thresh:
            base_query = f"""
                SELECT c.*, s.distance 
                FROM {self.table_name} c 
                INNER JOIN silverarrow_l2_hypersearch('{self.table_name}', 'embedding', '{embedding_vector}', {num_results}, {pf_blocks}, {pf_thresh}) s 
                ON c.id = s.id
            """
        else:
            base_query = f"""
                SELECT c.*, s.distance 
                FROM {self.table_name} c 
                INNER JOIN silverarrow_l2_search('{self.table_name}', 'embedding', '{embedding_vector}', {num_results}) s 
                ON c.id = s.id
            """
        
        where_clause = ""
        if metadata_filter:
            conditions = []
            for key, value in metadata_filter.items():
                conditions.append(f"c.metadata->>'{key}' = '{value}'")
            
            where_clause = "WHERE " + " AND ".join(conditions)
        
        final_query = base_query + " " + where_clause
        
        with self.conn.cursor() as cur:
            cur.execute(final_query)
            results = cur.fetchall()
            
        return results

    
    def keyword_query(self, keyword: str, num_results: int, metadata_filter: dict = None) -> list:
        """Queries the table for the keyword with optional metadata-based filtering."""
        
        where_conditions = [f"to_tsvector('english', text) @@ plainto_tsquery('english', '{keyword}')"]

        if metadata_filter:
            for key, value in metadata_filter.items():
                where_conditions.append(f"metadata->>'{key}' = '{value}'")

        where_clause = " AND ".join(where_conditions)
        
        with self.conn.cursor() as cur:
            cur.execute(f"""
                SELECT *, ts_rank_cd(to_tsvector('english', text), plainto_tsquery('english', '{keyword}')) AS rank
                FROM {self.table_name}
                WHERE {where_clause}
                ORDER BY rank DESC
                LIMIT {num_results}
            """)
            results = cur.fetchall()
            
        return results
    
    def hybrid_query(self, keyword: str, embedding_vector: str, num_results: int, metadata_filter: dict = None) -> list:
        """Queries the table for the keyword and embedding."""
        keyword_results = self.keyword_query(keyword, num_results, metadata_filter=metadata_filter)
        embedding_results = self.semantic_query(embedding_vector, num_results, metadata_filter=metadata_filter)
        
        # Merge the two result sets
        merged_results = []
        for keyword_result in keyword_results:
            distance_to_rank = 0
            merged_result = list(keyword_result)
            for embedding_result in embedding_results:
                if keyword_result[0] == embedding_result[0]:
                    # Found same result in both queries

                    # Convert the distance to a rank
                    distance_to_rank = 1000 / embedding_result[-1]
                    break
            merged_result[-1] = merged_result[-1] + distance_to_rank
            merged_results.append(merged_result)
        
        # Sort the merged results by rank and distance
        sorted_results = sorted(merged_results, key=lambda x: x[-1], reverse=True)
        
        return sorted_results
    
    def export(self, filePath: str = None, format: str = 'csv') -> None:
        """
        Exports the table data as a csv or numpy file, csv for csv, npy for numpy.
        """
        if filePath is None:
            filePath = f"{self.table_name}.{format}"

        with self.conn.cursor() as cur:
            cur.execute(f"SELECT * FROM {self.table_name}")
            
            if format == 'csv':
                column_names = [desc[0] for desc in cur.description]
                with open(filePath, 'w', newline='') as csv_file:
                    writer = csv.writer(csv_file)
                    writer.writerow(column_names)
                    for row in cur:
                        writer.writerow(row)
                
            elif format == 'npy':
                data = np.array(cur.fetchall())
                np.save(filePath, data)
                
            else:
                raise ValueError("Format should be either 'csv' or 'npy'.")
                
        print(f"Data exported to {os.path.abspath(filePath)}")

    def delete(self) -> None:
        """Deletes the table from the database."""
        with self.conn.cursor() as cur:
            cur.execute(f"DROP TABLE {self.table_name}")
        self.conn.commit()

    def clear(self) -> None:
        """Resets the table (deletes all data)."""
        with self.conn.cursor() as cur:
            cur.execute(f"TRUNCATE {self.table_name}")
        self.conn.commit()

