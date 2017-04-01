    
def get_all_links(cursor):
    query = "SELECT* FROM web_pages"
    cursor.execute(query)
    row = cursor.fetchall()
    return row

def insert_link(cursor, link, content, visited, indexed, lastVisited, frequency):
    query = "INSERT INTO web_pages(Link, Content, Visited, Indexed, LastVisited, Frequency) VALUES(%s, %s, %s, %s, %s, %s)"
    args = (link, content, visited, indexed, lastVisited, frequency)
    cursor.execute(query, args)
    
def get_link(cursor, link):
    query = "SELECT* FROM web_pages WHERE Link = %s"
    cursor.execute(query,(link,))
    row = cursor.fetchall()
    return row[0]

def delete_link(cursor, link):
    query = "DELETE FROM web_pages WHERE Link = %s"
    cursor.execute(query,(link,))
    
def update_link(cursor, ID, content, lastVisited):
    query = "UPDATE web_pages set Content = %s , LastVisited = %s WHERE ID = %s"
    args = (content,lastVisited,ID)
    cursor.execute(query, args)
    
def insert_queue(cursor, link, visited, indexed):
    query = "INSERT INTO web_pages(Link, Visited, Indexed) VALUES(%s, %s, %s)"
    args = (link, visited, indexed)
    cursor.execute(query, args)

def delete_all_not_visited(cursor):
    query = "DELETE FROM web_pages WHERE Visited = 0"
    cursor.execute(query)