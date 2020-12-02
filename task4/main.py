import argparse
import os
import json
from logging_config import get_logger
from db_config import db_config
from classes.Task4DbHandler import Task4DbHandler
from classes.ConnectorMySQL import ConnectorMySQL
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

    with Task4DbHandler(ConnectorMySQL, db_config, from_scratch=True) as dbh:
        # pass
        dbh.create_table_rooms()
        dbh.create_table_students()

        dbh.insert_rooms(rooms)
        dbh.insert_students(students)

        dbh.add_indexes()
        #                       (AVG(3))ms exec.  | PrimeryKey+ForeignKey / PrimeryKey / Nothing
        r1 = dbh.room_population()  #                       9               20              23
        r2 = dbh.top5_least_average_age()   #               18              13              15
        r3 = dbh.top5_max_diff_age()    #                   18              10              13
        r4 = dbh.mixed_sex()    #                           11              11              11

    rooms_and_students = {"room_population": r1,
                          "top5_least_average_age": r2,
                          "top5_max_diff_age": r3,
                          "mixed_sex": r4,
                          }
    filename = f"{args.output_name}.{args.output_format}"
    save_to_file(rooms_and_students, os.path.join(args.output_path, filename))


if __name__ == "__main__":
    main()
