import json
import argparse

classes = ['Power_Cell','Goal']
current_dir = "/Users/browncg/Documents/Robotics/ModelConversions/"
#current_dir = os.getcwd().replace("\\","/")[2:]

def convert_classes(classes, start=1):
    msg = ''
    for id, name in enumerate(classes, start=start):
        msg = msg + "item {\n"
        msg = msg + " id: " + str(id) + "\n"
        msg = msg + " name: '" + name + "'\n}\n\n"
    return msg[:-1]


def parse_arguments():
    parser = argparse.ArgumentParser(formatter_class=argparse.ArgumentDefaultsHelpFormatter)
    parser.add_argument("--classes", nargs='+', help="list of model labels", required=False,                     default=classes)
    parser.add_argument("--current_dir", help="path to directory to create pbtxt in", type=str, required=False,
                        default=current_dir)
    args = parser.parse_args()
    print("input args: \n", json.dumps(vars(args), indent=4, separators=(" , ", ":")))
    return args


if __name__ == '__main__':
    args = parse_arguments()
    classes = args.classes
    current_dir = args.current_dir
    label_map = convert_classes(classes)
    with open(current_dir + 'map.pbtxt', 'w') as f:
        f.write(label_map)
        f.close()
    print("map.pbtxt successfully generated")