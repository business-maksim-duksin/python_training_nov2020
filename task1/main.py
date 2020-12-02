import argparse
import os
import json
from logging_config import get_logger
from SaverToFile import SaverToJSON, SaverToXML

def commnad_line_arguments():
    parser = argparse.ArgumentParser(description="Form a list of rooms containing list of students inside every room.")
    parser.add_argument("students", type=str, help="path to students json")
    parser.add_argument("rooms", type=str, help="path to rooms json")
    parser.add_argument("output_format", type=str, help="output file format")
    parser.add_argument("-o", "--output_path", type=str, help="output file path", default=str(os.getcwd()))
    parser.add_argument("-n", "--output_name", type=str, help="output file name", default="result")
    args = parser.parse_args()

    log = get_logger(__name__)

    savers = {
        "json": SaverToJSON,
        "xml": SaverToXML,
    }
    # Check if valid save format
    try:
        save_to_file = savers[args.output_format].save_to_file
    except KeyError:
        msg = f"Unknown file format {args.output_format}, use one of these: {', '.join(savers.keys())}."
        log.error(msg)
        raise
    return args, log, save_to_file

def main():
    args, log, save_to_file = commnad_line_arguments()
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
    for student in students:
        room = rooms_and_students["Rooms"][student["room"]]
        room["Students"].append(student)
    # Get rid of useless depth layer  (room id as keys)
    rooms_and_students["Rooms"] = list(rooms_and_students["Rooms"].values())

    filename = f"{args.output_name}.{args.output_format}"
    save_to_file(rooms_and_students, os.path.join(args.output_path, filename))


if __name__ == "__main__":
    main()
