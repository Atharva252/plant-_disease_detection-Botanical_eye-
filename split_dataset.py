import json
import random
import os

# Load intents
def load_intents(file_path):
    with open(file_path, "r") as file:
        return json.load(file)

# Save splits
def save_split(data, file_path):
    with open(file_path, "w") as file:
        json.dump(data, file, indent=4)

# Split data
def split_data(intents, train_ratio=0.7, test_ratio=0.2):
    train, test, validate = {"intents": []}, {"intents": []}, {"intents": []}

    for intent in intents["intents"]:
        patterns = intent["patterns"]
        random.shuffle(patterns)

        train_end = int(len(patterns) * train_ratio)
        test_end = train_end + int(len(patterns) * test_ratio)

        train["intents"].append({"tag": intent["tag"], "patterns": patterns[:train_end], "responses": intent["responses"]})
        test["intents"].append({"tag": intent["tag"], "patterns": patterns[train_end:test_end], "responses": intent["responses"]})
        validate["intents"].append({"tag": intent["tag"], "patterns": patterns[test_end:], "responses": intent["responses"]})

    return train, test, validate

# Main
if __name__ == "__main__":
    intents = load_intents("intents.json")
    train, test, validate = split_data(intents)

    os.makedirs("splits", exist_ok=True)
    save_split(train, "splits/train.json")
    save_split(test, "splits/test.json")
    save_split(validate, "splits/validate.json")

    print("Dataset split into train, test, and validate!")
