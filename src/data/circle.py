from data.init import curs
from data.init import conn
from model.circle import Circle

curs.execute("""CREATE TABLE IF NOT EXISTS circle(
                radius REAL NOT NULL PRIMARY KEY)""")


def row_to_model(row: tuple) -> Circle:
    if (row==None): # if no entry is returned
        return None
    else:
        radius = row[0]
        return Circle(radius=radius)
    
def model_to_dict(circle: Circle) -> dict:
    print(circle.model_dump())
    return circle.model_dump()

def get_one(radius: float) -> Circle:
    qry = "SELECT * FROM circle WHERE radius=:radius"
    params = {"radius": radius}
    curs.execute(qry, params)
    row = curs.fetchone()
    return row_to_model(row)

def get_all() -> list[Circle]:
    qry = "SELECT * FROM circle"
    curs.execute(qry)
    rows = list(curs.fetchall())
    return [row_to_model(row) for row in rows]

def create(circle: Circle):
    qry = """INSERT OR IGNORE INTO circle VALUES (:radius)""" # Ignore if duplicate, we can do for single value entry
    params = model_to_dict(circle)
    curs.execute(qry, params)
    conn.commit()
    return circle

def modify(old_radius: float, new_radius: float) -> Circle:
    """Update an existing Circle's radius."""
    qry = "UPDATE circle SET radius=:new_radius WHERE radius=:old_radius"
    params = {"old_radius": old_radius, "new_radius": new_radius}
    curs.execute(qry, params)
    conn.commit()

    if curs.rowcount == 1:
        return get_one(new_radius)  # Return the updated circle
    else:
        return None  # If no row was modified, return None


def replace(circle: Circle):
    return circle

def delete(circle: Circle):
    qry = "DELETE FROM circle WHERE radius=:radius"
    params = {"radius": circle.radius}
    curs.execute(qry, params)
    conn.commit()