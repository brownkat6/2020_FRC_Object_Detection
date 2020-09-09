import os
import json
import csv
from PIL import Image
import argparse

bucket_name = "ball_goal_fix"
#current_dir = "/Users/browncg/Documents/Robotics/SV_to_Darknet/"

def get_input_dir_arr(input_dir, image_dir_prefixes):
    rows = []
    annotations = [filename for filename in list(os.listdir(input_dir)) if filename[-4:]=="json"]
    prefix = image_dir_prefixes[input_dir]
    for ann in annotations:
        with open(input_dir + ann,"r") as file:
            data = json.load(file)

            objects = data["objects"]
            width = data["size"]["width"]
            height = data["size"]["height"]
            image_name = ann[:-5].replace(".png",".jpg")
            new_image_name = prefix + "_" + image_name
            #image_name = image_name[:-4] + "-2020-08-03T20:57:23.190Z" + ".jpg"
            if len(objects) != 0:
                for object in objects:
                    row = {}
                    row["category"] = "UNASSIGNED"
                    row["bucket_name"] = "gs://" + bucket_name + new_image_name
                    row["class_title"] = object["classTitle"]
                    coords = object["points"]["exterior"]
                    row["xx"] = coords[0][0]/width
                    row["xy"] = coords[0][1]/height
                    row["yx"] = coords[1][0]/width
                    row["yy"] = coords[1][1]/height
                    rows.append(row)
                #move image to images directory
                #img = Image.open(input_dir[:-4] + "img/" + image_name)
                #img.save(all_images_path + new_image_name)
            else:
                row = {}
                row["category"] = "UNASSIGNED"
                row["bucket_name"] = "gs://" + bucket_name + image_name
                #rows.append(row)
    return rows

def main(bucket_name, current_dir):

    input_dirs = [
    current_dir + "input/Raw Data/Filming Day 1 Images/ann/",
    current_dir + "input/Raw Data/Filming Day 1 Video/ann/",
    current_dir + "input/Raw Data/Filming Day 2 Video/ann/"]

    all_images_path = current_dir + "input/data2/"

    image_dir_prefixes = {}
    for i,input_dir in enumerate(input_dirs):
        image_dir_prefixes[input_dir] = str(i)

    row_keys = ["category","bucket_name", "class_title", "xx","xy","_","__","yx","yy","___","____"]

    output_csv_path = current_dir + "output/" + bucket_name + "_labels.csv"

    with open(output_csv_path, 'a', newline='') as file:
        writer = csv.DictWriter(file,fieldnames=row_keys)
        writer.writeheader()
        for input_dir in input_dirs:
            rows = get_input_dir_arr(input_dir,image_dir_prefixes)
            for row in rows:
                writer.writerow(row)
        file.flush()

if __name__ == "__main__":
    parser = argparse.ArgumentParser(formatter_class=argparse.ArgumentDefaultsHelpFormatter)
    parser.add_argument("--bucket_name", help="name of your google cloud bucket", type=str, required=False,
                        default=bucket_name)
    args = parser.parse_args()
    print("input args: \n", json.dumps(vars(args), indent=4, separators=(" , ", ":")))
    bucket_name = args.bucket_name
    current_dir = os.getcwd().replace("\\","/")[2:] + "/"
    main(bucket_name, current_dir)
    print("Google Cloud", bucket_name + "_labels.csv", "file generated successfully")