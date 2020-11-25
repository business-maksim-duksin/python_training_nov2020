import argparse
import os
import json
from save_as import save_as_json, save_as_xml

parser = argparse.ArgumentParser(description="Form a list of rooms containing list of students inside every room.")
parser.add_argument("students", type=str, help="path to students json")
parser.add_argument("rooms", type=str, help="path to rooms json")
parser.add_argument("output_format", type=str, help="output file format")
parser.add_argument("-o", "--output_path", type=str, help="output file path", default=str(os.getcwd()))
parser.add_argument("-n", "--output_name", type=str, help="output file name", default="result")
args = parser.parse_args()

savers = {
    "json": save_as_json,
    "xml": save_as_xml,
}

# Check if valid save format
try:
    save_to_file = savers[args.output_format]
except KeyError:
    print(f"Unknown file format {args.output_format}, use one of these: {', '.join(savers.keys())}.")
    raise


def main():
    with open(args.students, 'r') as f:
        students = json.load(f)
    with open(args.rooms, 'r') as f:
        rooms = json.load(f)

    [room.update({"Students": []}) for room in rooms]
    rooms_and_students = {"Rooms":
                              {room["id"]:
                                   room for room in rooms
                               }
                          }
    [rooms_and_students["Rooms"][student["room"]]["Students"].append(student) for student in students]
    # Get rid of useless depth layer  (room id as keys)
    rooms_and_students["Rooms"] = list(rooms_and_students["Rooms"].values())

    filename = f"{args.output_name}.{args.output_format}"
    save_to_file(rooms_and_students, os.path.join(args.output_path, filename))


if __name__ == "__main__":
    main()
