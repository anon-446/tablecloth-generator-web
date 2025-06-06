import json, os, random, io
from PIL import Image
from flask import Flask, render_template, request, send_from_directory, make_response, send_file

app = Flask(__name__)
fp_open = open("config/teams.json", "r", encoding="utf-8")
teams_config = json.loads(fp_open.read())
id_config_file = open("config/id-teams.json", "r", encoding="utf-8")
id_configs = json.loads(id_config_file.read())
img_dir = "/static"
ROOT_DIR = os.path.dirname(os.path.abspath(__file__))
NUM_TEAMS = 18

tablecloth = Image.open(ROOT_DIR + "/static/mat.png")
border = Image.open(ROOT_DIR + "/static/table_border.png")
tech_lines = Image.open(ROOT_DIR + "/static/technical_lines.png")
tablecloth_dict = {}
for i in range(0, NUM_TEAMS):
    team_num_str = str(i + 1)
    tablecloth_dict[team_num_str] = Image.open(ROOT_DIR + "/static/tablecloth/team%s.png" % team_num_str)
tablecloth_dict["default"] = Image.open(ROOT_DIR + "/static/tablecloth/team%s.png" % "default")

@app.route("/team-image/", methods=["GET"])
def find_team_image():

    if request.method == "GET":
        team_name = request.args["team_name"]
        team_id = teams_config["teams"].index(team_name) + 1
        team_image = "team%d.png" % (team_id)

        return "/static/logos/" + team_image

@app.route("/generate-image/", methods=["POST"])
def generate_image():

    if request.method == "POST":
        east_team = request.form["east"]
        east_team = str(teams_config["teams"].index(east_team) + 1)
        south_team = request.form["south"]
        south_team = str(teams_config["teams"].index(south_team) + 1)
        west_team = request.form["west"]
        west_team = str(teams_config["teams"].index(west_team) + 1)
        north_team = request.form["north"]
        north_team = str(teams_config["teams"].index(north_team) + 1)
        print(east_team)
        print(south_team)
        print(west_team)
        print(north_team)

        final_tablecloth = create_tablecloth_image(east_team, south_team, west_team, north_team)
        data = io.BytesIO()
        final_tablecloth.save(data, "PNG")
        data.seek(0)

        return send_file(data, as_attachment=False, download_name='tablecloth.png')

def get_team_by_player_name(name):
    player_teams = teams_config["players"]
    for team in player_teams:
        lowercase_names = [item.lower() for item in player_teams[team]]
        if name.lower() in lowercase_names:
            return str(teams_config["teams"].index(team) + 1)
    return "default"

def _build_cors_preflight_response():
    response = make_response()
    response.headers.add("Access-Control-Allow-Origin", "*")
    response.headers.add('Access-Control-Allow-Headers', "*")
    response.headers.add('Access-Control-Allow-Methods', "*")
    return response

def _corsify_actual_response(response):
    response.headers.add("Access-Control-Allow-Origin", "*")
    return response

def create_tablecloth_image(east_team, south_team, west_team, north_team):
    east_image = tablecloth_dict[east_team]
    east_image = east_image.convert("RGBA")
    south_image = tablecloth_dict[south_team]
    #south_image = south_image.rotate(90, expand=True).convert("RGBA")
    west_image = tablecloth_dict[west_team]
    west_image = west_image.rotate(180, expand=True).convert("RGBA")
    north_image = tablecloth_dict[north_team]
    #north_image = north_image.rotate(-90, expand=True).convert("RGBA")

    final_tablecloth = Image.new("RGBA", (2048, 2048))
    final_tablecloth.paste(tablecloth, (0, 0), tablecloth)
    final_tablecloth.paste(border, (0,0), border)
    if east_image.size == (1568, 786):
        final_tablecloth.paste(east_image, (240, 1020), east_image)
    else:
        final_tablecloth.paste(east_image.resize((1568, 786)), (240, 1020), east_image.resize((1568, 786)))
    if south_image.size == (1568, 786):
        final_tablecloth.paste(south_image.rotate(90, expand=True).convert("RGBA"), (1020, 240), south_image.rotate(90, expand=True).convert("RGBA"))
    else:
        final_tablecloth.paste(south_image.resize((1568, 786)).rotate(90, expand=True).convert("RGBA"), (1020, 240), south_image.resize((1568, 786)).rotate(90, expand=True).convert("RGBA"))
    if west_image.size == (1568, 786):
        final_tablecloth.paste(west_image, (235, 240), west_image)
    else:
        final_tablecloth.paste(west_image.resize((1568, 786)), (235, 240), west_image.resize((1568, 786)))
    if north_image.size == (1568, 786):
        final_tablecloth.paste(north_image.rotate(-90, expand=True).convert("RGBA"), (240, 240), north_image.rotate(-90, expand=True).convert("RGBA"))
    else:
        final_tablecloth.paste(north_image.resize((1568, 786)).rotate(-90, expand=True).convert("RGBA"), (240, 240), north_image.resize((1568, 786)).rotate(-90, expand=True).convert("RGBA"))

    return final_tablecloth.convert("RGB")

@app.route("/generate-image-v2/tablecloth.png", methods = ["GET"])
def generate_image_v2():
    if request.method == "OPTIONS": # CORS preflight
        return _build_cors_preflight_response()
    east_team = get_team_by_player_name(request.args.get("east"))
    south_team = get_team_by_player_name(request.args.get("south"))
    west_team = get_team_by_player_name(request.args.get("west"))
    north_team = get_team_by_player_name(request.args.get("north"))
    print(east_team)
    print(south_team)
    print(west_team)
    print(north_team)

    final_tablecloth = create_tablecloth_image(east_team, south_team, west_team, north_team)
    data = io.BytesIO()
    final_tablecloth.save(data, "PNG")
    data.seek(0)

    response = send_file(data, as_attachment=False, download_name='tablecloth.png')

    return _corsify_actual_response(response)

def get_team_by_id(player_id):
    if player_id in id_configs:
        return id_configs[player_id]
    return "default"

@app.route("/generate-image-v3/tablecloth.png", methods = ["GET"])
def generate_image_v3():
    if request.method == "OPTIONS": # CORS preflight
        return _build_cors_preflight_response()
    east_team = get_team_by_id(request.args.get("east"))
    south_team = get_team_by_id(request.args.get("south"))
    west_team = get_team_by_id(request.args.get("west"))
    north_team = get_team_by_id(request.args.get("north"))
    print(east_team)
    print(south_team)
    print(west_team)
    print(north_team)

    final_tablecloth = create_tablecloth_image(east_team, south_team, west_team, north_team)
    data = io.BytesIO()
    final_tablecloth.save(data, "PNG")
    data.seek(0)

    response = send_file(data, as_attachment=False, download_name='tablecloth.png')

    return _corsify_actual_response(response)

@app.route("/")
def main():
    return render_template("index.html", team_names=teams_config["teams"], teams=teams_config["players"].items())

if __name__ == "__main__":
    app.run(debug=True)