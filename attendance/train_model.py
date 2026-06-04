import os

dataset_path = "media/students"
label_file = "media/trainer/labels.txt"

label_id = 1

with open(label_file, "w") as file:

    for folder in os.listdir(dataset_path):

        if os.path.isdir(
            os.path.join(dataset_path, folder)
        ):

            file.write(
                f"{label_id},{folder}\n"
            )

            label_id += 1

print("labels.txt created successfully")