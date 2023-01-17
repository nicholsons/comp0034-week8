from flask import Blueprint

bp = Blueprint("api", __name__, url_prefix="/api")


@bp.get("/noc")
def noc():
    """Returns a list of NOC region codes with region name and notes"""
    return "Returns a list of NOC codes"


@bp.get("/noc/<code>")
def noc_code(code):
    """Returns the details for a given code"""
    return f"The details for {code}."


# The following version combines two routes

'''
@bp.route("/noc")
@bp.route("/noc/<code>")
def noc(code=None):
    """Returns a list of NOC codes with the country/region name and notes or if a code is passed then returns the details for a given code"""
    if code:
        return f"The details for {code}."
    else:
        return "Returns a list of NOC codes"
'''


@bp.patch("/noc/<code>")
def noc_update(code):
    """Updates changed fields for the NOC record"""
    return f"The record for {code} has been updated."


@bp.post("/noc")
def noc_add(code):
    """Adds a new NOC record to the dataset."""
    return f"The record for {code} has been added."


@bp.delete("/noc/<code>")
def noc_delete(code):
    """Removes a NOC record from the dataset."""
    return f"The record for {code} has been deleted."


@bp.get("/event")
def event():
    """Returns the details for all events"""
    return f"The details for all events."


@bp.get("/event/<event_id>")
def event_id(event_id):
    """Returns the details for a specified event"""
    return f"The event details for {event_id}."


@bp.patch("/event/<event_id>")
def event_update(event_id):
    """Updates changed fields for the event"""
    return f"The record for {event_id} event has been updated."


@bp.post("/event")
def event_add():
    """Adds a new event record to the dataset."""
    return f"The record for the event has been added."
